from sqlalchemy import create_engine

DATABASE_URL = "mysql+pymysql://root:root@localhost/telecom_db"

def get_engine():
    return create_engine(DATABASE_URL)