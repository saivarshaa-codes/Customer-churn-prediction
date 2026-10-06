import os
import joblib
import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import (
    classification_report,
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
)

def train_models():
    # 1. Load data
    data_path = "customer_features.csv"
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Cannot find {data_path}")

    df = pd.read_csv(data_path)
    print(f"Loaded dataset: {df.shape[0]} rows, {df.shape[1]} columns")

    # 2. Target and Features
    y = df["churn"]
    numeric_cols = [
        "tenure",
        "monthly_charges",
        "total_charges",
        "service_count",
        "high_charge_flag",
        "is_long_term_customer",
        "auto_pay_flag",
        "has_streaming_bundle",
    ]
    categorical_cols = ["contract", "internet_service"]

    X = df[numeric_cols + categorical_cols].copy()
    X = pd.get_dummies(X, columns=categorical_cols, drop_first=False, dtype=int)

    print(f"Feature matrix X shape: {X.shape}, Target y shape: {y.shape}")
    print(f"Features: {X.columns.tolist()}")

    # 3. Train / Test Split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, stratify=y, random_state=42
    )

    # 4. Train Models
    logistic_model = LogisticRegression(max_iter=1000)
    tree_model = DecisionTreeClassifier(max_depth=5, random_state=42)

    logistic_model.fit(X_train, y_train)
    tree_model.fit(X_train, y_train)

    # 5. Evaluate
    y_pred_logistic = logistic_model.predict(X_test)
    y_pred_tree = tree_model.predict(X_test)

    print("\n" + "=" * 40)
    print("LOGISTIC REGRESSION CLASSIFICATION REPORT")
    print("=" * 40)
    print(classification_report(y_test, y_pred_logistic, target_names=["Active", "Churned"]))

    print("\n" + "=" * 40)
    print("DECISION TREE CLASSIFICATION REPORT")
    print("=" * 40)
    print(classification_report(y_test, y_pred_tree, target_names=["Active", "Churned"]))

    logistic_cv_f1 = cross_val_score(logistic_model, X, y, cv=5, scoring="f1")
    tree_cv_f1 = cross_val_score(tree_model, X, y, cv=5, scoring="f1")

    comparison = pd.DataFrame([
        {
            "Model": "Logistic Regression",
            "Accuracy": accuracy_score(y_test, y_pred_logistic),
            "Precision (Churned)": precision_score(y_test, y_pred_logistic),
            "Recall (Churned)": recall_score(y_test, y_pred_logistic),
            "F1 (Churned)": f1_score(y_test, y_pred_logistic),
            "CV F1": logistic_cv_f1.mean(),
        },
        {
            "Model": "Decision Tree",
            "Accuracy": accuracy_score(y_test, y_pred_tree),
            "Precision (Churned)": precision_score(y_test, y_pred_tree),
            "Recall (Churned)": recall_score(y_test, y_pred_tree),
            "F1 (Churned)": f1_score(y_test, y_pred_tree),
            "CV F1": tree_cv_f1.mean(),
        },
    ])

    print("\nComparison Table:")
    print(comparison.to_string(index=False))

    # 6. Save Models and Feature Schema
    import json
    os.makedirs("models", exist_ok=True)
    joblib.dump(logistic_model, "models/logistic_churn.pkl")
    joblib.dump(tree_model, "models/tree_churn.pkl")
    print("\nSaved models to models/logistic_churn.pkl and models/tree_churn.pkl")

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

    return comparison, X.columns.tolist()

if __name__ == "__main__":
    train_models()
