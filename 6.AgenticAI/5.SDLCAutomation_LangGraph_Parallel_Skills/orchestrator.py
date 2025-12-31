import os
from datetime import datetime
from tools.workspace import clean_workspace
from graph.codegen_graph import build_codegen_graph
from state.codegen_state import CodegenState

FEATURES = """Feature: Patient Management API
Scenario: CRUD operations
"""

def orchestrate():
    clean_workspace()

    run_dir = os.path.join(
        "runs",
        f"run_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    )
    os.makedirs(run_dir)
    os.chdir(run_dir)

    os.makedirs("requirements", exist_ok=True)
    with open("requirements/requirement.feature", "w") as f:
        f.write(FEATURES)

    graph = build_codegen_graph()

    # Initial state meaning all fields set to None or empty values
    # Setting None of empty makes the agents understand that they need to generate/fill these fields
    initial_state: CodegenState = {
    "raw_requirement": FEATURES,
    "refined_requirement": None,
    "architecture": None,
    "dev_output": None,
    "generated_files": [],
    "backend_build_ok": None,
    "frontend_build_ok": None,
    "error": None,
    }

    graph.invoke(initial_state)

    print("\n FULL PROJECT GENERATED")
