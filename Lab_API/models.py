from sqlalchemy import Column,Integer,String,create_engine,Enum,Float,ForeignKey
from sqlalchemy.orm import declarative_base,sessionmaker

Base = declarative_base()

DATABASE_URL = "mysql+pymysql://root:root@localhost/telecom_db"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

class DimContract(Base):
    __tablename__ = "dim_contract"
    contract_id = Column(Integer,primary_key=True,autoincrement=True)
    contract_type = Column(String(100), unique=True)

class DimPayment(Base):
    __tablename__ = "dim_payment"
    payment_id = Column(Integer,primary_key=True,autoincrement=True)
    payment_method = Column(String(100),unique=True)


class Customers(Base):
    __tablename__ = "customers"
    customer_id = Column(String(50),primary_key=True)
    gender = Column(String(20))
    senior_citizen = Column(Integer)
    partner = Column(Integer)
    dependents = Column(Integer)

class FactCustomerAccount(Base):
    __tablename__ = "fact_customer_account"
    fact_id = Column(Integer,primary_key=True,autoincrement=True)
    customer_id = Column(String(50),ForeignKey("customers.customer_id"))
    contract_id = Column(Integer,ForeignKey("dim_contract.contract_id"))
    payment_id = Column(Integer,ForeignKey("dim_payment.payment_id"))
    tenure = Column(Integer)
    monthly_charges = Column(Float)
    total_charges = Column(Float)
    churn = Column(Integer)
    

class CustomerMLFeatures(Base):
    __tablename__ = "customer_ml_features"

    customer_id = Column(String(50), primary_key=True)
    gender = Column(String(20))
    senior_citizen = Column(Integer)
    partner = Column(Integer)
    dependents = Column(Integer)
    tenure = Column(Integer)
    phone_service = Column(String(20))
    multiple_lines = Column(String(30))
    internet_service = Column(String(30))
    online_security = Column(Integer)
    online_backup = Column(Integer)
    device_protection = Column(Integer)
    tech_support = Column(Integer)
    streaming_tv = Column(Integer)
    streaming_movies = Column(Integer)
    contract_type = Column(String(30))
    paperless_billing = Column(String(20))
    payment_method = Column(String(50))
    monthly_charges = Column(Float)
    total_charges = Column(Float)
    tenure_bucket = Column(String(10))
    high_charge_flag = Column(Integer)
    service_count = Column(Integer)
    is_long_term_customer = Column(Integer)
    has_streaming_bundle = Column(Integer)
    auto_pay_flag = Column(Integer)
    churn = Column(Integer)


from sqlalchemy import Column, String, BigInteger, Float

class StgCustomerRaw(Base):
    __tablename__ = "stg_customer_raw"

    customerID = Column(String(50), primary_key=True)
    gender = Column(String(20))
    SeniorCitizen = Column(BigInteger)
    Partner = Column(String(10))
    Dependents = Column(String(10))
    tenure = Column(BigInteger)
    PhoneService = Column(String(20))
    MultipleLines = Column(String(30))
    InternetService = Column(String(30))
    OnlineSecurity = Column(String(30))
    OnlineBackup = Column(String(30))
    DeviceProtection = Column(String(30))
    TechSupport = Column(String(30))
    StreamingTV = Column(String(30))
    StreamingMovies = Column(String(30))
    Contract = Column(String(30))
    PaperlessBilling = Column(String(20))
    PaymentMethod = Column(String(50))
    MonthlyCharges = Column(Float)
    TotalCharges = Column(String(30))
    Churn = Column(String(10))

class HighRiskCustomer(Base):
    __tablename__ = "v_high_risk_customers"

    customer_id = Column(String(50), primary_key=True)
    contract_type = Column(String(30))
    tenure = Column(Integer)
    monthly_charges = Column(Float)
    risk_reason = Column(String(96))


Base.metadata.create_all(engine)
print("Tables created Successfully")



