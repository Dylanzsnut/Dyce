# Prompts and Function Calling Specifications: Assignment 05

## 1. Domain Overview
This assignment implements an intelligent **Travel Itinerary Architect** leveraging Azure OpenAI Function Calling / Tool Calling to enforce deterministic structured JSON output.

---

## 2. Function Calling Schema (`generate_itinerary`)

The function schema requires the LLM to structure travel planning data into validated fields:

```json
{
  "name": "generate_itinerary",
  "description": "Generate a detailed day-by-day travel itinerary with scheduled activities, budget estimates, and recommendations.",
  "parameters": {
    "type": "object",
    "properties": {
      "destination": {
        "type": "string",
        "description": "Target city and country for travel"
      },
      "duration_days": {
        "type": "integer",
        "description": "Total number of itinerary days"
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
            "day": { "type": "integer" },
            "theme": { "type": "string" },
            "morning_activity": { "type": "string" },
            "afternoon_activity": { "type": "string" },
            "evening_activity": { "type": "string" },
            "highlight_cuisine": { "type": "string" }
          },
          "required": ["day", "theme", "morning_activity", "afternoon_activity", "evening_activity", "highlight_cuisine"]
        }
      },
      "local_tips": {
        "type": "array",
        "items": { "type": "string" },
        "description": "Essential transit, cultural etiquette, or safety tips"
      }
    },
    "required": ["destination", "duration_days", "travel_style", "budget_tier", "estimated_cost_usd", "daily_schedule", "local_tips"]
  }
}
```

---

## 3. System Prompt Template
```text
You are an expert global travel architect and concierge.
Your mission is to formulate structured, realistic, and culturally enriched travel itineraries based on user constraints.
You must always structure your output by invoking the `generate_itinerary` function with complete, actionable day-by-day details.
```

---

## 4. User Prompt Batch Template
```text
Generate a comprehensive {duration_days}-day itinerary for {destination}.
Style preference: {travel_style}.
Budget level: {budget_tier}.
Ensure daily activities are logically grouped by neighborhood to minimize transit fatigue.
```

---

## 5. Tenacity Retry Strategy
- **Target Exceptions:** `RateLimitError` (HTTP 429), `APIConnectionError`, `APITimeoutError`, `InternalServerError` (HTTP 500/503).
- **Backoff Algorithm:** `wait_random_exponential(min=1, max=10)`
  - Adds jittered random delay between \( 1.0 \times 2^{\text{attempt}} \) bounded by 10s to prevent synchronization bottlenecks.
- **Maximum Attempts:** `stop_after_attempt(5)`
- **Exception Isolation:** Unrecoverable items catch errors, log diagnostic trace, and record status `FAILED` in the batch summary while permitting other batch requests to succeed.
