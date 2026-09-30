import joblib
import pandas as pd

# 263. Load the best model from models/ at module level
model = joblib.load("models/tree_churn.pkl")


# 264. Create a properly encoded single-row DataFrame
# matching the training feature columns
def preprocess_input(tenure,monthly_charges,contract_type,service_count):
    data = {
        "tenure": tenure,
        "monthly_charges": monthly_charges,
        "total_charges": monthly_charges * tenure,
        "service_count": service_count,
        "high_charge_flag": int(monthly_charges > 70.35),
        "is_long_term_customer": int(tenure >= 24),
        "auto_pay_flag": 0,
        "has_streaming_bundle": 0,
        "contract": contract_type,
        "internet_service": "Fiber optic"
    }
    X_input = pd.DataFrame([data])
    X_input = pd.get_dummies(X_input,columns=["contract", "internet_service"],drop_first=False,dtype=int)
    X_input = X_input.reindex(columns=model.feature_names_in_,fill_value=0)
    return X_input


# 265. Call preprocess_input, predict() and predict_proba()
def predict_churn(tenure,monthly_charges,contract_type,service_count):
    X_input = preprocess_input(tenure,monthly_charges,contract_type,service_count)
    prediction = model.predict(X_input)[0]
    probability = model.predict_proba(X_input)[0, 1]

    return {
        "risk_score": float(probability),
        "prediction": (
            "Likely to churn"
            if prediction == 1
            else "Unlikely to churn"
        ),
        "confidence": float(
            max(probability, 1 - probability)
        )
    }