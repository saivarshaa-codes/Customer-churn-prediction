import pandas as pd
from connection import get_engine
import json

engine = get_engine()


def check_null_rate(df, col, threshold):
    null_rate = float(df[col].isnull().mean() * 100)

    return {
        "check_name": f"{col}_null_rate",
        "status": "PASS" if null_rate <= threshold else "FAIL",
        "value_found": null_rate,
        "threshold": threshold
    }


def check_value_range(df, col, min, max=None):
    if max is None:
        passed = bool((df[col] > min).all())
        value_found = float(df[col].min())
        threshold = f"> {min}"
    else:
        passed = bool(df[col].between(min, max).all())
        value_found = {
            "min_found": float(df[col].min()),
            "max_found": float(df[col].max())
        }
        threshold = f"{min}-{max}"

    return {
        "check_name": f"{col}_value_range",
        "status": "PASS" if passed else "FAIL",
        "value_found": value_found,
        "threshold": threshold
    }


def check_allowed_values(df, col, allowed_set):
    unexpected = set(df[col].dropna().unique()) - allowed_set

    return {
        "check_name": f"{col}_allowed_values",
        "status": "PASS" if len(unexpected) == 0 else "FAIL",
        "value_found": list(unexpected),
        "threshold": list(allowed_set)
    }


def check_row_count(df, expected_min):
    row_count = int(len(df))

    return {
        "check_name": "row_count",
        "status": "PASS" if row_count >= expected_min else "FAIL",
        "value_found": row_count,
        "threshold": expected_min
    }


def check_no_duplicates(df, key_col):
    duplicate_count = int(df[key_col].duplicated().sum())

    return {
        "check_name": f"{key_col}_duplicates",
        "status": "PASS" if duplicate_count == 0 else "FAIL",
        "value_found": duplicate_count,
        "threshold": 0
    }


def check_churn_distribution(df):
    invalid_values = set(df["churn"].dropna().unique()) - {0, 1}

    return {
        "check_name": "churn_distribution",
        "status": "PASS" if len(invalid_values) == 0 else "FAIL",
        "value_found": list(invalid_values),
        "threshold": [0, 1]
    }


if __name__ == "__main__":

    df = pd.read_sql(
        "SELECT * FROM cleaned_customers",
        engine
    )

    results = [
    {**check_null_rate(df, "monthly_charges", 0), "severity": "CRITICAL"},
    {**check_null_rate(df, "tenure", 0), "severity": "CRITICAL"},
    {**check_value_range(df, "tenure", 0, 100), "severity": "CRITICAL"},
    {**check_value_range(df, "monthly_charges", 0), "severity": "CRITICAL"},
    {**check_allowed_values(df, "contract",{"Month-to-month", "One year", "Two year"}), "severity": "CRITICAL"},
    {**check_row_count(df, 7000), "severity": "CRITICAL"},
    {**check_no_duplicates(df, "customer_id"), "severity": "CRITICAL"},
    {**check_churn_distribution(df), "severity": "WARNING"}
]

    
    with open("quality_report.json", "w") as f:
        json.dump(results, f, indent=4)

    for result in results:
        if result["status"] == "FAIL":
            if result["severity"] == "CRITICAL":
                raise Exception(
                    f"CRITICAL quality check failed: {result['check_name']}"
                )
            elif result["severity"] == "WARNING":
                print(
                    f"WARNING: quality check failed: {result['check_name']}"
                )

    print("Quality report generated successfully.")

    



