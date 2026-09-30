import pandas as pd
import re
import numpy as np
import logging


logging.basicConfig(level=logging.INFO)
class CustomerCleaner:
    def __init__(self,df):
        self.df = df.copy()

    def standardize_column_names(self):
        logging.info("Standardizing column names")
        columns = []
        for col in self.df.columns:
            col = re.sub(r'([a-z0-9])([A-Z])',r'\1_\2',col)
            col = col.lower()
            columns.append(col)

        self.df.columns = columns

        return self.df


    def fix_total_charges(self):
        try:
            empty_rows = (self.df['total_charges'].astype(str).str.strip()=='').sum()
            logging.info(f"Found {empty_rows} blank values in total_charges")
            self.df['total_charges']=self.df['total_charges'].replace(r'^\s*$', np.nan, regex=True)
            self.df['total_charges']=pd.to_numeric(self.df['total_charges'],errors='coerce')
            logging.info("Converted total_charges to numeric")
            return self.df
        except Exception as e:
            logging.error(f"Error:{e}")
            raise


    def normalize_binary_columns(self):
        logging.info("Normalizing binary columns")
        binary_columns = ['partner','dependents','phone_service','paperless_billing','churn']
        for col in binary_columns:
            self.df[col]=self.df[col].map({"Yes":1,"No":0})
        return self.df

    def handle_nulls(self):
        self.df['total_charges']=self.df['total_charges'].fillna(self.df['monthly_charges'])
        logging.info(f"Filled null values in total_charges")
        return self.df

    def clean(self):
        logging.info("Starting cleaning process")
        self.df = self.standardize_column_names()
        self.df = self.fix_total_charges()
        self.df = self.normalize_binary_columns()
        self.df = self.handle_nulls()
        logging.info("Cleaning process completed")
        return self.df





