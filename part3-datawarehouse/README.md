# Part 3: Data Warehouse & Analytics

This directory focuses on the OLAP (Online Analytical Processing) component. We implement a **Star Schema** to enable efficient reporting and historical analysis of sales data.

## 📂 File Structure

| File | Description |
|------|-------------|
| `star_schema_design.md` | Design document explaining the choice of Schema, Granularity, and Dimension attributes. |
| `warehouse_schema.sql` | SQL script to create the `fleximart_dw` database and its Star Schema tables (`fact_sales`, dimensions). |
| `warehouse_data.sql` | SQL script illustrating data population with sample datasets for Dimensions and Facts. |
| `analytics_queries.sql` | Complex SQL queries for OLAP analysis (Drill-downs, Window Functions, Segmentation). |
| `setup_schema.py` | (Optional) Python helper script to execute the schema creation. |

## 🚀 Setup & Execution

### Prerequisites
1.  **MySQL Server** active.
2.  **Database Access**: Ability to create `fleximart_dw`.

### 1. Create Schema
Run the schema creation script to set up the tables:

```bash
mysql -u root -p < warehouse_schema.sql
```
*Note: This creates the `fleximart_dw` database and tables: `dim_date`, `dim_product`, `dim_customer`, `fact_sales`.*

### 2. Load Data
Populate the warehouse with the sample data:

```bash
mysql -u root -p fleximart_dw < warehouse_data.sql
```

### 3. Run Analytics
Execute the analytical queries to derive insights:

```bash
mysql -u root -p fleximart_dw < analytics_queries.sql
```

## 📈 Analytics implemented

1.  **Monthly Sales Drill-Down**: Analyzes sales hierarchy from Year → Quarter → Month.
2.  **Product Performance**: Uses Window Functions to calculate revenue contribution percentages for top products.
3.  **Customer Segmentation**: Segments customers into High/Medium/Low value tiers based on total spending.
