# Part 2: NoSQL Operations (MongoDB)

This directory contains scripts and data for the NoSQL component of the FlexiMart architecture. We use MongoDB to handle the flexible, document-oriented nature of the product catalog, which allows for varying product attributes and nested reviews.

## 📂 File Structure

| File | Description |
|------|-------------|
| `mongodb_operations.js | Node.js script that seeds the database and performs CRUD/Aggregation operations. |
| `products_catalog.json` | JSON dataset containing product documents with nested specifications and reviews. |
| `nosql_analysis.md` | In-depth analysis comparing SQL vs NoSQL for this specific use case, including schema design decisions. |
| `package.json` | Defines the project dependencies (specifically the `mongodb` driver). |

## 🚀 Setup & Execution

### Prerequisites
1.  **MongoDB Server** running locally on port `27017`.
2.  **Node.js** installed.

### Installation
Install the MongoDB driver for Node.js:

```bash
npm install
```

### Running the Operations
Execute the script:

```bash
node mongodb_operations.js
```

**What happens?**
1.  **Auto-Seeding**: The script checks if the `product_db.products` collection is empty. If so, it loads data from `products_catalog.json`.
2.  **Operations Executed**:
    -   **Find**: Retrieves high-value electronics.
    -   **Aggregation**: Calculates average product ratings and identifies top-rated items.
    -   **Update**: Adds a new user review to a specific product.
    -   **Complex Aggregation**: Computes average price per product category.
    -   **Formatting**: Transforms a document into a specific JSON output format as required.

## 📊 Key Features
-   **Schema Flexibility**: Handles diverse product specifications (e.g., screen size for TVs vs expiry date for groceries) without null columns.
-   **Nested Data**: Reviews are stored directly within the product document for faster read performance.
