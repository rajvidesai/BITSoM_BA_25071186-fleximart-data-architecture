// // mongodb_operations.js
// Task 2.2 – MongoDB Operations

const { MongoClient } = require("mongodb");
const fs = require("fs");
const path = require("path");
//Setup - Tell the script where the database is
const uri = "mongodb://localhost:27017";
const client = new MongoClient(uri);

async function runOperations() {
  try {
    // Connect to the MongoDB Server
    await client.connect();
    const db = client.db("product_db");
    const products = db.collection("products");

    console.log("Connected to MongoDB");

    // --------------------------------------------------
    // Operation 1: Load Data
    // Import products_catalog.json into 'products' collection
    // --------------------------------------------------
    const count = await products.countDocuments();
    // We read the file and put it into the database if it's empty
    if (count === 0) {
      const filePath = path.join(__dirname, "products_catalog.json");
      const data = fs.readFileSync(filePath, "utf8");
      const productData = JSON.parse(data);

      await products.insertMany(productData);
      console.log("Product data imported successfully.");
    } else {
      console.log("Products already exist. Skipping import.");
    }

    // --------------------------------------------------
    // Operation 2: Basic Query
    // Find Electronics products with price < 50000
    // Return name, price, stock only
    // --------------------------------------------------
    const electronicsUnder50k = await products.find(
      { category: "Electronics", price: { $lt: 50000 } },
      { projection: { _id: 0, name: 1, price: 1, stock: 1 } }
    ).toArray();

    console.log("Electronics under 50000:", electronicsUnder50k);

    // --------------------------------------------------
    // Operation 3: Review Analysis
    // Find products with average rating >= 4.0
    // --------------------------------------------------
    const highRatedProducts = await products.aggregate([
      { $unwind: "$reviews" },
      {
        $group: {
          _id: "$product_id",
          name: { $first: "$name" },
          avg_rating: { $avg: "$reviews.rating" }
        }
      },
      { $match: { avg_rating: { $gte: 4.0 } } }
    ]).toArray();

    console.log("High rated products:", highRatedProducts);

    // --------------------------------------------------
    // Operation 4: Update Operation
    // Add a new review to product ELEC001
    // --------------------------------------------------
    await products.updateOne(
      { product_id: "ELEC001" },
      {
        $push: {
          reviews: {
            user: "U999",
            rating: 4,
            comment: "Good value",
            date: new Date()
          }
        }
      }
    );

    console.log("New review added to ELEC001.");

    // --------------------------------------------------
    // Operation 5: Complex Aggregation
    // Calculate average price by category
    // --------------------------------------------------
    const avgPriceByCategory = await products.aggregate([
      {
        $group: {
          _id: "$category",
          avg_price: { $avg: "$price" },
          product_count: { $sum: 1 }
        }
      },
      { $sort: { avg_price: -1 } }
    ]).toArray();

    console.log("Average price by category:", avgPriceByCategory);

  } catch (error) {
    console.error("Error:", error);
  } finally {
    await client.close();
  }
}

runOperations();
