"""Simple app runner"""
import os
os.environ['FLASK_ENV'] = 'development'

from app import create_app, db

app = create_app('development')

if __name__ == '__main__':
    print("Starting LifeOS Flask Server...")
    print("Listening on http://localhost:5000")
    print("Press Ctrl+C to stop")
    app.run(host='0.0.0.0', port=5000, debug=True)

