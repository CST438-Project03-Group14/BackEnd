# test_db.py
import os
from dotenv import load_dotenv
import django
from django.db import connection

# Load environment variables
load_dotenv()

# Setup Django with your project name
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CST438.settings')
django.setup()

def test_connection():
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            print("✅ Database connection successful!")
    except Exception as e:
        print(f"❌ Connection failed: {e}")

if __name__ == "__main__":
    test_connection()