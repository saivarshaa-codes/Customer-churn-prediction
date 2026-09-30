from sqlalchemy import create_engine,Column,Integer,String,Enum,ForeignKey,Numeric
from sqlalchemy.orm import declarative_base

DATABASE_URL= "mysql+pymysql://root:root@localhost/lab_sql1"

engine = create_engine(
    DATABASE_URL,
    isolation_level = "AUTOCOMMIT"
)

Base = declarative_base()


class Customer(Base):
    __tablename__ = "customers"
    customer_id = Column(String(20),primary_key=True)
    gender = Column(Enum("Male","Female"))
    senior_citizen = Column(Integer)
    partner = Column(Enum("Yes","No"))
    dependents = Column(Enum("Yes","No"))

class Services(Base):
    __tablename__ = "services"
    customer_id = Column(String(20),ForeignKey("customers.customer_id"),primary_key=True)
    phone_service = Column(Enum("Yes","No"))
    multiple_lines = Column(Enum("Yes","No","No phone service"))
    internet_service = Column(Enum("DSL","Fiber optic","No"))
    online_security = Column(Enum("Yes", "No", "No internet service"))
    online_backup = Column(Enum("Yes","No","No internet service"))
    device_protection = Column( Enum("Yes", "No", "No internet service"))
    tech_support = Column(Enum("Yes", "No", "No internet service"))
    streaming_tv = Column(Enum("Yes", "No", "No internet service"))
    streaming_movies = Column(Enum("Yes", "No", "No internet service"))

class Contracts(Base):
    __tablename__ = "contracts"
    customer_id = Column(String(20),ForeignKey("customers.customer_id"),primary_key=True)
    contract = Column(Enum("Month-to-month","One year","Two year"))
    tenure = Column(Integer)


class Billing(Base):
    __tablename__ ="billing"
    customer_id = Column(String(20),ForeignKey("customers.customer_id"),primary_key=True)
    paperless_billing = Column(Enum("Yes","No"))
    payment_method = Column(Enum("Electronic check","Mailed check","Bank transfer (automatic)","Credit card (automatic)"))
    monthly_charges = Column(Numeric(10, 2))
    total_charges = Column(Numeric(10, 2))



class CustomerStatus(Base):
    __tablename__ = "customer_status"
    customer_id = Column( String(20),ForeignKey("customers.customer_id"),primary_key=True)
    churn = Column(Enum("Yes", "No"))



Base.metadata.create_all(engine)
print("Tables created successfully")