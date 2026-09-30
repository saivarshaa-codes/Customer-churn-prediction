import pandas as pd
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Lab_CP import customer_cleaner
from connection import get_engine
from sqlalchemy import text

engine = get_engine()

def clean_staging(engine):
    with engine.connect() as conn:
        df = pd.read_sql("stg_customer_raw",engine)
        cleaner = customer_cleaner.CustomerCleaner(df)
        df = cleaner.clean()
        df.to_sql("cleaned_customers",engine,index=False,if_exists="replace")
        staging_count = conn.execute(text("select count(*) from stg_customer_raw")).scalar()
        cleaned_count = conn.execute(text("select count(*) from cleaned_customers")).scalar()
        cust_null_count=conn.execute(text("select count(*) from cleaned_customers where customer_id is null")).scalar()
        monthly_charges_null_count = conn.execute(text("select count(*) from cleaned_customers where monthly_charges is null")).scalar()
        invalid_churn = conn.execute(text("select count(*) from cleaned_customers where churn not in (0,1)")).scalar()
        print("row count check:","PASS" if staging_count == cleaned_count else "FAIL","- staging_count:",staging_count,"cleaned_count:",cleaned_count )
        assert staging_count == cleaned_count
        print("customer_id NULL check:","PASS" if cust_null_count==0 else "FAIL","-",cust_null_count)
        assert cust_null_count==0
        print("monthly_charges NULL check:","PASS" if monthly_charges_null_count ==0 else "FAIL","-",monthly_charges_null_count)
        assert monthly_charges_null_count ==0
        print("Invalid churn values:","PASS" if invalid_churn==0 else "FAIL","-",invalid_churn)
        assert invalid_churn ==0


def build_curated_tables(engine):
    with engine.connect() as conn:
        #dim_contract
        contract_types = conn.execute(text("select distinct contract from cleaned_customers"))
        for row in contract_types:
            conn.execute(text("insert into dim_contract (contract_type) values (:contract)"),{
                "contract":row.contract
            })
        conn.commit()
        #dim_payment
        payment_types = conn.execute(text("select distinct payment_method from cleaned_customers"))
        for row in payment_types:
            conn.execute(text("insert into dim_payment(payment_method) values(:payment_method)"),{
                "payment_method":row.payment_method
            })
        conn.commit()
        #customers
        customer_data = conn.execute(text("select customer_id,gender,senior_citizen,partner,dependents from cleaned_customers"))
        for row in customer_data:
            conn.execute(text("insert into customers(customer_id,gender,senior_citizen,partner,dependents) values(:customer_id,:gender,:senior_citizen,:partner,:dependents)"),{
                "customer_id":row.customer_id,
                "gender":row.gender,
                "senior_citizen":row.senior_citizen,
                "partner":row.partner,
                "dependents":row.dependents
            })
        conn.commit()
        #fact_customer_account
        customer_account_data = conn.execute(text("select customer_id,contract_id,payment_id,tenure,monthly_charges,total_charges,churn from cleaned_customers cc join dim_contract c on cc.contract = c.contract_type join dim_payment p on cc.payment_method = p.payment_method"))
        for row in customer_account_data:
            conn.execute(text("insert into fact_customer_account(customer_id,contract_id,payment_id,tenure,monthly_charges,total_charges,churn) values (:customer_id,:contract_id,:payment_id,:tenure,:monthly_charges,:total_charges,:churn)"),{
                "customer_id":row.customer_id,
                "contract_id":row.contract_id,
                "payment_id":row.payment_id,
                "tenure":row.tenure,
                "monthly_charges":row.monthly_charges,
                "total_charges":row.total_charges,
                "churn":row.churn
            })
        conn.commit()


if __name__ == "__main__":
    clean_staging(engine)
    build_curated_tables(engine)
    






