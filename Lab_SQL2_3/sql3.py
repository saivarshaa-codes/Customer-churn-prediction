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
    

Base.metadata.create_all(engine)
print("Tables created Successfully")

customer = session.query(Customers).filter_by(customer_id = "7590-VHVEG").first()
print(customer)
print(customer.customer_id)
print(customer.gender)
print(customer.partner)