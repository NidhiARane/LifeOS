# 🚀 LifeOS Startup & Module 2 Access Guide

## Quick Start

### Step 1: Run the Application
Double-click: **START_APP.bat**

Or run manually:
```bash
cd "E:\WebBasedProjects\Life OS - BCA Project\LifeOS"
venv\Scripts\activate.bat
python run.py
```

### Step 2: Open Application
```
http://localhost:5000
```

### Step 3: Login or Register
- **Register**: Click "Register" link
  - Username: `demouser`
  - Email: `demo@example.com`
  - Password: `Demo@123456`

- **Or Login** if you have existing account

---

## 📍 Accessing Module 2 Features

### Option 1: From Dashboard (Easy)
1. After login, you'll see the main dashboard
2. Scroll down to see cards
3. Click **"Finance Dashboard"** or **"Grocery Management"** button

### Option 2: Direct URLs

**Finance Features:**
- Finance Dashboard: http://localhost:5000/finance/dashboard
- All Expenses: http://localhost:5000/finance/expenses
- Budget Analysis: http://localhost:5000/finance/budget
- AI Insights: http://localhost:5000/finance/insights

**Grocery Features:**
- Grocery Dashboard: http://localhost:5000/grocery/dashboard
- Shopping List: http://localhost:5000/grocery/shopping-list
- Purchase History: http://localhost:5000/grocery/history

---

## 💡 Using Module 2

### Finance Module 💰

#### Add an Expense
1. Go to Finance Dashboard
2. Click "Add Expense" button
3. Fill in:
   - Description: "Groceries"
   - Amount: "50.00"
   - Category: "Food & Dining"
   - Date: (auto-filled with today)
   - Notes: (optional)
4. Click "Add Expense"

#### Set Monthly Budget
1. Go to User Profile (Click username → Profile)
2. Click "Edit Profile"
3. Set "Monthly Budget": $3000
4. Save
5. Go back to Finance Dashboard to see budget tracking

#### View Analytics
1. Go to Finance Dashboard
   - See budget progress bar
   - See spending trends chart
   - See category breakdown pie chart
2. Go to Budget page for detailed analysis
3. Go to Insights page for AI recommendations

### Grocery Module 🛒

#### Add Shopping Item
1. Go to Grocery Dashboard
2. Click "Add Item" or go to Shopping List
3. Fill in:
   - Item Name: "Milk"
   - Quantity: "2"
   - Unit: "liters"
   - Price: "3.50"
   - Category: "Dairy" (optional)
4. Click "Add to Shopping List"

#### Mark as Purchased
1. Go to Shopping List
2. Click Edit button on item
3. Mark as purchased
4. Item moves to History

#### View Shopping Total
- Shopping List shows total cost automatically
- Category breakdown shows spending by category

---

## ❓ Troubleshooting

### Issue: Can't see Module 2 options
**Solution:**
1. Refresh the page (F5)
2. Clear browser cache (Ctrl+Shift+Delete)
3. Restart the app:
   - Press CTRL+C in terminal
   - Run START_APP.bat again

### Issue: "Database error" or similar
**Solution:**
1. Stop the app (CTRL+C)
2. Delete `lifeos_dev.db` file from project root
3. Start app again (it will auto-create)

### Issue: Port 5000 already in use
**Solution:**
```bash
# Find and kill process on port 5000
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Or use different port in run.py
# Change: port=5000 to port=5001
```

### Issue: Virtual environment not found
**Solution:**
```bash
cd "E:\WebBasedProjects\Life OS - BCA Project\LifeOS"
python -m venv venv
venv\Scripts\activate.bat
pip install -r requirements.txt
python run.py
```

---

## 📊 Module 2 Overview

### Finance Management 💰
- **Expense Tracking**: Add/edit/delete expenses
- **Budget Management**: Set budget, track spending
- **Analytics**: Charts, trends, category breakdown
- **AI Insights**: Smart recommendations and predictions

### Grocery Management 🛒
- **Shopping Lists**: Create and manage items
- **Price Tracking**: See total cost
- **Purchase History**: Track what you've bought
- **Category Filtering**: Organize by category

---

## 📚 Documentation

**Quick Questions?** → Read `MODULE_2_QUICK_START.md`

**Complete Guide?** → Read `MODULE_2_GUIDE.md`

**Need Navigation Map?** → Read `PROJECT_INDEX.md`

---

## 🎯 Test Data Entry

### Try Finance Features:
```
1. Add 3-5 expenses in different categories
2. Set monthly budget to $2000
3. Check dashboard to see:
   - Budget progress bar
   - Spending trends
   - Category breakdown
   - AI suggestions
```

### Try Grocery Features:
```
1. Add 5-10 items to shopping list
2. Assign prices and categories
3. Mark 2-3 as purchased
4. Check:
   - Total shopping cost
   - Category breakdown
   - Purchase history
```

---

## ⚙️ Configuration

### Change Database to MySQL
1. Edit `.env` file
2. Add: `DATABASE_URL=mysql+pymysql://user:pass@localhost:3306/lifeos`
3. Restart app

### Change Port
1. Edit `run.py`
2. Change: `port=5000` to desired port
3. Restart app

### Change Debug Mode
1. Edit `.env`
2. Set: `FLASK_ENV=production` (disable debug)
3. Restart app

---

## 🔑 Default Accounts

After registration, create test accounts:

**Financial Manager Account:**
- Username: `finance_user`
- Password: `Finance@123456`
- Monthly Budget: $3000

**Grocery Manager Account:**
- Username: `grocery_user`
- Password: `Grocery@123456`

---

## 📞 Need Help?

1. **App won't start?**
   - Check terminal for error messages
   - See Troubleshooting section above

2. **Can't find Module 2?**
   - Make sure you're logged in
   - Try direct URLs above
   - Refresh page (F5)

3. **Data not saving?**
   - Check browser console (F12)
   - Check terminal for errors
   - Ensure database file exists

4. **Want more features?**
   - Check MODULE_2_GUIDE.md for all features
   - Read PROJECT_INDEX.md for navigation

---

## ✅ Verification Checklist

After starting the app, verify:

- [ ] App runs without errors
- [ ] Can login/register
- [ ] Can see Dashboard
- [ ] Can see "Finance Dashboard" button
- [ ] Can see "Grocery Management" button
- [ ] Finance Dashboard loads with charts
- [ ] Can add expense
- [ ] Can add grocery item
- [ ] Can see budget progress
- [ ] Can see shopping list total

---

## 🎉 You're Ready!

Your LifeOS application with Module 2 is ready to use!

**Start with**: http://localhost:5000

**Then explore**: Finance Dashboard or Grocery Management

**Questions?** Check the documentation files listed above!

---

**Happy Life Management! 🚀**

---

Created: March 1, 2026
Version: 1.0
Status: Ready to Use

