import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sqlalchemy import create_engine
from sklearn.metrics import classification_report,accuracy_score,precision_score,recall_score,f1_score,confusion_matrix
import matplotlib.pyplot as plt
import os
import joblib


# ============================================================
# ML1 — DEFINE THE ML PROBLEM
# ============================================================

# 237. Load customer_features.csv
df = pd.read_csv("customer_features.csv")

print("Dataset shape:", df.shape)
print("\nColumns:")
print(df.columns.tolist())


# 238. Identify the target column: churn
y = df["churn"]

print("\nTarget:")
print(y.head())


# 239. Identify the drop column: customer_id
# customer_id is an identifier, not a feature
# We simply don't include it in X.


# 240. List all numeric columns
numeric_cols = ["tenure","monthly_charges","total_charges","service_count","high_charge_flag","is_long_term_customer","auto_pay_flag","has_streaming_bundle"]


print("\nNumeric columns:")
print(numeric_cols)


# 241. List the remaining categorical columns
categorical_cols = ["contract","internet_service"]

print("\nCategorical columns:")
print(categorical_cols)


# 242. Apply one-hot encoding to contract and internet_service
X = df[numeric_cols + categorical_cols].copy()

X = pd.get_dummies(X,columns=categorical_cols,drop_first=False,dtype=int)


# 243. Print final feature set X and target y
print("\nFinal X columns:")
print(X.columns.tolist())

print("\nX:")
print(X.head())

print("\nX shape:", X.shape)
print("y shape:", y.shape)


# 244. Print class balance
print("\nClass balance:")
print(y.value_counts(normalize=True)) 




# ============================================================
# ML2 — BUILD AND COMPARE BASELINE MODELS
# ============================================================

# 246. Split X and y
X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.2,stratify=y,random_state=42)


# 247. Train Logistic Regression and Decision Tree
logistic_model = LogisticRegression(max_iter=1000)

tree_model = DecisionTreeClassifier(max_depth=5)

logistic_model.fit(X_train, y_train)
tree_model.fit(X_train, y_train)


# 248. Predict on the test set
y_pred_logistic = logistic_model.predict(X_test)
y_pred_tree = tree_model.predict(X_test)


# 249. Classification report for both models
print("\n" + "=" * 30)
print("LOGISTIC REGRESSION")
print("=" * 30)

print(classification_report(y_test,y_pred_logistic,target_names=["Active", "Churned"]))


print("\n" + "=" * 30)
print("DECISION TREE")
print("=" * 30)

print(classification_report(y_test,y_pred_tree,target_names=["Active", "Churned"]))


# 250. Confusion matrix for both models
print("\nLogistic Regression - Confusion Matrix:")
print(confusion_matrix(y_test, y_pred_logistic))

print("\nDecision Tree - Confusion Matrix:")
print(confusion_matrix(y_test, y_pred_tree))


# 251. 5-fold cross-validation F1
logistic_cv_f1 = cross_val_score(logistic_model,X,y,cv=5,scoring="f1")
tree_cv_f1 = cross_val_score(tree_model,X,y,cv=5,scoring="f1")
print("\nLogistic Regression CV F1:", logistic_cv_f1)
print("Logistic Regression Mean CV F1:", logistic_cv_f1.mean())
print("\nDecision Tree CV F1:", tree_cv_f1)
print("Decision Tree Mean CV F1:", tree_cv_f1.mean())


# 252. Create comparison table
comparison = pd.DataFrame([
    {
        "Model": "Logistic Regression",
        "Accuracy": accuracy_score(y_test, y_pred_logistic),
        "Precision (Churned)": precision_score(
            y_test,
            y_pred_logistic
        ),
        "Recall (Churned)": recall_score(
            y_test,
            y_pred_logistic
        ),
        "F1 (Churned)": f1_score(
            y_test,
            y_pred_logistic
        ),
        "CV F1": logistic_cv_f1.mean()
    },
    {
        "Model": "Decision Tree",
        "Accuracy": accuracy_score(y_test, y_pred_tree),
        "Precision (Churned)": precision_score(
            y_test,
            y_pred_tree
        ),
        "Recall (Churned)": recall_score(
            y_test,
            y_pred_tree
        ),
        "F1 (Churned)": f1_score(
            y_test,
            y_pred_tree
        ),
        "CV F1": tree_cv_f1.mean()
    }
])

print("\nComparison table:")
print(comparison)



# 254. Save both models and feature schema
os.makedirs("models", exist_ok=True)
joblib.dump(logistic_model, "models/logistic_churn.pkl")
joblib.dump(tree_model, "models/tree_churn.pkl")
print("\nBoth models saved successfully.")

import json
feature_metadata = {
    "feature_names": X.columns.tolist(),
    "numeric_cols": numeric_cols,
    "categorical_cols": categorical_cols,
    "median_monthly_charges": float(df["monthly_charges"].median()),
    "target": "churn"
}
with open("models/feature_columns.json", "w") as f:
    json.dump(feature_metadata, f, indent=2)
print("Saved feature metadata to models/feature_columns.json")


# ============================================================
# ML3 — INTERPRET MODEL BEHAVIOUR
# ============================================================

# 255. Load the best model from ML2

best_model = joblib.load("models/tree_churn.pkl")


importance = pd.Series(best_model.feature_importances_,index=X.columns).sort_values(ascending=False)

print("\nDecision Tree feature importances:")
print(importance)

top_10 = importance.head(10).sort_values()

plt.figure(figsize=(10, 6))
plt.barh(top_10.index,top_10.values)
plt.xlabel("Importance")
plt.ylabel("Feature")
plt.title("Decision Tree - Top 10 Feature Importances")
plt.savefig("models/feature_importance.png")
plt.close()


# 258. Identify top 3 features associated with churn

top_3_features = importance.head(3)

print("\nTop 3 features associated with churn:")
print(top_3_features)


# 259. Score all customers in the test set
churn_probabilities = best_model.predict_proba(X_test)[:, 1]

results = X_test.copy()

results["actual_churn"] = y_test
results["risk_score"] = churn_probabilities


# 260. Find top 20 highest-risk customers
results["customer_id"] = df.loc[X_test.index,"customer_id"].values
top_20_risky = results.sort_values("risk_score",ascending=False).head(20)
print("\nTop 20 highest-risk customers:")
print(top_20_risky[["customer_id", "risk_score"]])


# 261. Compare with SQL6 rule-based list


engine = create_engine("mysql+pymysql://root:root@localhost/telecom_db")

high_risk_sql = pd.read_sql("SELECT * FROM v_high_risk_customers",engine)

ml_top20_ids = set(top_20_risky["customer_id"])

sql_high_risk_ids = set(high_risk_sql["customer_id"])
overlap = ml_top20_ids & sql_high_risk_ids
print("\nML top 20 high-risk customers:", len(ml_top20_ids))
print("SQL rule-based high-risk customers:",len(sql_high_risk_ids))
print("Overlap:", len(overlap), "customers")
print("Overlap %:",len(overlap) / len(ml_top20_ids) * 100)
print("\nCustomer IDs in both lists:")
print(overlap)




# Load the same model used by ML4
model = joblib.load("models/tree_churn.pkl")

# Get the customer
test_customer = df[
    (df["tenure"] < 12) &
    (df["contract"] == "Month-to-month") &
    (df["monthly_charges"] > df["monthly_charges"].mean())
].iloc[0]

print(test_customer[
    [
        "customer_id",
        "tenure",
        "monthly_charges",
        "contract",
        "service_count",
        "total_charges",
        "high_charge_flag",
        "is_long_term_customer",
        "auto_pay_flag",
        "has_streaming_bundle",
        "internet_service"
    ]
])

# Build the EXACT feature row used during training
customer_X = df.loc[
    [test_customer.name],
    [
        "tenure",
        "monthly_charges",
        "total_charges",
        "service_count",
        "high_charge_flag",
        "is_long_term_customer",
        "auto_pay_flag",
        "has_streaming_bundle",
        "contract",
        "internet_service"
    ]
].copy()

# Encode categorical columns exactly like training
customer_X = pd.get_dummies(
    customer_X,
    columns=["contract", "internet_service"],
    drop_first=False,
    dtype=int
)

# Make column order identical to the trained model
customer_X = customer_X.reindex(
    columns=model.feature_names_in_,
    fill_value=0
)

print("\nModel input:")
print(customer_X)

print("\nPrediction:")
print(model.predict(customer_X))

print("\nProbability:")
print(model.predict_proba(customer_X))