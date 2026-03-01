# LifeOS Development Guide

## Setup Instructions

### 1. Prerequisites
- Python 3.9 or higher
- MySQL 8.0 or higher
- Git
- pip or conda

### 2. Local Development Setup

#### Step 1: Clone Repository
```bash
git clone <repository-url>
cd LifeOS
```

#### Step 2: Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

#### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

#### Step 4: Setup Environment Variables
```bash
cp .env.example .env
# Edit .env with your configuration
```

#### Step 5: Setup Database
```bash
# Create database in MySQL
mysql -u root -p
CREATE DATABASE lifeos_dev;
EXIT;

# Run migrations
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

#### Step 6: Run Application
```bash
python run.py
```

Visit `http://localhost:5000` in your browser.

## Docker Setup

### Quick Start with Docker
```bash
docker-compose up --build
```

This will:
1. Start MySQL database on port 3306
2. Start Flask application on port 5000
3. Set up all configurations automatically

### Access Applications
- Web Application: http://localhost:5000
- MySQL: localhost:3306

## Project Structure

```
LifeOS/
├── app/                      # Main application package
│   ├── models/              # Database models
│   ├── routes/              # Route blueprints
│   ├── services/            # Business logic
│   ├── utils/               # Utility functions
│   ├── static/              # Static files (CSS, JS, images)
│   └── templates/           # HTML templates
├── tests/                    # Test suite
├── migrations/              # Database migrations
├── config.py                # Configuration
├── run.py                   # Application entry point
├── requirements.txt         # Python dependencies
├── docker-compose.yml       # Docker configuration
├── Dockerfile              # Docker image definition
└── README.md               # Project README
```

## Testing

### Run Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app

# Run specific test file
pytest tests/test_app.py

# Run with verbose output
pytest -v
```

## Development Workflow

### 1. Feature Branch
```bash
git checkout -b feature/feature-name
```

### 2. Make Changes
- Implement your feature
- Write tests
- Follow coding standards

### 3. Commit and Push
```bash
git add .
git commit -m "Add feature description"
git push origin feature/feature-name
```

### 4. Create Pull Request
- Go to GitHub repository
- Create pull request with description

## Code Standards

### Python Style
- Follow PEP 8
- Use meaningful variable names
- Add docstrings to functions
- Keep functions focused and small

### Git Commits
- Use clear commit messages
- Reference issues when applicable
- Keep commits atomic

### Database Migrations
```bash
# Create new migration
flask db migrate -m "Description"

# Apply migrations
flask db upgrade

# Rollback migration
flask db downgrade
```

## Useful Commands

### Create Admin User
```python
python
>>> from app import create_app, db
>>> from app.models.user import User
>>> app = create_app()
>>> with app.app_context():
...     admin = User(username='admin', email='admin@example.com', is_admin=True)
...     admin.set_password('AdminPassword123')
...     db.session.add(admin)
...     db.session.commit()
```

### Reset Database
```bash
# Drop all tables
flask shell
>>> from app import db
>>> db.drop_all()
>>> db.create_all()
```

## Troubleshooting

### Database Connection Error
1. Check MySQL is running
2. Verify DATABASE_URL in .env
3. Check database credentials

### Port Already in Use
```bash
# Windows - Find and kill process on port 5000
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# macOS/Linux
lsof -ti:5000 | xargs kill -9
```

### Module Import Errors
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

## API Documentation

### Authentication Endpoints
- POST `/auth/register` - Register new user
- POST `/auth/login` - Login user
- GET `/auth/logout` - Logout user

### User Endpoints
- GET `/user/profile` - View profile
- POST `/user/profile/edit` - Edit profile
- GET `/user/settings` - View settings
- POST `/user/change-password` - Change password

### Admin Endpoints
- GET `/admin/dashboard` - Admin dashboard
- GET `/admin/users` - List users
- GET `/admin/user/<id>` - View user details

### API Endpoints
- GET `/api/health` - Health check
- GET `/api/users` - Get all users (admin only)
- GET `/api/user/<id>` - Get user by ID

## Environment Variables

Required:
- `FLASK_ENV` - Environment (development/production/testing)
- `SECRET_KEY` - Session secret key
- `DATABASE_URL` - Database connection string
- `GEMINI_API_KEY` - Google Gemini API key

Optional:
- `MAIL_SERVER` - Email server
- `MAIL_PORT` - Email port
- `DEBUG` - Debug mode

## Contributing

1. Fork the repository
2. Create feature branch
3. Make changes and test
4. Submit pull request
5. Await review

## Support

For issues and questions:
- Create an issue on GitHub
- Contact support@lifeos.com

## License

This project is part of the BCA curriculum.

