import pwd
from state.codegen_state import CodegenState
from tools.shell import run_command
import os

def backend_compiler_node(state: CodegenState) -> CodegenState:
    print("\n🛠️ Building Backend Project...")
    if not os.path.exists("backend/pom.xml"):
        state["backend_build_ok"] = False
        #state["error"] = "pom.xml not found"
        print("pom.xml not found in backend directory.")
        return {"backend_build_ok": False}

    success, output =  run_command(["mvn", "clean", "install"], cwd="backend")


    state["backend_build_ok"] = success
    if not success:
        print("Backend build failed with error:\n", output)
        #state["error"] = f"Backend build failed:\n{output}"

    print("Backend build:", "✅ SUCCESS" if success else "❌ FAILED")
    return {"backend_build_ok": True}
