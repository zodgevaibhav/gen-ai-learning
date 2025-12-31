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
- Create response dto/pojo classes. Always return ResponseEntity<T> from controller methods.

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
6. Performance findings MUST be implemented
7. Security findings MUST be implemented

FORMAT:
===FILE===
path/to/file
<file content>
"""

def developer_node(state: CodegenState) -> CodegenState:
    dev_input = f"""
    ARCHITECTURE:
    {state['architecture']}

    PERFORMANCE FINDINGS:
    {chr(10).join(state.get('performance_findings', []))}

    SECURITY FINDINGS:
    {chr(10).join(state.get('security_findings', []))}
    """
    
    output = call_llm(DEV_PROMPT, dev_input)
    files = materialize_files(output)

    state["dev_output"] = output
    state["generated_files"] = files
    return state
