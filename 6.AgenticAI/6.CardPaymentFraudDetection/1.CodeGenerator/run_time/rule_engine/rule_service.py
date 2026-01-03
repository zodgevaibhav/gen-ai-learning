class RuleService:
    def __init__(self, rules):
        self.rules = rules

    def evaluate(self, transaction):
        matched_rules = []
        decision = "APPROVE"

        for rule in self.rules:
            if self._evaluate_rule(rule, transaction):
                matched_rules.append(rule)

                if rule["action"] == "DECLINE":
                    return {
                        "decision": "DECLINE",
                        "matched_rules": matched_rules,
                        "source": "RULE_ENGINE"
                    }

                if rule["action"] == "STEP_UP":
                    decision = "STEP_UP"

        return {
            "decision": decision,
            "matched_rules": matched_rules,
            "source": "RULE_ENGINE"
        }

    def _evaluate_rule(self, rule, transaction):
        try:
            return eval(rule["condition"], {}, transaction)
        except Exception:
            return False
