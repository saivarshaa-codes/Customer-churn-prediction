import pandas as pd
from customer_cleaner import CustomerCleaner

df = pd.read_csv("WA_Fn-UseC_-Telco-Customer-Churn.csv")
print("="*40)
print("Before Cleaning")
print("="*40)
print(f"Shape:{df.shape}")
print(f"Datatypes:{df.dtypes}")

customer_cleaner = CustomerCleaner(df)
customer_cleaner.clean()

print("="*40)
print("After Cleaning")
print("="*40)
print(f"Shape:{df.shape}")
print(f"Datatypes:{df.dtypes}")
    