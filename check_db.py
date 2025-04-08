#!/usr/bin/env python
"""
Simple script to check database connection and table existence.
"""
import os
import sys
import django
from django.db import connection
from django.db.utils import OperationalError

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djCMS.settings')
django.setup()

def check_database_connection():
    """Check if we can connect to the database."""
    try:
        connection.ensure_connection()
        print("✅ Database connection successful")
        return True
    except OperationalError as e:
        print(f"❌ Database connection failed: {e}")
        return False

def check_tables_exist():
    """Check if the required database tables exist."""
    required_tables = [
        'core_user',
        'pages_page',
        'blog_post',
        'categories_category',
        'navigation_menu',
        'theming_theme',
        'widgets_widgetarea'
    ]
    
    existing_tables = connection.introspection.table_names()
    print(f"Found {len(existing_tables)} tables in the database")
    
    missing_tables = [table for table in required_tables if table not in existing_tables]
    
    if missing_tables:
        print(f"❌ Missing tables: {', '.join(missing_tables)}")
        return False
    else:
        print("✅ All required tables exist")
        return True

def main():
    """Main function."""
    print("Checking database connection...")
    if not check_database_connection():
        sys.exit(1)
    
    print("\nChecking database tables...")
    if not check_tables_exist():
        print("\nSome required tables are missing. You may need to run migrations:")
        print("python manage.py migrate")
        sys.exit(1)
    
    print("\n✅ Database check completed successfully")

if __name__ == '__main__':
    main()