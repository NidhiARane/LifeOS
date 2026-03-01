#!/usr/bin/env python
"""
Debug script to test app startup
"""
import sys
import os

print("=" * 60)
print("LifeOS App Startup Debug")
print("=" * 60)

# Step 1: Check Python version
print(f"\n✓ Python version: {sys.version}")
print(f"✓ Python path: {sys.executable}")

# Step 2: Check current directory
print(f"\n✓ Current directory: {os.getcwd()}")
print(f"✓ Config.py exists: {os.path.exists('config.py')}")

# Step 3: Load environment variables
print("\n--- Loading environment variables ---")
from dotenv import load_dotenv
load_dotenv()
database_url = os.getenv('DATABASE_URL')
print(f"✓ DATABASE_URL: {database_url}")

# Step 4: Check config
print("\n--- Loading config ---")
from config import config, DevelopmentConfig
print(f"✓ Config loaded")
dev_config = DevelopmentConfig()
print(f"✓ Development config DB URI: {dev_config.SQLALCHEMY_DATABASE_URI}")

# Step 5: Import app factory
print("\n--- Importing app factory ---")
from app import create_app, db
print(f"✓ App factory imported")

# Step 6: Create app instance
print("\n--- Creating app instance ---")
try:
    app = create_app('development')
    print(f"✓ App created successfully")
except Exception as e:
    print(f"✗ Error creating app: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Step 7: Check database
print("\n--- Checking database ---")
with app.app_context():
    try:
        # Test connection
        from sqlalchemy import text
        db.session.execute(text('SELECT 1'))
        print(f"✓ Database connection successful")
        print(f"✓ Tables created")
    except Exception as e:
        print(f"✗ Database error: {e}")
        import traceback
        traceback.print_exc()

print("\n" + "=" * 60)
print("✓ App is ready to run!")
print("=" * 60)
print("\nStart the app with: python run.py")

