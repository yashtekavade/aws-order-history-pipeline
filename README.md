# 🧾 AWS Real-Time Order History Data Pipeline

[![AWS](https://img.shields.io/badge/AWS-232F3E?style=for-the-badge&logo=amazon-aws&logoColor=white)](https://aws.amazon.com/)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org/)
[![Apache Spark](https://img.shields.io/badge/Apache%20Spark-E25A1C?style=for-the-badge&logo=apache-spark&logoColor=white)](https://spark.apache.org/)

A real-time data ingestion and transformation pipeline using AWS services like **EC2**, **Kinesis Firehose**, **S3**, **Glue**, **Athena**, and **QuickSight**. The pipeline processes e-commerce order logs, enriches the data, and stores it for analytical queries and visualization.

## 📋 Table of Contents

- [Architecture Overview](#-architecture-overview)
- [Repository Structure](#-repository-structure)
- [Setup Instructions](#️-setup-instructions)
- [Data Transformations](#-data-transformations)
- [Sample Queries](#-sample-queries)
- [Monitoring & Troubleshooting](#-monitoring--troubleshooting)
- [Cost Optimization](#-cost-optimization)

## 🏗️ Architecture Overview

```
EC2 Instance (Log Generator)
        ↓
    Kinesis Agent
        ↓
Amazon Kinesis Data Firehose (tbsm-red-fire)
        ↓
Amazon S3 (Raw Logs Bucket)
        ↓
AWS Glue Crawler → AWS Glue Data Catalog
        ↓
AWS Glue ETL Job (Data Transformations)
        ↓
Amazon S3 (Partitioned Parquet Output)
        ↓
Amazon Athena / Amazon QuickSight
```

### Data Flow
1. **Data Generation**: EC2 instance generates simulated e-commerce order logs
2. **Real-time Ingestion**: Kinesis Agent streams logs to Firehose
3. **Raw Storage**: Firehose delivers data to S3 raw bucket
4. **Schema Discovery**: Glue Crawler automatically discovers schema
5. **Data Transformation**: Glue ETL job processes and enriches data
6. **Optimized Storage**: Transformed data stored as Parquet with partitioning
7. **Analytics**: Athena and QuickSight provide query and visualization capabilities

## ✨ Features

- **Real-time Data Ingestion**: Continuous streaming of order data
- **Serverless Architecture**: Fully managed AWS services with auto-scaling
- **Data Lake Pattern**: Scalable storage with schema-on-read capability
- **Advanced ETL**: Complex data transformations and enrichment
- **Partitioned Storage**: Optimized for query performance and cost
- **Business Intelligence**: Interactive dashboards and ad-hoc queries
- **Monitoring & Alerting**: Built-in AWS monitoring capabilities
- **Cost Optimization**: Intelligent tiering and lifecycle policies

## 📋 Prerequisites

### AWS Services & Permissions
- **AWS Account** with appropriate IAM permissions
- **EC2** - For log generation and Kinesis Agent
- **IAM Roles** with policies for:
  - Kinesis Firehose delivery
  - S3 read/write access
  - Glue job execution
  - Athena query execution
  - QuickSight data access

### Required IAM Policies
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "firehose:PutRecord",
        "firehose:PutRecordBatch",
        "s3:GetObject",
        "s3:PutObject",
        "s3:DeleteObject",
        "s3:ListBucket",
        "glue:*",
        "athena:*"
      ],
      "Resource": "*"
    }
  ]
}
```

### Software Requirements
- **Python 3.8+**
- **AWS CLI** configured with credentials
- **Boto3** library
- **Apache Spark** (managed by Glue)

## 📁 Repository Structure

```
aws-order-pipeline/
├── LogGenerator.py              # Simulates and writes e-commerce order logs to /var/log/orders/
├── agent.json                   # Kinesis Agent configuration to push logs to Firehose
├── transform_order_history.py   # AWS Glue ETL job script with data transformations
├── create_table.sql             # Athena external table creation over transformed Parquet files
├── queries.sql                  # Sample Athena queries for business insights
└── README.md                    # This documentation file
```

### File Descriptions

| File | Purpose | Key Features |
|------|---------|--------------|
| **LogGenerator.py** | Real-time log simulation | Generates realistic e-commerce order data with configurable patterns |
| **agent.json** | Kinesis Agent config | Monitors log files and streams to Firehose with buffering settings |
| **transform_order_history.py** | Glue ETL job | Data cleaning, enrichment, currency conversion, and partitioning |
| **create_table.sql** | Athena table setup | External table definition over partitioned Parquet files |
| **queries.sql** | Analytics queries | Business intelligence queries for insights and reporting |

## ⚙️ Setup Instructions

### Prerequisites
- AWS Account with appropriate IAM permissions
- EC2 instance with IAM role for Firehose, S3, and Glue access
- Python 3.8+ installed on EC2

### Required AWS Services
- **Amazon EC2** - Log generation and Kinesis Agent
- **Amazon Kinesis Data Firehose** - Real-time data delivery
- **Amazon S3** - Data lake storage (raw and processed)
- **AWS Glue** - ETL jobs and data catalog
- **Amazon Athena** - Serverless analytics
- **Amazon QuickSight** - Business intelligence (optional)

### Step 1: 🚀 Set Up Log Generation

1. **Launch EC2 Instance**
   ```bash
   # Launch with appropriate IAM role
   aws ec2 run-instances \
     --image-id ami-0abcdef1234567890 \
     --count 1 \
     --instance-type t3.medium \
     --iam-instance-profile Name=YourGlueFirehoseRole
   ```

2. **Deploy Log Generator**
   ```bash
   # SSH into EC2 and create log directory
   ssh -i your-key.pem ec2-user@your-instance-ip
   sudo mkdir -p /var/log/orders
   sudo chmod 755 /var/log/orders
   
   # Download and run the log generator
   wget https://raw.githubusercontent.com/your-repo/LogGenerator.py
   python3 LogGenerator.py
   ```

### Step 2: 🔥 Configure Kinesis Data Firehose

1. **Create Firehose Delivery Stream**
   ```bash
   aws firehose create-delivery-stream \
     --delivery-stream-name tbsm-red-fire \
     --extended-s3-destination-configuration \
     BucketARN=arn:aws:s3:::your-raw-bucket,\
     Prefix=year=!{timestamp:yyyy}/month=!{timestamp:MM}/day=!{timestamp:dd}/,\
     CompressionFormat=GZIP
   ```

2. **Install and Configure Kinesis Agent**
   ```bash
   # Install Kinesis Agent on EC2
   sudo yum install -y aws-kinesis-agent
   
   # Copy the agent.json configuration
   sudo cp agent.json /etc/aws-kinesis/agent.json
   
   # Start the agent
   sudo service aws-kinesis-agent start
   sudo chkconfig aws-kinesis-agent on
   ```

### Step 3: 🧬 Set Up AWS Glue

1. **Create Glue Database**
   ```bash
   aws glue create-database \
     --database-input Name=order_history_db,Description="E-commerce order history"
   ```

2. **Create and Run Crawler**
   ```bash
   # Create crawler for raw data discovery
   aws glue create-crawler \
     --name order-history-crawler \
     --role GlueServiceRole \
     --database-name order_history_db \
     --targets S3Targets=[{Path=s3://your-raw-bucket/}]
   
   # Start crawler
   aws glue start-crawler --name order-history-crawler
   ```

3. **Deploy Glue ETL Job**
   ```bash
   # Upload transform script to S3
   aws s3 cp transform_order_history.py s3://your-scripts-bucket/
   
   # Create Glue job
   aws glue create-job \
     --name transform-order-history \
     --role GlueServiceRole \
     --command Name=glueetl,ScriptLocation=s3://your-scripts-bucket/transform_order_history.py
   ```

### Step 4: 🧠 Configure Amazon Athena

1. **Set Up Athena Query Result Location**
   ```bash
   aws s3 mb s3://your-athena-results-bucket
   ```

2. **Create External Table**
   ```bash
   # Run the SQL from create_table.sql in Athena Console
   # Or use AWS CLI
   aws athena start-query-execution \
     --query-string file://create_table.sql \
     --result-configuration OutputLocation=s3://your-athena-results-bucket/
   ```

### Step 5: 📈 Set Up QuickSight (Optional)

1. **Sign up for QuickSight** and choose Standard edition
2. **Add Athena as Data Source**
   - Data source: Athena
   - Database: order_history_db
   - Table: transformed_orders
3. **Create Analysis** with visualizations for business insights

## 🔄 Data Transformations

### Input Schema (Raw Logs)
```json
{
  "InvoiceNo": "536365",
  "StockCode": "85123A",
  "Description": "WHITE HANGING HEART T-LIGHT HOLDER",
  "Quantity": 6,
  "InvoiceDate": "2010-12-01 08:26:00",
  "UnitPrice": 2.55,
  "CustomerID": "17850",
  "Country": "United Kingdom"
}
```

### Transformation Pipeline

| Step | Transformation | Description | Business Value |
|------|---------------|-------------|----------------|
| 1 | **ID Generation** | `SHA256(InvoiceNo + StockCode)` | Unique order identification |
| 2 | **Currency Conversion** | `Quantity × UnitPrice × 0.012` | Standardized USD amounts |
| 3 | **Date Parsing** | Split `InvoiceDate` → `Date` + `Hour` | Time-based analysis |
| 4 | **Geographic Mapping** | `Country` → `Region` mapping | Regional insights |
| 5 | **Data Quality** | Filter invalid records | Clean, reliable data |
| 6 | **Value Classification** | Tag high-value orders (>$100) | Customer segmentation |
| 7 | **Partitioning** | Partition by Country + Date | Query optimization |

### Output Schema (Transformed)
```json
{
  "orderid": "a1b2c3d4e5f6...",
  "invoiceno": "536365",
  "stockcode": "85123A",
  "description": "WHITE HANGING HEART T-LIGHT HOLDER",
  "quantity": 6,
  "invoicedateonly": "2010-12-01",
  "invoicehour": 8,
  "unitprice": 2.55,
  "customerid": "17850",
  "country": "United Kingdom",
  "region": "Europe",
  "totalamountusd": 183.6,
  "ordertag": "High"
}
```

## 📊 Monitoring & Troubleshooting

### CloudWatch Metrics
- **Kinesis Firehose**: Delivery success rate, error count
- **Glue Jobs**: Job duration, success/failure rates
- **S3**: Storage utilization, request metrics
- **Athena**: Query execution time, data scanned

### Common Issues & Solutions

| Issue | Symptoms | Solution |
|-------|----------|----------|
| **Kinesis Agent Not Sending** | No data in S3 | Check agent logs, verify IAM permissions |
| **Glue Job Failures** | Job status: FAILED | Review job logs, check data format |
| **Athena Query Timeouts** | Slow query performance | Optimize partitioning, use columnar formats |
| **Missing Partitions** | Data not visible in Athena | Run MSCK REPAIR TABLE |

### Log Locations
```bash
# Kinesis Agent logs
/var/log/aws-kinesis-agent/aws-kinesis-agent.log

# EC2 application logs
/var/log/orders/

# CloudWatch Logs
/aws/glue/jobs/transform-order-history
/aws/kinesis/firehose/tbsm-red-fire
```

## 💰 Cost Optimization

### Storage Optimization
- **S3 Intelligent Tiering**: Automatic cost optimization
- **Lifecycle Policies**: Archive old data to Glacier
- **Parquet Format**: 75% storage reduction vs JSON

### Compute Optimization
- **Glue Job Scheduling**: Run during off-peak hours
- **Auto Scaling**: Dynamic resource allocation
- **Spot Instances**: For non-critical workloads

### Query Optimization
- **Partition Pruning**: Reduce data scanned in Athena
- **Columnar Storage**: Query only needed columns
- **Result Caching**: Reuse query results

## 🔒 Security Considerations

### Data Protection
- **Encryption at Rest**: S3 SSE-KMS encryption
- **Encryption in Transit**: HTTPS/TLS for all communications
- **Access Control**: Fine-grained IAM policies

### Network Security
- **VPC**: Deploy resources in private subnets
- **Security Groups**: Restrict port access
- **NAT Gateway**: Secure internet access

### Compliance
- **Data Masking**: PII protection in transformations
- **Audit Logging**: CloudTrail for API calls
- **Data Retention**: Automated deletion policies

## 🔍 Sample Queries

### Business Intelligence Queries

```sql
-- Top 10 High-Value Orders
SELECT 
    orderid,
    country,
    totalamountusd,
    invoicedateonly
FROM transformed_orders 
WHERE ordertag = 'High'
ORDER BY totalamountusd DESC 
LIMIT 10;

-- Regional Revenue Analysis
SELECT 
    region,
    COUNT(*) as order_count,
    SUM(totalamountusd) as total_revenue,
    AVG(totalamountusd) as avg_order_value
FROM transformed_orders 
GROUP BY region
ORDER BY total_revenue DESC;

-- Peak Hours Analysis
SELECT 
    invoicehour,
    COUNT(*) as order_count,
    SUM(totalamountusd) as hourly_revenue
FROM transformed_orders 
GROUP BY invoicehour
ORDER BY invoicehour;

-- Country Performance (Partitioned Query)
SELECT 
    country,
    invoicedateonly,
    COUNT(*) as daily_orders,
    SUM(totalamountusd) as daily_revenue
FROM transformed_orders 
WHERE country_partition = 'United Kingdom'
    AND date_partition >= '2023-01-01'
GROUP BY country, invoicedateonly
ORDER BY invoicedateonly DESC;
```

### Data Quality Queries

```sql
-- Check for Missing Data
SELECT 
    'Missing CustomerID' as issue,
    COUNT(*) as count
FROM transformed_orders 
WHERE customerid IS NULL

UNION ALL

SELECT 
    'Zero Quantity Orders' as issue,
    COUNT(*) as count
FROM transformed_orders 
WHERE quantity <= 0;

-- Duplicate Order Detection
SELECT 
    orderid,
    COUNT(*) as duplicate_count
FROM transformed_orders 
GROUP BY orderid
HAVING COUNT(*) > 1;
```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### Development Setup
```bash
# Clone repository
git clone https://github.com/your-org/aws-order-pipeline.git
cd aws-order-pipeline

# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
pytest tests/

# Code formatting
black . && flake8 .
```


