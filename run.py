"""
Application Entry Point
Main runner for LifeOS application
"""
import os
from dotenv import load_dotenv
from app import create_app, db

# Load environment variables
load_dotenv()

# Create application instance
app = create_app(os.getenv('FLASK_ENV', 'development'))

if __name__ == '__main__':
    with app.app_context():
        # Create tables if they don't exist
        db.create_all()

    # Run the application
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=app.config['DEBUG']
    )

