"""
LifeOS Application Factory
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from config import config

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

def create_app(config_name='development'):
    """
    Application Factory Pattern
    Creates and configures Flask application instance

    Args:
        config_name: Configuration environment (development, production, testing)

    Returns:
        Configured Flask application instance
    """
    app = Flask(__name__)

    # Load configuration
    app.config.from_object(config.get(config_name))

    # Initialize extensions with app
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # Configure login manager
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'

    # Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.user import user_bp
    from app.routes.admin import admin_bp
    from app.routes.api import api_bp
    from app.routes.finance import finance_bp
    from app.routes.grocery import grocery_bp
    from app.routes.health import health_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(finance_bp)
    app.register_blueprint(grocery_bp)
    app.register_blueprint(health_bp)

    # Register main route
    from app.routes.main import main_bp
    app.register_blueprint(main_bp)

    # Context processor for template globals
    @app.context_processor
    def inject_config():
        return {'app_name': 'LifeOS'}

    # Error handlers
    @app.errorhandler(404)
    def not_found(e):
        from flask import render_template
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_error(e):
        from flask import render_template
        db.session.rollback()
        return render_template('errors/500.html'), 500

    # Create database tables
    with app.app_context():
        db.create_all()

    return app

