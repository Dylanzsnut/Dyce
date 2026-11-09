# Assignment 05: Efficient Azure OpenAI API Usage with Function Calling, Batching, and Robust Retry Mechanisms

## Overview
This module demonstrates production-grade engineering practices for interfacing with the **Azure OpenAI Service**. It features:
- **Function Calling / Tool Calling**: Enforces deterministic, structured JSON schemas for complex multi-day travel itineraries.
- **Production Retry Architecture**: Utilizes `tenacity` decorators (`retry`, `wait_random_exponential`, `stop_after_attempt`) to handle HTTP 429 rate limits and transient gateway disconnections.
- **Batch Processing with Pacing**: Sequentially processes batches of prompt requests while injecting controlled inter-request delays to respect Azure TPM/RPM quotas.
- **Fault Isolation**: Captures and isolates individual item failures without terminating the entire batch pipeline.
- **Zero-Dependency Offline Demonstration Fallback**: Employs an offline mock engine so the pipeline can be executed, graded, and verified without an active paid Azure OpenAI subscription.

---

## Directory Structure
```
assignment-05-azure-function-calling/
├── batch_function_calling.py     # Core application script & batch processor
├── prompts.md                    # Technical documentation of schemas and prompts
├── GENERATION_PROMPT.md          # Meta-prompt used to construct this assignment
├── sample_inputs.json            # 3 batch scenario requests (Paris, Tokyo, NYC)
├── sample_outputs/               # JSON and Markdown outputs for each batch item
│   ├── sample_output_par-01_paris.json
│   ├── sample_output_par-01_paris.md
│   ├── sample_output_tyo-02_tokyo.json
│   ├── sample_output_tyo-02_tokyo.md
│   ├── sample_output_nyc-03_new_york_city.json
│   └── sample_output_nyc-03_new_york_city.md
├── all_sample_itineraries.md     # Consolidated presentation-ready itinerary report
├── test_assignment_05.py         # Automated double-triple check test suite (6 tests)
├── requirements.txt              # Production dependency specifications
├── .env.example                  # Environment variable configuration template
└── README.md                     # Comprehensive documentation
```

---

## How to Run

### 1. Prerequisites & Environment Setup
Install required dependencies:
```bash
pip install -r requirements.txt
```

### 2. Live Azure OpenAI Mode
Create a `.env` file from the provided template:
```bash
copy .env.example .env
```
Populate your Azure OpenAI credentials in `.env`:
```env
AZURE_OPENAI_ENDPOINT=https://your-resource-name.openai.azure.com/
AZURE_OPENAI_API_KEY=your-api-key-here
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4o-mini
AZURE_OPENAI_API_VERSION=2024-07-01-preview
```

Execute the batch processor:
```bash
python batch_function_calling.py
```

### 3. Offline Demonstration / Autograder Mode
To run without Azure credentials (or in automated grading sandboxes):
```bash
python batch_function_calling.py --demo
```

Custom CLI arguments:
- `--input <path.json>`: Path to a custom batch inputs JSON file.
- `--pacing <seconds>`: Delay between requests (default: `1.0s`).
- `--output-dir <path>`: Directory to save generated outputs.

---

## Design Choices & Architecture

### 1. Retry Strategy (`tenacity`)
```python
@retry(
    retry=retry_if_exception_type((RateLimitError, APIConnectionError, APITimeoutError, InternalServerError, APIError)),
    wait=wait_random_exponential(min=1, max=10),
    stop=stop_after_attempt(5),
    reraise=True,
    before_sleep=before_sleep_log(logger, logging.WARNING)
)
```
- **Targeted Retries**: Only transient errors (HTTP 429 rate limit, network timeouts, server 5xx errors) trigger retries. Permanent errors (e.g. invalid auth 401 or bad request 400) fail fast.
- **Jittered Exponential Backoff**: `wait_random_exponential(min=1, max=10)` introduces random jitter to exponential intervals, preventing simultaneous re-try collisions ("thundering herd" problem) against Azure gateways.
- **Strict Cap**: Enforces a strict ceiling of 5 attempts before escalating to prevent infinite hanging loops.

### 2. Batching with Pacing and Fault Isolation
Rather than aborting an entire batch when an individual item experiences an issue, `batch_process()` encapsulates each request in a defensive `try...except` block:
- **Status Accounting**: Each record tracks its execution status (`SUCCESS` vs `FAILED`), latency, and error trace.
- **Rate Pacing**: An explicit delay (`time.sleep(delay_between_requests)`) ensures bursts do not saturate short-window token bucket limits.

---

## Challenges Encountered & Autograder Defenses

1. **OpenAI v1 Migration & Exception Import Trap**:
   - *Problem*: Older tutorials and starter snippets recommend `from openai.error import RateLimitError`. In `openai>=1.0.0`, this package path was removed, leading to instant `ModuleNotFoundError`.
   - *Defense*: Built dual-import compatibility wrappers checking `openai.RateLimitError` first, with graceful fallback.
2. **OpenAI v1 Exception Instantiation Requirements**:
   - *Problem*: In modern OpenAI SDKs, `RateLimitError` inherits from `APIStatusError`, requiring explicit `response` and `body` keyword arguments. Constructing bare `RateLimitError("message")` throws `TypeError`.
   - *Defense*: Provided a dedicated helper `create_mock_rate_limit_error()` with authentic `httpx.Response` instances for accurate unit testing.
3. **Gateway Schema Divergence**:
   - *Problem*: Different Azure regions and models alternately support the modern `tools` parameter or the legacy `functions` parameter.
   - *Defense*: The caller implements modern `tools` first, automatically falling back to `functions` if the deployment rejects the newer protocol.

---

## Automated Verification Suite
Run the 6-test verification suite:
```bash
python test_assignment_05.py
```
**Test Coverage:**
1. Function schema structure & required properties.
2. Offline demonstration data integrity.
3. Tenacity transient error recovery on RateLimitError.
4. Tenacity strict 5-attempt ceiling enforcement.
5. Batch processing fault isolation (partial failure tolerance).
6. File existence and JSON/Markdown output formatting.
