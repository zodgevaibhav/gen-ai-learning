from state.codegen_state import CodegenState
from tools.llm import call_llm
import os

REFINER_PROMPT = """
You are a Senior Business Analyst and Solution Architect.

TASK:
Refine the given requirement into a DETAILED, STRUCTURED specification.

RULES:
- Do NOT assume features not mentioned
- Explicitly list assumptions
- Clearly separate Functional vs Non-Functional requirements
- Include validation rules
- Include error scenarios
- Be implementation-agnostic
- Use clear numbered sections

OUTPUT FORMAT:

1. Business Context
2. Actors / Roles
3. Functional Requirements
4. Validation Rules
5. Data Model (logical)
6. API Requirements
7. Non-Functional Requirements
8. Constraints & Assumptions
9. Out of Scope
"""

def requirement_refiner_node(state: CodegenState) -> CodegenState:
    refined = call_llm(REFINER_PROMPT, state["raw_requirement"])

    os.makedirs("requirements", exist_ok=True)
    with open("requirements/refined_requirements.md", "w") as f:
        f.write(refined)

    state["refined_requirement"] = refined
    return state
