# LifeOS: An AI-Powered Personal Life Optimization System

## [Title Page]

**Project Title:** LifeOS: An AI-Powered Personal Life Optimization System  
**Submitted by:** [Student Names]  
**College Name:** RNS First Grade College  
**Course:** Bachelor of Computer Applications (BCA)  
**Academic Year:** 2025–2026  
**Project Type:** Team Project  

---

## [Certificate]

This is to certify that the project report entitled “LifeOS: An AI-Powered Personal Life Optimization System” submitted by [Student Names] in partial fulfillment of the requirements for the award of the degree of Bachelor of Computer Applications (BCA) to Karnatak University, is a record of the bonafide work carried out by them under my supervision and guidance.

**Project Guide:** [Guide Name]  
**Head of Department:** [HOD Name]  
**Principal:** [Principal Name]

---

## [Declaration]

We hereby declare that the project work entitled “LifeOS: An AI-Powered Personal Life Optimization System” is an original work carried out by us and has not been submitted to any other university or institution for the award of any degree or diploma.

**Place:** Bengaluru  
**Date:** [Date]  
**Signatures:** [Student Names]

---

## [Acknowledgement]

We hereby express our sincere gratitude to our project guide [Guide Name], faculty of the Department of Computer Science, RNS First Grade College, and Karnatak University for their constant encouragement and guidance during the completion of this project. We also thank our peers and family members for their moral and technical support.

---

## Table of Contents

1. Synopsis
2. Objective of the Project
3. Project Category
4. Languages To Be Used
5. Structure of the Program
6. Hardware Requirements
7. Software Requirements
8. Data Structure
9. Description
10. Future Scope of Project
11. Software Requirement Specification
    11.1 Introduction
    11.2 Developmental Requirement
    11.3 Requirement Specification
    11.4 Purpose
    11.5 Scope
    11.6 Overview
    11.7 Overall Description
    11.8 Product Description
    11.9 User Characteristics
    11.10 Specific Requirement
    11.11 External Interface Requirements
    11.12 Functional Requirement
    11.13 Performance Requirement
    11.14 Design Constraints
12. Description about Languages / Frameworks / Tools Used
    12.1 QT Designer
    12.2 Python
    12.3 SQL
    12.4 SQLiteStudio
    12.5 PyCharm
13. System Design
    13.1 Data Flow Diagram (DFD)
    13.2 Use Case Diagram
    13.3 Activity Diagram
    13.4 Explanation of Diagrams
14. Database Design
    14.1 Database Tables
    14.2 Fields and Attributes
    14.3 Relationships
    14.4 Activity Diagram for User Database Table
    14.5 Module Description
15. System Analysis
    15.1 Functional Description
    15.2 Hardware Requirement
16. Testing
    16.1 Black Box Testing
    16.2 Levels of Testing
    16.3 Unit Testing
    16.4 Integration Testing
    16.5 System Testing
    16.6 Acceptance Testing
    16.7 Regression Testing
17. Project Snapshots
18. Coding
    18.1 Login System
    18.2 Database Connection
    18.3 Expense Tracker
    18.4 Habit Tracker
    18.5 AI Recommendation Logic
19. Future Enhancement
20. Conclusion
21. Bibliography

---

# 1. Synopsis

1.1 Project Overview

LifeOS is an integrated personal life optimization platform that assists users in managing finances, health (meals and nutrition), daily habits, goals, groceries, and personalised AI-driven recommendations. The system collects user inputs (expenses, meals, habit logs) and computes actionable insights, visual summaries, and a composite "Life Score" that reflects overall personal discipline. LifeOS aims to be an intelligent assistant that reduces cognitive load and helps users maintain consistent healthy routines and financial discipline.

1.2 Problem Statement

Modern life generates many small but consequential decisions—what to eat, how much to spend, which habits to maintain—that collectively affect well-being. Users often lack integrated tools that correlate financial, health, and habit data to provide holistic guidance. LifeOS intends to solve this by providing a unified system that integrates routine tracking with AI suggestions.

1.3 Project Motivation

- Encourage healthier lifestyles through structured meal logging and habit tracking.
- Improve personal financial outcomes by simple expense tracking and AI-driven budget recommendations.
- Provide a singular dashboard for users to monitor progress across multiple life areas.

1.4 Deliverables

- Desktop application frontend designed using Qt Designer and packaged for distribution.
- Backend APIs and services written in Python using Flask and SQLAlchemy (SQLite/MySQL supported).
- Database schema for user accounts, expenses, meals, habits, and AI reports.
- AI suggestion engine with modular hooks for third-party language models.
- Comprehensive documentation and test cases suitable for BCA project submission.

# 2. Objective of the Project

2.1 Primary Objective

To design and implement LifeOS, an AI-assisted personal life optimization system that enables users to log and manage finances, nutrition, habits, and goals; to provide analytics, visualizations and AI-driven actionable recommendations.

2.2 Secondary Objectives

- Compute a composite "Life Score" using analytics across health, finance, and habit data.
- Provide intelligent suggestions (budgeting, meal ideas, habit nudges) using lightweight AI heuristics and modular integration with larger LLM services.
- Offer an extensible architecture to add new modules (e.g., sleep tracking, calendar sync) in future.

# 3. Project Category

- Type: Team Project
- Category: AI-assisted Personal Productivity and Optimization System
- Semester / Evaluation Type: BCA – Final Year Project (Practical + Viva)

# 4. Languages To Be Used

- Backend: Python (Flask microframework)  
- Database: SQL (SQLite for local development; MySQL supported for deployment)  
- Frontend UI: Qt Designer (PyQt / PySide for integration)  
- Tools & IDE: PyCharm, SQLiteStudio  

# 5. Structure of the Program

5.1 Architectural Overview

The system follows a modular, service-oriented architecture comprising: Presentation Layer (Qt UI), Application Layer (Flask-based REST APIs and services), Data Layer (SQLAlchemy ORM with SQLite/MySQL), and Analytics/AI Layer (Python services for analytics and recommendations).

5.2 Major Modules

- Authentication & User Management
- Expense & Budget Management
- Meal & Nutrition Logging
- Habit Tracking & Streaks
- Goal Management
- Grocery Manager
- Analytics & Life Score Engine
- AI Suggestions & Report Generation
- Reporting & Export (PDF/CSV)

5.3 Flow Summary

1. User authenticates via login UI.  
2. User logs expenses/meals/habits via UI.  
3. Backend records data to the database.  
4. AnalyticsService computes summaries and Life Score.  
5. AISuggestionsService analyzes patterns and produces recommendations.  
6. UI displays dashboard, charts and recommendations.

# 6. Hardware Requirements

| Component         | Minimum Requirement         | Recommended              |
|-------------------|-----------------------------|--------------------------|
| Processor         | Intel i3 / equivalent       | Intel i5 / i7            |
| RAM               | 4 GB                        | 8 GB                     |
| Storage           | 100 GB free                 | 256 GB SSD               |
| Display           | 1024x768                    | 1920x1080                |
| Network           | Internet for updates/LLMs   | Stable broadband         |

# 7. Software Requirements

| Software Component    | Version / Notes                                  |
|----------------------|--------------------------------------------------|
| Operating System     | Windows 10/11 (development)                       |
| Python               | 3.10+                                            |
| Flask                | 2.x                                              |
| SQLAlchemy           | 1.4+                                             |
| SQLite / MySQL       | SQLite for local, MySQL 8+ supported             |
| PyCharm              | Community / Professional                         |
| Qt Designer          | Compatible with PyQt5 / PySide2                  |
| SQLiteStudio         | Latest                                           |
| Dependencies         | Listed in requirements.txt                       |

# 8. Data Structure

8.1 In-memory Structures

- Dictionaries: For JSON-like API payloads and service-layer aggregations.  
- Lists: Ordered collections for time-series data (daily expenses, meals).  
- Named tuples / dataclasses: Lightweight records for intermediate analytics calculations.

8.2 Persistent Structures (Database Tables)

- users: Stores authentication and profile data.  
- expenses: Stores expense entries with category and metadata.  
- expense_categories: Master table for expense categories.  
- meals: Meal logs with nutritional values.  
- habits, habit_logs: Habit definitions and completion logs.  
- goals: Goal tracking.  
- chat_messages, ai_reports: Stores AI conversation and generated insights.  
- life_scores, user_budgets: Computed metrics for dashboards.

# 9. Description

This chapter contains a detailed explanation of each module, data flows and user interactions.

9.1 Authentication Module

- Secure registration and login with password hashing (Werkzeug).  
- Session management using Flask-Login.  
- Profile editing and last-login tracking.

9.2 Expense Module

- Create, read, update, delete (CRUD) operations for expenses.  
- Category management, monthly summaries, and trend charts.  
- Alerts for budget threshold crossings.

9.3 Meal & Nutrition Module

- Meal logging with calories, protein, carbs, fats.  
- Daily and weekly nutritional summaries and averages.  
- Meal suggestions based on user goals and AI recommendations.

9.4 Habit Tracker

- Habit creation with frequency and target.  
- Habit logs record completions, streaks and longest streak.  
- Habit progress visualization and reminders.

9.5 AI & Analytics

- Analytics compute component scores and Life Score.  
- AISuggestionsService provides heuristics-based and model-assisted recommendations (budget alerts, meal suggestions, habit nudges).  
- Data export and AI-generated weekly reports stored in ai_reports.

9.6 Reports and Exports

- PDF generation for weekly/monthly reports (report scheduler service).  
- CSV export for expenses and meal logs.

# 10. Future Scope of Project

- Integrate advanced LLMs (e.g., OpenAI/Gemini) for conversational recommendations and natural-language planning.
- Mobile clients (Android/iOS) using the same backend APIs.  
- Calendar, sleep and wearable integration for richer analytics.  
- Machine learning models for personalized prediction (expense forecasting, personalized meal plans).  
- Multi-user family/accounts and syncing across devices.

# 11. Software Requirement Specification (SRS)

## 11.1 Introduction

This SRS details the functional and non-functional requirements of LifeOS. It establishes the basis for system design, implementation and testing.

## 11.2 Developmental Requirement

- Development Tools: PyCharm, Qt Designer, SQLiteStudio.  
- Programming Language: Python 3.10+  
- Database: SQLite for development; MySQL supported for production.  
- Libraries: Flask, SQLAlchemy, Flask-Login, PyQt5/PySide2, pandas (optional for analytics).

## 11.3 Requirement Specification

Functional requirements (high level):
- FR1: User registration and authentication.  
- FR2: Expense CRUD and category management.  
- FR3: Meal logging and nutritional summaries.  
- FR4: Habit creation and completion logging.  
- FR5: Analytics dashboard with Life Score.  
- FR6: AI suggestions and weekly report generation.  

Non-functional requirements:
- NFR1: Data security (password hashes, input validation).  
- NFR2: Performance - dashboard loads within 3 seconds for typical datasets.  
- NFR3: Scalability - supports migration from SQLite to MySQL.  
- NFR4: Usability - clear UI using Qt best practices.

## 11.4 Purpose

To provide a complete specification to guide implementation and testing of the LifeOS system, ensuring that deliverables meet user needs and academic evaluation criteria.

## 11.5 Scope

The system supports single-user accounts initially, with optional multi-account extension. It covers expense, meal, habit and goal tracking, analytics, AI recommendations, and reporting.

## 11.6 Overview

This document covers functional requirements, system interfaces, performance goals and design constraints.

## 11.7 Overall Description

User interacts via Qt-based desktop UI which calls backend Flask APIs. Data persistence uses SQLAlchemy ORM. Analytics and AI layers are implemented as Python services invoked by the backend.

## 11.8 Product Description

LifeOS is a productivity/health/finance assistant that aggregates user logs and yields insights and recommendations designed to improve personal outcomes.

## 11.9 User Characteristics

- Primary Users: Students, young professionals, homemakers with basic computer literacy.  
- Secondary Users: Researchers or power users who wish to analyze life metrics.

## 11.10 Specific Requirement

Authentication: secure password hashing, email uniqueness.  
Data integrity: foreign key constraints, input validation, and sanitized exports.

## 11.11 External Interface Requirements

- Optional: External LLM API (OpenAI/Gemini) for enhanced natural language responses.  
- Export: PDF/CSV via standard libraries; optional email delivery.

## 11.12 Functional Requirement

(Expanded)
- User Management: register, login, logout, profile update.  
- Expense Management: add/edit/delete expense, view by date range, category summaries.  
- Meal Management: add meal, nutritional breakdown, daily targets.  
- Habit Management: CRUD habits, log completions, calculate streaks.  
- AI Module: produce recommendations and generate human-readable weekly summaries.

## 11.13 Performance Requirement

- The system must respond to dashboard requests in under 3 seconds for up to 10,000 records on a standard development machine.  
- Background jobs (report generation) run asynchronously and must not block the UI thread.

## 11.14 Design Constraints

- Desktop-first implementation using Qt Designer; a web UI could be added later.  
- SQLite primary development DB to simplify submission and grading; MySQL migration support must be maintained.

# 12. Description about Languages / Frameworks / Tools Used

## 12.1 QT Designer

Qt Designer is used to visually design the desktop application UI. Screens produced are converted into Python code using pyuic (for PyQt) or used directly with PySide2. The UI follows accessibility and responsiveness practices for desktop windows.

## 12.2 Python

Python 3.10+ is used for the backend logic, services and glue code. Flask is the lightweight framework chosen for REST APIs and service wiring. SQLAlchemy is used as ORM to abstract database differences between SQLite and MySQL.

## 12.3 SQL

SQL is used for persistent data storage. SQLAlchemy generates database-agnostic queries; raw SQL snippets are used for specific reporting queries where performance is important.

## 12.4 SQLiteStudio

SQLiteStudio is the recommended tool for inspecting and managing the local SQLite database during development, enabling quick schema edits and data inspection.

## 12.5 PyCharm

PyCharm provides an integrated development environment with debugging, virtual environment management, and easy project navigation and refactoring.

# 13. System Design

## 13.1 Data Flow Diagram (DFD)

[Insert DFD Level 0 and Level 1 diagrams here]

Description placeholder: Level 0 shows user interacting with the front-end which communicates with the backend services and the database. Level 1 expands into modules: Auth, Expense, Meals, Habits, Analytics, AI Service, Reporting.

## 13.2 Use Case Diagram

[Insert Use Case Diagram here]

Description placeholder: Actors: User, Admin (future). Use cases include Register, Login, Log Expense, Log Meal, Add Habit, Generate Report, View Dashboard, Receive AI Suggestions.

## 13.3 Activity Diagram

[Insert Activity Diagram here]

Description placeholder: Example flow for adding an expense — User -> Enter details -> Validate -> Persist -> Update dashboard -> Recompute analytics.

## 13.4 Explanation of Diagrams

Each diagram should be included as an image in the final report and explained: processes, data stores, actors, and flows.

# 14. Database Design

14.1 Database Tables (Summary)

- users (id, username, email, password_hash, profile fields, created_at)  
- expense_categories (id, name, description, icon)  
- expenses (id, user_id, category_id, title, amount, currency, expense_date)  
- meals (id, user_id, name, calories, protein, carbs, fat, meal_type, meal_date)  
- habits (id, user_id, name, frequency, target, current_streak)  
- habit_logs (id, habit_id, completed_date, notes)  
- goals (id, user_id, title, target_value, current_value, target_date)  
- chat_messages (id, user_id, message_type, content, topic, created_at)  
- ai_reports (id, user_id, report_type, title, content, report_date)  
- life_scores (id, user_id, overall_score, health_score, financial_score, habit_score)

14.2 Fields and Attributes (Example Table: users)

| Field | Type | Constraints | Description |
|---|---:|---|---|
| id | INTEGER | PK, AUTOINCREMENT | Unique user identifier |
| username | VARCHAR(80) | UNIQUE, NOT NULL | Login name |
| email | VARCHAR(120) | UNIQUE, NOT NULL | User email |
| password_hash | VARCHAR(255) | NOT NULL | Hashed password |
| first_name | VARCHAR(100) | NULLABLE | First name |
| last_name | VARCHAR(100) | NULLABLE | Last name |
| monthly_budget | FLOAT | DEFAULT 0.0 | Monthly budget set by user |
| created_at | DATETIME | DEFAULT now | Creation timestamp |

14.3 Relationships

- users 1 - * expenses  (one user can have many expenses)  
- users 1 - * meals  
- users 1 - * habits  
- habits 1 - * habit_logs  
- expenses * - 1 expense_categories

14.4 Activity Diagram for User Database Table

[Insert activity diagram: create user, authenticate, update profile, delete account]

14.5 Module Description

Each module interacts with specific database tables. For instance, FinanceService interfaces with expenses and expense_categories; AnalyticsService reads expenses, meals and habits for Life Score computation.

# 15. System Analysis

## 15.1 Functional Description

- The system provides CRUD functionality across modules, scheduled reports and AI suggestions.  
- The dashboard aggregates data and performs analytics to derive the Life Score which is stored and displayed.  
- The AI module inspects trends and issues user-friendly recommendations.

## 15.2 Hardware Requirement

(Repeated from section 6) — ensure recommended specs for smooth operation.

# 16. Testing

Testing is planned and executed across multiple levels with clear test cases and expected outcomes.

## 16.1 Black Box Testing

Focus: functionality without inspecting internal code. Test cases include user registration, login, expense creation, and report generation. Example test: Create expense and verify dashboard updates the monthly total.

## 16.2 Levels of Testing

- Unit Testing: Individual functions and services (FinanceService.create_expense, AnalyticsService.calculate_life_score).  
- Integration Testing: Interaction between API endpoints and database.  
- System Testing: End-to-end application with UI interactions.  
- Acceptance Testing: Per user requirements and academic rubric.  
- Regression Testing: Re-run unit/integration tests after bug fixes.

## 16.3 Unit Testing

Example: Test FinanceService.get_monthly_total returns correct sum for the provided test dataset. Use pytest and factory fixtures to create test data.

## 16.4 Integration Testing

Example: Start a test Flask app with an in-memory SQLite DB to test API endpoints for creating and retrieving expenses.

## 16.5 System Testing

Example: Manual test steps verifying UI flows—login, add expense, add meal, view dashboard, generate report.

## 16.6 Acceptance Testing

Acceptance criteria: all functional requirements (FR1-FR6) implemented and demonstrable during viva.

## 16.7 Regression Testing

Maintain a test suite and run on each change. Use CI (GitHub Actions) if available.

# 17. Project Snapshots

- Login Page: [Image Placeholder — include screenshot of login window]  
- Dashboard: [Image Placeholder — include dashboard screenshot showing Life Score and charts]  
- Finance Module: [Image Placeholder — expense list and add expense form]  
- Meal Planner: [Image Placeholder — meal logging and nutrition summary]  
- Habit Tracker: [Image Placeholder — habit list and streaks view]  
- AI Recommendation Page: [Image Placeholder — AI suggestions panel]  
- Reports Page: [Image Placeholder — weekly AI report and export options]

# 18. Coding

The following code snippets are concise, well-commented examples representing the core functionality. These are extracted and adapted from the project source for educational clarity.

## 18.1 Login System

```python
# app/services/auth_service.py - simplified example
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from app.models.user import User

class AuthService:
    @staticmethod
    def register(username, email, password):
        if User.query.filter((User.username==username)|(User.email==email)).first():
            raise ValueError('User exists')
        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return user

    @staticmethod
    def authenticate(username_or_email, password):
        user = User.query.filter((User.username==username_or_email)|(User.email==username_or_email)).first()
        if not user:
            return None
        if user.check_password(password):
            user.update_last_login()
            return user
        return None
```

## 18.2 Database Connection

```python
# app/__init__.py - app factory (simplified)
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()

def create_app(config_name=None):
    app = Flask(__name__)
    app.config.from_object('config')

    db.init_app(app)
    login_manager.init_app(app)

    with app.app_context():
        db.create_all()  # For development only; migrations recommended

    return app
```

## 18.3 Expense Tracker

```python
# app/services/finance_service.py - create and query expense
from app import db
from app.models.expense import Expense

class FinanceService:
    @staticmethod
    def create_expense(user_id, title, amount, category_id, expense_date=None, description=''):
        expense = Expense(user_id=user_id, title=title, amount=amount,
                          category_id=category_id, expense_date=expense_date or datetime.utcnow(),
                          description=description)
        db.session.add(expense)
        db.session.commit()
        return expense

    @staticmethod
    def get_monthly_total(user_id, year, month):
        # simplified query using SQLAlchemy
        result = db.session.query(db.func.sum(Expense.amount)).filter(
            Expense.user_id==user_id,
            db.extract('year', Expense.expense_date)==year,
            db.extract('month', Expense.expense_date)==month
        ).scalar()
        return float(result or 0.0)
```

## 18.4 Habit Tracker

```python
# app/services/habit_service.py
from app import db
from app.models.habit import Habit, HabitLog
from datetime import datetime

class HabitService:
    @staticmethod
    def log_habit(habit_id, note=''):
        habit = Habit.query.get(habit_id)
        if not habit:
            raise ValueError('Habit not found')

        log = HabitLog(habit_id=habit_id, completed_date=datetime.utcnow(), notes=note)
        db.session.add(log)

        # Update streaks (simplified)
        habit.current_streak = habit.current_streak + 1
        habit.longest_streak = max(habit.longest_streak, habit.current_streak)
        db.session.commit()
        return log
```

## 18.5 AI Recommendation Logic

```python
# app/services/ai_suggestions_service.py - simplified heuristics + placeholder for LLM
from datetime import datetime, timedelta

class AISuggestionsService:
    @staticmethod
    def get_saving_suggestions(user_id):
        # Use FinanceService to get trends then return structured suggestions
        trends = FinanceService.get_spending_trends(user_id, months=3)
        suggestions = []
        # Heuristic: if current month > 20% above average -> recommend savings
        if trends:
            avg = sum(t['total'] for t in trends)/len(trends)
            current = trends[-1]['total']
            if current > avg * 1.2:
                suggestions.append({'type':'spending_spike', 'message':'You are spending more than usual'})
        return suggestions

    @staticmethod
    def generate_weekly_report(user_id):
        # Aggregate data and (optionally) call an LLM to produce a natural-language report
        expense_summary = AnalyticsService.get_expense_summary(user_id)
        health_summary = AnalyticsService.get_health_summary(user_id)
        habit_progress = AnalyticsService.get_habit_progress(user_id)
        # Compose a simple textual summary
        report_text = f"Weekly Report:\nExpenses: {expense_summary.get('total_spent')}\nHealth Avg Calories: {health_summary.get('avg_calories')}"
        # Save to AIReport model
        return report_text
```

# 19. Future Enhancement

- Mobile app front-end with the same REST APIs.  
- Deeper ML models for personalized predictions (expense forecasting, optimal meal plans).  
- Integrations: bank transaction import, fitness wearable sync, calendar sync.  
- Multi-language support and accessibility improvements.

# 20. Conclusion

LifeOS demonstrates an application of software engineering and applied AI concepts in a practical tool for improving personal outcomes. The project integrates frontend design (Qt Designer), backend architecture (Python/Flask), and database design (SQLite/MySQL) to provide an extensible, modular platform.

# 21. Bibliography

- Flask Documentation: https://flask.palletsprojects.com/  
- SQLAlchemy Documentation: https://www.sqlalchemy.org/  
- PyQt / PySide Documentation: https://www.riverbankcomputing.com/software/pyqt/intro  
- SQLite Documentation: https://sqlite.org/docs.html  
- General readings on Habit Formation: Duhigg, C. The Power of Habit.  

---

Appendix A: Sample Database Schema and SQL Queries

-- Create users table (SQLite syntax example)
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(80) NOT NULL UNIQUE,
    email VARCHAR(120) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    monthly_budget FLOAT DEFAULT 0.0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Create expense category table
CREATE TABLE IF NOT EXISTS expense_categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT
);

-- Create expenses table
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    category_id INTEGER NOT NULL,
    title VARCHAR(200) NOT NULL,
    amount FLOAT NOT NULL,
    currency VARCHAR(3) DEFAULT 'USD',
    expense_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES users(id),
    FOREIGN KEY(category_id) REFERENCES expense_categories(id)
);

-- Sample reporting query: monthly total per category
SELECT ec.name as category, SUM(e.amount) as total
FROM expenses e
JOIN expense_categories ec ON e.category_id = ec.id
WHERE e.user_id = ? AND strftime('%Y-%m', e.expense_date) = '2026-05'
GROUP BY ec.id
ORDER BY total DESC;


Appendix B: Diagram Placeholders

- DFD Level 0: [Insert image]  
- Use Case Diagram: [Insert image]  
- ER Diagram: [Insert image]

---

*Notes on formatting*: This document is prepared as a comprehensive Markdown report suitable for conversion to DOCX or PDF. Add page numbers and university cover formatting in the final converted document. Diagrams and screenshots should be inserted in the indicated placeholders before printing or PDF export.
