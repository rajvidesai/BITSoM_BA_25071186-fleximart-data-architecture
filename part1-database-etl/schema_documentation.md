# FlexiMart Database Schema Documentation

---

## Introduction

This document provides a detailed explanation of the FlexiMart database schema designed for storing customer, product, and sales information. The schema is created to support efficient data storage, avoid redundancy, and ensure data integrity. It follows standard database design principles and is normalized up to the Third Normal Form (3NF). This documentation explains the entities, their attributes, relationships, normalization rationale, and sample data representation.

---

## 1. Entity–Relationship Description

### ENTITY: customers

**Purpose:**
The `customers` table stores information about users who register and shop on the FlexiMart platform. Each record represents one unique customer.

**Attributes:**

* `customer_id` (Primary Key): A unique auto-incremented identifier for each customer.
* `first_name`: Stores the customer’s first name.
* `last_name`: Stores the customer’s last name.
* `email`: Stores the customer’s email address. This value is unique and mandatory.
* `phone`: Stores the customer’s contact number in standardized format.
* `city`: Indicates the city in which the customer resides.
* `registration_date`: Stores the date on which the customer registered on the platform.

**Relationships:**

* One customer can place **many orders**.
* This represents a **one-to-many (1:M)** relationship between `customers` and `orders`.

---

### ENTITY: products

**Purpose:**
The `products` table stores details of all products available for sale on FlexiMart.

**Attributes:**

* `product_id` (Primary Key): Unique auto-incremented identifier for each product.
* `product_name`: Name of the product.
* `category`: Category to which the product belongs (e.g., Electronics, Fashion).
* `price`: Selling price of the product.
* `stock_quantity`: Quantity of product currently available in inventory.

**Relationships:**

* One product can be associated with **many order items**.
* This represents a **one-to-many (1:M)** relationship between `products` and `order_items`.

---

### ENTITY: orders

**Purpose:**
The `orders` table stores high-level information about orders placed by customers. Each record represents one order.

**Attributes:**

* `order_id` (Primary Key): Unique auto-incremented identifier for each order.
* `customer_id` (Foreign Key): References `customers.customer_id`, identifying who placed the order.
* `order_date`: Date on which the order was placed.
* `total_amount`: Total monetary value of the order.
* `status`: Current order status such as Pending or Completed.

**Relationships:**

* Each order is placed by **one customer** (many-to-one with customers).
* Each order can contain **multiple order items** (one-to-many with order_items).

---

### ENTITY: order_items

**Purpose:**
The `order_items` table stores detailed line-item information for each order. It resolves the many-to-many relationship between orders and products.

**Attributes:**

* `order_item_id` (Primary Key): Unique auto-incremented identifier for each order item.
* `order_id` (Foreign Key): References `orders.order_id`.
* `product_id` (Foreign Key): References `products.product_id`.
* `quantity`: Number of units of the product ordered.
* `unit_price`: Price of a single unit at the time of purchase.
* `subtotal`: Total cost for the item, calculated as `quantity`× `unit_price`.

**Relationships:**

* Each order item belongs to **one order**.

* Each order item references **one product**.

## 2. Normalization Explanation (Third Normal Form – 3NF)

* The FlexiMart database schema is designed according to the principles of Third Normal Form (3NF) to ensure minimal redundancy and maximum data integrity. First Normal Form (1NF) is satisfied as all tables contain atomic values and no repeating groups. Each column holds a single value, and each record can be uniquely identified using a primary key.

* Second Normal Form (2NF) is achieved because all non-key attributes in each table are fully functionally dependent on the entire primary key. For example, in the order_items table, attributes such as quantity, unit_price, and subtotal depend entirely on the primary key order_item_id and not on a partial key.

* Third Normal Form (3NF) is satisfied because there are no transitive dependencies. In the customers table, customer details such as email, phone, and city depend only on customer_id and not on any other non-key attribute. Similarly, product information is stored only in the products table and not repeated in orders or order_items. Order-related attributes are stored exclusively in the orders table.

* This design avoids update anomalies by ensuring that changes to customer or product data need to be made in only one place. It avoids insertion anomalies by allowing orders and products to be added independently. Deletion anomalies are avoided because removing an order does not delete customer or product information. Hence, the schema fully complies with Third Normal Form (3NF).

## 3. Sample Data Representation
`customers`
| customer_id | first_name | last_name | email                                                   | phone          | city      | registration_date |
| ----------- | ---------- | --------- | ------------------------------------------------------- | -------------- | --------- | ----------------- |
| 1           | Rahul      | Sharma    | [rahul.sharma@gmail.com](mailto:rahul.sharma@gmail.com) | +91-9876543210 | Bangalore | 2023-01-15        |
| 2           | Priya      | Patel     | [priya.patel@yahoo.com](mailto:priya.patel@yahoo.com)   | +91-9988776655 | Mumbai    | 2023-02-20        |

`products`
| product_id | product_name       | category    | price    | stock_quantity |
| ---------- | ------------------ | ----------- | -------- | -------------- |
| 1          | Samsung Galaxy S21 | Electronics | 45999.00 | 150            |
| 2          | Nike Running Shoes | Fashion     | 3499.00  | 80             |


`orders`
| order_id | customer_id | order_date | total_amount | status    |
| -------- | ----------- | ---------- | ------------ | --------- |
| 1        | 1           | 2024-01-15 | 45999.00     | Completed |
| 2        | 2           | 2024-01-16 | 5998.00      | Completed |


`order_items`
| order_item_id | order_id | product_id | quantity | unit_price | subtotal |
| ------------- | -------- | ---------- | -------- | ---------- | -------- |
| 1             | 1        | 1          | 1        | 45999.00   | 45999.00 |
| 2             | 2        | 2          | 2        | 2999.00    | 5998.00  |

