## Task 3.1 – Star Schema Design Documentation

Your goal is to **explain** (not code) how FlexiMart’s **data warehouse** is structured and **why** it’s designed that way.

**Design Justification: Star Schema Implementation**

The data warehouse for FlexiMart has been designed using a star schema, which is a widely adopted dimensional modeling approach for analytical and reporting systems. The star schema was chosen because it provides simplicity, high query performance, and ease of understanding, making it suitable for sales analysis.

**Choice of Star Schema**

The star schema consists of a central fact table (fact_sales) connected to multiple dimension tables (dim_date, dim_product, dim_customer). This structure allows business users to analyze sales data efficiently across multiple perspectives such as time, product, and customer.

The design minimizes table joins and simplifies query logic, which is especially important for analytical workloads involving aggregations like total sales, monthly revenue, or customer-wise purchasing patterns.

A **star schema** has:

* **One fact table** → stores numbers you analyze (sales amounts, quantities)[What happened]
* **Multiple dimension tables** → give context (date, product, customer)[Who, What, When, Where]

Dimension Table Design Justification
1. dim_date

The dim_date table stores all time-related attributes in a single table, including day, month, quarter, year, and weekend indicator.
This design enables flexible time-based analysis such as:

Weekday vs weekend sales comparison

Monthly and quarterly trends

Yearly performance reporting

Using a surrogate key (date_key) improves performance and ensures consistency when joining with the fact table.

2. dim_product

The dim_product table contains descriptive attributes such as product name, category, subcategory, and unit price.
Separating product information into a dimension table avoids data redundancy and allows:

Category-wise and subcategory-wise sales analysis

Easy addition of new products without affecting historical sales data

The use of an auto-increment surrogate key (product_key) ensures efficient joins and supports future changes in product attributes.

3. dim_customer

The dim_customer table stores customer-related details including city, state, and customer segment.
This design supports customer-focused analytics such as:

City-wise and state-wise sales distribution

Segment-based analysis (Retail, Corporate, Online, etc.)

Using a surrogate key (customer_key) ensures stable references even if customer details change over time.

# Star Schema Design for FlexiMart

## Section 1: Schema Overview

### FACT TABLE: `fact_sales`

**Grain:**
One row per **product per order line item**
This means if one order has 3 products, there will be **3 rows**.

**Business Process:**
Sales transactions

### Measures (Numeric Facts)

* `quantity_sold` – Number of units sold
* `unit_price` – Price per unit at the time of sale
* `discount_amount` – Discount applied on the sale
* `total_amount` – Final sale amount
  *(quantity_sold × unit_price − discount_amount)*

### Foreign Keys

* `date_key` → `dim_date`
* `product_key` → `dim_product`
* `customer_key` → `dim_customer`

---

### DIMENSION TABLE: `dim_date`

**Purpose:**
Used for time-based analysis (daily, monthly, yearly trends)

**Type:**
Conformed dimension (shared across reports)

**Attributes:**

* `date_key` (PK): Surrogate key (YYYYMMDD)
* `full_date`: Actual calendar date
* `day_of_week`: Monday, Tuesday, etc.
* `month`: 1–12
* `month_name`: January, February, etc.
* `quarter`: Q1, Q2, Q3, Q4
* `year`: 2023, 2024, etc.
* `is_weekend`: True/False

---

### DIMENSION TABLE: `dim_product`

**Purpose:**
Stores product-related details

**Attributes:**

* `product_key` (PK): Surrogate key
* `product_name`: Laptop, Mobile, etc.
* `category`: Electronics, Grocery, Clothing
* `brand`: Dell, Samsung, Apple
* `unit_cost`: Cost price of the product

---

### DIMENSION TABLE: `dim_customer`

**Purpose:**
Stores customer information for customer-based analysis

**Attributes:**

* `customer_key` (PK): Surrogate key
* `customer_name`: Full name of customer
* `gender`: Male/Female/Other
* `city`: Mumbai, Delhi, etc.
* `state`: Maharashtra, Karnataka
* `customer_type`: Regular, Premium

---

## Section 2: Design Decisions (≈150 words)

### Why this granularity?

The grain is set at **transaction line-item level** so that FlexiMart can analyze sales at the most detailed level. This allows accurate tracking of individual product performance, discounts, and quantities sold per order. Higher-level summaries (daily, monthly, yearly) can always be derived from detailed data.

### Why surrogate keys?

Surrogate keys are used instead of natural keys because they:

* Improve query performance
* Avoid issues when business data changes (e.g., customer name or product code)
* Make joins simpler and more efficient

### How this supports drill-down and roll-up?

The design allows:

* **Drill-down:** Year → Quarter → Month → Day
* **Roll-up:** Product → Category → Brand
  This flexibility helps analysts view sales at different levels without changing the schema.

---

## Section 3: Sample Data Flow

### Source Transaction

Order #101
Customer: John Doe
Product: Laptop
Quantity: 2
Price: 50,000

---

### Data Warehouse Representation

**fact_sales**

```
date_key: 20240115
product_key: 5
customer_key: 12
quantity_sold: 2
unit_price: 50000
discount_amount: 0
total_amount: 100000
```

**dim_date**

```
date_key: 20240115
full_date: 2024-01-15
month: 1
month_name: January
quarter: Q1
year: 2024
is_weekend: false
```

**dim_product**

```
product_key: 5
product_name: Laptop
category: Electronics
brand: Dell
```

**dim_customer**

```
customer_key: 12
customer_name: John Doe
city: Mumbai
state: Maharashtra
customer_type: Regular
```

---


