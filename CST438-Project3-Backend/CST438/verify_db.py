import os
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import Error

def verify_env():
    load_dotenv()
    
    # Print environment variables (excluding password)
    print("\nEnvironment Variables:")
    print(f"DB_NAME: {os.environ.get('DB_NAME')}")
    print(f"DB_USER: {os.environ.get('DB_USER')}")
    print(f"DB_HOST: {os.environ.get('DB_HOST')}")
    print(f"DB_PORT: {os.environ.get('DB_PORT')}")
    print(f"DB_PASSWORD is {'set' if os.environ.get('DB_PASSWORD') else 'not set'}")

def test_connection():
    try:
        print("\nTesting MySQL Connection...")
        conn = mysql.connector.connect(
            host=os.environ.get('DB_HOST'),
            user=os.environ.get('DB_USER'),
            password=os.environ.get('DB_PASSWORD'),
            database=os.environ.get('DB_NAME')
        )
        
        if conn.is_connected():
            print("✅ Successfully connected to database!")
            cursor = conn.cursor()
            cursor.execute("SHOW TABLES;")
            tables = cursor.fetchall()
            print("\nAvailable Tables:")
            for table in tables:
                print(f"- {table[0]}")
    except Error as e:
        print(f"❌ Error: {e}")
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()
            print("\nConnection closed.")

if __name__ == "__main__":
    verify_env()
    test_connection()