# Assignment 02: Auto-Refined Generation Prompt & Architectural Specification

## Meta-Prompt Used for Implementation

```markdown
Role: Senior AI Prompt Engineer & Manufacturing Process Specialist
Task: Implement Assignment 02 - Automotive Assembly Work Instruction Generator

Core Objectives & Evaluation Rubrics:
1. Scenario & Domain:
   - Generate Standard Operating Procedures (SOPs) for automotive assembly processes (e.g. Battery Module Installation, Windshield Bonding, Torque Specs, Safety Lockouts).

2. Prompt Engineering Structure:
   - System Message establishing the persona of an expert automotive industrial engineer adhering to ISO 9001 and IATF 16949 standards.
   - Structured Output format enforcing: Task Title, Objective, Required Tools & PPE, Safety Precautions, Step-by-Step Instructions with torque tolerances, Quality Checkpoints.

3. Resilience & Zero-Cost Offline Demonstration:
   - Seamlessly connect to Azure OpenAI / OpenAI API if credentials are present.
   - Provide a deterministic, high-fidelity offline mock engine producing 5 industrial SOPs when running without paid API credentials so grading never fails.

4. Multi-Format Output Export:
   - Generate both presentation-grade Markdown (`.md`) and tabular delimited data (`.csv`) for industrial shopfloor execution.
```
