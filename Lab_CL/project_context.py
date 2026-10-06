"""
project_context.py — Durable Project Memory for Customer Retention System
Kept under 200 lines. Imported by every script that interfaces with Claude.
"""

PROJECT_NAME = "Customer Retention Intelligence System"

PROJECT_CONTEXT = """
# CUSTOMER RETENTION INTELLIGENCE SYSTEM — PROJECT MEMORY

## 1. Domain & Dataset Profile
- Business Context: Telecom retention intelligence system predicting customer churn.
- Dataset: IBM / Kaggle Telco Customer Churn dataset.
- Volume: Exactly 7,043 customers, 21 raw columns.
- Baseline Churn Rate: ~26.5% churned (1,869 customers), ~73.5% active (5,174 customers).
- Class Imbalance: Mild imbalance (~73% No / 27% Yes). Accuracy is misleading; primary ML metrics are F1-score and Recall on the Churned class.

## 2. Key Data Quirks & Handling Rules
- TotalCharges Blanks: Stored as string in raw source. Contains ~11 whitespace (" ") values for new customers with tenure=0.
  - Rule: Convert to NaN and fill with monthly_charges (since tenure=0 customers have only paid their first month).
- Identifier Leakage: customer_id is a unique alphanumeric string (e.g., '7590-VHVEG'). It carries no generalizable signal and MUST ALWAYS be excluded from ML feature matrices.
- Binary Columns: partner, dependents, phone_service, paperless_billing, and churn are encoded to 1 (Yes) and 0 (No).
- Tenure Bins: [0, 12, 24, 48, 72] labeled as '0-12', '13-24', '25-48', '49-72'.

## 3. Database Layer Architecture (MySQL/telecom_db)
- Staging Layer:
  - `stg_customer_raw`: Exact mirror of incoming CSV without transformation (TotalCharges as VARCHAR).
  - `ingestion_log`: Audit trail for loads (filename, status, row_count, reason, loaded_at).
- Curated Warehouse Layer:
  - `dim_contract`: Lookup table for contract types (Month-to-month, One year, Two year).
  - `dim_payment`: Lookup table for payment methods (Electronic check, Mailed check, Bank transfer, Credit card).
  - `customers`: Customer demographic identities with 0/1 encoded attributes.
  - `fact_customer_account`: Central account fact table (tenure, monthly_charges, total_charges, foreign keys to dims, churn).
- Serving & Analytical Views:
  - `customer_ml_features`: Materialized feature table with 6 derived flags + one-hot encodings.
  - `v_high_risk_customers`: Rule-based SQL view filtering customers with:
    `contract_type = 'Month-to-month' AND tenure < 12 AND monthly_charges > average`.

## 4. Machine Learning & Inference Standards
- Production Model: DecisionTreeClassifier (max_depth=5) saved in `models/tree_churn.pkl`.
- Feature Schema: Exact feature list and ordering persisted in `models/feature_columns.json`.
- Inference Rule: Prediction code must dynamically reindex input DataFrames to `models/feature_columns.json` to prevent feature mismatches or silent drift.
- Top Feature Churn Drivers:
  1. Month-to-month contracts (highest positive correlation with churn).
  2. Fiber optic internet service.
  3. Short tenure (especially tenure < 12 months).
  4. Electronic check payment method.
  Protective factors: Multi-year contracts, tenure >= 24 months, auto-pay, bundled services.

## 5. System Architecture & Assistant Boundaries
- Backend: FastAPI service (Lab_API) with endpoints:
  - `GET /customer/{customer_id}`: Customer profile lookup.
  - `GET /churn/summary`: High-level executive KPIs.
  - `GET /customers/high-risk`: Rule-based actionable retention list.
  - `GET /customer/{customer_id}/features`: ML feature vector.
  - `POST /predict-churn`: Live model scoring.
- Assistant Behavior:
  - NEVER invent or hallucinate customer IDs or risk metrics.
  - Every numerical metric reported to users MUST trace back to an authorized tool execution.
  - Explainability first: always link churn predictions back to concrete risk factors (e.g. month-to-month contract, lack of auto-pay).
"""

def get_system_context() -> str:
    """Returns the durable system context string to prepend to system prompts."""
    return PROJECT_CONTEXT.strip()

if __name__ == "__main__":
    lines = PROJECT_CONTEXT.strip().split("\n")
    print(f"Project context loaded successfully. Total lines: {len(lines)} (Limit: <200 lines)")
    assert len(lines) < 200, f"Context exceeds 200 lines limit! Found {len(lines)}"
