from customer_cleaner import CustomerCleaner
from lab_cp4 import build_features
import pandas as pd
from datetime import datetime
import os
import logging


logging.basicConfig(level=logging.INFO)

def load_data(filepath):
    df= pd.read_csv(filepath)
    logging.info(f" The number of rows in the dataframe is :{df.shape[0]}")
    return df

def save_outputs(clean_df, feature_df, output_dir):
    timestamp = datetime.now().strftime("%Y%m%d")
    clean_file = f"{output_dir}/cleaned_file_{timestamp}.csv"
    feature_file = f"{output_dir}/feature_file_{timestamp}.csv"
    assert clean_df['monthly_charges'].notnull().all(),"Error : monthly_charges contains null values"
    assert clean_df['churn'].isin([0,1]).all(),"Error:churn contains values other than 0 and 1"
    assert feature_df['monthly_charges'].notnull().all(),"Error : monthly_charges contains null values"
    assert feature_df['churn'].isin([0,1]).all(),"Error:churn contains values other than 0 and 1"
    clean_df.to_csv(clean_file, index=False)
    feature_df.to_csv(feature_file, index=False)
    logging.info(f"Clean file saved: {clean_file}")
    logging.info(f"Feature file saved: {feature_file}")



def main():
    logging.info(f"Pipeline started at {datetime.now()}")
    try:
        logging.info("Loading data...")
        df = load_data("C:\\Users\\saivarshaa.sujee\\Prodapt_Labs\\WA_Fn-UseC_-Telco-Customer-Churn.csv")
        logging.info("Data loading completed")
    except Exception as e:
        logging.error(f"Data loading failed {e}")
        raise
    try:
        logging.info("Data cleaning started")
        df_cleaner=CustomerCleaner(df)
        clean_df = df_cleaner.clean()
        logging.info("Data cleaning completed")
    except Exception as e:
        logging.error(f"Data cleaning failed:{e}")
        raise
    try:
        logging.info("Feature addition started")
        feature_df = build_features(clean_df.copy())
        logging.info("New features added")
    except Exception as e:
        logging.error(f"Feature addition failed:{e}")
        raise
    try:
        logging.info("Saving output...")
        save_outputs(clean_df,feature_df,".")
        logging.info("Output is saved")
    except Exception as e:
        logging.error(f"Saving output failed:{e}")
        raise
    logging.info("Pipeline Completed Successfully")


if __name__=='__main__':
    main()



