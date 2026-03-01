#!/usr/bin/env python3
"""
LifeOS Simple Flask Launcher
No debug mode, no reloader - just run the app
"""

if __name__ == '__main__':
    import os
    from dotenv import load_dotenv

    # Load environment
    load_dotenv()
    os.environ['FLASK_ENV'] = 'development'

    # Import and create app
    from app import create_app

    app = create_app('development')

    # Run the server
    print("\n" + "="*70)
    print("  LifeOS Flask Application")
    print("="*70)
    print("  [+] Server starting on http://localhost:5000")
    print("  [+] Open your browser and navigate to http://localhost:5000")
    print("  [+] Press Ctrl+C to stop the server")
    print("="*70 + "\n")

    app.run(
        host='0.0.0.0',
        port=5000,
        debug=False,
        use_reloader=False
    )

