# 🏗️ Module 3 Architecture & Structure Guide

## System Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    LifeOS Application                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Module 1: User & System Management                     │  │
│  │  (Authentication, Profile, Admin)                       │  │
│  └──────────────────────────────────────────────────────────┘  │
│                           ↓                                      │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Module 2: Finance & Grocery Management                 │  │
│  │  (Expenses, Budgets, Grocery Tracking)                  │  │
│  └──────────────────────────────────────────────────────────┘  │
│                           ↓                                      │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Module 3: Health, Meal & Habit Management ✅            │  │
│  │  (Meals, Habits, Goals)                                 │  │
│  └──────────────────────────────────────────────────────────┘  │
│                           ↓                                      │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Module 4: AI Intelligence Module (Coming)              │  │
│  │  (Gemini Chat, Insights, Reports)                       │  │
│  └──────────────────────────────────────────────────────────┘  │
│                           ↓                                      │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Module 5: Analytics & Dashboard (Coming)               │  │
│  │  (Charts, Life Score, Predictions)                      │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Module 3: Detailed Component Breakdown

```
Module 3: Health, Meal & Habit Management
│
├─── 🍽️ MEAL SUBSYSTEM
│    │
│    ├─ Model: Meal
│    │  ├─ id, user_id, name, description
│    │  ├─ meal_type (breakfast/lunch/dinner/snack)
│    │  ├─ calories, protein, carbs, fat
│    │  ├─ meal_date, created_at, updated_at
│    │  └─ Relationships: User (Many-to-One)
│    │
│    ├─ Routes: health_bp.meals_*
│    │  ├─ GET  /health/meals              → View dashboard
│    │  ├─ GET  /health/meal/log           → Form
│    │  ├─ POST /health/meal/log           → Create
│    │  ├─ POST /health/meal/<id>/delete   → Delete
│    │  └─ GET  /health/api/meals-summary  → API
│    │
│    ├─ Templates:
│    │  ├─ meals.html               (Dashboard + History)
│    │  └─ log_meal.html            (Form)
│    │
│    └─ Features:
│       ├─ Daily nutrition stats
│       ├─ Progress bars (Calories/Protein)
│       ├─ Meal history with pagination
│       └─ Goal comparison
│
├─── 🏃 HABIT SUBSYSTEM
│    │
│    ├─ Models: Habit, HabitLog
│    │  ├─ Habit:
│    │  │  ├─ id, user_id, name, description
│    │  │  ├─ category, frequency, target
│    │  │  ├─ current_streak, longest_streak
│    │  │  ├─ is_active, created_at, updated_at
│    │  │  └─ Relationships: User (Many-to-One), HabitLog (One-to-Many)
│    │  │
│    │  └─ HabitLog:
│    │     ├─ id, habit_id, completed_date, notes
│    │     ├─ created_at
│    │     └─ Relationships: Habit (Many-to-One)
│    │
│    ├─ Routes: health_bp.habit_*
│    │  ├─ GET  /health/habits              → Dashboard
│    │  ├─ GET  /health/habit/create       → Form
│    │  ├─ POST /health/habit/create       → Create
│    │  ├─ POST /health/habit/<id>/checkin → Check-in
│    │  ├─ POST /health/habit/<id>/delete  → Delete
│    │  └─ GET  /health/api/habits-summary → API
│    │
│    ├─ Templates:
│    │  ├─ habits.html               (Dashboard)
│    │  └─ create_habit.html         (Form)
│    │
│    └─ Features:
│       ├─ Daily check-in tracking
│       ├─ Streak calculation & display
│       ├─ Consistency scoring
│       ├─ Toast notifications
│       └─ Category organization
│
└─── 🎯 GOAL SUBSYSTEM
     │
     ├─ Model: Goal
     │  ├─ id, user_id, title, description
     │  ├─ category, target_value, current_value
     │  ├─ unit, priority, is_completed
     │  ├─ start_date, target_date, completed_at
     │  ├─ created_at, updated_at
     │  └─ Relationships: User (Many-to-One)
     │
     ├─ Routes: health_bp.goal_*
     │  ├─ GET  /health/goals                      → Dashboard
     │  ├─ GET  /health/goal/create               → Form
     │  ├─ POST /health/goal/create               → Create
     │  ├─ POST /health/goal/<id>/update-progress → Update
     │  ├─ POST /health/goal/<id>/delete          → Delete
     │  └─ GET  /health/api/goals-summary         → API
     │
     ├─ Templates:
     │  ├─ goals.html               (Dashboard)
     │  └─ create_goal.html         (Form)
     │
     └─ Features:
        ├─ Goal creation with targets
        ├─ Progress percentage calculation
        ├─ Category organization
        ├─ Priority levels
        ├─ Modal-based updates
        └─ Completion detection
```

---

## Data Layer Architecture

```
┌─────────────────────────────────────────┐
│         Database (SQLite)               │
├─────────────────────────────────────────┤
│                                         │
│  ┌─────────────────────────────────┐   │
│  │ users (from Module 1)           │   │
│  ├─────────────────────────────────┤   │
│  │ id (PK), username, email, ...   │   │
│  └─────────────────────────────────┘   │
│           ↑                             │
│      (FK Link)                          │
│           │                             │
│  ┌────────┴──────────────────────────┐ │
│  │                                   │ │
│  ├─────────────────────────────────┐ │ │
│  │ meals                          │ │ │
│  ├─────────────────────────────────┤ │ │
│  │ id, user_id, name, meal_type   │ │ │
│  │ calories, protein, carbs, fat  │ │ │
│  │ meal_date, created_at, ...     │ │ │
│  └─────────────────────────────────┘ │ │
│  ├─────────────────────────────────┐ │ │
│  │ habits                         │ │ │
│  ├─────────────────────────────────┤ │ │
│  │ id, user_id, name, category    │ │ │
│  │ frequency, current_streak, ... │ │ │
│  └─────────────────────────────────┘ │ │
│       ↑                               │ │
│       │ (One-to-Many)                 │ │
│       │                               │ │
│  ├─────────────────────────────────┐ │ │
│  │ habit_logs                     │ │ │
│  ├─────────────────────────────────┤ │ │
│  │ id, habit_id, completed_date   │ │ │
│  │ notes, created_at              │ │ │
│  └─────────────────────────────────┘ │ │
│  │                                   │ │
│  ├─────────────────────────────────┐ │ │
│  │ goals                          │ │ │
│  ├─────────────────────────────────┤ │ │
│  │ id, user_id, title, category   │ │ │
│  │ target_value, current_value    │ │ │
│  │ unit, priority, is_completed   │ │ │
│  │ target_date, created_at, ...   │ │ │
│  └─────────────────────────────────┘ │ │
│                                   │ │
└───────────────────────────────────┴─┘ │
│                                         │
└─────────────────────────────────────────┘
```

---

## Request/Response Flow

### Meal Logging Flow
```
┌──────────────┐
│  User Click  │ (Log Meal button)
└──────┬───────┘
       │
       ↓
┌──────────────────────────┐
│ GET /health/meal/log     │
│ (Show Form Template)     │
└──────┬───────────────────┘
       │
       ↓
┌──────────────────────────┐
│  User Fills Form         │
└──────┬───────────────────┘
       │
       ↓
┌──────────────────────────┐
│ POST /health/meal/log    │
│ (Form Data)              │
└──────┬───────────────────┘
       │
       ↓
┌──────────────────────────┐
│ Backend Validation       │
│ ├─ Check required fields │
│ ├─ Validate data types   │
│ └─ Verify user auth      │
└──────┬───────────────────┘
       │
       ↓
┌──────────────────────────┐
│ Create Meal Object       │
│ Save to Database         │
└──────┬───────────────────┘
       │
       ↓
┌──────────────────────────┐
│ Flash Success Message    │
│ Redirect to /meals       │
└──────┬───────────────────┘
       │
       ↓
┌──────────────────────────┐
│ GET /health/meals        │
│ (Show Updated Dashboard) │
└──────────────────────────┘
```

### Habit Check-in Flow
```
┌──────────────┐
│  User Click  │ (Check In Today button)
└──────┬───────┘
       │
       ↓
┌──────────────────────────────────┐
│ AJAX POST /habit/<id>/checkin   │
└──────┬───────────────────────────┘
       │
       ├─→ Already checked today? → Error Response
       │
       ↓
┌──────────────────────────────────┐
│ Create HabitLog Entry            │
└──────┬───────────────────────────┘
       │
       ↓
┌──────────────────────────────────┐
│ Calculate New Streak             │
│ ├─ Check yesterday's check-in    │
│ ├─ Increment or reset streak     │
│ └─ Update longest_streak if new  │
└──────┬───────────────────────────┘
       │
       ↓
┌──────────────────────────────────┐
│ Return JSON Response             │
│ {                                │
│   "status": "success",          │
│   "current_streak": 5,          │
│   "longest_streak": 7           │
│ }                                │
└──────┬───────────────────────────┘
       │
       ↓
┌──────────────────────────────────┐
│ JavaScript:                      │
│ ├─ Show toast notification      │
│ ├─ Display new streak value     │
│ └─ Optional: Reload page        │
└──────────────────────────────────┘
```

### Goal Progress Update Flow
```
┌──────────────┐
│  User Click  │ (Update Progress)
└──────┬───────┘
       │
       ↓
┌──────────────────────────────┐
│ Open Modal Dialog            │
│ Show current_value field     │
└──────┬──────────────────────┘
       │
       ↓
┌──────────────────────────────┐
│  User Enters New Value       │
└──────┬──────────────────────┘
       │
       ↓
┌──────────────────────────────┐
│ AJAX POST /goal/<id>/update  │
│ {current_value: 7.5}         │
└──────┬──────────────────────┘
       │
       ↓
┌──────────────────────────────┐
│ Backend:                     │
│ ├─ Validate authorization   │
│ ├─ Update current_value     │
│ ├─ Calculate progress %     │
│ └─ Check if completed       │
└──────┬──────────────────────┘
       │
       ↓
┌──────────────────────────────┐
│ Return JSON:                 │
│ {                            │
│   "status": "success",      │
│   "progress": 75.0          │
│ }                            │
└──────┬──────────────────────┘
       │
       ↓
┌──────────────────────────────┐
│ JavaScript:                  │
│ ├─ Close modal              │
│ ├─ Show success message     │
│ └─ Reload page              │
└──────────────────────────────┘
```

---

## Technology Stack

```
┌─────────────────────────────────────────────────────┐
│         Module 3 Technology Stack                   │
├─────────────────────────────────────────────────────┤
│                                                     │
│  Backend                                            │
│  ├─ Framework: Flask 3.1.2                         │
│  ├─ ORM: SQLAlchemy 2.0                            │
│  ├─ Database: SQLite (via SQLAlchemy)              │
│  ├─ Auth: Flask-Login                              │
│  └─ Validation: Flask form & Python                │
│                                                     │
│  Frontend                                           │
│  ├─ CSS: Bootstrap 5.3                             │
│  ├─ JavaScript: Vanilla JS (fetch API)             │
│  ├─ Icons: Font Awesome 6                          │
│  └─ Templates: Jinja2                              │
│                                                     │
│  Development                                        │
│  ├─ Version Control: Git                           │
│  ├─ Deployment: Docker (optional)                  │
│  ├─ Server: Gunicorn                               │
│  └─ Environment: Python 3.10+                      │
│                                                     │
└─────────────────────────────────────────────────────┘
```

---

## Security Architecture

```
┌─────────────────────────────────────────┐
│     Security Layers (Module 3)          │
├─────────────────────────────────────────┤
│                                         │
│  Layer 1: Authentication                │
│  ├─ Flask-Login session management      │
│  ├─ @login_required decorator           │
│  └─ Redirect to login if not auth       │
│                                         │
│  Layer 2: Authorization                 │
│  ├─ User ID validation on all ops       │
│  ├─ Check user_id == current_user.id   │
│  └─ Return 403 if unauthorized          │
│                                         │
│  Layer 3: Input Validation              │
│  ├─ Required field checks               │
│  ├─ Data type validation                │
│  ├─ Range/length validation             │
│  └─ Bootstrap form validation           │
│                                         │
│  Layer 4: SQL Injection Prevention      │
│  ├─ SQLAlchemy ORM (parameterized)     │
│  ├─ No raw SQL queries                  │
│  └─ Automatic escaping                  │
│                                         │
│  Layer 5: CSRF Protection               │
│  ├─ Flask default CSRF tokens           │
│  ├─ Form token validation               │
│  └─ AJAX header checks                  │
│                                         │
│  Layer 6: Error Handling                │
│  ├─ Try-except blocks                   │
│  ├─ DB rollback on error                │
│  ├─ Generic error messages              │
│  └─ Error logging                       │
│                                         │
└─────────────────────────────────────────┘
```

---

## File Structure

```
LifeOS/
│
├── app/
│   ├── models/
│   │   ├── user.py              ✓ (Module 1)
│   │   ├── expense.py           ✓ (Module 2)
│   │   ├── grocery.py           ✓ (Module 2)
│   │   ├── meal.py              ✓ (Module 3 - Used)
│   │   ├── habit.py             ✓ (Module 3 - Used)
│   │   └── goal.py              ✓ (Module 3 - Used)
│   │
│   ├── routes/
│   │   ├── auth.py              ✓ (Module 1)
│   │   ├── user.py              ✓ (Module 1)
│   │   ├── admin.py             ✓ (Module 1)
│   │   ├── finance.py           ✓ (Module 2)
│   │   ├── grocery.py           ✓ (Module 2)
│   │   ├── main.py              ✓
│   │   ├── api.py               ✓
│   │   └── health.py            ✓ (Module 3 - NEW)
│   │
│   ├── templates/
│   │   ├── base.html
│   │   ├── dashboard/
│   │   │   └── index.html       ✓ (Updated with health links)
│   │   ├── health/              ✓ (Module 3 - NEW)
│   │   │   ├── meals.html
│   │   │   ├── log_meal.html
│   │   │   ├── habits.html
│   │   │   ├── create_habit.html
│   │   │   ├── goals.html
│   │   │   └── create_goal.html
│   │   ├── finance/             ✓ (Module 2)
│   │   ├── grocery/             ✓ (Module 2)
│   │   └── auth/                ✓ (Module 1)
│   │
│   └── __init__.py              ✓ (Updated - health blueprint)
│
├── Documentation/
│   ├── MODULE_3_COMPLETE.md                    ✓
│   ├── MODULE_3_QUICK_ACCESS.md                ✓
│   ├── MODULE_3_ROUTES.md                      ✓
│   ├── MODULE_3_IMPLEMENTATION_SUMMARY.md      ✓
│   └── MODULE_3_ARCHITECTURE.md                ✓ (This file)
│
└── Database
    └── lifeos_dev.db            ✓ (SQLite - contains all tables)
```

---

## Deployment Architecture

```
┌─────────────────────────────────────────────────┐
│         Deployment Flow (Optional)              │
├─────────────────────────────────────────────────┤
│                                                 │
│  Local Development                              │
│  ├─ Flask dev server (port 5000)                │
│  ├─ SQLite database                             │
│  └─ Live reload enabled                         │
│           ↓                                      │
│  Docker Container (Optional)                    │
│  ├─ Python image                                │
│  ├─ Flask app                                   │
│  └─ Volume mounts for code/db                   │
│           ↓                                      │
│  Production Deployment                          │
│  ├─ Gunicorn WSGI server                        │
│  ├─ Nginx reverse proxy                         │
│  ├─ PostgreSQL database (recommended)           │
│  ├─ SSL/TLS certificates                        │
│  └─ Render hosting (as per tech stack)          │
│                                                 │
└─────────────────────────────────────────────────┘
```

---

## Performance Considerations

```
Optimization Strategies Implemented:

1. Database
   ├─ Lazy loading for relationships
   ├─ Index on user_id for faster queries
   ├─ Pagination for large datasets
   └─ Query optimization with .filter()

2. Frontend
   ├─ AJAX for non-blocking updates
   ├─ Bootstrap CSS minified
   ├─ Font Awesome CDN
   ├─ Lazy loading of images (future)
   └─ CSS/JS caching headers

3. Backend
   ├─ Request validation before DB
   ├─ Efficient streak calculation
   ├─ Progress calculation cached
   └─ Minimal DB transactions

4. Caching (Future)
   ├─ Redis for session storage
   ├─ Browser cache for assets
   └─ DB query caching
```

---

**Architecture Document**
**Module 3: Health, Meal & Habit Management**
**Date**: April 11, 2026
**Status**: ✅ Complete & Production Ready

