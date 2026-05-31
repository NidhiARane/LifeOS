import sqlite3
import random
from datetime import datetime, timedelta
from pathlib import Path

# =====================================================
# DB CONNECTION (safe path)
# =====================================================
DB_PATH = Path(__file__).resolve().parent / "lifeos_dev.db"
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# =====================================================
# CONSTANTS
# =====================================================
ADMIN_ID = 12
USER_ID = 13

TODAY = datetime.now()

def dt(x):
    """Convert datetime → SQLite-safe string"""
    return x.isoformat()

def rand_date(days_back=60):
    return TODAY - timedelta(
        days=random.randint(0, days_back),
        hours=random.randint(0, 23),
        minutes=random.randint(0, 59),
    )

# =====================================================
# USER BUDGETS
# =====================================================
for user_id in [ADMIN_ID, USER_ID]:
    cursor.execute("""
        INSERT OR IGNORE INTO user_budgets
        (user_id, monthly_limit, alert_threshold, created_at)
        VALUES (?, ?, ?, ?)
    """, (
        user_id,
        50000 if user_id == ADMIN_ID else 25000,
        80,
        dt(TODAY)
    ))

# =====================================================
# CATEGORIES
# =====================================================
categories = [
    ("Food", "Food and dining", "utensils", "#FF5733"),
    ("Transport", "Transportation", "car", "#3498DB"),
    ("Shopping", "Shopping", "bag", "#9B59B6"),
    ("Health", "Health expenses", "heart", "#2ECC71"),
    ("Entertainment", "Movies and fun", "film", "#F39C12"),
    ("Utilities", "Bills and utilities", "bolt", "#F1C40F"),
]

for cat in categories:
    cursor.execute("""
        INSERT OR IGNORE INTO expense_categories
        (name, description, icon, color, created_at)
        VALUES (?, ?, ?, ?, ?)
    """, (*cat, dt(TODAY)))

conn.commit()

cursor.execute("SELECT id, name FROM expense_categories")
category_map = {name: cid for cid, name in cursor.fetchall()}

# =====================================================
# EXPENSE TITLES (FIXED)
# =====================================================
expense_titles = {
    "Food": ["Restaurant", "Coffee", "Lunch"],
    "Transport": ["Uber", "Fuel", "Metro"],
    "Shopping": ["Amazon Order", "Clothes"],
    "Health": ["Medicines", "Doctor Visit"],
    "Entertainment": ["Movie Ticket", "Netflix"],
    "Utilities": ["Electricity Bill", "Water Bill", "Internet"],
}

# =====================================================
# HABITS
# =====================================================
habits_data = [
    ("Morning Walk", "Health", "daily"),
    ("Read 20 Pages", "Learning", "daily"),
    ("Meditation", "Mindfulness", "daily"),
]

for user_id in [ADMIN_ID, USER_ID]:
    for name, category, frequency in habits_data:
        cursor.execute("""
            INSERT INTO habits
            (user_id,name,category,frequency,target,
             current_streak,longest_streak,is_active,created_at)
            VALUES (?,?,?,?,?,?,?,?,?)
        """, (
            user_id,
            name,
            category,
            frequency,
            1,
            random.randint(5, 30),
            random.randint(20, 60),
            1,
            dt(TODAY)
        ))

conn.commit()

# =====================================================
# GOALS
# =====================================================
goals = [
    ("Save Emergency Fund", "Finance", 100000),
    ("Lose Weight", "Health", 10),
    ("Read Books", "Learning", 12),
]

for user_id in [ADMIN_ID, USER_ID]:
    for title, category, target in goals:
        cursor.execute("""
            INSERT INTO goals
            (user_id,title,category,target_value,current_value,
             start_date,target_date,is_completed,priority,created_at)
            VALUES (?,?,?,?,?,?,?,?,?,?)
        """, (
            user_id,
            title,
            category,
            target,
            target * random.uniform(0.2, 0.8),
            dt(TODAY - timedelta(days=60)),
            dt(TODAY + timedelta(days=120)),
            0,
            random.choice(["high", "medium"]),
            dt(TODAY)
        ))

conn.commit()

# =====================================================
# 60 DAYS DATA GENERATION
# =====================================================
chat_topics = ["finance", "fitness", "nutrition", "productivity"]
meal_types = ["Breakfast", "Lunch", "Dinner"]
grocery_items_list = ["Milk", "Eggs", "Rice", "Chicken", "Bananas", "Bread"]

for day in range(60):
    current_date = TODAY - timedelta(days=day)

    for user_id in [ADMIN_ID, USER_ID]:

        # ---------------- EXPENSES ----------------
        for _ in range(random.randint(1, 4)):
            category = random.choice(list(category_map.keys()))

            title = random.choice(
                expense_titles.get(category, ["Misc Expense"])
            )

            cursor.execute("""
                INSERT INTO expenses
                (user_id,category_id,title,description,
                 amount,currency,expense_date,created_at)
                VALUES (?,?,?,?,?,?,?,?)
            """, (
                user_id,
                category_map[category],
                title,
                f"{category} expense",
                round(random.uniform(100, 2500), 2),
                "INR",
                dt(current_date),
                dt(current_date)
            ))

        # ---------------- MEALS ----------------
        for meal in meal_types:
            cursor.execute("""
                INSERT INTO meals
                (user_id,name,calories,protein,
                 carbs,fat,meal_type,meal_date,created_at)
                VALUES (?,?,?,?,?,?,?,?,?)
            """, (
                user_id,
                f"{meal} Meal",
                random.randint(300, 900),
                round(random.uniform(10, 50), 1),
                round(random.uniform(20, 80), 1),
                round(random.uniform(5, 30), 1),
                meal,
                dt(current_date),
                dt(current_date)
            ))

        # ---------------- CHAT ----------------
        for _ in range(random.randint(1, 3)):
            cursor.execute("""
                INSERT INTO chat_messages
                (user_id,message_type,content,topic,created_at)
                VALUES (?,?,?,?,?)
            """, (
                user_id,
                random.choice(["user", "assistant"]),
                "Sample conversation message",
                random.choice(chat_topics),
                dt(current_date)
            ))

        # ---------------- GROCERIES ----------------
        if random.random() > 0.7:
            cursor.execute("""
                INSERT INTO grocery_items
                (user_id,name,category,quantity,
                 unit,price,currency,is_purchased,
                 purchase_date,created_at)
                VALUES (?,?,?,?,?,?,?,?,?,?)
            """, (
                user_id,
                random.choice(grocery_items_list),
                "Groceries",
                random.randint(1, 5),
                "pcs",
                round(random.uniform(50, 500), 2),
                "INR",
                1,
                dt(current_date),
                dt(current_date)
            ))

# =====================================================
# HABIT LOGS
# =====================================================
cursor.execute("SELECT id FROM habits")
habit_ids = [r[0] for r in cursor.fetchall()]

for habit_id in habit_ids:
    for day in range(60):
        if random.random() < 0.8:
            d = TODAY - timedelta(days=day)

            cursor.execute("""
                INSERT INTO habit_logs
                (habit_id,completed_date,notes,created_at)
                VALUES (?,?,?,?)
            """, (
                habit_id,
                dt(d),
                "Completed successfully",
                dt(d)
            ))

# =====================================================
# LIFE SCORES
# =====================================================
for user_id in [ADMIN_ID, USER_ID]:
    for week in range(8):
        d = TODAY - timedelta(days=week * 7)

        cursor.execute("""
            INSERT INTO life_scores
            (user_id,overall_score,health_score,
             financial_score,habit_score,
             health_discipline,financial_discipline,
             habit_consistency,calculated_at)
            VALUES (?,?,?,?,?,?,?,?,?)
        """, (
            user_id,
            round(random.uniform(65, 95), 1),
            round(random.uniform(60, 95), 1),
            round(random.uniform(60, 95), 1),
            round(random.uniform(60, 95), 1),
            round(random.uniform(60, 95), 1),
            round(random.uniform(60, 95), 1),
            round(random.uniform(60, 95), 1),
            dt(d)
        ))

# =====================================================
# AI REPORTS
# =====================================================
for user_id in [ADMIN_ID, USER_ID]:
    for week in range(8):
        end = TODAY - timedelta(days=week * 7)
        start = end - timedelta(days=6)

        cursor.execute("""
            INSERT INTO ai_reports
            (user_id,report_type,title,content,
             financial_summary,health_summary,
             habits_summary,key_insights,
             recommendations,report_date,
             week_start,week_end,created_at)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)
        """, (
            user_id,
            "weekly",
            f"Weekly Report #{week+1}",
            "Auto generated report",
            "Stable spending",
            "Good health",
            "Consistent habits",
            "Positive trend",
            "Keep going",
            dt(end),
            dt(start),
            dt(end),
            dt(end)
        ))

# =====================================================
# FINAL COMMIT
# =====================================================
conn.commit()
conn.close()

print("✅ Seed data inserted successfully into lifeos.db")