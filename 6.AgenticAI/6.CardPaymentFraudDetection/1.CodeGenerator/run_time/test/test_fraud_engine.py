from run_time.rule_engine.rule_loader import RuleLoader
from run_time.rule_engine.rule_service import RuleService
from run_time.ml_engine.fraud_detection_service_using_ml import MLService
from run_time.decision_engine.fraud_decision_engine import FraudDecisionEngine


# --------------------------------------------------
# BOOTSTRAP REAL ENGINE
# --------------------------------------------------

RULE_BOOK_PATH = "/Users/vzodge/Documents/ALL_GITHUB_REPO/gen-ai-learning/6.AgenticAI/6.CardPaymentFraudDetection/1.CodeGenerator/artifacts/rule_book.json"
MODEL_PATH = "/Users/vzodge/Documents/ALL_GITHUB_REPO/gen-ai-learning/6.AgenticAI/6.CardPaymentFraudDetection/1.CodeGenerator/artifacts/model/fraud_xgboost_model.joblib"

rules = RuleLoader.load_rules(RULE_BOOK_PATH)
rule_service = RuleService(rules)

ml_service = MLService(MODEL_PATH)

engine = FraudDecisionEngine(rule_service, ml_service)

print("\n✅ FraudDecisionEngine initialized\n")


# --------------------------------------------------
# TEST TRANSACTIONS (REAL SCENARIOS)
# --------------------------------------------------

TEST_TRANSACTIONS = [
    {
        "name": "🔴 Rule-based DECLINE (Velocity)",
        "txn": {
            "txn_count_5m": 6,
            "amount_spike_ratio": 1.2
        }
    },
    {
        "name": "🔴 Rule-based DECLINE (Offline transaction)",
        "txn": {
            "offline_txn_flag": True,
            "entry_mode": "card"
        }
    },
    {
        "name": "🟡 Rule STEP_UP + ML APPROVE",
        "txn": {
            "new_merchant_flag": True,
            "merchant_risk_score": "medium",
            "txn_velocity_5m": 1
        }
    },
    {
        "name": "🟡 ML STEP_UP (behavioral anomaly)",
        "txn": {
            "txn_density": 2.1,
            "peer_spend_zscore": 2.3,
            "amount_spike_ratio": 1.7
        }
    },
    {
        "name": "🔴 ML DECLINE (high risk pattern)",
        "txn": {
            "geo_distance_km": 2500,
            "txn_density": 3.2,
            "amount_spike_ratio": 3.5,
            "card_age_days": 5
        }
    },
    {
        "name": "🟢 Clean APPROVE",
        "txn": {
            "txn_count_5m": 1,
            "amount_spike_ratio": 1.0,
            "geo_distance_km": 3,
            "card_age_days": 1200
        }
    }
]

# --------------------------------------------------
# EXECUTE TESTS
# --------------------------------------------------

for i, test in enumerate(TEST_TRANSACTIONS, start=1):
    print(f"\n==============================")
    print(f"TEST {i}: {test['name']}")
    print(f"Transaction: {test['txn']}")

    result = engine.evaluate(test["txn"])

    print("Result:")
    print(result)
