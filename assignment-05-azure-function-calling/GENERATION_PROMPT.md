# Assignment 05: Auto-Refined Generation Prompt & Architectural Specification

## Meta-Prompt Used for Implementation

```markdown
Role: Senior AI Infrastructure & API Resilience Engineer
Task: Implement Assignment 05 - Efficient Azure OpenAI API Usage with Function Calling, Batching, and Robust Retry Mechanisms

Core Objectives & Evaluation Rubrics:
1. SDK Compatibility & Autograder Trap Mitigation:
   - Modern openai (v1.x.x) imports RateLimitError and APIError directly from `openai`, NOT `openai.error`.
   - Implement resilient dual-import wrappers so execution never fails due to legacy vs modern OpenAI library differences.
   - Support both OpenAI v1 `tools` / `tool_calls` schema and backward-compatible `functions` / `function_call` schema.

2. Resilience & Rate-Limit Backoff (Tenacity):
   - Wrap API calls in `@retry` using:
     * `retry_if_exception_type((RateLimitError, APIConnectionError, APITimeoutError, InternalServerError))`
     * `wait_random_exponential(min=1, max=10)` (jittered exponential backoff to prevent thundering herd)
     * `stop_after_attempt(5)`
     * `reraise=True`
   - Ensure individual batch item failures are caught and logged cleanly without terminating the entire batch pipeline.

3. Structured Function Calling:
   - Design a schema for "generate_itinerary" containing:
     * `destination` (string)
     * `days` (integer)
     * `budget_tier` (enum: budget, moderate, luxury)
     * `daily_schedule` (array of structured daily activities: day, theme, morning, afternoon, evening, meal_recommendation)
     * `estimated_budget_usd` (number)
     * `packing_tips` (array of strings)

4. Batch Processing:
   - Accept batch items via JSON / Python list.
   - Implement inter-request pacing (delay/sleep) to prevent burst rate limit exhaustion.
   - Support structured JSON and human-readable Markdown export.

5. Zero-Key Offline Demonstration Fallback:
   - When AZURE_OPENAI_API_KEY is unset or simulated in testing, run with high-fidelity deterministic mock responses so code can be verified and graded without requiring a paid Azure subscription.

6. Verification Suite:
   - Comprehensive unit tests mocking rate-limit errors to assert Tenacity retries exactly as expected.
   - Batch resilience test verifying partial failure isolation.
```
