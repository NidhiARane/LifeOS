"""App runner with logging to file"""
import os
import sys

# Redirect output to file
output_file = open('app_startup.log', 'w', buffering=1)
sys.stdout = output_file
sys.stderr = output_file

print("=" * 60)
print("LifeOS Flask Application Startup")
print("=" * 60)

try:
    print("\n[1] Setting environment...")
    os.environ['FLASK_ENV'] = 'development'
    print("✓ Environment set")

    print("\n[2] Importing Flask app...")
    from app import create_app, db
    print("✓ Imports successful")

    print("\n[3] Creating Flask app instance...")
    app = create_app('development')
    print("✓ App instance created")

    print("\n[4] Starting server...")
    print("=" * 60)
    print("✓ Server is starting on http://localhost:5000")
    print("=" * 60)
    output_file.flush()

    # Start the server
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)

except Exception as e:
    print(f"\n✗ ERROR: {e}")
    import traceback
    traceback.print_exc()
    output_file.close()
    sys.exit(1)

