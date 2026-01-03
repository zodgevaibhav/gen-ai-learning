import json

class RuleLoader:
    @staticmethod
    def load_rules(path: str):
        with open(path, "r") as f:
            rules = json.load(f)

        # Basic validation
        required_fields = {"rule_id", "condition", "action", "use_case"}

        for r in rules:
            missing = required_fields - r.keys()
            if missing:
                raise ValueError(f"Rule {r.get('rule_id')} missing fields: {missing}")

        return rules
