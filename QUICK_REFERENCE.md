# LifeOS - Quick Reference Guide

## 🚀 Quick Start (Choose One)

### Option 1: Local Development (Recommended for Development)
```bash
# 1. Activate virtual environment
cd E:\WebBasedProjects\Life\ OS\ -\ BCA\ Project\LifeOS
python -m venv venv
venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Create MySQL database
mysql -u root -p
CREATE DATABASE lifeos_dev;
EXIT;

# 4. Run application
python run.py

# 5. Open browser
http://localhost:5000
```

### Option 2: Docker (Recommended for Production)
```bash
cd E:\WebBasedProjects\Life\ OS\ -\ BCA\ Project\LifeOS
docker-compose up --build
http://localhost:5000
```

---

## 📝 Default Routes

### Public Routes
| Route | Purpose |
|-------|---------|
| `/` | Home page |
| `/auth/register` | User registration |
| `/auth/login` | User login |
| `/auth/forgot-password` | Forgot password |
| `/about` | About page |
| `/contact` | Contact page |

### Authenticated User Routes
| Route | Purpose |
|-------|---------|
| `/dashboard` | User dashboard |
| `/user/profile` | View profile |
| `/user/profile/edit` | Edit profile |
| `/user/settings` | Account settings |
| `/user/change-password` | Change password |
| `/user/delete-account` | Delete account |
| `/auth/logout` | Logout |

### Admin Routes
| Route | Purpose |
|-------|---------|
| `/admin/dashboard` | Admin dashboard |
| `/admin/users` | Manage users |
| `/admin/user/<id>` | View user details |

### API Routes
| Method | Route | Purpose |
|--------|-------|---------|
| GET | `/api/health` | Health check |
| GET | `/api/users` | List users |
| GET | `/api/user/<id>` | Get user |

---

## 🔑 Test Credentials (After Setup)

Create test user via Python shell:
```python
python
>>> from app import create_app, db
>>> from app.models.user import User
>>> app = create_app()
>>> with app.app_context():
...     user = User(username='demo', email='demo@example.com')
...     user.set_password('Demo@123456')
...     db.session.add(user)
...     db.session.commit()
...     print("User created!")
```

Login with:
- **Username**: `demo`
- **Password**: `Demo@123456`

---

## 📁 Important Files

| File | Purpose |
|------|---------|
| `run.py` | Start application here |
| `config.py` | Configuration settings |
| `.env` | Environment variables |
| `requirements.txt` | Python dependencies |
| `app/__init__.py` | App factory |
| `app/models/` | Database models |
| `app/routes/` | Route handlers |
| `app/templates/` | HTML templates |
| `app/static/` | CSS, JS, images |

---

## 🛠️ Common Commands

### Development
```bash
# Start app
python run.py

# Access Python shell
flask shell

# Run tests
pytest

# Check code coverage
pytest --cov=app
```

### Database
```bash
# Create migrations
flask db migrate -m "Description"

# Apply migrations
flask db upgrade

# Rollback
flask db downgrade

# Reset database
flask shell
>>> from app import db
>>> db.drop_all()
>>> db.create_all()
```

### Docker
```bash
# Start services
docker-compose up

# Stop services
docker-compose down

# View logs
docker-compose logs -f

# Access database
docker exec -it lifeos_mysql mysql -u lifeos_user -p lifeos_dev
```

---

## 🔐 Password Requirements

Passwords must have:
- **Minimum 8 characters**
- **At least 1 uppercase letter** (A-Z)
- **At least 1 lowercase letter** (a-z)
- **At least 1 number** (0-9)

Example: `MyPassword123` ✅

---

## 🎨 UI Features

- **Gradient Color Scheme**: Purple (#667eea) to Pink (#764ba2)
- **Bootstrap 5**: Responsive grid system
- **Font Awesome**: 6000+ icons
- **Chart.js**: Ready for analytics
- **Smooth Animations**: Hover effects and transitions
- **Dark Mode Ready**: CSS variables for theming

---

## 📊 Database Models

```
User
├── id (Primary Key)
├── username (Unique)
├── email (Unique)
├── password_hash
├── first_name, last_name
├── phone, location
├── monthly_budget
├── weight_goal, savings_goal
├── daily_calorie_goal, daily_protein_goal
├── is_active, is_admin
└── timestamps (created_at, updated_at, last_login)

ExpenseCategory
├── id (Primary Key)
├── name (Unique)
└── color, icon

Expense
├── id (Primary Key)
├── user_id (Foreign Key)
├── category_id (Foreign Key)
├── amount, currency
└── timestamps

Meal
├── id (Primary Key)
├── user_id (Foreign Key)
├── calories, protein, carbs, fat
└── meal_date

Habit
├── id (Primary Key)
├── user_id (Foreign Key)
├── frequency, current_streak
└── is_active

Goal
├── id (Primary Key)
├── user_id (Foreign Key)
├── target_value, current_value
└── progress tracking

GroceryItem
├── id (Primary Key)
├── user_id (Foreign Key)
├── quantity, price
└── is_purchased
```

---

## 🔄 File Organization

```
LifeOS/
├── Backend Logic
│   ├── app/routes/auth.py         ← Login/Register
│   ├── app/routes/user.py         ← User management
│   ├── app/routes/admin.py        ← Admin dashboard
│   ├── app/models/user.py         ← User model
│   └── app/utils/                 ← Helpers & validators
│
├── Frontend
│   ├── app/templates/auth/        ← Auth pages
│   ├── app/templates/user/        ← User pages
│   ├── app/templates/admin/       ← Admin pages
│   ├── app/static/css/            ← Styling
│   └── app/static/js/             ← JavaScript
│
├── Configuration
│   ├── config.py                  ← Environment config
│   ├── .env                       ← Secrets
│   └── requirements.txt           ← Dependencies
│
└── Deployment
    ├── Dockerfile                 ← Docker image
    └── docker-compose.yml         ← Docker setup
```

---

## 🐛 Troubleshooting

### MySQL Connection Error
```
Solution:
1. Check MySQL is running
2. Verify DATABASE_URL in .env
3. Check username/password in .env
```

### Port Already in Use
```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# macOS/Linux
lsof -ti:5000 | xargs kill -9
```

### Module Import Error
```bash
pip install -r requirements.txt --force-reinstall
```

### Database Locked
```bash
flask shell
>>> from app import db
>>> db.session.rollback()
```

---

## 📚 Documentation Files

- **README.md** - Project overview
- **DEVELOPMENT.md** - Development setup guide
- **PROJECT_STATUS.md** - Module completion status
- **QUICK_REFERENCE.md** - This file!

---

## 🎯 Module 1 Checklist

- ✅ User registration with validation
- ✅ Secure login system
- ✅ User profile management
- ✅ Password change functionality
- ✅ Account deletion
- ✅ Admin dashboard
- ✅ User management system
- ✅ Beautiful responsive UI
- ✅ Database models
- ✅ API endpoints
- ✅ Error handling
- ✅ Testing setup

---

## 🚀 Ready for Next Module?

Module 1 is complete! Next modules:
- **Module 2**: Finance & Grocery Management 💰
- **Module 3**: Health & Habit Management 🥗
- **Module 4**: AI Intelligence 🤖
- **Module 5**: Analytics Dashboard 📊

---

## 📞 Support

For issues:
1. Check PROJECT_STATUS.md
2. Review DEVELOPMENT.md
3. Check Troubleshooting section above
4. Review code comments

**Happy coding! 🎉**

