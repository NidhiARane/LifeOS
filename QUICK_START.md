# 🚀 LifeOS Quick Start - Two Options

## ⚡ Option A: Quick Start with SQLite (No MySQL needed!)

**This is the FASTEST way to get running right now.**

### Step 1: Modify config.py to use SQLite

Edit your current `config.py` and change the DevelopmentConfig to use SQLite:

```python
class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False
    # Change this line to use SQLite:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///lifeos_dev.db'
    SESSION_COOKIE_SECURE = False
```

**OR** simply use the provided `config_sqlite.py` instead:

```powershell
# In your project directory
Rename-Item -Path config.py -NewName config_mysql.py
Copy-Item -Path config_sqlite.py -Destination config.py
```

### Step 2: Run the app

```powershell
cd "E:\WebBasedProjects\Life OS - BCA Project\LifeOS"
.\venv\Scripts\Activate.ps1
python run.py
```

### Step 3: Open browser

Visit: http://localhost:5000

**That's it!** 🎉 SQLite database file will be created automatically.

---

## 📦 Option B: Setup with MySQL (Full Production Setup)

This requires MySQL to be installed and running.

### Step 1: Check/Install MySQL

See `MYSQL_SETUP.md` for detailed instructions, or:

**Quick Check:**
```powershell
# Check if MySQL service exists
Get-Service -Name "MySQL*" -ErrorAction SilentlyContinue
```

If nothing appears, install MySQL from: https://dev.mysql.com/downloads/mysql/

### Step 2: Start MySQL Service

```powershell
# Start MySQL service
Start-Service -Name "MySQL80"  # or MySQL57, depending on your version

# Verify it's running
Get-Service -Name "MySQL80"
```

### Step 3: Create Database

```powershell
cd "E:\WebBasedProjects\Life OS - BCA Project\LifeOS"
.\venv\Scripts\Activate.ps1
python setup_db.py
```

### Step 4: Run the app

```powershell
python run.py
```

Visit: http://localhost:5000

---

## ✅ Recommended Path (As of now)

1. **Use SQLite first** (Option A) - Get the app running in 2 minutes
2. **Test functionality** - Make sure everything works
3. **Switch to MySQL** (Option B) later for production

---

## 📋 What's the difference?

| Feature | SQLite | MySQL |
|---------|--------|-------|
| Setup Time | 1 minute | 10+ minutes |
| Installation | None needed | Requires installation |
| Data Persistence | File-based (lifeos_dev.db) | Server-based |
| Production Ready | No | Yes |
| Multi-user | Limited | Full support |
| Performance | Good for development | Better for production |

---

## 🆘 Troubleshooting

### "ModuleNotFoundError: No module named 'app'"
```powershell
# Make sure you're in the correct directory:
cd "E:\WebBasedProjects\Life OS - BCA Project\LifeOS"
.\venv\Scripts\Activate.ps1
python run.py
```

### "Port 5000 already in use"
```powershell
# Kill the process using port 5000
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

### "AttributeError: 'NoneType' object has no attribute 'execute'"
Usually means database connection failed. Try SQLite option instead.

---

## 🎯 Next Steps After Starting

Once the app is running:

1. **Register a new account**: http://localhost:5000/auth/register
2. **Login**: http://localhost:5000/auth/login
3. **Access Dashboard**: http://localhost:5000/dashboard
4. **Admin Panel**: http://localhost:5000/admin (if admin user)

---

**Ready? Pick Option A (SQLite) or Option B (MySQL) and give it a try!**

