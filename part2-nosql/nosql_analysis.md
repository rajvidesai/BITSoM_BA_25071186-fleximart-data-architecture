# NoSQL Database Analysis – MongoDB

---

## `Section A: Limitations of RDBMS`

**Rigid Schema Structure:**  
Relational Database Management Systems (RDBMS) such as MySQL enforce a fixed schema, meaning every record in a table must follow the same structure. In the FlexiMart product catalog, products can have highly diverse attributes. For example, laptops require specifications like RAM, processor, and storage, while shoes require attributes such as size, color, and material. Representing all these attributes in a single table leads to sparse tables filled with NULL values, which wastes storage and complicates queries.

**Complex Data Modeling for Variability:**  
To handle product diversity, RDBMS often require advanced modeling techniques such as the Entity-Attribute-Value (EAV) model or multiple subtype tables. These approaches increase query complexity, reduce performance, and make data validation difficult, especially as the number of product types grows.

**Difficulty in Schema Evolution:**  
Whenever FlexiMart introduces a new product type with unique attributes, the database schema must be modified using `ALTER TABLE` commands. In large systems, frequent schema changes can cause table locks, downtime, and require code changes across applications, making the system inflexible and costly to maintain.

**Inefficiency with Nested Data:**  
Customer reviews typically contain nested data such as ratings, comments, timestamps, and user details. RDBMS are designed for flat data structures, so storing reviews requires multiple tables and joins, which increases query complexity and reduces performance.

---

## `Section B: Benefits of NoSQL (MongoDB)`

**Flexible Schema Design:**  
MongoDB uses a document-oriented, schema-less model that allows each product document to store only the attributes relevant to that product. For example, laptop documents can include RAM and processor fields, while shoe documents can include size and color. This flexibility makes MongoDB ideal for handling diverse and evolving product catalogs without schema redesign.

**Support for Embedded Documents:**  
MongoDB allows related data to be stored as embedded documents. Customer reviews can be stored directly inside product documents, including ratings, comments, timestamps, and reviewer details. This eliminates the need for joins and enables faster data retrieval with simpler queries.

**Ease of Schema Evolution:**  
New product attributes or categories can be added without modifying existing documents or database structure. This allows FlexiMart to adapt quickly to changing business requirements without downtime or complex migrations.

**Horizontal Scalability:**  
MongoDB supports horizontal scaling through sharding, allowing data to be distributed across multiple servers. This makes it suitable for handling large volumes of product data, reviews, and increasing user traffic as FlexiMart grows.

---

## `Section C: Trade-offs of Using MongoDB`

**Lack of Enforced Relationships:**  
MongoDB does not enforce foreign key constraints like relational databases. While this provides flexibility, it shifts the responsibility of maintaining data integrity to the application layer, increasing the risk of inconsistent or orphaned data if not handled properly.

**Weaker Support for Complex Transactions:**  
Although MongoDB supports transactions, relational databases such as MySQL are more mature and reliable for complex, multi-table ACID transactions. Operations such as financial reporting and order processing are generally easier and safer to manage in an RDBMS.

**Data Redundancy Risks:**  
The use of embedded documents can lead to data duplication, especially when the same information is stored across multiple documents. This may increase storage usage and make updates more complex if not carefully designed.

---

## `Conclusion`

MongoDB is well-suited for managing FlexiMart’s diverse and evolving product catalog due to its flexible schema, embedded document support, and scalability. However, relational databases remain better suited for transactional and highly structured data. A hybrid approach using both technologies can provide the most effective solution.
