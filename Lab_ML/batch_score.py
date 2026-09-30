import pandas as pd
from predict import predict_churn
from datetime import datetime
from sqlalchemy import create_engine

engine = create_engine("mysql+pymysql://root:root@localhost/telecom_db")

df = pd.read_csv("customer_features.csv")

predictions = df.apply(
    lambda row: predict_churn(
        tenure=row["tenure"],
        monthly_charges=row["monthly_charges"],
        contract_type=row["contract"],
        service_count=row["service_count"]
    ),
    axis=1
)

df["risk_score"] = predictions.apply(lambda x: x["risk_score"])
df["prediction"] = predictions.apply(lambda x: x["prediction"])
df["confidence"] = predictions.apply(lambda x: x["confidence"])



df["scoring_date"] = datetime.today().strftime("%Y-%m-%d")

risk_table = df[
    [
        "customer_id",
        "risk_score",
        "prediction",
        "confidence",
        "scoring_date"
    ]
]

risk_table.to_csv("customer_risk_table.csv",index=False)

print("customer_risk_table.csv saved successfully.")


prediction_counts = df["prediction"].value_counts()

print("Prediction summary:")
print(prediction_counts)

likely_to_churn = prediction_counts.get("Likely to churn", 0)
unlikely_to_churn = prediction_counts.get("Unlikely to churn", 0)

total_customers = len(df)

predicted_churn_rate = (
    likely_to_churn / total_customers
) * 100

print("\nLikely to churn:", likely_to_churn)
print("Unlikely to churn:", unlikely_to_churn)
print(f"Predicted churn rate: {predicted_churn_rate:.2f}%")

print("Actual training churn rate:")
print(f"{df['churn'].mean() * 100:.2f}%")


# 278. Print top 10 highest-risk customers

top_10_risky = df.sort_values(
    "risk_score",
    ascending=False
).head(10)

print("\nTop 10 highest-risk customers:")
print(
    top_10_risky[
        ["customer_id", "risk_score"]
    ]
)