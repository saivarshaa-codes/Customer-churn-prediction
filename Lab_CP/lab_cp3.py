import pandas as pd
from customer_cleaner import CustomerCleaner

df = pd.read_csv("WA_Fn-UseC_-Telco-Customer-Churn.csv")
customer_cleaner = CustomerCleaner(df)
customer_cleaner.clean()
df.to_csv("cleaned_customer_churn.csv",index=False)

churn_rate_contract = df.groupby('contract')['churn'].mean().sort_values(ascending=False) *100
print("Churn rate by contract ")
print(churn_rate_contract)
print(f"Highest Churn Rate Category : {churn_rate_contract.index[0]}")



churn_rate_internet_service = df.groupby('internet_service')['churn'].mean()*100
print("Churn rate by internet service")
print(churn_rate_internet_service)


churn_rate_payments = df.groupby('payment_method')['churn'].mean()*100
print("Churn rate by payment method")
print(churn_rate_payments)

df['tenure_bucket'] = pd.cut(df['tenure'],bins=[0, 12, 24, 48, 72],labels=["0-12", "13-24", "25-48", "49-72"],include_lowest=True)
churn_rate_buckets = df.groupby('tenure_bucket')['churn'].mean()*100
print(churn_rate_buckets)


avg_monthly_charges = df.groupby('churn')['monthly_charges'].mean().rename(index={0: 'Non-Churned', 1: 'Churned'})
print(avg_monthly_charges)

churn_rate = df.groupby(['contract','internet_service'])['churn'].mean().sort_values(ascending=False)
print(f"Combination having the highest churn rate: {churn_rate.index[0][0]} and {churn_rate.index[0][1]}")