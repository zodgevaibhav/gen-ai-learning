from state.codegen_state import CodegenState
from tools.llm import call_llm
import os

PERFORMANCE_PROMPT = """
You are a Performance Architect.

TASK:
Analyze the given architecture and identify:
- Potential bottlenecks
- Scalability risks
- Database & API performance concerns
- Caching, async, or indexing recommendations

RULES:
- Be architecture-driven
- Do NOT redesign system
- Output bullet points only
"""

def performance_skill_node(state: CodegenState) -> CodegenState:
    print("\n⚡ Running Performance Analysis Skill...")

    findings = call_llm(
        PERFORMANCE_PROMPT,
        state["architecture"]
    )

    os.makedirs("analysis", exist_ok=True)
    with open("analysis/performance.md", "w") as f:
        f.write(findings)

    state["performance_findings"] = findings.split("\n")
    return state
