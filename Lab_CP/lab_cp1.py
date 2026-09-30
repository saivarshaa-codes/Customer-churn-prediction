import pandas as pd
import numpy as np
df = pd.read_csv("C:\\Users\\saivarshaa.sujee\\Prodapt_Labs\\Lab_SQL1\\WA_Fn-UseC_-Telco-Customer-Churn.csv") 
# print(df.shape)

# print(df.dtypes)


# null_counts = df.isnull().sum()
# null_percentages = (null_counts / len(df)) * 100
# # print("Null value counts:\n", null_counts)
# print("Null value percentages:\n", null_percentages)



# For each key categorical column (gender, Partner, Dependents, PhoneService, InternetService, Contract, PaymentMethod, Churn) print unique values and value counts 
# categorical_columns = ['gender', 'Partner', 'Dependents', 'PhoneService', 'InternetService', 'Contract', 'PaymentMethod', 'Churn']
# for col in categorical_columns:
#     print(f"Unique values in {col}: {df[col].unique()}")
#     print(f"Value counts in {col}:\n{df[col].value_counts()}\n")   

# Count churned vs non-churned customers — calculate the churn rate as a percentage 
# churn_counts = df['Churn'].value_counts()
# churn_rate = (churn_counts['Yes'] / len(df)) * 100
# print(f"Churn rate: {churn_rate:.2f}%")
# non_churn_rate = (churn_counts['No'] / len(df)) * 100
# print(f"Non-churn rate: {non_churn_rate:.2f}%")

#Inspect the TotalCharges column specifically: print its dtype, then try pd.to_numeric() with errors="coerce" and count how many NaN values appear 
print(f"TotalCharges dtype: {df['TotalCharges'].dtype}")
df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
print(f"Number of NaN values in TotalCharges: {df['TotalCharges'].isnull().sum()}")


#Print min/max/mean for tenure, MonthlyCharges, TotalCharges 
print(f"Min tenure:{df['tenure'].min()}")  
print(f"Max tenure:{df['tenure'].max()}")
print(f"Mean tenure:{df['tenure'].mean()}")
print(f"Min MonthlyCharges:{df['MonthlyCharges'].min()}")
print(f"Max MonthlyCharges:{df['MonthlyCharges'].max()}")
print(f"Mean MonthlyCharges:{df['MonthlyCharges'].mean()}")
print(f"Min TotalCharges:{df['TotalCharges'].min()}")
print(f"Max TotalCharges:{df['TotalCharges'].max()}")
df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
mean = df['TotalCharges'].mean()


# Write a short profiling summary: 5 bullet points of things the data team needs to know before using this data 
print("Profiling Summary:")
print("• The dataset contains information about telecom customers and their churn behavior.")
print("• Key variables include tenure, MonthlyCharges, and TotalCharges.")
print("• The 'TotalCharges' column has some missing values that need to be handled.")
print("• The 'Churn' column indicates whether a customer has left the company.")
print("• There are several categorical variables that may require encoding for analysis.")  
