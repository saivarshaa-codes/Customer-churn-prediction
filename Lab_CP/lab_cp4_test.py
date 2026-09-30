from lab_cp4 import build_features
import pandas as pd


df = pd.read_csv("C:\\Users\\saivarshaa.sujee\\Prodapt_Labs\\cleaned_customer_churn.csv")
df = build_features(df)
tenure_churn = df.groupby('tenure_bucket')['churn'].mean()
new_features = ['high_charge_flag','service_count','is_long_term_customer','has_streaming_bundle','auto_pay_flag']
churn_corr = df[new_features].corrwith(df['churn'])
print(tenure_churn)
print(churn_corr)

df.to_csv('customer_features.csv',index=False)
print("Cleaned csv file created successfully!")