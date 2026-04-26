# 📊 MarketMaven — Cloud-Ready Data Engineering Pipeline (Spark → AWS Glue → Athena)

---

# 🧠 Overview

MarketMaven is an end-to-end **data engineering pipeline** designed to process market time-series data using Apache Spark locally and evolving into a **production-grade AWS cloud architecture** using S3, AWS Glue, and Athena.

The project demonstrates core Data Engineering concepts including:

* Batch data ingestion
* Data cleaning and transformation
* Feature engineering using window functions
* Partitioned data lake storage
* Cloud ETL migration (AWS Glue)
* SQL-based analytics (Athena)
* Optional orchestration using Airflow

---

# ⚙️ Current Local Architecture (Implemented)

```
JSON Data (Local)
        ↓
PySpark Job (spark_job.py)
        ↓
Data Cleaning + Feature Engineering
        ↓
Window Functions (price lag, delta)
        ↓
Parquet Output
        ↓
s3a://marketmaven-data-abhas/market_data/
```

---

# 🧪 Features Implemented

## ✔ Data Ingestion

* Reads structured JSON market data
* Schema enforcement using PySpark StructType

## ✔ Data Cleaning

* Removes invalid price records

## ✔ Feature Engineering

* Timestamp conversion
* Hour extraction
* Date extraction
* Price change using window functions

## ✔ Aggregation Layer

* Average price per symbol
* Average volume per symbol

## ✔ Storage Layer

* Partitioned Parquet output
* Partition keys: symbol, date

---

# ☁️ Target Cloud Architecture (Future Upgrade)

## 🚀 AWS-Based Production Pipeline

```
Market Data API / Files
        ↓
Amazon S3 (Raw Layer)
        ↓
AWS Glue ETL Job (PySpark)
        ↓
Amazon S3 (Curated Layer)
        ↓
AWS Glue Data Catalog
        ↓
Amazon Athena (SQL Analytics)
        ↓
Amazon QuickSight (Dashboards)
```

---

# 🔧 AWS Components

## 🪣 Amazon S3

* Raw, Processed, and Curated zones
* Central data lake storage

## ⚙️ AWS Glue

* Serverless Spark-based ETL
* Replaces local Spark execution
* Handles schema inference & transformation

## 🧠 Glue Data Catalog

* Metadata layer for datasets
* Enables Athena SQL queries

## 📊 Amazon Athena

* SQL querying over S3
* No infrastructure management

## 📈 (Optional) QuickSight

* BI dashboards for market trends

---

# 🔄 Orchestration (Optional Future Layer)

## Apache Airflow (Lightweight DAG)

Pipeline flow:

```
1. Load raw data → S3
2. Trigger AWS Glue ETL job
3. Validate output dataset
4. Notify completion
```

---

# 🧱 Tech Stack

### Core

* Python
* PySpark
* Pandas (supporting analysis)

### Big Data

* Apache Spark
* Window Functions

### Cloud (Future)

* AWS S3
* AWS Glue
* AWS Athena
* AWS Glue Data Catalog

### Orchestration (Optional)

* Apache Airflow

---

# 📁 Project Structure

```
MarketMaven/
│
├── data/
│   └── raw/
│       └── market_events.json
│
├── src/
│   └── spark/
│       └── spark_job.py
│
├── archive/
│   └── models/
│
├── venv/
├── README.md
└── requirements.txt
```

---

# ⚠️ Known Issues (Local Setup)

### ❌ S3A Initialization Error

* Error: `NumberFormatException: "60s"`
* Root cause: Hadoop/Spark timeout config mismatch

### ❌ Windows Spark Limitations

* winutils dependency
* unstable S3A filesystem behavior

---

# 🧠 Key Learning Outcomes

* Distributed data processing using Spark
* Window-based feature engineering
* Data lake architecture design
* Cloud migration strategy (Spark → AWS Glue)
* SQL analytics on large datasets

---

# 🚀 Future Improvements

## Phase 1 — Stability Fix

* Resolve S3A timeout configuration issues
* Migrate to Spark 3.5 stable build

## Phase 2 — AWS Migration

* Move Spark job to AWS Glue
* Store raw data in S3 bucket
* Enable Athena querying

## Phase 3 — Production Pipeline

* Add Airflow orchestration
* Add logging + monitoring
* Add data validation layer

## Phase 4 — BI Layer

* Integrate QuickSight dashboards
* Market trend visualization

---

# 📌 Resume Value

This project demonstrates:

* Real-world data engineering pipeline design
* Spark-based transformation logic
* Cloud migration strategy
* Data lake architecture (Medallion-style)
* Production thinking (orchestration + analytics)

---

# 👨‍💻 Author

Abhas Nayak

---

# 📈 Status

* Local Spark Pipeline: ✅ Working (partial issue in S3 layer)
* AWS Architecture Design: 🚧 In progress
* Orchestration Layer: 🚧 Planned
* Production Deployment: 🚧 Future scope
