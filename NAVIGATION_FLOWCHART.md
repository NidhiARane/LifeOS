# MODULE 2 NAVIGATION FLOWCHART

## START APP
```
┌─────────────────────────────────────────┐
│  Double-Click: START_APP.bat            │
│                                         │
│  OR Run: python run.py                  │
└─────────────────────────┬───────────────┘
                          │
                          ▼
┌─────────────────────────────────────────┐
│  Wait for message:                      │
│  "Running on http://localhost:5000"     │
│                                         │
│  Terminal shows app details              │
│  ✅ Web URL                             │
│  ✅ Database path                       │
│  ✅ Module information                  │
└─────────────────────────┬───────────────┘
                          │
                          ▼
┌─────────────────────────────────────────┐
│  Open Browser                           │
│  http://localhost:5000                  │
└─────────────────────────┬───────────────┘
                          │
                          ▼
                    ┌─────────────┐
                    │  Login Page │
                    └──────┬──────┘
                           │
           ┌───────────────┼───────────────┐
           │                               │
           ▼                               ▼
    ┌──────────────┐             ┌──────────────┐
    │   Register   │             │    Login     │
    │   New User   │             │ Existing User│
    └──────┬───────┘             └──────┬───────┘
           │                            │
           └────────────┬───────────────┘
                        │
                        ▼
            ┌─────────────────────┐
            │  MAIN DASHBOARD     │
            │                     │
            │ ┌─────────────────┐ │
            │ │  User Profile   │ │
            │ │  Goals Display  │ │
            │ │  Quick Stats    │ │
            │ └─────────────────┘ │
            │                     │
            │ ┌─────────────────┐ │
            │ │  Module Cards   │ │
            │ │ ┌─────────────┐ │ │
            │ │ │ Finance     │ │ │  ← Click Here!
            │ │ │ Dashboard   │ │ │
            │ │ │ [BUTTON] ◄─┼┼┼┼──┐
            │ │ └─────────────┘ │ │  │
            │ │ ┌─────────────┐ │ │  │
            │ │ │ Grocery     │ │ │  │
            │ │ │ Management  │ │ │  │
            │ │ │ [BUTTON] ◄─┼┼┼┼──┐
            │ │ └─────────────┘ │ │  │
            │ └─────────────────┘ │  │
            └─────────────────────┘  │
                                     │
                    ┌────────────────┴────────────────┐
                    │                                 │
                    ▼                                 ▼
        ┌─────────────────────┐        ┌──────────────────────┐
        │ FINANCE DASHBOARD   │        │ GROCERY DASHBOARD    │
        │                     │        │                      │
        │ ┌─────────────────┐ │        │ ┌────────────────┐  │
        │ │ Budget Status   │ │        │ │ Quick Stats    │  │
        │ │ (4 cards)       │ │        │ │ - Items count  │  │
        │ │ - Monthly       │ │        │ │ - Total cost   │  │
        │ │ - Spent         │ │        │ │ - Categories   │  │
        │ │ - Remaining     │ │        │ └────────────────┘  │
        │ │ - % Used        │ │        │                      │
        │ └─────────────────┘ │        │ ┌────────────────┐  │
        │                     │        │ │ Recent Items   │  │
        │ ┌─────────────────┐ │        │ │ (Quick view)   │  │
        │ │ Charts & Graphs │ │        │ │                │  │
        │ │ - Spending      │ │        │ │ [Add Item]     │  │
        │ │   Trends        │ │        │ └────────────────┘  │
        │ │ - Category      │ │        │                      │
        │ │   Breakdown     │ │        │ ┌────────────────┐  │
        │ └─────────────────┘ │        │ │ Category       │  │
        │                     │        │ │ Breakdown      │  │
        │ ┌─────────────────┐ │        │ └────────────────┘  │
        │ │ AI Suggestions  │ │        └──────────────────────┘
        │ │ & Tips          │ │                    │
        │ └─────────────────┘ │                    └─────────────────┐
        │                     │                                      │
        │ [Add Expense]       │                         ┌────────────▼────────┐
        │ [View All]          │                         │ SHOPPING LIST       │
        └────┬────────────────┘                         │                     │
             │                                          │ ┌─────────────────┐ │
             └──────────────────────┬────────────────────│ │ Items Table     │ │
                                   │                   │ │ with:           │ │
            ┌──────────────────────┬┴──┐               │ │ - Name          │ │
            │                      │   │               │ │ - Qty & Unit    │ │
            ▼                      ▼   ▼               │ │ - Price         │ │
    ┌──────────────────┐   ┌────────────────┐        │ │ - Total Cost    │ │
    │ VIEW EXPENSES    │   │ BUDGET ANALYSIS│        │ │ - Edit/Delete   │ │
    │                  │   │                │        │ │ - Mark Purchased│ │
    │ Filters:         │   │ 12-Month       │        │ └─────────────────┘ │
    │ - Category       │   │ Trends Chart   │        │                     │
    │ - Date Range     │   │                │        │ Total Cost Display  │
    │ - Amount Range   │   │ Progress Bar   │        │                     │
    │                  │   │ (%) Indicator  │        │ Filters:            │
    │ Sort By:         │   │                │        │ - Category          │
    │ - Date           │   │ Category       │        │ - Sort by Price     │
    │ - Amount         │   │ Breakdown      │        │ - Search            │
    │                  │   │ List           │        │                     │
    │ [Add] [Edit] [Δ] │   │                │        │ [Add Item]          │
    │                  │   │ (Visualization)         └─────────────────────┘
    └──────────────────┘   └────────────────┘                   │
            │                      │                            │
            └──────────────┬───────┴───────────────────────────┘
                           │
                           ▼
                    ┌─────────────────┐
                    │ AI INSIGHTS     │
                    │                 │
                    │ - Saving Tips   │
                    │ - Budget Tips   │
                    │ - Predictions   │
                    │ - Trends        │
                    └─────────────────┘
```

---

## QUICK ACCESS PATHS

### Direct URL Shortcuts

**Finance:**
- `/finance/dashboard` → Main finance view with charts
- `/finance/expenses` → List all expenses with filters
- `/finance/expense/add` → Add new expense
- `/finance/budget` → Budget analysis & trends
- `/finance/insights` → AI suggestions & predictions

**Grocery:**
- `/grocery/dashboard` → Main grocery view
- `/grocery/shopping-list` → Your shopping list
- `/grocery/item/add` → Add new item
- `/grocery/history` → Purchase history

**User:**
- `/user/profile` → Your profile
- `/user/profile/edit` → Edit profile (set budget here!)
- `/user/settings` → Account settings
- `/dashboard` → Main dashboard (with Module 2 buttons)

---

## ACTION SEQUENCES

### First Time Finance Setup
```
1. Dashboard
   ↓
2. Click "Finance Dashboard"
   ↓
3. Notice empty state (no expenses yet)
   ↓
4. Go to User Profile
   ↓
5. Edit Profile → Set "Monthly Budget" to $2000
   ↓
6. Return to Finance Dashboard
   ↓
7. Click "Add Expense"
   ↓
8. Add 3-4 expenses
   ↓
9. Watch budget bar fill up!
   ↓
10. Click "Insights" → See AI recommendations
```

### First Time Grocery Setup
```
1. Dashboard
   ↓
2. Click "Grocery Management"
   ↓
3. Click "Add Item"
   ↓
4. Add milk ($3), bread ($2), eggs ($2.50)
   ↓
5. Watch total cost calculate
   ↓
6. Click item edit → Mark as "Purchased"
   ↓
7. Check "History" → See purchased items
```

---

## KEY FEATURES BY LOCATION

| Feature | Location | How to Use |
|---------|----------|-----------|
| **Add Expense** | `/finance/expenses` | Click "Add Expense" button |
| **View Trends** | `/finance/dashboard` | Scroll down to see charts |
| **Check Budget** | `/finance/budget` | View progress bar & analysis |
| **Get Tips** | `/finance/insights` | Read AI recommendations |
| **Set Budget** | `/user/profile/edit` | Edit "Monthly Budget" field |
| **Add Item** | `/grocery/shopping-list` | Click "Add Item" button |
| **Track Total** | `/grocery/shopping-list` | See at top of page |
| **Mark Purchased** | `/grocery/shopping-list` | Click edit button on item |
| **View History** | `/grocery/history` | See all purchased items |

---

## NAVIGATION TIPS

✅ **From Dashboard**: Use buttons to access modules
✅ **From Module**: Use sidebar/menu to navigate pages
✅ **Direct URLs**: Paste into address bar for quick access
✅ **Back Button**: Browser back button always works
✅ **Refresh**: F5 if page seems stuck

---

## SHORTCUTS

| Action | Key | Works On |
|--------|-----|----------|
| New Expense | Click "Add" button | Finance pages |
| New Item | Click "Add" button | Grocery pages |
| Edit | Click pencil icon | Any list page |
| Delete | Click trash icon | Any list page |
| Filter | Select dropdown | Expense/Item lists |
| Sort | Click header | Table columns |
| Refresh | F5 | All pages |

---

## COMMON FLOWS

**Quick Add & View:**
```
Dashboard 
  → Click "Finance Dashboard"
  → Click "Add Expense"
  → Enter details
  → Submit
  → See updated dashboard
```

**Budget Tracking:**
```
Dashboard
  → Click "Finance Dashboard"
  → See budget bar
  → Click "Budget" for detailed view
  → Analyze spending
```

**Shopping:**
```
Dashboard
  → Click "Grocery Management"
  → Click "Add Item"
  → Add items with prices
  → See total update
  → Mark items as purchased
```

---

**Ready to navigate? Start with the dashboard!** 🚀

