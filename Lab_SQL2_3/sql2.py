from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pandas as pd

DATABASE_URL = "mysql+pymysql://root:root@localhost/telecom_db"

engine = create_engine(DATABASE_URL)

csv_file = "WA_Fn-UseC_-Telco-Customer-Churn.csv"
 
df = pd.read_csv(csv_file)
print(df.head())
df.to_sql(name="stg_customer_raw",if_exists="replace",con=engine,index=False)
print("CSV loaded successfully")




