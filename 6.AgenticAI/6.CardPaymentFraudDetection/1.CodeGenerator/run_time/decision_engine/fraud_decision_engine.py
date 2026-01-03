class FraudDecisionEngine:
    def __init__(self, rule_service, ml_service):
        self.rule_service = rule_service
        self.ml_service = ml_service

    def evaluate(self, transaction):
        # 1️⃣ Rules first
        rule_result = self.rule_service.evaluate(transaction)

        if rule_result["decision"] == "DECLINE":
            return {
                "decision": "DECLINE",
                "reasons": self._rule_reasons(rule_result),
                "source": "RULE_ENGINE"
            }

        # 2️⃣ ML next
        ml_result = self.ml_service.score(transaction)

        final_decision = self._combine(rule_result, ml_result)

        return {
            "decision": final_decision,
            "fraud_score": ml_result["score"],
            "reasons": self._rule_reasons(rule_result),
            "source": "RULE_ENGINE + ML"
        }

    def _combine(self, rule_result, ml_result):
        if ml_result["decision"] == "DECLINE":
            return "DECLINE"

        if rule_result["decision"] == "STEP_UP" or ml_result["decision"] == "STEP_UP":
            return "STEP_UP"

        return "APPROVE"

    def _rule_reasons(self, rule_result):
        return [r["use_case"] for r in rule_result.get("matched_rules", [])]
