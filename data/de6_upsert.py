from connection import get_engine
from sqlalchemy import text
import pandas as pd

engine = get_engine()


def upsert_customer(filepath):
    df = pd.read_csv(filepath)

    rows_inserted = 0
    rows_updated = 0
    rows_unchanged = 0

    with engine.connect() as conn:

        for i, row in df.iterrows():

            partner = 1 if row.Partner == "Yes" else 0
            dependents = 1 if row.Dependents == "Yes" else 0

            existing = conn.execute(
                text("""
                    SELECT gender, senior_citizen, partner, dependents
                    FROM customers
                    WHERE customer_id = :customer_id
                """),
                {"customer_id": row.customerID}
            ).fetchone()

            if existing is None:
                rows_inserted += 1

            else:
                if (
                    existing.gender != row.gender
                    or existing.senior_citizen != row.SeniorCitizen
                    or existing.partner != partner
                    or existing.dependents != dependents
                ):
                    rows_updated += 1
                else:
                    rows_unchanged += 1

            conn.execute(
                text("""
                    INSERT INTO customers
                    (customer_id, gender, senior_citizen, partner, dependents)
                    VALUES
                    (:customer_id, :gender, :senior_citizen, :partner, :dependents)
                    ON DUPLICATE KEY UPDATE
                        gender = :gender,
                        senior_citizen = :senior_citizen,
                        partner = :partner,
                        dependents = :dependents
                """),
                {
                    "customer_id": row.customerID,
                    "gender": row.gender,
                    "senior_citizen": row.SeniorCitizen,
                    "partner": partner,
                    "dependents": dependents
                }
            )

        conn.execute(
            text("""
                INSERT INTO pipeline_run_log
                (file_name, rows_inserted, rows_updated, rows_unchanged)
                VALUES
                (:file_name, :rows_inserted, :rows_updated, :rows_unchanged)
            """),
            {
                "file_name": filepath,
                "rows_inserted": rows_inserted,
                "rows_updated": rows_updated,
                "rows_unchanged": rows_unchanged
            }
        )

        conn.commit()

        print("Inserted:", rows_inserted)
        print("Updated:", rows_updated)
        print("Unchanged:", rows_unchanged)


if __name__ == "__main__":
    upsert_customer(
        "data\\landing\\WA_Fn-UseC_-Telco-Customer-Churn.csv"
    )