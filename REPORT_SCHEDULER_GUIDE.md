# Running Weekly Report Scheduler

## Overview
The Weekly Report Scheduler can automatically generate reports for all users. This is useful for sending weekly emails or generating reports in the background.

## Quick Start

### Generate Reports for All Users
```bash
# Run from the project root directory
python -c "from app.services.report_scheduler import WeeklyReportScheduler; WeeklyReportScheduler.generate_reports_for_all_users()"
```

### Generate Report for Specific User
```bash
python -c "from app.services.report_scheduler import WeeklyReportScheduler; print(WeeklyReportScheduler.generate_report_for_user(1))"
```

## Schedule as Cron Job (Linux/Mac)

### Edit Crontab
```bash
crontab -e
```

### Add This Line (Runs every Sunday at midnight)
```cron
0 0 * * 0 cd /path/to/LifeOS && python -c "from app.services.report_scheduler import WeeklyReportScheduler; WeeklyReportScheduler.generate_reports_for_all_users()" >> /var/log/lifeos_reports.log 2>&1
```

### Alternative (with Virtual Environment)
```cron
0 0 * * 0 cd /path/to/LifeOS && /path/to/venv/bin/python -c "from app.services.report_scheduler import WeeklyReportScheduler; WeeklyReportScheduler.generate_reports_for_all_users()" >> /var/log/lifeos_reports.log 2>&1
```

## Schedule as Task (Windows)

### Using Task Scheduler GUI
1. Open Task Scheduler
2. Create Basic Task
3. **Name**: LifeOS Weekly Reports
4. **Trigger**: Weekly, Sunday, 00:00
5. **Action**: 
   - Program: `C:\path\to\python.exe`
   - Arguments: `-c "from app.services.report_scheduler import WeeklyReportScheduler; WeeklyReportScheduler.generate_reports_for_all_users()"`
   - Start in: `C:\path\to\LifeOS`

### Using PowerShell Script
Create `generate_reports.ps1`:
```powershell
cd "C:\path\to\LifeOS"
python -c "from app.services.report_scheduler import WeeklyReportScheduler; WeeklyReportScheduler.generate_reports_for_all_users()"
```

Then schedule it:
```powershell
# Run as Administrator
$action = New-ScheduledTaskAction -Execute "powershell.exe" -Argument "-File C:\path\to\generate_reports.ps1"
$trigger = New-ScheduledTaskTrigger -Weekly -DaysOfWeek Sunday -At 00:00
Register-ScheduledTask -Action $action -Trigger $trigger -TaskName "LifeOS Weekly Reports" -Description "Generate weekly reports for all users"
```

## Direct Python Script

### Create `run_report_scheduler.py`
```python
#!/usr/bin/env python
import os
import sys
from dotenv import load_dotenv

# Set up environment
os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
load_dotenv()

from app.services.report_scheduler import WeeklyReportScheduler

if __name__ == '__main__':
    result = WeeklyReportScheduler.generate_reports_for_all_users()
    print(f"\nReport Generation Results:")
    print(f"Total Users: {result['total_users']}")
    print(f"Successful: {result['success']}")
    print(f"Errors: {result['errors']}")
    sys.exit(0 if result['errors'] == 0 else 1)
```

### Run the Script
```bash
python run_report_scheduler.py
```

## Docker Integration

### Add to `docker-compose.yml`
```yaml
services:
  lifeos:
    # ... existing config ...
    
  report-scheduler:
    build: .
    command: python -c "from app.services.report_scheduler import WeeklyReportScheduler; WeeklyReportScheduler.generate_reports_for_all_users()"
    environment:
      - FLASK_ENV=production
      - GEMINI_API_KEY=${GEMINI_API_KEY}
      - DATABASE_URL=${DATABASE_URL}
    depends_on:
      - lifeos
    restart: no
    # Or use a cron service
```

### Using APScheduler (Alternative)
Add to your Flask app for in-process scheduling:

```python
from apscheduler.schedulers.background import BackgroundScheduler
from app.services.report_scheduler import WeeklyReportScheduler

def start_scheduler(app):
    scheduler = BackgroundScheduler()
    
    # Schedule weekly reports - every Sunday at midnight
    scheduler.add_job(
        func=lambda: WeeklyReportScheduler.generate_reports_for_all_users(),
        trigger="cron",
        day_of_week="sun",
        hour=0,
        minute=0,
        id="weekly_reports",
        name="Generate weekly reports for all users",
        replace_existing=True
    )
    
    scheduler.start()
    return scheduler

# In your app initialization
if __name__ == '__main__':
    app = create_app()
    scheduler = start_scheduler(app)
    app.run()
```

## Monitoring

### Check Log Output
```bash
# Linux/Mac
tail -f /var/log/lifeos_reports.log

# Windows
Get-Content "C:\path\to\logs\lifeos_reports.log" -Tail 50 -Wait
```

### Database Check
```sql
-- Check reports generated in last week
SELECT user_id, COUNT(*) as reports_count, MAX(report_date) as last_report
FROM ai_reports
WHERE report_date >= DATE_SUB(NOW(), INTERVAL 7 DAY)
GROUP BY user_id;
```

### Test Run
```bash
# Test if scheduler works without scheduling
python -c "
from app.services.report_scheduler import WeeklyReportScheduler
result = WeeklyReportScheduler.generate_reports_for_all_users()
print('Test successful!' if result['errors'] == 0 else 'Test failed!')
"
```

## Troubleshooting

### Permission Denied
**Windows**:
- Run Task Scheduler as Administrator
- Or use `runas` command

**Linux/Mac**:
```bash
chmod +x run_report_scheduler.py
```

### Python Not Found
**Full Path Solution**:
```bash
/usr/bin/python3 -c "..."
# or
C:\Python314\python.exe -c "..."
```

### Module Not Found
**Make sure environment is set up**:
```bash
# Activate virtual environment first
source venv/bin/activate  # Linux/Mac
.\venv\Scripts\activate   # Windows

# Then run
python run_report_scheduler.py
```

### Database Connection Error
**Check**:
1. DATABASE_URL environment variable is set
2. Database is running and accessible
3. Connection string is correct

### API Key Error
**Check**:
1. GEMINI_API_KEY is set in .env
2. API key is valid
3. API has remaining quota

## Best Practices

1. **Schedule at Off-Peak Time**: Run at midnight or early morning
2. **Add Timeout**: Use `timeout` command to prevent long runs
   ```bash
   timeout 300 python run_report_scheduler.py  # 5 min timeout
   ```
3. **Log Output**: Redirect to file for debugging
   ```bash
   python run_report_scheduler.py >> /var/log/lifeos_reports.log 2>&1
   ```
4. **Email Notifications**: Add email alerts for failures
5. **Database Cleanup**: Archive old reports periodically
6. **Rate Limiting**: Don't run more than once per week

## Monitoring Dashboard

### Add to Admin Panel (Optional)
```python
@admin_bp.route('/scheduler-status')
@admin_required
def scheduler_status():
    last_run = db.session.execute(
        "SELECT MAX(report_date) as last_report FROM ai_reports"
    ).fetchone()
    
    users = User.query.count()
    reports_last_week = AIReport.query.filter(
        AIReport.report_date >= datetime.utcnow() - timedelta(days=7)
    ).count()
    
    return render_template('admin/scheduler_status.html', 
                          last_run=last_run, 
                          total_users=users,
                          reports_generated=reports_last_week)
```

## FAQ

**Q: Will it send emails?**
A: Not automatically, but you can hook it into an email service.

**Q: Can I customize what goes in reports?**
A: Yes, modify the `generate_weekly_report()` method in `ai_service.py`.

**Q: What if the API fails?**
A: Reports still generate with fallback content, and errors are logged.

**Q: Does it remove duplicates?**
A: Yes, it checks if a report was already generated this week.

**Q: Can I skip certain users?**
A: Yes, modify the scheduler to filter users first.

---

**Last Updated**: April 18, 2026
**Version**: 1.0

