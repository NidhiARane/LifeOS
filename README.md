# LifeOS - Comprehensive Life Management System

A web-based intelligent platform that integrates financial tracking, grocery management, nutrition monitoring, habit tracking, and predictive analytics.

## Features

### 🔐 User & System Management Module
- User registration and authentication with secure password hashing
- Session management and user authentication
- Profile management and goal settings
- Admin dashboard for user monitoring
- Account deletion with data cleanup

### 💰 Smart Finance & Grocery Management Module
- Expense tracking and categorization
- Monthly budget monitoring
- Grocery item management
- AI-powered saving suggestions
- Expense prediction using ML

### 🥗 Health, Meal & Habit Management Module
- Meal logging with nutrition details
- Weekly meal planning
- Calorie and protein tracking
- Habit creation and streak tracking
- Goal management

### 🤖 AI Intelligence Module
- Conversational assistant powered by Google Gemini
- Weekly AI-generated reports
- Financial and health insights
- Chat history management
- ML models for predictions

### 📊 Analytics & Dashboard Module
- Financial and health statistics
- Interactive charts using Chart.js
- Unique Life Score calculation
- Visual analytics and insights

## Technology Stack

### Backend
- Python
- Flask
- SQLAlchemy ORM
- REST APIs

### Frontend
- HTML5
- CSS3
- Bootstrap 5
- JavaScript (Vanilla & Chart.js)

### Database
- MySQL

### AI/ML
- Google Gemini API
- Pandas
- Scikit-learn

### DevOps
- Docker
- Git
- Render (Deployment)

## Project Structure

```
LifeOS/
├── app/
│   ├── __init__.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── expense.py
│   │   ├── meal.py
│   │   ├── habit.py
│   │   └── goal.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── user.py
│   │   ├── admin.py
│   │   ├── finance.py
│   │   ├── health.py
│   │   └── api.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── user_service.py
│   │   ├── finance_service.py
│   │   ├── ai_service.py
│   │   └── ml_service.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── decorators.py
│   │   ├── validators.py
│   │   └── helpers.py
│   ├── static/
│   │   ├── css/
│   │   ├── js/
│   │   └── images/
│   └── templates/
│       ├── base.html
│       ├── auth/
│       ├── dashboard/
│       ├── user/
│       └── admin/
├── tests/
├── migrations/
├── config.py
├── run.py
├── requirements.txt
├── .env
├── .env.example
├── Dockerfile
├── docker-compose.yml
└── README.md
```

## Installation & Setup

### Prerequisites
- Python 3.9+
- MySQL 8.0+
- Docker (optional)

### Local Setup

1. Clone the repository
```bash
git clone <repository-url>
cd LifeOS
```

2. Create virtual environment
```bash
python -m venv venv
source venv/Scripts/activate  # Windows
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Configure environment
```bash
cp .env.example .env
# Update .env with your configurations
```

5. Initialize database
```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

6. Run the application
```bash
python run.py
```

Visit `http://localhost:5000` in your browser.

## Docker Setup

```bash
docker-compose up --build
```

## API Documentation

API endpoints are available at `/api/` route.

## Contributing

Please follow the coding standards and create feature branches for new features.

## License

This project is part of the BCA curriculum.
