# Part 1: Relational Database & ETL Pipeline

This directory contains the source code and documentation for the ETL (Extract, Transform, Load) process. The goal is to ingest raw CSV transactional data, clean it, and load it into a normalized MySQL relational database.

## 📂 File Structure

| File | Description |
|------|-------------|
| `etl_pipeline.py` | Main Python script that reads CSVs, performs data cleaning, and loads data into MySQL. |
| `business_queries.sql` | SQL queries to validate the data and answer business questions (e.g., top-selling products). |
| `schema_documentation.md` | Detailed documentation of the MySQL database schema, constraints, and relationships. |
| `requirements.txt` | Python dependencies required to run the pipeline. |
| `data_quality_report.txt` | Generated report summarizing data health (records processed, missing values fixed, etc.). |

## 🚀 Setup & Execution

### Prerequisites
1.  **MySQL Server** running locally on port `3306`.
2.  **Database Created**: Ensure a database named `fleximart` exists (or user rights to create/write to it).
    ```sql
    CREATE DATABASE fleximart;
    ```
3.  **Python 3.x** installed.

### Installation
Install the required Python libraries:

```bash
pip install -r requirements.txt
```

### Running the Pipeline
Execute the ETL script to process the data:

```bash
python etl_pipeline.py
```

**What happens?**
-   Raw CSV files (`customers.csv`, `products.csv`, `sales.csv`) are read (assumed to be in root or specified path).
-   Data is cleaned: duplicates removed, dates standardized, missing values handled.
-   Data is loaded into the `fleximart` MySQL database.
-   A `data_quality_report.txt` is generated.

## 📊 Verification
After running the pipeline, you can execute the business questions query to verify the data:

```bash
mysql -u root -p fleximart < business_queries.sql
```
