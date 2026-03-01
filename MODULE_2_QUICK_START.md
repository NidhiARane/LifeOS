# 🚀 Module 2 Quick Setup & Usage Guide

## ⚡ Quick Start (2 minutes)

### Prerequisites
- Python 3.9+ (already installed)
- Flask (already installed from Module 1)
- SQLite (comes with Python)

### Step 1: Run the Application
```bash
cd "E:\WebBasedProjects\Life OS - BCA Project\LifeOS"
python run.py
```

### Step 2: Create Test User (Optional)
```python
python
>>> from app import create_app, db
>>> from app.models.user import User
>>> app = create_app()
>>> with app.app_context():
...     user = User(username='finance_test', email='finance@test.com', monthly_budget=3000)
...     user.set_password('Test@12345')
...     db.session.add(user)
...     db.session.commit()
...     print("User created!")
```

### Step 3: Access Module 2
- Login at `http://localhost:5000/auth/login`
- Go to Dashboard
- Click "Finance Dashboard" or "Grocery Management"

---

## 📍 Navigation

### Main Dashboard Links
```
Dashboard
├── Finance Dashboard     → /finance/dashboard
│   ├── Expenses        → /finance/expenses
│   ├── Budget          → /finance/budget
│   └── Insights        → /finance/insights
│
└── Grocery Management   → /grocery/dashboard
    ├── Shopping List   → /grocery/shopping-list
    └── History         → /grocery/history
```

---

## 💰 Finance Features

### 1. Add Expense
```
Finance → Expenses → "Add Expense" button
  → Fill form:
     - Description (required)
     - Amount (required, 2 decimals)
     - Category (required)
     - Date (auto-filled with today)
     - Notes (optional)
  → Click "Add Expense"
```

### 2. View Expenses
```
Finance → Expenses
  → Shows all expenses with:
     - Filter by category
     - Sort by date/amount
     - Edit/Delete buttons
     - Pagination (20 per page)
```

### 3. Budget Management
```
Finance → Budget
  → Shows:
     - Monthly budget status
     - Spending progress bar
     - 12-month trends chart
     - Category breakdown
```

### 4. AI Insights
```
Finance → Insights
  → Get:
     - Spending recommendations
     - Budget analysis
     - 3-month spending predictions
```

---

## 🛒 Grocery Features

### 1. Add Shopping Item
```
Grocery → Add Item
  → Fill form:
     - Item name (required)
     - Quantity (required)
     - Unit (kg, liters, pieces, etc.)
     - Unit price (required)
     - Category (optional)
     - Notes (optional)
  → Click "Add to Shopping List"
```

### 2. Shopping List
```
Grocery → Shopping List
  → View all items with:
     - Filter by category
     - Sort by price/name
     - Total cost calculation
     - Edit/Delete buttons
```

### 3. Mark as Purchased
```
Shopping List
  → Click edit button
  → Or use "Toggle Purchase" feature
  → Item moves to history
```

### 4. Purchase History
```
Grocery → History
  → View all purchased items
  → See purchase dates
  → Re-edit if needed
```

---

## 🎯 Budget Setup

### Set Monthly Budget
1. Go to User Profile (`/user/profile`)
2. Click "Edit Profile"
3. Set "Monthly Budget" field
4. Save changes

### Budget Status
- **Green**: On track (0-80%)
- **Yellow**: Approaching limit (80-100%)
- **Red**: Over budget (>100%)

---

## 📊 Dashboard Overview

### Finance Dashboard Shows:
- Monthly budget status (4 cards)
- Budget progress bar
- 6-month spending trends chart
- Category pie chart
- Recent transactions table
- AI suggestions widget

### Grocery Dashboard Shows:
- Items to buy count
- Estimated total cost
- Category breakdown
- Recent items list
- Quick add button

---

## 🔌 API Endpoints (for Mobile Apps)

### Finance APIs
```
GET /finance/api/expenses
  Returns: [{ id, title, amount, category, date }]

GET /finance/api/budget-status
  Returns: { budget, spent, remaining, percentage_used }

GET /finance/api/suggestions
  Returns: [{ type, title, message, severity }]
```

### Grocery APIs
```
GET /grocery/api/shopping-list
  Returns: [{ id, name, quantity, unit, price, total }]

GET /grocery/api/shopping-total
  Returns: { total: 125.50 }

POST /grocery/api/items/bulk-mark
  Body: { item_ids: [1, 2, 3] }
  Returns: { status, count }
```

---

## 💾 Database (SQLite)

### Auto-Created on First Run
- File: `lifeos_dev.db` (in project root)
- Size: ~1MB (starts small, grows as data added)
- Location: `E:\WebBasedProjects\Life OS - BCA Project\LifeOS\lifeos_dev.db`

### View Database
```python
# Using Python sqlite3
python
>>> import sqlite3
>>> conn = sqlite3.connect('lifeos_dev.db')
>>> cursor = conn.cursor()
>>> cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
>>> print(cursor.fetchall())
# Shows all tables
```

---

## 🧮 Example Workflows

### Workflow 1: Track Monthly Expenses
```
1. Set monthly budget in profile ($3000)
2. Add expenses daily
3. Check "Finance → Budget" to see progress
4. Get AI insights automatically
```

### Workflow 2: Plan Grocery Shopping
```
1. Add items to "Shopping List"
2. See total cost estimate
3. Buy items from list
4. Mark as purchased
5. Check history for past purchases
```

### Workflow 3: Analyze Spending
```
1. Go to "Finance → Insights"
2. Review AI suggestions
3. Check spending predictions
4. Compare with budget
5. Adjust spending patterns
```

---

## 🎨 UI Features

### Charts
- Line charts auto-update
- Pie charts show percentages
- Bar charts show monthly data
- All responsive on mobile

### Forms
- Auto-date filling on expense form
- Required field validation
- Clear error messages
- Mobile-friendly inputs

### Tables
- Click column header to sort
- Use filters to narrow down
- Page through large datasets
- Edit/delete inline

---

## ⚙️ Configuration

### SQLite (Default)
```python
# In config.py
DATABASE_URL = 'sqlite:///lifeos_dev.db'
```

### MySQL (Alternative)
```python
# Set in .env
DATABASE_URL = mysql+pymysql://user:pass@localhost/lifeos
```

---

## 🔧 Troubleshooting

### Database Locked Error
```python
python
>>> from app import db, create_app
>>> app = create_app()
>>> with app.app_context():
...     db.session.rollback()
...     print("Done")
```

### Reset All Data
```python
python
>>> from app import db, create_app
>>> app = create_app()
>>> with app.app_context():
...     db.drop_all()
...     db.create_all()
...     print("Database reset!")
```

### Port Already in Use
```bash
# Find process on port 5000
netstat -ano | findstr :5000
# Kill process
taskkill /PID <PID> /F
# Or use different port
python run.py --port 5001
```

---

## 📱 Mobile Responsiveness

✅ Works on:
- iPhone/Android (portrait & landscape)
- Tablets (iPad, Android tablets)
- Small desktops (1024px width)
- Large desktops (1920px+ width)

📝 Features:
- Touch-friendly buttons
- Optimized spacing
- Collapsible menus
- Responsive tables

---

## 🔒 Data Security

- All user data isolated by user_id
- Password hashing (Werkzeug)
- SQL injection prevention (ORM)
- CSRF protection ready
- No sensitive data in logs

---

## 📈 Performance Tips

1. **Large Expense Lists**: Use pagination (20 per page)
2. **Many Categories**: Filter before viewing
3. **Mobile App**: Use API endpoints for speed
4. **Charts**: Limited to 12 months for performance

---

## 🎓 Learning Resources

### Service Layer
See: `app/services/finance_service.py`
Example method calls and data manipulation

### Route Handlers
See: `app/routes/finance.py`
HTTP request/response handling

### Database Models
See: `app/models/expense.py`
SQLAlchemy ORM patterns

### HTML Templates
See: `app/templates/finance/dashboard.html`
Chart.js integration and forms

---

## 📞 Common Tasks

### Add Budget Alert
```python
# In finance_service.py - already implemented
status = check_budget_status(user_id)
if status['is_over_budget']:
    # Send alert
```

### Export Expenses
```python
# Ready for Module X
expenses = FinanceService.get_user_expenses(user_id)
# Export to CSV/PDF
```

### Sync with Grocery
```python
# Items marked as purchased create expenses
# Ready for Module X
```

---

## 🚀 Next: Module 3 Preview

Module 3 will add:
- Meal logging with nutrition
- Calorie tracking
- Habit management
- Goal monitoring

**Reusing Module 2:**
- Budget integration
- Expense linking
- Goal progress tracking
- AI integration

---

## 📝 Notes

- All operations are user-specific
- Data auto-saves to SQLite
- No manual database backups needed
- Migration ready for MySQL
- API endpoints ready for mobile apps

---

**Happy Expense Tracking! 🎉**

For issues, check:
1. `MODULE_2_GUIDE.md` - Full documentation
2. `MODULE_2_COMPLETE.md` - Feature summary
3. `DEVELOPMENT.md` - Dev setup

---

Created: March 1, 2026  
Version: 1.0  
Status: ✅ Ready to Use

