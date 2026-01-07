import mysql.connector
import os

# DB Configuration
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "root123",
}

def run_schema_script():
    try:
        # Connect to MySQL Server (no db yet)
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        print("Connected to MySQL Server")

        # Create Database
        cursor.execute("CREATE DATABASE IF NOT EXISTS fleximart_dw")
        print("Database 'fleximart_dw' created/exists")
        
        # Select Database
        cursor.execute("USE fleximart_dw")
        
        # Read SQL Script
        script_path = "warehouse_schema.sql"
        if not os.path.exists(script_path):
            print(f"Error: {script_path} not found")
            return

        with open(script_path, "r") as f:
            sql_script = f.read()

        # Split and Execute Statements
        # Simple splitting by semicolon for this specific file format
        statements = sql_script.split(";")
        
        for statement in statements:
            if statement.strip():
                try:
                    cursor.execute(statement)
                    print("Executed statement successfully")
                except mysql.connector.Error as err:
                    # Ignore "Table already exists" or empty line errors if benign
                    print(f"Statement execution: {err}")

        conn.commit()
        print("Schema script execution completed successfully.")

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()
            print("MySQL connection closed")

if __name__ == "__main__":
    run_schema_script()
