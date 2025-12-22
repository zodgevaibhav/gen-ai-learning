from state.codegen_state import CodegenState
from tools.shell import run_command
import os

def backend_compiler_node(state: CodegenState) -> CodegenState:
    if not os.path.exists("pom.xml"):
        state["backend_build_ok"] = False
        state["error"] = "pom.xml not found"
        return state

    success, output = run_command(["mvn", "clean", "install"])

    state["backend_build_ok"] = success

    if not success:
        state["error"] = f"Backend build failed:\n{output}"

    print("☕ Backend build:", "✅ SUCCESS" if success else "❌ FAILED")
    return state
