from fastapi import FastAPI, Depends , HTTPException,status,Request,Header
from fastapi.responses import JSONResponse
from sqlalchemy.orm import declarative_base,sessionmaker
from sqlalchemy import create_engine,func
from sqlalchemy.exc import SQLAlchemyError
from pydantic import BaseModel,Field
from Lab_API.models import Customers,FactCustomerAccount,DimContract,DimPayment,CustomerMLFeatures,StgCustomerRaw,HighRiskCustomer
import logging
from starlette.exceptions import HTTPException as StarletteHTTPException
import os
from fastapi.middleware.cors import CORSMiddleware
from Lab_ML.predict import predict_churn

API_KEY = os.getenv("API_KEY")
logger =logging.getLogger(__name__)





app = FastAPI()
app.add_middleware(CORSMiddleware,
                allow_origins=["http://localhost:5173"],
                allow_credentials=True,
                allow_methods=["*"],
                allow_headers=["*"],)





@app.exception_handler(404)
async def handle_404(request: Request, exc: StarletteHTTPException):
    logger.warning(f"Response status: 404 - {request.url.path}")

    error = ErrorResponseModel(
        detail=exc.detail,
        status_code=404
    )

    return JSONResponse(
        status_code=404,
        content=error.model_dump()
    )


def verify_api_key(x_api_key: str | None = Header(None)):
    if x_api_key != API_KEY:
        raise HTTPException(
            status_code=401,
            detail="Invalid or missing API key"
        )


url = "mysql+pymysql://root:root@localhost:3306/telecom_db"

engine = create_engine(
    url,
    isolation_level = "AUTOCOMMIT"
)

Base = declarative_base()

SessionLocal = sessionmaker(
    bind = engine,
    autocommit = False,
    autoflush = False
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

###########################################
#PYDANTIC MODELS
##########################################
class CustomerResponse(BaseModel):
    customer_id : str
    tenure: int
    contract_type:str
    monthly_charges:float
    churn: int

class CustomerFeatures(BaseModel):
    service_count:int
    tenure_bucket:str
    high_charge_flag:int
    is_long_term_customer:int
    has_streaming_bundle:int
    auto_pay_flag:int
    monthly_charges:float
    total_charges:float

class ChurnPredictionRequest(BaseModel):
    tenure:int = Field(ge=0,le=100 )
    monthly_charges:float = Field(gt=0)
    contract_type:str
    service_count:int

class ErrorResponseModel(BaseModel):
    detail : str
    status_code:int



################################################
#API ENDPOINTS
#################################################

#Customer Profile Endpoint
@app.get("/customer/{customer_id}",response_model=CustomerResponse,dependencies=[Depends(verify_api_key)])
def get_customer(customer_id:str ,request:Request,db = Depends(get_db)):
    logger.info(f"Request:{request.method} {request.url.path} customer_id = {customer_id}")
    try:
        customer = (
        db.query(
            Customers.customer_id,
            FactCustomerAccount.tenure,
            DimContract.contract_type,
            FactCustomerAccount.monthly_charges,
            FactCustomerAccount.churn
        )
        .join(
            FactCustomerAccount,
            Customers.customer_id == FactCustomerAccount.customer_id
        )
        .join(
            DimContract,
            FactCustomerAccount.contract_id == DimContract.contract_id
        )
        .filter(
            Customers.customer_id == customer_id
        )
        .first()
    )
    except SQLAlchemyError:
        logger.error("Response status: 500")
        error = ErrorResponseModel(
            detail="Database not available",
            status_code=500
        )
        return JSONResponse(
            status_code=500,
            content=error.model_dump()
        )

        
    if not customer:
        logger.error("Response status: 404")
        raise HTTPException(
            status_code = 404,
            detail = f"Customer {customer_id} not found"
        )
    logger.info("Response status: 200")
    return {
    "customer_id": customer.customer_id,
    "tenure": customer.tenure,
    "contract_type": customer.contract_type,
    "monthly_charges": customer.monthly_charges,
    "churn": customer.churn
}
        





#Churn Summary Endpoint

@app.get("/churn/summary",dependencies=[Depends(verify_api_key)])

def churn_summary(request:Request,db=Depends(get_db)):
    return get_churn_summary(request,db)


def get_churn_summary(request,db):
    logger.info(f"Request {request.method} {request.url.path}")
    try:
        total_customers = db.query(func.count(Customers.customer_id)).scalar()
        total_churned = db.query(func.count(FactCustomerAccount.customer_id)).filter(FactCustomerAccount.churn==1).scalar()
        churn_rate = round((total_churned/total_customers),2)
        contract_type_churn_rate = db.query(DimContract.contract_type,func.sum(FactCustomerAccount.churn).label("churned_count"),func.count(FactCustomerAccount.customer_id).label("total_count"))\
        .join(
            FactCustomerAccount,
            FactCustomerAccount.contract_id == DimContract.contract_id
        ).group_by(DimContract.contract_type).all() 
        contract_type_churn = []
        for row in contract_type_churn_rate:
            contract_type_churn.append({
                "contract_type":row.contract_type,
                "churn_rate":round(
                    (row.churned_count/row.total_count)*100,2
                )
            }
            )
        internet_service_churn_rate = db.query(StgCustomerRaw.InternetService,func.sum(FactCustomerAccount.churn).label("churned_count"),func.count(FactCustomerAccount.customer_id).label("total_count"))\
        .join(FactCustomerAccount,FactCustomerAccount.customer_id==StgCustomerRaw.customerID).group_by(StgCustomerRaw.InternetService).all()
    except SQLAlchemyError:
            logger.error("Response status: 500")
            error = ErrorResponseModel(
                detail="Database not available",
                status_code=500
            )
            return JSONResponse(
                status_code=500,
                content=error.model_dump()
            )
    internet_service_churn = []
    for row in internet_service_churn_rate:
        internet_service_churn.append({
            "internet_service":row.InternetService,
            "churn_rate":round((row.churned_count/row.total_count)*100,2)
        })
    logger.info("Response status: 200")
    return{
        "Total_Customers":total_customers,
        "Total_Churned":total_churned,
        "Churn_rate":churn_rate,
        "Churn_rate_by_contract_Type":contract_type_churn,
        "Internet_Service_churn_rate":internet_service_churn
        }


#High Risk Customers Endpoint

@app.get("/customers/high-risk",dependencies=[Depends(verify_api_key)])
def get_high_risk_customers(request:Request,db=Depends(get_db),limit:int = 50,min_tenure : int | None = None , max_tenure: int | None = None):
    logger.info(f"Request {request.method} {request.url.path} limit={limit} min_tenure={min_tenure} max_tenure={max_tenure}")
    try:
        query=  db.query(HighRiskCustomer)

        if min_tenure is not None:
            query  = query.filter(HighRiskCustomer.tenure >= min_tenure)

        if max_tenure is not None:
            query = query.filter(HighRiskCustomer.tenure<=max_tenure)

        high_risk_customers = query.limit(limit).all()
    except SQLAlchemyError:
            logger.error("Response status: 500")
            error = ErrorResponseModel(
                detail="Database not available",
                status_code=500
            )
            return JSONResponse(
                status_code=500,
                content=error.model_dump()
            )

    high_risk_list = []

    for row in high_risk_customers:
        high_risk_list.append({
        "customer_id":row.customer_id,
        "tenure":row.tenure,
        "monthly_charges":row.monthly_charges,
        "contract_type":row.contract_type,
        "risk_reason":row.risk_reason
    })
    logger.info("Response status: 200")
    return high_risk_list 


#Customer Features Endpoint

@app.get("/customer/{customer_id}/features",dependencies=[Depends(verify_api_key)])
def get_customer_ml_features(customer_id:str,request:Request,db = Depends(get_db)):
    logger.info(f"Request: {request.method} {request.url.path} customer_id={customer_id}")
    try:
        customer = db.query(CustomerMLFeatures).filter(CustomerMLFeatures.customer_id==customer_id).first()
    except SQLAlchemyError:
            logger.error("Response status: 500")
            error = ErrorResponseModel(
                detail="Database not available",
                status_code=500
            )
            return JSONResponse(
                status_code=500,
                content=error.model_dump()
            )
    if customer is None:
        logger.error("Response status: 404")
        raise HTTPException(
            status_code=404,
            detail=f"Customer {customer_id} not found"
        )
    logger.info("Response status: 200")

    return{
            "service_count":customer.service_count,
            "tenure_bucket":customer.tenure_bucket,
            "high_charge_flag":customer.high_charge_flag,
            "is_long_term_customer":customer.is_long_term_customer,
            "has_streaming_bundle":customer.has_streaming_bundle,
            "auto_pay_flag":customer.auto_pay_flag,
            "monthly_charges":customer.monthly_charges,
            "total_charges":customer.total_charges
            }


#Prediction Stub Endpoint
@app.post("/predict-churn", dependencies=[Depends(verify_api_key)])
def predict_churn_endpoint(request: Request, data: ChurnPredictionRequest):

    logger.info(
        f"Request: {request.method} {request.url.path} data={data}"
    )

    result = predict_churn(
        tenure=data.tenure,
        monthly_charges=data.monthly_charges,
        contract_type=data.contract_type,
        service_count=data.service_count
    )

    logger.info("Response status: 200")

    return result
    







    




    










