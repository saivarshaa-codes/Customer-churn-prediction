import pandas as pd 
from customer_cleaner import CustomerCleaner
def build_features(df):
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
    return df




