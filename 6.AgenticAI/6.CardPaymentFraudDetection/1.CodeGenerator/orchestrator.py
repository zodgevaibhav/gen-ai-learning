import os
from datetime import datetime
from tools.workspace import clean_workspace
from state.State import FraudRuleState
from graph import build_fraud_rule_graph

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

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

    use_cases_path = os.path.join(SCRIPT_DIR, "UseCases.md")
    with open(use_cases_path, "r") as f:
        useCaseMarkup = f.read()

    use_cases_path = os.path.join(SCRIPT_DIR, "UseCaseFeatureMap.md")
    with open(use_cases_path, "r") as f:
        feature_map = f.read()


    graph = build_fraud_rule_graph()

    # Initial state meaning all fields set to None or empty values
    # Setting None of empty makes the agents understand that they need to generate/fill these fields

    initial_state: FraudRuleState = {
        "raw_table": useCaseMarkup,
        "json_output": [],
        "use_cases": [],
        "feature_map": feature_map,
        "rule_book": [],
        "rule_engine_rules": [],
        "ml_rules": [],
        "rule_service_code": "",
        "run_dir":run_dir
    }

    graph.invoke(initial_state)

    print("\n FULL PROJECT GENERATED")
