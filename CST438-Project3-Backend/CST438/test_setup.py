import os
import django
import logging
from django.core.management import execute_from_command_line
from django.apps import apps

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_django_setup():
    logger.info("Starting Django setup test")
    
    try:
        # Check Django setup
        logger.info("Checking Django configuration...")
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CST438.settings')
        django.setup()
        logger.info("✅ Django setup successful")
        
        # Check installed apps
        logger.info("\nChecking installed apps...")
        installed_apps = apps.get_app_configs()
        for app in installed_apps:
            logger.info(f"Found app: {app.name}")
            
        # Check if 'api' app is installed
        if apps.is_installed('api'):
            logger.info("✅ API app is properly installed")
        else:
            logger.error("❌ API app is not installed")
            
        # Check migrations
        logger.info("\nChecking migrations...")
        execute_from_command_line(['manage.py', 'showmigrations'])
        
        # Check database connection
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            logger.info("✅ Database connection successful")
            
            # List all tables
            cursor.execute("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = DATABASE()
            """)
            tables = cursor.fetchall()
            logger.info("\nAvailable database tables:")
            for table in tables:
                logger.info(f"- {table[0]}")
                
    except Exception as e:
        logger.error(f"❌ Setup test failed: {str(e)}")
        raise

if __name__ == "__main__":
    test_django_setup()