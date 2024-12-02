# test_db.py
import os
from dotenv import load_dotenv
import django
from django.db import connection
import logging
import mysql.connector
from django.conf import settings

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)
import os
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import Error

def test_connection():
    load_dotenv()
    
    config = {
        'host': os.getenv('DB_HOST'),
        'user': os.getenv('DB_USER'),
        'password': os.getenv('DB_PASSWORD'),
        'database': os.getenv('DB_NAME')
    }
    
    try:
        print("Trying to connect to the database...")
        print(f"Host: {config['host']}")
        print(f"Database: {config['database']}")
        print(f"User: {config['user']}")
        
        connection = mysql.connector.connect(**config)
        
        if connection.is_connected():
            db_info = connection.get_server_info()
            print(f"Successfully connected to MySQL database. MySQL Server version: {db_info}")
            
            cursor = connection.cursor()
            cursor.execute("select database();")
            record = cursor.fetchone()
            print(f"Connected to database: {record[0]}")
            
    except Error as e:
        print(f"Error connecting to MySQL database: {e}")
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed.")

if __name__ == "__main__":
    test_connection()
# Load environment variables
load_dotenv()

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CST438.settings')
django.setup()

def print_separator():
    print("\n" + "="*50 + "\n")

def test_connection():
    print_separator()
    print("🔍 STARTING DATABASE DIAGNOSTICS")
    print_separator()

    # 1. Environment Variables Check
    print("📋 ENVIRONMENT VARIABLES CHECK:")
    print(f"DB_NAME: {os.getenv('DB_NAME', 'Not set')}")
    print(f"DB_USER: {os.getenv('DB_USER', 'Not set')}")
    print(f"DB_HOST: {os.getenv('DB_HOST', 'Not set')}")
    print(f"DB_PORT: {os.getenv('DB_PORT', 'Not set')}")
    print("DB_PASSWORD: {'Set' if os.getenv('DB_PASSWORD') else 'Not set'}")

    print_separator()
    
    # 2. Django Settings Check
    print("⚙️ DJANGO DATABASE SETTINGS:")
    db_settings = settings.DATABASES['default']
    print(f"ENGINE: {db_settings['ENGINE']}")
    print(f"NAME: {db_settings['NAME']}")
    print(f"USER: {db_settings['USER']}")
    print(f"HOST: {db_settings['HOST']}")
    print(f"PORT: {db_settings['PORT']}")

    print_separator()

    # 3. Connection Test
    print("🔌 TESTING DATABASE CONNECTION:")
    try:
        # Test Django connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            print("✅ Django database connection successful!")

            # Get MySQL version
            cursor.execute("SELECT VERSION()")
            version = cursor.fetchone()
            print(f"📊 MySQL Version: {version[0]}")

            # List all tables
            print("\n📑 AVAILABLE TABLES:")
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            if tables:
                for table in tables:
                    print(f"  - {table[0]}")
                    # Get table details
                    cursor.execute(f"DESCRIBE {table[0]}")
                    columns = cursor.fetchall()
                    for column in columns:
                        print(f"    └─ {column[0]} ({column[1]})")
            else:
                print("  No tables found in the database")

    except Exception as e:
        print("❌ Connection failed!")
        print(f"Error details: {str(e)}")
        print("\n🔍 Troubleshooting tips:")
        print("1. Check if MySQL server is running")
        print("2. Verify your .env file settings")
        print("3. Ensure MySQL user has correct permissions")
        print("4. Check if the database exists")

    print_separator()

if __name__ == "__main__":
    test_connection()