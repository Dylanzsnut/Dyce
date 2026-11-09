"""
Assignment 04: Building an AI-Powered Conversational Assistant with Advanced Prompting Techniques
-------------------------------------------------------------------------------------------------
Simulates an Event Management Assistant utilizing:
- Role-based message construction (system, user, assistant)
- Few-shot prompting for attendee sentiment analysis
- Chain-of-Thought (CoT) prompting for step-by-step reasoning
- Multi-turn conversational context preservation
- Offline demonstration mode (when Azure credentials are not set)
- Interactive CLI mode (--interactive)

Required Environment Variables:
- AZURE_OPENAI_API_KEY: Your Azure OpenAI resource API key
- AZURE_OPENAI_ENDPOINT: Your Azure OpenAI resource endpoint URL
- AZURE_OPENAI_DEPLOYMENT_NAME: Model deployment name (defaults to 'gpt-4o-mini')
"""

import argparse
import os
import sys
from pathlib import Path
from openai import AzureOpenAI, OpenAIError

try:
    from dotenv import load_dotenv

    load_dotenv(Path(__file__).resolve().parent / ".env")
    load_dotenv()
except ImportError:
    pass

API_VERSION = "2024-07-01-preview"
DEFAULT_DEPLOYMENT = "gpt-4o-mini"

# Module-level aliases matching specification snippets
api_version = os.getenv("AZURE_OPENAI_API_VERSION", API_VERSION)
deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", DEFAULT_DEPLOYMENT)
client = None

SYSTEM_PROMPT = (
    "You are an expert event management assistant specializing in corporate conferences, "
    "networking galas, and product launches. Your capabilities include providing "
    "conversation starters, evaluating attendee sentiment with clear explanations, and "
    "solving logistical problems using step-by-step chain-of-thought reasoning while "
    "maintaining continuous conversational context across multiple turns."
)

# Step 1: Few-Shot Examples for Sentiment Analysis
FEW_SHOT_SENTIMENT_EXAMPLES = [
    {
        "role": "user",
        "content": "Analyze the sentiment of this text: 'I love attending networking events!'",
    },
    {
        "role": "assistant",
        "content": "Sentiment: Positive. The text expresses enthusiasm and enjoyment.",
    },
    {
        "role": "user",
        "content": "Analyze the sentiment of this text: 'Networking can be really stressful sometimes.'",
    },
    {
        "role": "assistant",
        "content": "Sentiment: Negative. The text shows discomfort and stress related to networking.",
    },
    {
        "role": "user",
        "content": "Analyze the sentiment of this text: 'The agenda was fine, though registration took a bit longer than expected.'",
    },
    {
        "role": "assistant",
        "content": "Sentiment: Neutral / Mixed. The text acknowledges an acceptable agenda alongside a minor logistical delay.",
    },
]

# Step 2: Three Multi-Turn Scenarios Demonstrating CoT, Sentiment & Context
SAMPLE_SCENARIOS = [
    {
        "id": 1,
        "title": "Networking Conversation Starters & Attendee Feedback Analysis",
        "turns": [
            {
                "user": (
                    "What are some good conversation starters at networking events? "
                    "Explain your reasoning step-by-step."
                ),
            },
            {
                "user": (
                    "Analyze the sentiment of this feedback from an attendee yesterday: "
                    "'I found the networking lounge too loud to have meaningful discussions, "
                    "though the icebreaker app was helpful.'"
                ),
            },
            {
                "user": (
                    "Given that feedback and your earlier conversation starter recommendations, "
                    "how should we reconfigure the lounge layout for this evening's session?"
                ),
            },
        ],
    },
    {
        "id": 2,
        "title": "Venue Capacity & Catering Budget Trade-Off Reasoning",
        "turns": [
            {
                "user": (
                    "We need to select a venue for a 200-person tech symposium dinner with a $35,000 budget. "
                    "Venue A: $18,000 flat rental fee + $75/person catering (includes AV). "
                    "Venue B: $12,000 flat rental fee + $95/person catering + $2,500 mandatory AV fee. "
                    "Calculate the total costs step-by-step, factor in a 10% contingency reserve, "
                    "and provide your recommendation."
                ),
            },
            {
                "user": (
                    "Analyze the sentiment of this message from our keynote sponsor: "
                    "'We are thrilled to sponsor the symposium dinner, provided the main stage has dual projection screens.'"
                ),
            },
            {
                "user": (
                    "Considering our budget calculation for Venue A vs B and the sponsor's screen request, "
                    "which venue gives us the financial headroom to accommodate their AV requirement?"
                ),
            },
        ],
    },
    {
        "id": 3,
        "title": "Outdoor Gala Weather Risk Mitigation & Crisis Management",
        "turns": [
            {
                "user": (
                    "We have an outdoor awards gala for 300 guests scheduled tomorrow night at 7:00 PM. "
                    "The forecast reports a 45% chance of severe thunderstorms between 6:00 PM and 9:00 PM. "
                    "Option 1: Tent the lawn for $6,500 (requires 5-hour advance notice, deadline 1:00 PM). "
                    "Option 2: Move into the indoor backup ballroom for $2,000 flip fee, but max ballroom capacity is 260. "
                    "Walk through your risk-mitigation reasoning step-by-step and provide an action timeline."
                ),
            },
            {
                "user": (
                    "Analyze the sentiment of this comment posted by a VIP guest on the event app: "
                    "'Really hoping the banquet isn't crammed indoors if it drizzles; the outdoor garden is why I bought tickets.'"
                ),
            },
            {
                "user": (
                    "Based on that guest sentiment and your step-by-step decision framework, "
                    "what is our final call at the 1:00 PM decision cutoff, and how do we communicate it?"
                ),
            },
        ],
    },
]


# Step 3: Azure Client Initialization
def create_azure_client():
    """Initialize and return the AzureOpenAI client and deployment name from env vars."""
    api_key = (os.getenv("AZURE_OPENAI_API_KEY") or "").strip()
    endpoint = (os.getenv("AZURE_OPENAI_ENDPOINT") or "").strip()
    curr_api_version = (os.getenv("AZURE_OPENAI_API_VERSION") or API_VERSION).strip()
    curr_deployment = (
        os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME") or DEFAULT_DEPLOYMENT
    ).strip()

    missing = []
    if not api_key:
        missing.append("AZURE_OPENAI_API_KEY")
    if not endpoint:
        missing.append("AZURE_OPENAI_ENDPOINT")

    if missing:
        raise EnvironmentError(
            f"Missing required environment variable(s): {', '.join(missing)}.\n"
            "Please configure your .env file or export these variables in your terminal."
        )

    client_inst = AzureOpenAI(
        api_version=curr_api_version,
        azure_endpoint=endpoint,
        api_key=api_key,
    )
    return client_inst, curr_deployment


# Step 4: Multi-Turn Conversation Runner
class ConversationalAssistantSession:
    """Manages role-based multi-turn conversation messages, few-shot prompts, and context."""

    def __init__(self, system_prompt=SYSTEM_PROMPT, few_shots=None):
        self.messages = [{"role": "system", "content": system_prompt}]
        if few_shots:
            self.messages.extend(few_shots)

    def add_user_message(self, content):
        self.messages.append({"role": "user", "content": content})

    def add_assistant_message(self, content):
        self.messages.append({"role": "assistant", "content": content})

    def get_messages(self):
        return list(self.messages)


def run_turn(
    session,
    user_input,
    client=None,
    deployment_name=None,
    temperature=0.7,
):
    """Execute a single conversational turn with role tracking and context preservation."""
    session.add_user_message(user_input)

    if client is None or deployment_name is None:
        client, deployment_name = create_azure_client()

    response = client.chat.completions.create(
        model=deployment_name,
        messages=session.get_messages(),
        temperature=temperature,
    )
    reply = response.choices[0].message.content or ""
    clean_reply = reply.strip()
    session.add_assistant_message(clean_reply)
    return clean_reply


def run_full_scenario(scenario, client, deployment_name):
    """Run all conversational turns for a scenario, demonstrating context preservation."""
    session = ConversationalAssistantSession(
        system_prompt=SYSTEM_PROMPT,
        few_shots=FEW_SHOT_SENTIMENT_EXAMPLES,
    )

    history_records = []
    print(f"\n=======================================================")
    print(f"Scenario {scenario['id']}: {scenario['title']}")
    print(f"=======================================================")

    for idx, turn in enumerate(scenario["turns"], start=1):
        user_msg = turn["user"]
        print(f"\n[Turn {idx} - User]:\n{user_msg}\n")

        assistant_msg = run_turn(
            session=session,
            user_input=user_msg,
            client=client,
            deployment_name=deployment_name,
        )
        print(f"[Turn {idx} - Assistant]:\n{assistant_msg}\n")
        history_records.append(
            {
                "turn": idx,
                "user": user_msg,
                "assistant": assistant_msg,
            }
        )

    return history_records


# Step 5: Save Verified Outputs & Offline Demonstration Support
def save_sample_outputs(all_results, output_dir):
    """Write individual scenario Markdown records and a consolidated report."""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    combined_lines = [
        "# AI-Powered Conversational Assistant — Verified Sample Outputs (3 Samples)\n",
        "Demonstrating role-based messaging, few-shot sentiment analysis, chain-of-thought reasoning, and multi-turn context retention.\n",
    ]

    for scenario_res in all_results:
        s_id = scenario_res["id"]
        title = scenario_res["title"]
        turns = scenario_res["turns"]

        single_lines = [
            f"# Sample Conversation {s_id:02d}: {title}\n",
            f"**System Prompt:** `{SYSTEM_PROMPT}`\n",
            f"**Few-Shot Exemplars Injected:** {len(FEW_SHOT_SENTIMENT_EXAMPLES)} messages\n\n---\n",
        ]

        combined_lines.append(f"## Scenario {s_id}: {title}\n")

        for t in turns:
            turn_md = (
                f"### Turn {t['turn']}\n"
                f"**User Query:**\n> {t['user']}\n\n"
                f"**Assistant Response (Chain-of-Thought / Sentiment / Context):**\n\n"
                f"{t['assistant']}\n\n---\n"
            )
            single_lines.append(turn_md)
            combined_lines.append(turn_md)

        sample_file = output_dir / f"sample_0{s_id}_conversation.md"
        sample_file.write_text("\n".join(single_lines), encoding="utf-8")

    combined_file = output_dir.parent / "all_sample_conversations.md"
    combined_file.write_text("\n".join(combined_lines), encoding="utf-8")


def run_interactive_ui(client, deployment_name):
    """Run interactive CLI multi-turn assistant session."""
    session = ConversationalAssistantSession(
        system_prompt=SYSTEM_PROMPT,
        few_shots=FEW_SHOT_SENTIMENT_EXAMPLES,
    )

    print("\n=======================================================")
    print("   Event Management Assistant — Interactive Console   ")
    print("=======================================================")
    print("Type your questions or attendee feedback below.")
    print("Context is preserved automatically across turns.")
    print("Commands: 'exit' or 'quit' to end session; 'reset' to start fresh.\n")

    turn_count = 1
    while True:
        try:
            user_input = input(f"[Turn {turn_count}] You: ").strip()
            if not user_input:
                continue
            if user_input.lower() in ("exit", "quit", "q"):
                print("Exiting conversational assistant. Goodbye!")
                break
            if user_input.lower() == "reset":
                session = ConversationalAssistantSession(
                    system_prompt=SYSTEM_PROMPT,
                    few_shots=FEW_SHOT_SENTIMENT_EXAMPLES,
                )
                turn_count = 1
                print("--- Conversation reset. Context cleared. ---")
                continue

            reply = run_turn(
                session=session,
                user_input=user_input,
                client=client,
                deployment_name=deployment_name,
            )
            print(f"\nAssistant:\n{reply}\n")
            turn_count += 1
        except (KeyboardInterrupt, EOFError):
            print("\nExiting conversational assistant. Goodbye!")
            break


# Step 6: CLI Entry Point
def main():
    parser = argparse.ArgumentParser(
        description="AI-Powered Conversational Assistant with Advanced Prompting Techniques"
    )
    parser.add_argument(
        "--interactive",
        action="store_true",
        help="Launch interactive multi-turn console chat with the assistant.",
    )
    parser.add_argument(
        "--scenario",
        type=int,
        choices=[1, 2, 3],
        help="Run a specific sample scenario (1, 2, or 3).",
    )
    args = parser.parse_args()

    base_dir = Path(__file__).resolve().parent
    outputs_dir = base_dir / "sample_outputs"

    try:
        azure_client, curr_deployment = create_azure_client()
    except EnvironmentError as env_err:
        # Offline demonstration fallback mode: display verified precomputed outputs
        combined_file = base_dir / "all_sample_conversations.md"
        if combined_file.exists() and not args.interactive:
            print("================================================================")
            print("Notice: Azure OpenAI credentials not detected in .env/environment.")
            print("Displaying verified conversation samples in offline demonstration mode.")
            print("(To run live LLM completions, configure .env with your Azure key.)")
            print("================================================================\n")
            print(combined_file.read_text(encoding="utf-8"))
            return
        print(f"Configuration Error:\n{env_err}", file=sys.stderr)
        sys.exit(1)

    if args.interactive:
        run_interactive_ui(azure_client, curr_deployment)
        return

    # Batch or single scenario execution
    scenarios_to_run = (
        [s for s in SAMPLE_SCENARIOS if s["id"] == args.scenario]
        if args.scenario
        else SAMPLE_SCENARIOS
    )

    all_results = []
    for s in scenarios_to_run:
        history = run_full_scenario(s, azure_client, curr_deployment)
        all_results.append(
            {
                "id": s["id"],
                "title": s["title"],
                "turns": history,
            }
        )

    save_sample_outputs(all_results, outputs_dir)
    print(f"\nSuccessfully generated and saved all scenario outputs to: {outputs_dir}")


if __name__ == "__main__":
    main()
