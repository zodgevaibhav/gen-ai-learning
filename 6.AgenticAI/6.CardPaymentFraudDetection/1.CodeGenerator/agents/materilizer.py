import json
import os
from state.State import FraudRuleState

ARTIFACT_DIR = "artifacts"

def materialize_files(state: FraudRuleState) -> FraudRuleState:
    os.makedirs(ARTIFACT_DIR, exist_ok=True)

    with open(f"{ARTIFACT_DIR}/rule_book.json", "w") as f:
        json.dump(state["rule_book"], f, indent=2)

    with open(f"{ARTIFACT_DIR}/rule_engine_rules.json", "w") as f:
        json.dump(state["rule_engine_rules"], f, indent=2)

    with open(f"{ARTIFACT_DIR}/ml_rules.json", "w") as f:
        json.dump(state["ml_rules"], f, indent=2)

    with open(f"{ARTIFACT_DIR}/rule_service.py", "w") as f:
        f.write(state["rule_service_code"])

    print("✅ Artifacts written to disk")

    return state
