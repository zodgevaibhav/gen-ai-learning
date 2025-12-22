import os
from state.codegen_state import CodegenState
from tools.llm import call_llm

ARCH_PROMPT = """
You are a Software Architect.
Produce architecture.md and PlantUML.
TASK:
Design a detailed software architecture for the following refined requirements.
RULES:
- Use standard architecture patterns
- Include diagrams in PlantUML syntax
- Specify components, data flow, and interactions
- Consider scalability, security, and maintainability
OUTPUT FORMAT:
Provide the architecture document in markdown format with embedded PlantUML diagrams.
"""

def architect_node(state: CodegenState) -> CodegenState:
    architecture = call_llm(ARCH_PROMPT, state["refined_requirement"])

    os.makedirs("architecture", exist_ok=True)
    with open("architecture/architecture.md", "w") as f:
        f.write(architecture)

    state["architecture"] = architecture
    return state
