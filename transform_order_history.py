import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.sql.functions import *
from pyspark.sql.types import StringType
from awsglue.dynamicframe import DynamicFrame

args = getResolvedOptions(sys.argv, ['JOB_NAME'])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Load from Glue Data Catalog
datasource = glueContext.create_dynamic_frame.from_catalog(
    database="tbsm-red",
    table_name="13",  # Update this to your actual crawler table
    transformation_ctx="datasource"
)

# Convert and rename
df = datasource.toDF().toDF(
    "InvoiceNo", "StockCode", "Description", "Quantity",
    "InvoiceDate", "UnitPrice", "CustomerID", "Country"
)

# Filter invalid
df = df.filter((col("Quantity") > 0) & (col("UnitPrice") > 0) & col("CustomerID").isNotNull())

# Order ID Hash
df = df.withColumn("OrderID", sha2(concat_ws("-", col("InvoiceNo"), col("StockCode")), 256))

# Total amount + USD conversion
df = df.withColumn("TotalAmount", col("Quantity") * col("UnitPrice"))
df = df.withColumn("TotalAmountUSD", col("TotalAmount") * lit(0.012))

# Date and Time
df = df.withColumn("InvoiceTimestamp", to_timestamp("InvoiceDate", "MM/d/yyyy H:mm"))
df = df.withColumn("InvoiceDateOnly", to_date("InvoiceTimestamp"))
df = df.withColumn("InvoiceHour", hour("InvoiceTimestamp"))

# Tagging high orders
df = df.withColumn("OrderTag", when(col("TotalAmount") > 100, "High").otherwise("Normal"))

# Region mapping
@udf(returnType=StringType())
def map_region(country):
    country = country.lower()
    if "united kingdom" in country: return "Europe"
    elif "france" in country: return "Europe"
    elif "germany" in country: return "Europe"
    elif "usa" in country: return "North America"
    elif "japan" in country: return "Asia"
    elif "australia" in country: return "Oceania"
    else: return "Other"

df = df.withColumn("Region", map_region(col("Country")))

# Final schema
final_df = df.select(
    "CustomerID", "OrderID", "InvoiceNo", "StockCode", "Description",
    "Quantity", "UnitPrice", "TotalAmount", "TotalAmountUSD",
    "OrderTag", "InvoiceDate", "InvoiceDateOnly", "InvoiceHour", "Country", "Region"
)

# Write to S3 in Parquet partitioned
final_dyf = DynamicFrame.fromDF(final_df, glueContext, "final_dyf")

glueContext.write_dynamic_frame.from_options(
    frame=final_dyf,
    connection_type="s3",
    connection_options={
        "path": "s3://tbsm-red/target/",
        "partitionKeys": ["Country", "InvoiceDateOnly"]
    },
    format="parquet"
)

job.commit()
