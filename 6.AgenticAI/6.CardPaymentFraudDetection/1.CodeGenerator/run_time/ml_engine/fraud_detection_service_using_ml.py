from joblib import load
import pandas as pd

class MLService:
    def __init__(self, model_path, decline_threshold=0.85, step_up_threshold=0.65):
        self.model = load(model_path)
        self.features = self.model.get_booster().feature_names
        self.decline_threshold = decline_threshold
        self.step_up_threshold = step_up_threshold

    def score(self, transaction: dict):
        df = pd.DataFrame([transaction])

        # bool → int
        for col in df.select_dtypes(include=["bool"]).columns:
            df[col] = df[col].astype(int)

        df = df.reindex(columns=self.features, fill_value=0)

        score = float(self.model.predict_proba(df)[0][1])

        if score >= self.decline_threshold:
            decision = "DECLINE"
        elif score >= self.step_up_threshold:
            decision = "STEP_UP"
        else:
            decision = "APPROVE"

        return {
            "decision": decision,
            "score": round(score, 4),
            "source": "ML"
        }
