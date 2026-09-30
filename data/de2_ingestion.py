import os
import csv
import pandas as pd
from sqlalchemy import text,create_engine
from connection import get_engine

engine = get_engine()

EXPECTED_COLS = [
    "customerID", "gender", "SeniorCitizen", "Partner", "Dependents",
    "tenure", "PhoneService", "MultipleLines", "InternetService",
    "OnlineSecurity", "OnlineBackup", "DeviceProtection", "TechSupport",
    "StreamingTV", "StreamingMovies", "Contract", "PaperlessBilling",
    "PaymentMethod", "MonthlyCharges", "TotalCharges", "Churn"
]

def detect_files():
    files = os.listdir("data/landing")
    csv_files = []
    for file in files:
        if file.endswith(".csv"):
            csv_files.append(file)
    return csv_files

def validate_schema(filepath):
    with open(filepath) as file:
        reader=csv.reader(file)
        header = next(reader)
    return header==EXPECTED_COLS,header



def load_to_staging(filepath):
    df = pd.read_csv(filepath)
    df.to_sql("stg_customer_raw",engine,if_exists="replace",index=False)
    return len(df)


def log_ingestion(filename,status,rows,reason):
    with engine.connect() as conn:
        conn.execute(text("""insert into ingestion_log(filename,row_count,status,reason) values(:filename,:rows,:status,:reason)"""),
                     {
                         "filename":filename,
                         "status":status,
                         "rows":rows,
                         "reason":reason
                     })
        conn.commit()



def process_landing():
    files = detect_files()
    for file in files:
        filepath = "data/landing/"+file
        is_valid , headers = validate_schema(filepath)
        if is_valid:
           num_of_rows = load_to_staging(filepath)
           log_ingestion(file,"LOADED",num_of_rows,"Valid file")
        else:
            log_ingestion(file,"REJECTED",0,"Invalid schema(Column mismatch)")
        

if __name__ == "__main__":
    process_landing()


