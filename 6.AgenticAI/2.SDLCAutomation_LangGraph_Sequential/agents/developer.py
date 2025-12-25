from state.codegen_state import CodegenState
from tools.llm import call_llm
from tools.filesystem import materialize_files

DEV_PROMPT = """
You are a Senior Full Stack Developer.

Generate a FULLY RUNNABLE project.

Backend:
- Inside backend folder
- Spring Boot
- Maven
- REST CRUD
- JPA + H2
- Add CORS configuration to allow requests from the React frontend 3000 port.
- Use spring boot parent project with latest stable version.

Frontend:
- inside frontend folder
- React
- npm

STRICT RULES:
1. Use ONLY the format below
2. Every file MUST start with ===FILE===
3. Use full relative file paths
4. No explanations, no markdown
5. Add CORS configuration to allow requests from the React frontend 3000 port.

FORMAT:
===FILE===
path/to/file
<file content>
"""

def developer_node(state: CodegenState) -> CodegenState:
    output = call_llm(DEV_PROMPT, state["architecture"])
    files = materialize_files(output)

    state["dev_output"] = output
    state["generated_files"] = files
    return state
