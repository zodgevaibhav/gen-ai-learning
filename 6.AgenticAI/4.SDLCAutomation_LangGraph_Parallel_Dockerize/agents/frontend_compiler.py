import os
from state.codegen_state import CodegenState
from tools.shell import run_command

def frontend_compiler_node(state: CodegenState) -> CodegenState:
    print("\n🎨 Building Frontend Project (Docker)...")

    host_root = os.environ.get("HOST_PROJECT_ROOT")
    if not host_root:
        raise RuntimeError("HOST_PROJECT_ROOT not set")
    
    frontend_path  = os.path.join(
        host_root,
        "runs",
        "frontend"
    )

    if not os.path.exists("/app/runs/frontend"):
        print("⚠️ Frontend skipped (no frontend directory)")
        return {"frontend_build_ok": True}

    docker_cmd = [
        "docker", "run", "--rm",
        "-v", f"{frontend_path}:/workspace",
        "-w", "/workspace",
        "frontend-builder:latest",
        "sh", "-c",
        "npm install && npm run build"
    ]

    success, output = run_command(docker_cmd)

    state["frontend_build_ok"] = success

    if not success:
        print("❌ Frontend build failed:\n", output)
        return {"frontend_build_ok": False}

    print("✅ Frontend build SUCCESS")
    return {"frontend_build_ok": True}
