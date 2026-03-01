# 🔧 MySQL Setup Instructions for Windows

## ❌ MySQL Not Found Error

The error you received means MySQL is either:
1. **Not installed** on your system
2. **Not in the system PATH** (not accessible from command line)
3. **Not running** as a service

---

## ✅ Solution: Install and Configure MySQL

### Option 1: Check if MySQL is Already Installed

1. **Open Services:**
   - Press `Windows Key + R`
   - Type: `services.msc`
   - Press Enter
   - Look for a service named "MySQL*" (like "MySQL80" or "MySQL57")
   - If found, right-click and select **"Start"** if it's not running

2. **If you see it:**
   - The service is installed, just needs to be started
   - Go to Step 2 below

3. **If you don't see it:**
   - MySQL is not installed, go to Option 2

---

### Option 2: Install MySQL Server

#### Method 1: Using MySQL Community Installer (Recommended)

1. Download MySQL Server:
   - Visit: https://dev.mysql.com/downloads/mysql/
   - Download "MySQL Community Server" (latest version)
   - Choose Windows installer (.msi file)

2. Run the installer and follow these steps:
   - Click "Next" through setup wizard
   - Choose "Server only" installation
   - In Configuration:
     - **Port:** Keep as 3306 (default)
     - **MySQL Server Type:** Development Machine
     - **Config Type:** Server Machine
     - **Create MySQL System Service:** Check this box
     - **Windows Service Name:** MySQL80 (or similar)
   - When asked for credentials, set:
     - **Root account password:** `password` (or your preferred password)
   - Complete the installation

3. After installation, MySQL will be running automatically

#### Method 2: Using Docker (Alternative)

If you prefer containers, use Docker:

```powershell
# Install Docker Desktop from https://www.docker.com/products/docker-desktop

# Run MySQL in Docker
docker run -d --name lifeos-mysql -e MYSQL_ROOT_PASSWORD=password -p 3306:3306 mysql:8.0
```

---

## ✅ Verify MySQL is Working

Once installed/running, test the connection:

```powershell
# If MySQL is in PATH (should work after installation):
mysql -u root -p

# If that doesn't work, try the full path:
"C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe" -u root -p
```

When prompted, enter: `password`

You should see: `mysql>`

Type `EXIT` to exit.

---

## 🚀 Proceed with Database Setup

Once MySQL is running, go back to PowerShell and run:

```powershell
cd "E:\WebBasedProjects\Life OS - BCA Project\LifeOS"
.\venv\Scripts\Activate.ps1
python setup_db.py
```

---

## ⚡ Quick Summary

**Current Status:**
- ✅ Python & Flask installed
- ✅ Virtual environment ready
- ❌ MySQL not running or installed

**Next Steps:**
1. **Install/Start MySQL** (see above)
2. **Run:** `python setup_db.py`
3. **Start app:** `python run.py`
4. **Visit:** http://localhost:5000

---

## 💡 If You're Still Having Issues

Run this command to diagnose:

```powershell
# Shows all services with "mysql" in the name
Get-Service | Where-Object { $_.Name -like "*mysql*" } | Format-Table

# Check if port 3306 is in use
netstat -ano | findstr :3306
```

If nothing shows up, MySQL is definitely not installed/running.


