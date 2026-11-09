# Assignment 03: Auto-Refined Generation Prompt & Architectural Specification

## Meta-Prompt Used for Implementation

```markdown
Role: Senior AI NLP Architect & Executive Intelligence Specialist
Task: Implement Assignment 03 - AI-Powered Meeting Summarizer

Core Objectives & Evaluation Rubrics:
1. Executive Intelligence Extraction:
   - Extract core meeting purpose, attendees, executive summary, key decisions made, action items (with owner and deadline), and open risks/blockers.

2. Transcript Processing & Chunking:
   - Ingest raw conversational meeting transcripts containing speaker labels, timestamps, and multi-speaker exchanges.
   - Support realistic edge cases: informal speech, tangent discussions, conflicting opinions, and unclear action owners.

3. Resilience & Demonstration Engine:
   - Connect to Azure OpenAI Service if environment credentials exist.
   - Provide a deterministic fallback engine with 5 comprehensive sample transcripts and 5 structured outputs across Product, Engineering, Design, Incident Response, and Executive Syncs.

4. Formats:
   - Export individual Markdown summary reports as well as a consolidated master executive document.
```
