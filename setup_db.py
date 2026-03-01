"""
Database Setup Script
Creates the database and initializes tables
"""
import os
import sys
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import Error

# Load environment variables
load_dotenv()

def create_database():
    """Create the lifeos_dev database"""
    try:
        # Connection parameters
        host = os.getenv('DB_HOST', 'localhost')
        user = os.getenv('DB_USER', 'root')
        password = os.getenv('DB_PASSWORD', 'password')

        # Connect to MySQL server (without specifying database)
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password
        )

        if connection.is_connected():
            print("✅ Connected to MySQL Server")
            cursor = connection.cursor()

            # Create database
            cursor.execute("CREATE DATABASE IF NOT EXISTS lifeos_dev;")
            print("✅ Database 'lifeos_dev' created or already exists")

            cursor.close()
            connection.close()
            return True

    except Error as e:
        print(f"❌ Error connecting to MySQL: {e}")
        print("\n📋 Please ensure:")
        print("  1. MySQL Server is running")
        print("  2. You have the correct username and password")
        print("  3. Check your .env file for DB_HOST, DB_USER, DB_PASSWORD")
        return False

def initialize_app():
    """Initialize Flask app and create tables"""
    try:
        from app import create_app, db

        app = create_app('development')
        with app.app_context():
            print("✅ Flask app created")
            db.create_all()
            print("✅ Database tables created")
        return True
    except Exception as e:
        print(f"❌ Error initializing app: {e}")
        return False

if __name__ == '__main__':
    print("🚀 LifeOS Database Setup\n")

    # Step 1: Create database
    print("Step 1: Creating database...")
    if not create_database():
        sys.exit(1)

    print("\n" + "="*50)
    print("Step 2: Initializing Flask application...")
    if not initialize_app():
        sys.exit(1)

    print("\n" + "="*50)
    print("✅ Database setup complete!")
    print("\n🎉 You can now run: python run.py")

