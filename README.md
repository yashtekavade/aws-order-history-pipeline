```markdown
# 🧾 AWS Real-Time Order History Data Pipeline

This project demonstrates a real-time data ingestion and transformation pipeline using AWS services like **EC2**, **Kinesis Firehose**, **S3**, **Glue**, **Athena**, and **QuickSight**. The pipeline processes e-commerce order logs, enriches the data, and stores it for analytical queries and visualization.

---

## 📊 Architecture

```

EC2 (Log Generator)
↓
AWS Kinesis Firehose (tbsm-red-fire)
↓
Amazon S3 (Raw Logs Bucket)
↓
AWS Glue Crawler → AWS Glue Job (Data Transformations)
↓
Amazon S3 (Partitioned Output)
↓
Amazon Athena / Amazon QuickSight

```

---

## 📁 Repository Structure

```
.
├── data-generator/
│   └── LogGenerator.py            # Simulates and writes order logs to /var/log/orders/
│
├── kinesis-agent/
│   └── agent.json                 # Kinesis Agent config to push logs to Firehose
│
├── glue-job/
│   └── transform\_order\_history.py # Main Glue ETL job script with all transformations
│
├── athena/
│   ├── create\_table.sql           # Athena external table over transformed Parquet files
│   └── queries.sql                # Sample Athena queries for insights
│
└── README.md

````

---

## ⚙️ Setup Instructions

### 1. 🚀 Real-Time Log Generation

- Launch EC2 instance with the necessary permissions (Firehose, S3).
- Place `LogGenerator.py` in the EC2 and execute it to start writing log files to `/var/log/orders/`.

```bash
python3 LogGenerator.py
````

---

### 2. 🔥 Kinesis Firehose

* Create a Firehose delivery stream named `tbsm-red-fire` pointing to your raw S3 bucket.
* On EC2, install and configure the **Kinesis Agent**:

```bash
sudo yum install -y aws-kinesis-agent
sudo cp kinesis-agent/agent.json /etc/aws-kinesis/agent.json
sudo service aws-kinesis-agent start
```

---

### 3. 🧬 AWS Glue

* Create a **Glue Crawler** to scan raw S3 logs.
* Create a **Glue Job** using `glue-job/transform_order_history.py` that:

  * Generates unique Order IDs
  * Converts to USD
  * Splits Date/Time
  * Maps Country → Region
  * Tags high-value orders
  * Filters bad records
  * Writes to S3 (Parquet, partitioned by Country & Date)

---

### 4. 🧠 Amazon Athena

* Run `athena/create_table.sql` to register your transformed data as an external table.
* Execute queries from `athena/queries.sql` to explore insights like:

  * Top 10 high value orders
  * Region-wise orders
  * Peak ordering hours
  * Query by country partitions

---

### 5. 📈 Amazon QuickSight

* Connect QuickSight to the S3/Athena dataset.
* Build visualizations for:

  * Daily order trends
  * Region-wise heatmaps
  * Order volume by hour

---

## ✅ Transformations Performed

| Transformation        | Description                                                              |
| --------------------- | ------------------------------------------------------------------------ |
| 🔑 OrderID            | SHA-256 Hash of `InvoiceNo + StockCode`                                  |
| 💰 TotalAmountUSD     | `Quantity * UnitPrice * ConversionRate (0.012)`                          |
| 🕒 InvoiceDate Split  | Parsed into `InvoiceDateOnly` and `InvoiceHour`                          |
| 🌍 Region Mapping     | Maps Country → Region                                                    |
| 🧹 Data Cleaning      | Filters rows with missing `CustomerID`, or negative `Quantity/UnitPrice` |
| 🏷️ Order Tag         | Marks orders with value > 100 as `High`                                  |
| 🧱 Partitioned Output | Written to S3 by `Country` and `InvoiceDateOnly` in **Parquet** format   |

---

## 🧠 Sample Use Cases

* 🔍 Business analysis of high-value customers
* 🗺️ Geo insights: orders per region/country
* ⏰ Time-based patterns: hourly peaks
* 📦 Detect and clean bad input data

```
