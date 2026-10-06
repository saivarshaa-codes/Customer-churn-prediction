import os
import json
import joblib
import pandas as pd

# Load model and feature metadata at module level
MODEL_PATH = os.path.join("models", "tree_churn.pkl")
METADATA_PATH = os.path.join("models", "feature_columns.json")

model = joblib.load(MODEL_PATH)

if os.path.exists(METADATA_PATH):
    with open(METADATA_PATH, "r") as f:
        feature_metadata = json.load(f)
    FEATURE_NAMES = feature_metadata.get("feature_names", list(model.feature_names_in_))
    MEDIAN_MONTHLY_CHARGES = feature_metadata.get("median_monthly_charges", 70.35)
else:
    FEATURE_NAMES = list(model.feature_names_in_)
    MEDIAN_MONTHLY_CHARGES = 70.35

def preprocess_input(
    tenure: int,
    monthly_charges: float,
    contract_type: str,
    service_count: int,
    internet_service: str = "DSL",
    auto_pay_flag: int = 0,
    has_streaming_bundle: int = 0,
    total_charges: float | None = None
) -> pd.DataFrame:
    # Handle total_charges realistically: if tenure == 0, charges equal monthly_charges
    if total_charges is None:
        total_charges = monthly_charges * tenure if tenure > 0 else monthly_charges

    high_charge = int(monthly_charges > MEDIAN_MONTHLY_CHARGES)
    is_long_term = int(tenure >= 24)

    data = {
        "tenure": tenure,
        "monthly_charges": monthly_charges,
        "total_charges": total_charges,
        "service_count": service_count,
        "high_charge_flag": high_charge,
        "is_long_term_customer": is_long_term,
        "auto_pay_flag": int(auto_pay_flag),
        "has_streaming_bundle": int(has_streaming_bundle),
        "contract": contract_type,
        "internet_service": internet_service
    }

    df_input = pd.DataFrame([data])
    df_input = pd.get_dummies(df_input, columns=["contract", "internet_service"], drop_first=False, dtype=int)
    # Dynamically align to feature columns specified in models/feature_columns.json
    df_aligned = df_input.reindex(columns=FEATURE_NAMES, fill_value=0)
    return df_aligned

def predict_churn(
    tenure: int,
    monthly_charges: float,
    contract_type: str,
    service_count: int,
    internet_service: str = "DSL",
    auto_pay_flag: int = 0,
    has_streaming_bundle: int = 0,
    total_charges: float | None = None
) -> dict:
    X_input = preprocess_input(
        tenure=tenure,
        monthly_charges=monthly_charges,
        contract_type=contract_type,
        service_count=service_count,
        internet_service=internet_service,
        auto_pay_flag=auto_pay_flag,
        has_streaming_bundle=has_streaming_bundle,
        total_charges=total_charges
    )

    pred = int(model.predict(X_input)[0])
    prob = float(model.predict_proba(X_input)[0, 1])

    return {
        "risk_score": prob,
        "prediction": "Likely to churn" if pred == 1 else "Unlikely to churn",
        "confidence": float(max(prob, 1.0 - prob))
    }
