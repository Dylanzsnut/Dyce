# Prompts Specification & Engineering Guide — Assignment 04

This document details the exact prompt architectures, system prompts, few-shot demonstration exemplars, chain-of-thought (CoT) reasoning triggers, and conversational context management strategies implemented in `conversational_assistant.py`.

---

## 1. System Prompt

The system prompt establishes the AI persona, domain boundary, and behavioral guidelines as an expert Event Management Assistant:

```text
You are an expert event management assistant specializing in corporate conferences, networking galas, and product launches.
Your capabilities include:
1. Providing actionable, psychologically grounded conversation starters and networking strategies.
2. Performing sentiment analysis on attendee feedback with clear category labeling and evidence-based justifications.
3. Conducting rigorous, step-by-step Chain-of-Thought (CoT) reasoning for logistical, budgeting, and crisis planning problems.
4. Maintaining seamless multi-turn conversational context across iterative planning requests.

Always maintain a professional, encouraging, and structured tone. When asked for reasoning or analysis, clearly enumerate your logical steps.
```

### Rationale:
- **Role Anchoring:** Directly grounds the model in event planning domain knowledge.
- **Output Constraints:** Explicitly commands evidence-based justifications and enumerated reasoning steps.

---

## 2. Few-Shot Prompting: In-Context Sentiment Analysis

Few-shot prompting embeds input/output demonstration pairs directly into the conversation history using standard `user` and `assistant` message roles. This establishes the target output schema without requiring JSON-mode constraints.

### Exemplar 1 (Positive Enthusiasm):
- **User:**
  ```text
  Analyze the sentiment of this attendee feedback: 'I absolutely loved the keynote speaker and the interactive breakout rooms! Best summit yet.'
  ```
- **Assistant:**
  ```text
  Sentiment: Positive.
  Explanation: The attendee expresses strong enthusiasm and high satisfaction using superlative language ('absolutely loved', 'Best summit yet') and specifically praises the speaker and breakout sessions.
  ```

### Exemplar 2 (Negative / Frustration):
- **User:**
  ```text
  Analyze the sentiment of this attendee feedback: 'The venue Wi-Fi was completely unusable and the badge pickup line took over 45 minutes.'
  ```
- **Assistant:**
  ```text
  Sentiment: Negative.
  Explanation: The feedback highlights acute logistical friction and dissatisfaction regarding critical infrastructure ('completely unusable Wi-Fi') and excessive delay ('over 45 minutes').
  ```

### Exemplar 3 (Neutral / Constructive Mixed):
- **User:**
  ```text
  Analyze the sentiment of this attendee feedback: 'The catering options were adequate, but having more vegan lunch choices would be helpful next year.'
  ```
- **Assistant:**
  ```text
  Sentiment: Neutral / Constructive.
  Explanation: The tone is balanced and matter-of-fact; 'adequate' denotes acceptable baseline performance, followed by a forward-looking suggestion rather than a complaint.
  ```

---

## 3. Chain-of-Thought (CoT) Prompting

Chain-of-thought prompting forces the model to articulate intermediate reasoning steps before arriving at a final recommendation, mitigating hallucination and improving logical consistency.

### CoT Trigger Pattern:
```text
[Task or Problem Description]
Explain your reasoning step-by-step, evaluating constraints, trade-offs, and failure modes before giving your final recommendation.
```

### Application in Sample 1 (Networking Conversation Starters):
- **Prompt:**
  ```text
  What are some effective conversation starters for introverted attendees at an evening tech networking reception? Explain your psychological reasoning step-by-step.
  ```

### Application in Sample 2 (Venue Selection & Budget Trade-off):
- **Prompt:**
  ```text
  We have a budget of $35,000 for a 200-person tech symposium dinner. Venue A costs $18,000 rental + $75/person catering (including AV). Venue B costs $12,000 rental + $95/person catering, but charges a $2,500 mandatory AV technician fee. Evaluate the total costs step-by-step, factor in a 10% contingency reserve, and recommend the best choice.
  ```

### Application in Sample 3 (Outdoor Gala Rain Contingency):
- **Prompt:**
  ```text
  A 40% chance of heavy thunderstorm is forecasted 3 hours before our 300-guest outdoor awards banquet. Tenting costs $6,500 with a 4-hour setup cutoff, while moving indoors to the ballroom requires a $2,000 flip fee but reduces capacity to 260 seats. Walk through your risk-mitigation reasoning step-by-step and provide an actionable decision framework.
  ```

---

## 4. Multi-Turn Context Maintenance

In multi-turn conversations, the assistant preserves context by appending prior turns (`user` query and `assistant` response) to the message list passed to `client.chat.completions.create(messages=...)`.

### Context Continuation Pattern:
1. **Turn 1 (CoT Planning):** User asks for strategy/analysis. Assistant responds with step-by-step rationale.
2. **Turn 2 (Few-Shot Guided Sentiment Analysis):** User feeds attendee feedback from that specific scenario. Assistant classifies sentiment matching the few-shot template.
3. **Turn 3 (Contextual Synthesis):** User asks a follow-up question referencing prior turns (e.g. *"Based on that feedback and the venue we selected earlier, what immediate adjustment should we make to tomorrow's schedule?"*).
4. **Resolution:** Assistant resolves ambiguous pronouns (*"that feedback"*, *"the venue"*) by referencing the ongoing message history.
