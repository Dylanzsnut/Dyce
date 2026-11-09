"""
Assignment 05: Efficient Azure OpenAI API Usage with Function Calling,
Batching, and Robust Retry Mechanisms.

Features:
- Azure OpenAI Service integration using official openai library
- Function Calling / Tool Calling for structured JSON schema enforcement
- Robust retry logic using tenacity decorators:
    - retry_if_exception_type (RateLimitError, APIConnectionError, etc.)
    - wait_random_exponential (exponential backoff with jitter)
    - stop_after_attempt (max 5 attempts)
- Batch request processor with inter-request rate pacing
- Error handling that captures individual failures without crashing batch
- Offline demonstration mode when Azure credentials are not configured
"""

import os
import sys
import json
import time
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional

# Load environment variables if python-dotenv is present
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Tenacity imports for production retry mechanisms
from tenacity import (
    retry,
    wait_random_exponential,
    stop_after_attempt,
    retry_if_exception_type,
    before_sleep_log,
)

# Robust OpenAI exception imports compatible with both openai>=1.0 and legacy
try:
    from openai import (
        AzureOpenAI,
        RateLimitError,
        APIError,
        APIConnectionError,
        APITimeoutError,
        InternalServerError,
    )
    RETRYABLE_EXCEPTIONS = (
        RateLimitError,
        APIConnectionError,
        APITimeoutError,
        InternalServerError,
        APIError,
    )
except ImportError:
    try:
        from openai.error import RateLimitError, APIError, Timeout, APIConnectionError  # type: ignore
        from openai import AzureOpenAI  # type: ignore
        RETRYABLE_EXCEPTIONS = (RateLimitError, APIError, Timeout, APIConnectionError)  # type: ignore
    except ImportError:
        RateLimitError = Exception  # type: ignore
        APIError = Exception  # type: ignore
        RETRYABLE_EXCEPTIONS = (Exception,)  # type: ignore
        AzureOpenAI = None  # type: ignore

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("BatchFunctionCalling")


# =====================================================================
# FUNCTION SCHEMA DEFINITION (Step 2 from Assignment 05)
# =====================================================================
ITINERARY_FUNCTION_SCHEMA = {
    "name": "generate_itinerary",
    "description": "Generate a travel itinerary for a given destination and duration.",
    "parameters": {
        "type": "object",
        "properties": {
            "destination": {
                "type": "string",
                "description": "Travel destination city or country"
            },
            "days": {
                "type": "integer",
                "description": "Number of days to plan for"
            },
            "duration_days": {
                "type": "integer",
                "description": "Number of days to plan for"
            },
            "travel_style": {
                "type": "string",
                "enum": ["cultural", "adventure", "culinary", "leisure", "family"],
                "description": "Primary travel experience style"
            },
            "budget_tier": {
                "type": "string",
                "enum": ["budget", "moderate", "luxury"],
                "description": "Target financial accommodation and dining tier"
            },
            "estimated_cost_usd": {
                "type": "number",
                "description": "Estimated total trip budget per person in USD"
            },
            "daily_schedule": {
                "type": "array",
                "description": "Chronological itinerary broken down by day",
                "items": {
                    "type": "object",
                    "properties": {
                        "day": {"type": "integer"},
                        "theme": {"type": "string"},
                        "morning_activity": {"type": "string"},
                        "afternoon_activity": {"type": "string"},
                        "evening_activity": {"type": "string"},
                        "highlight_cuisine": {"type": "string"}
                    },
                    "required": [
                        "day", "theme", "morning_activity",
                        "afternoon_activity", "evening_activity", "highlight_cuisine"
                    ]
                }
            },
            "local_tips": {
                "type": "array",
                "items": {"type": "string"},
                "description": "Essential transit, cultural etiquette, or safety tips"
            }
        },
        "required": ["destination", "days"]
    }
}

# Functions list definition matching Assignment 05 specification
functions = [ITINERARY_FUNCTION_SCHEMA]

# Modern tools format for OpenAI v1
TOOLS_SCHEMA = [
    {
        "type": "function",
        "function": ITINERARY_FUNCTION_SCHEMA
    }
]


# =====================================================================
# OFFLINE DEMONSTRATION FALLBACK ENGINE
# =====================================================================
MOCK_DATABASE = {
    "Paris, France": {
        "destination": "Paris, France",
        "duration_days": 3,
        "travel_style": "cultural",
        "budget_tier": "moderate",
        "estimated_cost_usd": 1250.0,
        "daily_schedule": [
            {
                "day": 1,
                "theme": "Historical Heart & River Romance",
                "morning_activity": "Explore Île de la Cité, Sainte-Chapelle stained glass, and Notre-Dame exterior.",
                "afternoon_activity": "Guided visit through the Louvre Museum focusing on the Denon and Sully wings.",
                "evening_activity": "Sunset Seine River cruise followed by dinner in Saint-Germain-des-Prés.",
                "highlight_cuisine": "Duck confit with pommes sarladaises and tarte tatin."
            },
            {
                "day": 2,
                "theme": "Bohemian Heights & Impressionist Art",
                "morning_activity": "Climb Montmartre hill to Sacré-Cœur Basilica and discover Place du Tertre.",
                "afternoon_activity": "Tour Musée d'Orsay to admire Monet, Degas, and Van Gogh masterpieces.",
                "evening_activity": "Walk through Tuileries Garden and enjoy dusk views from Pont Alexandre III.",
                "highlight_cuisine": "French onion soup (soupe à l'oignon gratinée) and crêpes."
            },
            {
                "day": 3,
                "theme": "Royal Grandeur & Chic Marais",
                "morning_activity": "Visit the Eiffel Tower summit and walk through Champ de Mars.",
                "afternoon_activity": "Browse contemporary galleries and historic mansions in Le Marais.",
                "evening_activity": "Farewell tasting dinner at a classic Parisian bistro near Place des Vosges.",
                "highlight_cuisine": "Coq au vin with Burgundy Pinot Noir and macarons."
            }
        ],
        "local_tips": [
            "Use the Paris Metro Navigo Easy pass for seamless underground transit.",
            "Book Louvre and Eiffel Tower time slots at least 2 weeks in advance.",
            "Always greet shopkeepers with 'Bonjour Madame/Monsieur' upon entering."
        ]
    },
    "Tokyo, Japan": {
        "destination": "Tokyo, Japan",
        "duration_days": 5,
        "travel_style": "culinary",
        "budget_tier": "luxury",
        "estimated_cost_usd": 3800.0,
        "daily_schedule": [
            {
                "day": 1,
                "theme": "Ancient Traditions & Street Bites",
                "morning_activity": "Visit Senso-ji temple in Asakusa and stroll Nakamise Dori street stalls.",
                "afternoon_activity": "Culinary food tour through Tsukiji Outer Market sampling fresh sashimi and tamagoyaki.",
                "evening_activity": "Omakase sushi dinner at a Ginza multi-course sushi counter.",
                "highlight_cuisine": "Otoro nigiri and uni flight with premium junmai daiginjo sake."
            },
            {
                "day": 2,
                "theme": "Subculture & Electric Dining",
                "morning_activity": "Tour Akihabara electronic district and retro gaming arcades.",
                "afternoon_activity": "Discover Ueno Park and the Tokyo National Museum culinary exhibit.",
                "evening_activity": "Yakitori experience under the train tracks in Yurakucho / Ginza Corridor.",
                "highlight_cuisine": "Charcoal-grilled binchotan tsukune with raw organic egg yolk."
            },
            {
                "day": 3,
                "theme": "Modern Pop Culture & Sky Views",
                "morning_activity": "Cross Shibuya Scramble crossing and visit Meiji Shrine in Harajuku.",
                "afternoon_activity": "Shop luxury fashion along Omotesando avenue and stop at artisanal matcha cafes.",
                "evening_activity": "Cocktails at the Park Hyatt New York Bar overlooking Shinjuku skyline.",
                "highlight_cuisine": "A5 Wagyu beef teppanyaki cooked tableside with wasabi salt."
            },
            {
                "day": 4,
                "theme": "Art, Architecture & Kaiseki",
                "morning_activity": "Explore teamLab Planets digital interactive art museum in Toyosu.",
                "afternoon_activity": "Visit Roppongi Hills Mori Art Museum and tranquil Mohri Garden.",
                "evening_activity": "10-course seasonal Kaiseki dinner in Roppongi.",
                "highlight_cuisine": "Traditional seasonal kaiseki featuring matsutake broth and sweetfish."
            },
            {
                "day": 5,
                "theme": "Tranquil Gardens & Farewell Ramen",
                "morning_activity": "Walk through Shinjuku Gyoen National Garden and tea house ceremony.",
                "afternoon_activity": "Souvenir hunting in Nihombashi traditional craft stores.",
                "evening_activity": "Late night Tokyo ramen crawl in Shinjuku Golden Gai.",
                "highlight_cuisine": "Rich tonkotsu broth ramen with handmade noodles and chashu."
            }
        ],
        "local_tips": [
            "Purchase a digital Suica or Pasmo IC card on Apple/Google Wallet for transit and convenience store payments.",
            "Tipping is strictly not customary in Japan; exceptional service is already included.",
            "Carry a small bag for your trash, as public waste bins are rare in Tokyo."
        ]
    },
    "New York City, USA": {
        "destination": "New York City, USA",
        "duration_days": 4,
        "travel_style": "leisure",
        "budget_tier": "budget",
        "estimated_cost_usd": 850.0,
        "daily_schedule": [
            {
                "day": 1,
                "theme": "Midtown Icons & Urban Parks",
                "morning_activity": "Walk Central Park from Bethesda Terrace to Strawberry Fields with a picnic bagel.",
                "afternoon_activity": "Marvel at New York Public Library Rose Main Reading Room and Bryant Park.",
                "evening_activity": "Take in the neon lights of Times Square and Grand Central Terminal constellation ceiling.",
                "highlight_cuisine": "Everything bagel with scallion cream cheese and classic New York slice pizza."
            },
            {
                "day": 2,
                "theme": "Downtown History & Harbor Views",
                "morning_activity": "Free Staten Island Ferry round-trip ride offering prime views of Statue of Liberty.",
                "afternoon_activity": "Reflect at the 9/11 Memorial Plaza and walk through Wall Street and Oculus.",
                "evening_activity": "Stroll across the iconic Brooklyn Bridge during sunset into DUMBO.",
                "highlight_cuisine": "Coal-fired brick oven margherita pizza in Brooklyn."
            },
            {
                "day": 3,
                "theme": "Elevated Architecture & Vibrant Neighborhoods",
                "morning_activity": "Walk the High Line elevated park from Hudson Yards to Chelsea Market.",
                "afternoon_activity": "Explore Greenwich Village brownstones and Washington Square Park street performers.",
                "evening_activity": "Browse bookshops in Soho and dine at historic Chinatown spots.",
                "highlight_cuisine": "Steamed pork soup dumplings (xiaolongbao) and warm Portuguese egg tarts."
            },
            {
                "day": 4,
                "theme": "Arts, Culture & River Vistas",
                "morning_activity": "Pay-what-you-wish or free morning entry to neighborhood cultural galleries.",
                "afternoon_activity": "Walk along Brooklyn Heights Promenade with panoramic Lower Manhattan skyline views.",
                "evening_activity": "Dessert and skyline night gazing from Gantry Plaza State Park in Queens.",
                "highlight_cuisine": "Classic pastrami on rye sandwich and black-and-white cookies."
            }
        ],
        "local_tips": [
            "Use OMNY contactless tap-to-pay on subways; after 12 rides in a Monday-Sunday week, all additional rides are free.",
            "Enjoy free iconic views from the Staten Island Ferry instead of expensive boat tours.",
            "Walk across the bridges instead of taking taxis to avoid heavy traffic delays."
        ]
    }
}


# =====================================================================
# STEP 1: CLIENT INITIALIZATION
# =====================================================================
def get_azure_client() -> Optional[Any]:
    """Initialize AzureOpenAI client from environment variables if present."""
    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    api_key = os.getenv("AZURE_OPENAI_API_KEY")
    api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2024-07-01-preview")

    if not endpoint or not api_key or AzureOpenAI is None:
        return None

    try:
        return AzureOpenAI(
            azure_endpoint=endpoint,
            api_key=api_key,
            api_version=api_version,
        )
    except Exception as e:
        logger.warning(f"Could not initialize AzureOpenAI client: {e}")
        return None


# Module-level client instance (falls back to None for offline mock)
client = get_azure_client()


# =====================================================================
# STEP 3: TENACITY-DECORATED API CALL
# =====================================================================
@retry(
    retry=retry_if_exception_type(RETRYABLE_EXCEPTIONS),
    wait=wait_random_exponential(min=1, max=10),
    stop=stop_after_attempt(5),
    reraise=True,
    before_sleep=before_sleep_log(logger, logging.WARNING)
)
def call_openai_function(
    prompt: str,
    destination: str,
    days: Optional[int] = None,
    client: Optional[Any] = None,
    model_deployment: Optional[str] = None,
    duration_days: Optional[int] = None,
    **kwargs
) -> Dict[str, Any]:
    """
    Step 3: Call Azure OpenAI Function Calling under Tenacity retry management.
    Retries on rate limits or transient errors with exponential backoff (max 5 attempts).
    """
    actual_days = days if days is not None else (duration_days if duration_days is not None else 3)
    active_client = client if client is not None else globals().get("client")
    deployment = model_deployment or os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "gpt-4o-mini")
    style = kwargs.get("travel_style", "cultural")
    budget = kwargs.get("budget_tier", "moderate")

    # If client is not available or mock mode, generate structured mock
    if active_client is None:
        return mock_generate_itinerary(destination, actual_days, style, budget)

    system_message = (
        "You are an expert travel architect and concierge. "
        "Formulate structured day-by-day travel itineraries. "
        "You MUST invoke the `generate_itinerary` function to supply all structured fields."
    )
    user_message = (
        f"{prompt}\n\n"
        f"Constraints: Destination: {destination}, Duration: {actual_days} days, "
        f"Style: {style}, Budget: {budget}."
    )

    # Modern Tools API (OpenAI >= 1.0)
    try:
        response = active_client.chat.completions.create(
            model=deployment,
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message}
            ],
            tools=TOOLS_SCHEMA,
            tool_choice={"type": "function", "function": {"name": "generate_itinerary"}}
        )
        message = response.choices[0].message
        if message.tool_calls:
            tool_call = message.tool_calls[0]
            args = json.loads(tool_call.function.arguments)
            # Ensure "days" field is present
            if "days" not in args and "duration_days" in args:
                args["days"] = args["duration_days"]
            return args
    except (TypeError, AttributeError, KeyError):
        # Fallback to legacy functions schema for older deployment versions
        response = active_client.chat.completions.create(
            model=deployment,
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message}
            ],
            functions=functions,
            function_call={"name": "generate_itinerary"}
        )
        func_call = response.choices[0].message.function_call
        args = json.loads(func_call.arguments)
        if "days" not in args and "duration_days" in args:
            args["days"] = args["duration_days"]
        return args

    raise ValueError("No valid function call received from API response.")


# Backwards-compatible alias
call_openai_function_with_retry = call_openai_function


def mock_generate_itinerary(destination: str, duration_days: int, travel_style: str = "cultural", budget_tier: str = "moderate") -> Dict[str, Any]:
    """Generates deterministic mock itinerary when running in demonstration mode."""
    for key, data in MOCK_DATABASE.items():
        if destination.lower() in key.lower() or key.lower() in destination.lower():
            res = dict(data)
            res["days"] = res.get("duration_days", duration_days)
            return res

    # Dynamic generic mock if destination is not in pre-defined set
    return {
        "destination": destination,
        "days": duration_days,
        "duration_days": duration_days,
        "travel_style": travel_style,
        "budget_tier": budget_tier,
        "estimated_cost_usd": 250.0 * duration_days,
        "daily_schedule": [
            {
                "day": d + 1,
                "theme": f"Exploring {destination} - Day {d + 1}",
                "morning_activity": f"Visit primary landmarks and cultural heritage sites in {destination}.",
                "afternoon_activity": f"Sample local markets and traditional craft centers in {destination}.",
                "evening_activity": f"Dine at acclaimed regional restaurant and enjoy local evening sights.",
                "highlight_cuisine": f"Signature regional dishes of {destination}."
            }
            for d in range(duration_days)
        ],
        "local_tips": [
            "Always keep local transit maps handy and verify museum operating hours.",
            "Sample regional specialties from verified hygienic food stalls.",
            "Respect local etiquette and quiet hours in residential districts."
        ]
    }


# =====================================================================
# STEP 5: EXAMPLE BATCH INPUTS (from Assignment 05 specification)
# =====================================================================
batch_inputs = [
    {"prompt": "Plan a travel itinerary.", "destination": "Paris", "days": 3},
    {"prompt": "Plan a travel itinerary.", "destination": "Tokyo", "days": 5},
    {"prompt": "Plan a travel itinerary.", "destination": "New York", "days": 4},
]


# =====================================================================
# STEP 4: BATCH PROCESSING FUNCTION
# =====================================================================
def batch_process(
    inputs: Optional[List[Dict[str, Any]]] = None,
    client: Optional[Any] = None,
    model_deployment: Optional[str] = None,
    delay_between_requests: float = 1.0,
    force_demo: bool = False
) -> List[Dict[str, Any]]:
    """
    Step 4: Processes a batch of itinerary requests using Azure OpenAI function calling.

    Key Features:
    - Isolates exceptions: a failure on one item does not crash the pipeline.
    - Paces requests to prevent bursting rate limits.
    - Returns structured outcome logs with timing and status.
    """
    if inputs is None:
        inputs = batch_inputs

    active_client = client if client is not None else globals().get("client")
    if force_demo:
        active_client = None

    if model_deployment is None:
        model_deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "gpt-4o-mini")

    use_mock = (active_client is None)
    if use_mock:
        logger.info("Running batch processing in DEMONSTRATION / OFFLINE mode.")
    else:
        logger.info(f"Running batch processing via Azure OpenAI (Deployment: {model_deployment}).")

    results = []
    total_items = len(inputs)

    for idx, input_data in enumerate(inputs, 1):
        item_id = input_data.get("id", f"REQ-{idx:02d}")
        destination = input_data.get("destination", "Unknown Destination")
        days = input_data.get("days", input_data.get("duration_days", 3))
        style = input_data.get("travel_style", "cultural")
        budget = input_data.get("budget_tier", "moderate")
        prompt = input_data.get("prompt", f"Plan a travel itinerary for {destination}.")

        logger.info(f"[{idx}/{total_items}] Processing '{item_id}' ({destination}, {days} days)...")
        start_time = time.time()

        result_record = {
            "id": item_id,
            "destination": destination,
            "days": days,
            "duration_days": days,
            "travel_style": style,
            "budget_tier": budget,
            "status": "PENDING",
            "data": None,
            "error": None,
            "latency_seconds": 0.0
        }

        try:
            if use_mock:
                time.sleep(0.1)
                data = mock_generate_itinerary(destination, days, style, budget)
            else:
                data = call_openai_function(
                    prompt=prompt,
                    destination=destination,
                    days=days,
                    client=active_client,
                    model_deployment=model_deployment,
                    travel_style=style,
                    budget_tier=budget
                )

            result_record["status"] = "SUCCESS"
            result_record["data"] = data
            logger.info(f"[{idx}/{total_items}] Successfully generated itinerary for '{destination}'.")

        except Exception as exc:
            result_record["status"] = "FAILED"
            result_record["error"] = str(exc)
            logger.error(f"Error processing {destination}: {exc}", exc_info=False)

        finally:
            result_record["latency_seconds"] = round(time.time() - start_time, 2)
            results.append(result_record)

            # Optional: prevent hitting rate limits aggressively
            if idx < total_items and delay_between_requests > 0:
                time.sleep(delay_between_requests)

    return results


def format_itinerary_markdown(record: Dict[str, Any]) -> str:
    """Formats an itinerary record into presentation-grade GitHub Flavored Markdown."""
    if record["status"] != "SUCCESS" or not record["data"]:
        return f"### Request {record['id']} ({record['destination']})\n**Status:** Failed ({record['error']})\n"

    data = record["data"]
    md = []
    md.append(f"## {data.get('destination', 'Travel Destination')} - {data.get('duration_days', 3)}-Day Itinerary")
    md.append(f"**Style:** {data.get('travel_style', 'N/A').title()} | **Budget Tier:** {data.get('budget_tier', 'N/A').title()} | **Estimated Cost:** ${data.get('estimated_cost_usd', 0):,.2f} USD")
    md.append("")
    md.append("### Daily Schedule")
    md.append("")

    for day in data.get("daily_schedule", []):
        md.append(f"#### Day {day.get('day', 1)}: {day.get('theme', 'Exploration')}")
        md.append(f"- **Morning:** {day.get('morning_activity', 'N/A')}")
        md.append(f"- **Afternoon:** {day.get('afternoon_activity', 'N/A')}")
        md.append(f"- **Evening:** {day.get('evening_activity', 'N/A')}")
        md.append(f"- **Cuisine Highlight:** {day.get('highlight_cuisine', 'N/A')}")
        md.append("")

    tips = data.get("local_tips", [])
    if tips:
        md.append("### Local Tips & Logistics")
        for tip in tips:
            md.append(f"- {tip}")
        md.append("")

    md.append("---")
    return "\n".join(md)


# =====================================================================
# MAIN RUNNER
# =====================================================================
def main():
    import argparse
    parser = argparse.ArgumentParser(description="Batch Azure OpenAI Function Calling")
    parser.add_argument("--input", default=None, help="Path to JSON file containing batch inputs")
    parser.add_argument("--demo", action="store_true", help="Force offline demonstration mode")
    parser.add_argument("--output-dir", default=None, help="Directory to save sample outputs")
    parser.add_argument("--pacing", type=float, default=1.0, help="Delay in seconds between batch requests")
    args = parser.parse_args()

    script_dir = Path(__file__).parent.resolve()
    input_file = Path(args.input) if args.input else (script_dir / "sample_inputs.json")

    if not input_file.exists():
        logger.error(f"Input file not found at: {input_file}")
        sys.exit(1)

    with open(input_file, "r", encoding="utf-8") as f:
        batch_inputs = json.load(f)

    logger.info(f"Loaded {len(batch_inputs)} requests from {input_file.name}")

    client = None if args.demo else get_azure_client()
    results = batch_process(
        inputs=batch_inputs,
        client=client,
        delay_between_requests=args.pacing,
        force_demo=args.demo or (client is None)
    )

    # Print summary table
    print("\n" + "=" * 70)
    print("                 BATCH PROCESSING SUMMARY REPORT")
    print("=" * 70)
    print(f"{'ID':<10} | {'Destination':<20} | {'Status':<10} | {'Latency':<8} | {'Details'}")
    print("-" * 70)
    for r in results:
        details = f"${r['data']['estimated_cost_usd']:,.0f}" if r["status"] == "SUCCESS" else (r["error"] or "Error")
        print(f"{r['id']:<10} | {r['destination'][:20]:<20} | {r['status']:<10} | {r['latency_seconds']:<7}s | {details}")
    print("=" * 70)

    # Save outputs if output-dir is specified or save to sample_outputs/
    out_dir = Path(args.output_dir) if args.output_dir else (script_dir / "sample_outputs")
    out_dir.mkdir(parents=True, exist_ok=True)

    consolidated_md = ["# Consolidated Batch Itinerary Outputs\n\nGenerated with Azure OpenAI Function Calling.\n\n"]

    for r in results:
        file_slug = r["destination"].split(",")[0].strip().lower().replace(" ", "_")
        json_path = out_dir / f"sample_output_{r['id'].lower()}_{file_slug}.json"
        md_path = out_dir / f"sample_output_{r['id'].lower()}_{file_slug}.md"

        with open(json_path, "w", encoding="utf-8") as jf:
            json.dump(r, jf, indent=2)

        md_content = format_itinerary_markdown(r)
        with open(md_path, "w", encoding="utf-8") as mf:
            mf.write(md_content)

        consolidated_md.append(md_content)

    all_md_path = script_dir / "all_sample_itineraries.md"
    with open(all_md_path, "w", encoding="utf-8") as af:
        af.write("\n\n".join(consolidated_md))

    logger.info(f"All sample outputs written to: {out_dir}")
    logger.info(f"Consolidated markdown report written to: {all_md_path}")


if __name__ == "__main__":
    main()
