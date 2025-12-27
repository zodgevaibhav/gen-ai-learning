import os
from state.codegen_state import CodegenState
from tools.shell import run_command

def backend_compiler_node(state: CodegenState) -> CodegenState:
    print("\n🏗️ Building Backend Project (Docker)...")

    host_root = os.environ.get("HOST_PROJECT_ROOT")
    if not host_root:
        raise RuntimeError("HOST_PROJECT_ROOT not set")

    backend_path = os.path.join(
        host_root,
        "runs",
        "backend"
    )

    print(f"📁 Backend host path: {backend_path}")

    pom_path = os.path.join("/app/runs/backend", "pom.xml")
    if not os.path.exists(pom_path):
        print(f"❌ pom.xml not found at {pom_path}")
        return {"backend_build_ok": False}

    docker_cmd = [
        "docker", "run", "--rm",
        "-v", f"{backend_path}:/workspace",
        "-w", "/workspace",
        "backend-builder:latest",
        "mvn", "clean", "package"
    ]

    success, output = run_command(docker_cmd)

    if not success:
        print("❌ Backend build failed:\n", output)
        return {"backend_build_ok": False}

    print("✅ Backend build SUCCESS")
    return {"backend_build_ok": True}
