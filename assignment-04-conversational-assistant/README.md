# Assignment 04: Building an AI-Powered Conversational Assistant with Advanced Prompting Techniques

A modular conversational AI application built with Python 3.12 and **Azure OpenAI (`gpt-4o-mini`)** demonstrating **role-based message construction**, **few-shot prompting**, **chain-of-thought (CoT) reasoning**, and **multi-turn conversational context preservation** within the domain of an expert **Event Management Assistant**.

---

## 1. Objectives & Concepts Covered

- **Role Assignment:** Proper construction of conversation messages utilizing the `system`, `user`, and `assistant` roles in Azure OpenAI chat completions.
- **Few-Shot Prompting:** In-context exemplars embedded within conversation history to establish the exact output format and criteria for attendee sentiment analysis.
- **Chain-of-Thought (CoT) Reasoning:** Prompting strategies that guide the model to break complex logistical and analytical challenges down into clear, numbered, step-by-step reasoning phases before reaching a conclusion.
- **Multi-Turn Context Management:** Retaining ongoing dialogue history across consecutive turns so the assistant seamlessly resolves references to prior topics, decisions, and calculations.
- **Offline Demonstration Fallback Mode:** Allows grading and demonstration runs even without live Azure credentials by surfacing precomputed, verified outputs.
- **Prompt Transparency (`prompts.md`):** Complete documentation of all prompt templates, few-shot demonstration pairs, and reasoning triggers.

---

## 2. Directory Structure

```text
assignment-04-conversational-assistant/
├── .env.example                               # Azure OpenAI credentials template
├── requirements.txt                           # Python dependencies (openai, python-dotenv)
├── conversational_assistant.py                # Main conversational application & CLI
├── test_assignment_04.py                      # Automated test suite (5 double-check tests)
├── GENERATION_PROMPT.md                       # Auto-refined prompt used to create this assignment
├── prompts.md                                 # Full prompt engineering specifications & templates
├── README.md                                  # Documentation and run instructions
├── all_sample_conversations.md                # Consolidated report of all 3 multi-turn scenarios
└── sample_outputs/                            # Individual scenario conversation logs
    ├── sample_01_conversation.md              # Scenario 1: Networking Starters & Sentiment
    ├── sample_02_conversation.md              # Scenario 2: Venue Budget & Trade-Offs
    └── sample_03_conversation.md              # Scenario 3: Weather Contingency Planning
```

---

## 3. Advanced Prompting Techniques Explained

### 3.1 Few-Shot Prompting (In-Context Sentiment Analysis)
Instead of relying solely on zero-shot instructions, the assistant incorporates structured few-shot pairs directly into the conversation stream:
```python
few_shot_examples = [
    {"role": "user", "content": "Analyze the sentiment of this text: 'I love attending networking events!'"},
    {"role": "assistant", "content": "Sentiment: Positive. The text expresses enthusiasm and enjoyment."},
    {"role": "user", "content": "Analyze the sentiment of this text: 'Networking can be really stressful sometimes.'"},
    {"role": "assistant", "content": "Sentiment: Negative. The text shows discomfort and stress related to networking."},
    ...
]
```
**Benefits:**
- Enforces consistent output format (`Sentiment: [Category]. Explanation: [Reason]`).
- Calibrates the model to distinguish between mixed feedback and purely negative feedback without requiring specialized fine-tuning or JSON schemas.

### 3.2 Chain-of-Thought (CoT) Prompting
When dealing with subjective advice (networking starters), mathematical planning (budget formulas), or risk management (weather thresholds), prompts append explicit reasoning directives:
> *"What are some good conversation starters at networking events? Explain your reasoning step-by-step."*

**Benefits:**
- Prevents premature conclusions or arithmetic hallucinations by forcing the model to generate intermediate logical tokens.
- Produces transparent, verifiable advice that event organizers can defend to stakeholders.

### 3.3 Context Preservation Across Conversation History
Conversational state is maintained by appending previous assistant answers and user prompts into a cumulative `messages` list:
```python
messages = [
    {"role": "system", "content": SYSTEM_PROMPT},
    *FEW_SHOT_SENTIMENT_EXAMPLES,
    {"role": "user", "content": turn_1_question},
    {"role": "assistant", "content": turn_1_answer},
    {"role": "user", "content": turn_2_question}, # Follow-up referencing turn 1
]
```
**Benefits:**
- Enables the assistant to understand referential pronouns (*"Given that feedback..."*, *"Which venue allows that?"*) without repeating context.

---

## 4. Setup & Running

### Prerequisites
- Python 3.12 installed
- Azure OpenAI Resource (optional for offline demonstration mode)

### Install Dependencies
```powershell
py -3.12 -m pip install -r requirements.txt
```

### Configure Credentials (Optional for Live Execution)
Copy `.env.example` to `.env`:
```ini
AZURE_OPENAI_API_KEY=your_key_here
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4o-mini
AZURE_OPENAI_API_VERSION=2024-07-01-preview
```

---

## 5. Execution Modes

### Mode 1: Batch Run of All 3 Scenarios (Default)
```powershell
py -3.12 conversational_assistant.py
```
*(If no `.env` is configured, automatically runs in offline demonstration mode, displaying all 3 verified multi-turn scenario outputs without crashing).*

### Mode 2: Run a Specific Scenario
```powershell
py -3.12 conversational_assistant.py --scenario 1
```

### Mode 3: Interactive Multi-Turn Console UI
```powershell
py -3.12 conversational_assistant.py --interactive
```
Launches a live chat session where conversation context is preserved across each message you enter.
