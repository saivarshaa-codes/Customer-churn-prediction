from pyspark.sql import SparkSession
from pyspark.sql.types import (StructType,StructField,StringType,IntegerType,DoubleType)
from pyspark.sql import functions as F
import os
os.environ["HADOOP_HOME"] = r"C:\Users\saivarshaa.sujee\pyspark_demo\hadoop"
os.environ["PATH"] = os.environ["PATH"] + r";C:\Users\saivarshaa.sujee\pyspark_demo\hadoop\bin"


spark = (
    SparkSession.builder\
    .master("local[2]")\
    .config("spark.driver.memory","4g")
    .getOrCreate()
)

schema = StructType([
    StructField("customerID", StringType(), True),
    StructField("gender", StringType(), True),
    StructField("SeniorCitizen", IntegerType(), True),
    StructField("Partner", StringType(), True),
    StructField("Dependents", StringType(), True),
    StructField("tenure", IntegerType(), True),
    StructField("PhoneService", StringType(), True),
    StructField("MultipleLines", StringType(), True),
    StructField("InternetService", StringType(), True),
    StructField("OnlineSecurity", StringType(), True),
    StructField("OnlineBackup", StringType(), True),
    StructField("DeviceProtection", StringType(), True),
    StructField("TechSupport", StringType(), True),
    StructField("StreamingTV", StringType(), True),
    StructField("StreamingMovies", StringType(), True),
    StructField("Contract", StringType(), True),
    StructField("PaperlessBilling", StringType(), True),
    StructField("PaymentMethod", StringType(), True),
    StructField("MonthlyCharges", DoubleType(), True),
    StructField("TotalCharges", StringType(), True),
    StructField("Churn", StringType(), True)
])

df = spark.read.csv(
    "data/landing/WA_Fn-UseC_-Telco-Customer-Churn.csv",
    header=True,
    schema=schema
)
df.printSchema()

df = df.withColumn("TotalCharges",F.regexp_replace(F.col("TotalCharges"),r"^\s*$","").cast(DoubleType()))

df = df.withColumn("Churn",F.when(F.col("Churn")=="Yes",1).otherwise(0))

contract_summary = df.groupBy("Contract").agg(F.count("*").alias("customer_count"),F.avg("Churn").alias("churn_rate"))
contract_summary.show()


internet_summary = df.groupBy("InternetService").agg(F.avg("MonthlyCharges").alias("Average Monthly Charges"),F.avg("Churn").alias("Average Churn"))
internet_summary.show()

contract_summary.write.mode("overwrite").partitionBy("Contract").parquet("data/spark_output/contract_summary/")

new_df = spark.read.parquet("data/spark_output/contract_summary/")
new_df.printSchema()
print(new_df.count())