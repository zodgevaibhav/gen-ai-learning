from rule_loader import RuleLoader
from rule_service import RuleService
from fraud_detection_service_using_ml import MLService
from fraud_decision_engine import FraudDecisionEngine

if __name__ == "__main__":
    # Load rules dynamically
    rules = RuleLoader.load_rules("rule_book.json")

    rule_service = RuleService(rules)
    ml_service = MLService("fraud_xgboost_model.joblib")

    engine = FraudDecisionEngine(rule_service, ml_service)

    transaction = {
        "txn_count_5m": 4,
        "same_amount_repeat": 1,
        "amount_spike_ratio": 1.2
    }

    result = engine.evaluate(transaction)
    print(result)
