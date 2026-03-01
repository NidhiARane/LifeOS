# LifeOS Architecture Overview

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     CLIENT LAYER (Frontend)                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  HTML5 Templates          Bootstrap 5         JavaScript        │
│  ├─ Register Page    ├─ Responsive Grid  ├─ Form Validation    │
│  ├─ Login Page       ├─ Card Components  ├─ API Calls          │
│  ├─ Dashboard        ├─ Navigation       ├─ Dynamic UI          │
│  ├─ User Profile     ├─ Forms            └─ User Interactions   │
│  ├─ Admin Dashboard  └─ Tables                                  │
│  └─ Settings Page                                               │
│                                                                   │
│                          Static Assets                           │
│                    CSS (Style.css) + Icons                       │
│                                                                   │
└────────────────────────────┬──────────────────────────────────────┘
                             │
                    HTTP Requests & Responses
                             │
┌────────────────────────────▼──────────────────────────────────────┐
│                    ROUTE LAYER (Flask Blueprints)                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  auth_bp/          user_bp/          admin_bp/      api_bp/     │
│  ├─ /register      ├─ /profile       ├─ /dashboard  ├─ /health  │
│  ├─ /login         ├─ /settings      ├─ /users      ├─ /users   │
│  ├─ /logout        ├─ /edit-profile  └─ /user/<id>  └─ /user/<id>│
│  └─ /forgot-pwd    └─ /change-pwd                                │
│                                                                   │
│                        main_bp/                                  │
│                   ├─ / (Home)                                    │
│                   ├─ /dashboard                                  │
│                   ├─ /about                                      │
│                   └─ /contact                                    │
│                                                                   │
└────────────────────────────┬──────────────────────────────────────┘
                             │
                   Flask Request Handlers
                             │
┌────────────────────────────▼──────────────────────────────────────┐
│                  SERVICE LAYER (Business Logic)                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  user_service.py       finance_service.py    ai_service.py      │
│  ├─ Register User      ├─ Track Expense      ├─ Get AI Insights │
│  ├─ Authenticate       ├─ Calculate Budget   ├─ Generate Report │
│  ├─ Update Profile     └─ Predict Spending   └─ Chat Integration│
│  ├─ Validate Input                                               │
│  └─ Password Mgmt      ml_service.py                             │
│                        ├─ Predict Trends                         │
│  decorators.py         ├─ Analyze Habits                         │
│  ├─ @login_required    └─ Calculate Scores                       │
│  ├─ @admin_required                                              │
│  └─ @anonymous_required  validators.py                          │
│                           ├─ Validate Email                      │
│                           ├─ Validate Password                   │
│                           └─ Validate Input                      │
│                                                                   │
└────────────────────────────┬──────────────────────────────────────┘
                             │
                  Database Operations
                             │
┌────────────────────────────▼──────────────────────────────────────┐
│                  PERSISTENCE LAYER (Models)                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  SQLAlchemy ORM Models                                          │
│                                                                   │
│  User Model              Related Models                          │
│  ├─ id (PK)              ├─ ExpenseCategory                      │
│  ├─ username (Unique)    ├─ Expense                              │
│  ├─ email (Unique)       ├─ Meal                                 │
│  ├─ password_hash        ├─ Habit (with HabitLog)               │
│  ├─ profile info         ├─ Goal                                 │
│  ├─ goals & preferences  └─ GroceryItem                          │
│  ├─ permissions                                                  │
│  └─ timestamps           Relationships:                          │
│                          └─ User → Expenses (1:N)               │
│                          └─ User → Meals (1:N)                  │
│                          └─ User → Habits (1:N)                 │
│                          └─ User → Goals (1:N)                  │
│                          └─ User → Groceries (1:N)              │
│                                                                   │
└────────────────────────────┬──────────────────────────────────────┘
                             │
                    SQL Queries via ORM
                             │
┌────────────────────────────▼──────────────────────────────────────┐
│                  DATABASE LAYER (MySQL 8.0)                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌──────────┐  ┌────────────┐  ┌──────────┐  ┌──────────────┐  │
│  │  users   │  │ expenses   │  │  meals   │  │   habits     │  │
│  ├──────────┤  ├────────────┤  ├──────────┤  ├──────────────┤  │
│  │ id (PK)  │  │ id (PK)    │  │ id (PK)  │  │ id (PK)      │  │
│  │ username │  │ user_id(FK)│  │user_id(FK)│ │ user_id (FK) │  │
│  │ email    │  │ category_id│  │ calories │  │ name         │  │
│  │ pwd_hash │  │ amount     │  │ protein  │  │ streak       │  │
│  │ ...      │  │ ...        │  │ ...      │  │ ...          │  │
│  └──────────┘  └────────────┘  └──────────┘  └──────────────┘  │
│                                                                   │
│  ┌──────────────────┐  ┌─────────────┐  ┌──────────────────┐  │
│  │ expense_categorie│  │   goals     │  │  grocery_items   │  │
│  ├──────────────────┤  ├─────────────┤  ├──────────────────┤  │
│  │ id (PK)          │  │ id (PK)     │  │ id (PK)          │  │
│  │ name (Unique)    │  │ user_id(FK) │  │ user_id (FK)     │  │
│  │ description      │  │ title       │  │ name             │  │
│  │ icon, color      │  │ target_val  │  │ quantity, price  │  │
│  └──────────────────┘  └─────────────┘  └──────────────────┘  │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

---

## Data Flow Diagram

```
USER INTERACTION
    │
    ├─ Opens browser
    │   │
    ├─ Navigates to /register
    │   │
    ├─ Enters credentials
    │   │
    └─> FORM SUBMIT
         │
         ├─ HTML Form → POST /auth/register
         │
         └─> FLASK ROUTE (auth.py)
              │
              ├─ Receives form data
              │
              ├─ SERVICE LAYER (validators)
              │  ├─ validate_email()
              │  ├─ validate_password()
              │  └─ validate_username()
              │
              ├─ Check if user exists
              │  └─ User.query.filter_by(username=...)
              │
              ├─ Create new User object
              │  ├─ user = User(...)
              │  └─ user.set_password() [hash password]
              │
              ├─ Database Write
              │  ├─ db.session.add(user)
              │  └─ db.session.commit()
              │
              ├─ Database Layer (MySQL)
              │  └─ INSERT INTO users (...)
              │
              └─> Response
                  ├─ Redirect to login
                  └─ Flash message: "Registration successful!"
```

---

## Authentication Flow

```
┌─────────────┐
│  User Form  │
└──────┬──────┘
       │
       ▼
┌──────────────────────┐
│ POST /auth/login     │
│ (username, password) │
└──────┬───────────────┘
       │
       ▼
┌──────────────────────┐
│ auth.py Route        │
│ def login():         │
└──────┬───────────────┘
       │
       ▼
┌──────────────────────┐      ┌─────────────────┐
│ Find User by username├─────>│ User.query.     │
└──────┬───────────────┘      │ filter_by()     │
       │                      └─────────────────┘
       ├─ User found?
       │  │
       │  ├─ NO  ──> Error: Invalid credentials
       │  │
       │  └─ YES ──> ┌──────────────────────┐
       │             │ check_password()     │
       │             │ (compare hashes)     │
       │             └──────┬───────────────┘
       │                    │
       │            ┌───────┴────────┐
       │            │                │
       │        Correct         Incorrect
       │            │                │
       │            ▼                ▼
       │      login_user()      Error Message
       │            │
       │            ▼
       │      Session Created
       │      (Flask-Login)
       │            │
       │            ▼
       │      Redirect Dashboard
       │
       └─> Response with session cookie
```

---

## Module Dependencies

```
Module 1: User & System Management (✅ COMPLETE)
│
├─> Enables → Module 2: Finance & Grocery Management
│   ├─ User required for expenses
│   ├─ Budget goals from Module 1
│   └─ Goals structure ready
│
├─> Enables → Module 3: Health & Habit Management
│   ├─ User required for meals/habits
│   ├─ Calorie goals from Module 1
│   └─ Goal tracking structure ready
│
├─> Enables → Module 4: AI Intelligence
│   ├─ User profiles for personalization
│   ├─ User data for insights
│   └─ Chat history per user
│
└─> Enables → Module 5: Analytics Dashboard
    ├─ User data aggregation
    ├─ Admin statistics
    └─ Life Score calculation
```

---

## Request-Response Cycle

```
CLIENT                      FLASK APP                    DATABASE
  │                             │                            │
  ├─ HTTP Request ─────────────>│                            │
  │ (Form data)                 │                            │
  │                             ├─ Parse Request            │
  │                             │                            │
  │                             ├─ Route Matching           │
  │                             │ (Find blueprint function)  │
  │                             │                            │
  │                             ├─ Authentication           │
  │                             │ (if required)             │
  │                             │                            │
  │                             ├─ Validation               │
  │                             │ (Input checks)            │
  │                             │                            │
  │                             ├─ Database Query ─────────>│
  │                             │                           │
  │                             │<─ Query Result ───────────│
  │                             │                            │
  │                             ├─ Process Data             │
  │                             │ (Service layer)           │
  │                             │                            │
  │                             ├─ Database Write ─────────>│
  │                             │                           │
  │                             │<─ Confirmation ───────────│
  │                             │                            │
  │                             ├─ Render Template          │
  │                             │ (or JSON response)        │
  │                             │                            │
  │<─ HTTP Response ────────────┤                            │
  │ (HTML/JSON)                 │                            │
  │                             │                            │
  └─ Render in Browser          │                            │
    (JavaScript)                │                            │
```

---

## Security Layers

```
┌─────────────────────────────────────────┐
│        CLIENT-SIDE VALIDATION           │
│  (JavaScript form validation)           │
└────────────────┬────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────┐
│     ROUTE-LEVEL AUTHENTICATION          │
│  (@login_required, @admin_required)     │
└────────────────┬────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────┐
│      INPUT VALIDATION & SANITIZATION    │
│  (Email, password, username validation) │
└────────────────┬────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────┐
│      PASSWORD HASHING & VERIFICATION    │
│  (Werkzeug security - bcrypt-like)      │
└────────────────┬────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────┐
│     DATABASE LAYER PROTECTION           │
│  (SQLAlchemy ORM prevents SQL injection)│
└────────────────┬────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────┐
│    SECURE SESSION MANAGEMENT            │
│  (HttpOnly, Secure, SameSite cookies)   │
└─────────────────────────────────────────┘
```

---

## Deployment Architecture

```
┌──────────────────────────────────────────────┐
│          Docker Container                    │
├──────────────────────────────────────────────┤
│  ┌────────────────────────────────────────┐  │
│  │  Flask Application (Gunicorn Server)   │  │
│  │  ├─ Port: 5000                         │  │
│  │  ├─ Workers: 4                         │  │
│  │  └─ Timeout: 30s                       │  │
│  └────────────────────────────────────────┘  │
│                   │                           │
│           Connects to MySQL                   │
│                   │                           │
│  ┌────────────────────────────────────────┐  │
│  │  MySQL Database Container              │  │
│  │  ├─ Version: 8.0                       │  │
│  │  ├─ Port: 3306                         │  │
│  │  └─ Volume: mysql_data                 │  │
│  └────────────────────────────────────────┘  │
└──────────────────────────────────────────────┘
         │
         │ docker-compose
         │
    ┌────▼─────┐
    │ nginx    │ (Optional - for production)
    │ Reverse  │
    │ Proxy    │
    └──────────┘
```

---

## Module Organization

```
app/
│
├── __init__.py              (App Factory - Creates Flask app)
│
├── models/                  (Database Models)
│   ├── __init__.py
│   ├── user.py             (User + UserMixin)
│   ├── expense.py          (Expense + Category)
│   ├── meal.py             (Meal logs)
│   ├── habit.py            (Habit + HabitLog)
│   ├── goal.py             (Goal tracking)
│   └── grocery.py          (Grocery items)
│
├── routes/                  (Flask Blueprints)
│   ├── __init__.py
│   ├── auth.py             (Register, Login, Password)
│   ├── user.py             (Profile, Settings, Account)
│   ├── admin.py            (Admin Dashboard)
│   ├── main.py             (Home, Dashboard)
│   └── api.py              (REST endpoints)
│
├── services/               (Business Logic - Expandable)
│   ├── __init__.py
│   ├── user_service.py     (Future)
│   ├── finance_service.py  (Future)
│   ├── ai_service.py       (Future)
│   └── ml_service.py       (Future)
│
├── utils/                  (Helper Functions)
│   ├── __init__.py
│   ├── validators.py       (Email, password, username)
│   ├── decorators.py       (Custom decorators)
│   └── helpers.py          (Utility functions)
│
├── static/                 (Client Assets)
│   ├── css/
│   │   └── style.css       (Custom styling)
│   └── js/
│       └── main.js         (Utility JS functions)
│
└── templates/              (Jinja2 Templates)
    ├── base.html           (Base template)
    ├── index.html          (Home page)
    ├── auth/               (Register, Login, ForgotPwd)
    ├── user/               (Profile, Settings, Account)
    ├── admin/              (Dashboard, Users, Details)
    ├── dashboard/          (Main dashboard)
    ├── errors/             (404, 500)
    ├── about.html
    └── contact.html
```

---

This architecture provides:
- ✅ **Scalability** - Easy to add modules
- ✅ **Maintainability** - Clear separation of concerns
- ✅ **Security** - Multiple layers of protection
- ✅ **Performance** - Efficient database queries
- ✅ **Testing** - Isolated components
- ✅ **Flexibility** - Pluggable modules

