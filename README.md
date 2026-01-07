# FlexiMart Data Architecture Project

**Student Name:** Rajvi Desai
**Student ID:** BITSoM_BA_25071186
**Email:** desairajvi29@gmail.com
**Date:** 06-Jan-2026

## Project Overview

I have built a robust data architecture for FlexiMart, a retail analytics platform. This project involves a full data lifecycle implementation: extracting raw transactional data, loading it into a Relational Database (MySQL) via an ETL pipeline, performing NoSQL analysis (MongoDB) on product catalogs, and finally designing and populating a Star Schema Data Warehouse for high-performance OLAP analytics.

## Repository Structure
```
├── part1-database-etl/
│   ├── etl_pipeline.py
│   ├── schema_documentation.md
│   ├── business_queries.sql
│   └── data_quality_report.txt
├── part2-nosql/
│   ├── nosql_analysis.md
│   ├── mongodb_operations.js
│   └── products_catalog.json
├── part3-datawarehouse/
│   ├── star_schema_design.md
│   ├── warehouse_schema.sql
│   ├── warehouse_data.sql
│   └── analytics_queries.sql
└── README.md
```

## Technologies Used

- **Languages:** Python 3.14, SQL, JavaScript
- **Databases:** MySQL 8.x, MongoDB 6.x
- **Libraries:** pandas, mysql-connector-python, pymongo

## Setup Instructions

### Database Setup

Ensure MySQL and MongoDB are running locally.

```bash
# Create databases (if not automatically handled by scripts)
mysql -u root -p -e "CREATE DATABASE IF NOT EXISTS fleximart;"
mysql -u root -p -e "CREATE DATABASE IF NOT EXISTS fleximart_dw;"
```

### 1. ETL Pipeline Execution
Extracts CSV data, transforms it, and loads into `fleximart` MySQL DB.

```bash
cd part1-database-etl
python etl_pipeline.py
```

### 2. Business SQL Queries
Runs operational queries on the transactional database.

```bash
mysql -u root -p fleximart < business_queries.sql
```

### 3. NoSQL Operations
Seeds `product_db` in MongoDB and runs aggregation queries.

```bash
cd ../part2-nosql
node mongodb_operations.js
```

### 4. Data Warehouse & Analytics
Sets up the Star Schema and runs OLAP queries.

```bash
cd ../part3-datawarehouse

# Create Schema
mysql -u root -p fleximart_dw < warehouse_schema.sql

# Load Data
mysql -u root -p fleximart_dw < warehouse_data.sql

# Run Analytics
mysql -u root -p fleximart_dw < analytics_queries.sql
```

## Key Learnings

1.  **ETL Complexity**: Learned how to handle messy raw data (duplicates, missing values) using Pandas before loading it into a relational schema.
2.  **NoSQL vs SQL**: Understood the flexibility of MongoDB for unstructured product attributes compared to the rigid structure of SQL tables.
3.  **Dimensional Modeling**: Gained practical experience in designing a Star Schema (Facts vs Dimensions) to optimize analytical query performance.

## Challenges Faced

1.  **Data Quality Issues**: The raw CSVs contained non-standardized formats (phone numbers, dates).
    -   *Solution*: Implemented robust Python transformation functions in `etl_pipeline.py` to clean and standardize fields.
2.  **Referential Integrity**: ensuring foreign keys matched between Fact and Dimension tables during manual data generation.
    -   *Solution*: Carefully mapped `date_key`, `product_key`, and `customer_key` in the `INSERT` statements to ensure consistency.
