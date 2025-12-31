from state.codegen_state import CodegenState
from tools.shell import run_command
import os

def frontend_compiler_node(state: CodegenState) -> CodegenState:
    print("\n🛠️ Building Frontend Project...")
    if not os.path.exists("frontend"):
        # frontend optional → don’t fail whole pipeline
        state["frontend_build_ok"] = True
        print("Frontend skipped (no frontend directory)")
        return {"frontend_build_ok": False}


    success, output = run_command(
        ["npm", "install"],
        cwd="frontend"
    )

    if success:
        success, output = run_command(
            ["npm", "run", "build"],
            cwd="frontend"
        )

    state["frontend_build_ok"] = success

    if not success:
        #state["error"] = f"Frontend build failed:\n{output}"
        print("Frontend build failed with error:\n", output)

    print("Frontend build:", "✅ SUCCESS" if success else "❌ FAILED")
    return {"frontend_build_ok": success}
