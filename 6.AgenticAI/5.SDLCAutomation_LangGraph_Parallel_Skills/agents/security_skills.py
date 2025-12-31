from state.codegen_state import CodegenState
from tools.llm import call_llm
import os

SECURITY_PROMPT = """
You are a Security Architect (OWASP-focused).

TASK:
Review the requirements and architecture to identify:
- Authentication & Authorization gaps
- PII / sensitive data risks
- Input validation issues
- Logging & audit requirements
- Compliance considerations

RULES:
- Assume zero trust
- Output explicit security controls
- Do NOT generate code
"""

def security_skill_node(state: CodegenState) -> CodegenState:
    print("\n🔐 Running Security Analysis Skill...")

    findings = call_llm(
        SECURITY_PROMPT,
        state["architecture"]
    )

    os.makedirs("analysis", exist_ok=True)
    with open("analysis/security.md", "w") as f:
        f.write(findings)

    state["security_findings"] = findings.split("\n")
    return state
