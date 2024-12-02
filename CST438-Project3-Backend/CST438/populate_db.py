import os
import django
from django.db import connection
from datetime import datetime, date

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CST438.settings')
django.setup()

def execute_sql(query, params=None):
    with connection.cursor() as cursor:
        try:
            cursor.execute(query, params)
            print(f"Successfully executed: {query[:100]}...")
        except Exception as e:
            print(f"Error executing query: {query[:100]}...")
            print(f"Error message: {str(e)}")

def populate_database():
    # Add new books
    book_queries = [
        """
        INSERT INTO book (title, author, description, genre, published_date, available_copies, created_at, updated_at)
        VALUES (
            'Pride and Prejudice',
            'Jane Austen',
            'A romantic novel of manners.',
            'FICTION',
            '1813-01-28',
            5,
            NOW(),
            NOW()
        );
        """,
        """
        INSERT INTO book (title, author, description, genre, published_date, available_copies, created_at, updated_at)
        VALUES (
            'To Kill a Mockingbird',
            'Harper Lee',
            'A story of racial injustice and loss of innocence.',
            'FICTION',
            '1960-07-11',
            3,
            NOW(),
            NOW()
        );
        """
    ]

    # Create shelves for existing users
    shelf_queries = [
        """
        INSERT INTO shelf (user_id, shelf_type, created_at)
        VALUES (1, 'Currently Reading', NOW());
        """,
        """
        INSERT INTO shelf (user_id, shelf_type, created_at)
        VALUES (1, 'Want to Read', NOW());
        """,
        """
        INSERT INTO shelf (user_id, shelf_type, created_at)
        VALUES (2, 'Favorites', NOW());
        """
    ]

    print("Adding new books...")
    for query in book_queries:
        execute_sql(query)

    print("\nCreating shelves...")
    for query in shelf_queries:
        execute_sql(query)

    # Get the latest book IDs and shelf IDs for shelf_book relationships
    print("\nLinking books to shelves...")
    shelf_book_query = """
    INSERT INTO shelf_book (shelf_id, book_id, added_at)
    SELECT 
        s.shelf_id,
        b.book_id,
        NOW()
    FROM shelf s
    CROSS JOIN book b
    WHERE s.user_id = 1 
    AND b.title IN ('Pride and Prejudice', 'To Kill a Mockingbird')
    AND NOT EXISTS (
        SELECT 1 FROM shelf_book sb 
        WHERE sb.shelf_id = s.shelf_id 
        AND sb.book_id = b.book_id
    )
    LIMIT 2;
    """
    execute_sql(shelf_book_query)

def check_data():
    queries = {
        "Books": "SELECT * FROM book ORDER BY book_id",
        "Shelves": "SELECT * FROM shelf ORDER BY shelf_id",
        "Shelf-Book Relationships": """
            SELECT s.shelf_id, u.username, s.shelf_type, b.title
            FROM shelf s
            JOIN user u ON s.user_id = u.user_id
            JOIN shelf_book sb ON s.shelf_id = sb.shelf_id
            JOIN book b ON sb.book_id = b.book_id
            ORDER BY s.shelf_id
        """
    }

    for title, query in queries.items():
        print(f"\n{title}:")
        with connection.cursor() as cursor:
            cursor.execute(query)
            results = cursor.fetchall()
            for row in results:
                print(row)

if __name__ == "__main__":
    print("Populating database with additional data...")
    populate_database()
    print("\nChecking all data...")
    check_data()