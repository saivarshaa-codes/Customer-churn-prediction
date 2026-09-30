from connection import get_engine
import pandas as pd
from sqlalchemy import text
engine = get_engine()

def build_features(engine):
    df = pd.read_sql("cleaned_customers",engine)
    #Feature 1
    df['tenure_bucket']=pd.cut(df["tenure"],bins=[0,12,24,48,72],labels=["0-12", "13-24", "25-48", "49-72"],include_lowest=True)
    
    #Feature 2
    median_charge = df['monthly_charges'].median()
    df["high_charge_flag"]=(df['monthly_charges']>median_charge).astype(int)
    
    #feature 3
    services = ['online_security', 'online_backup','device_protection','tech_support','streaming_tv','streaming_movies']
    for service in services:
        df[service] = df[service].map({"Yes":1,"No":0}).fillna(0).astype(int)
    df['service_count']=df[services].sum(axis=1)

    #feature 4
    df['is_long_term_customer']=(df["tenure"]>=24).astype(int)
    
    #feature 5
    df['has_streaming_bundle']=((df['streaming_tv'] == 1) & (df['streaming_movies'] == 1)).astype(int)
    
    #Feature 6
    df['auto_pay_flag']=(df['payment_method'].str.contains("automatic",case=False)).astype(int)

    df.to_sql("customer_ml_features",engine,if_exists="replace",index=False)

from connection import get_engine
import pandas as pd
from sqlalchemy import text
engine = get_engine()

def build_features(engine):
    df = pd.read_sql("cleaned_customers",engine)
    #Feature 1
    df['tenure_bucket']=pd.cut(df["tenure"],bins=[0,12,24,48,72],labels=["0-12", "13-24", "25-48", "49-72"],include_lowest=True)
    
    #Feature 2
    median_charge = df['monthly_charges'].median()
    df["high_charge_flag"]=(df['monthly_charges']>median_charge).astype(int)
    
    #feature 3
    services = ['online_security', 'online_backup','device_protection','tech_support','streaming_tv','streaming_movies']
    for service in services:
        df[service] = df[service].map({"Yes":1,"No":0}).fillna(0).astype(int)
    df['service_count']=df[services].sum(axis=1)

    #feature 4
    df['is_long_term_customer']=(df["tenure"]>=24).astype(int)
    
    #feature 5
    df['has_streaming_bundle']=((df['streaming_tv'] == 1) & (df['streaming_movies'] == 1)).astype(int)
    
    #Feature 6
    df['auto_pay_flag']=(df['payment_method'].str.contains("automatic",case=False)).astype(int)

    df.to_sql("customer_ml_features",engine,if_exists="replace",index=False)

    feature_columns = ["tenure_bucket","high_charge_flag","service_count","is_long_term_customer","has_streaming_bundle","auto_pay_flag"]

    with engine.connect() as conn:
        cleaned_count = conn.execute(text("select count(*) from cleaned_customers")).scalar()
        feature_count = conn.execute(text("select count(*) from customer_ml_features")).scalar()
        for col in feature_columns:
            null_count = conn.execute(text(f"select count(*) from customer_ml_features where {col} is null")).scalar()
            assert null_count == 0
        assert cleaned_count==feature_count


if __name__ == "__main__":
    build_features(engine)