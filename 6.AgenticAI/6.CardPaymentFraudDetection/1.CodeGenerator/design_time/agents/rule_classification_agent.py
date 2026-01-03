from state.State import FraudRuleState
from tools.filesystem import write_file
import json

def classify_rules(state: FraudRuleState) -> FraudRuleState:
    rule_engine = []
    ml_rules = []

    for rule in state["rule_book"]:
        primary = rule["primary_feature"]

        if any(k in primary for k in ["count", "velocity", "flag", "ratio", "threshold"]):
            rule_engine.append(rule)
        else:
            ml_rules.append(rule)
    write_file("rule_engine_rules.json",json.dumps(rule_engine, indent=2), state["run_dir"])
    write_file("ml_rules.json",json.dumps(ml_rules, indent=2), state["run_dir"])
    state["rule_engine_rules"] = rule_engine
    state["ml_rules"] = ml_rules
    return state
