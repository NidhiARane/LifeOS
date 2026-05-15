# Deployment Guide - Weekly Reports Feature

## Quick Deployment Summary

**Status**: ✅ Ready for production  
**Time to Deploy**: 15-30 minutes  
**Rollback Time**: 5 minutes  
**Risk Level**: Low  

---

## Pre-Deployment Checklist

### Code Review
- [ ] Review `app/routes/ai.py` changes
- [ ] Review `app/templates/ai/reports.html` redesign
- [ ] Review `app/services/ai_service.py` improvements
- [ ] Review `app/services/report_scheduler.py` (new file)
- [ ] Check for any merge conflicts

### Testing
- [ ] Run `python test_report_simple.py`
- [ ] Verify `debug_report.log` shows success
- [ ] Test report generation manually
- [ ] Verify all endpoints work
- [ ] Test error scenarios

### Configuration
- [ ] Verify `.env` has `GEMINI_API_KEY`
- [ ] Verify `FLASK_ENV=production` (if applicable)
- [ ] Verify `DATABASE_URL` is correct
- [ ] Check SECRET_KEY is set

### Documentation
- [ ] Prepare user communication
- [ ] Download `QUICK_START_REPORTS.md` for sharing
- [ ] Review `VERIFICATION_CHECKLIST.md`
- [ ] Plan monitoring strategy

---

## Deployment Steps

### Step 1: Backup (5 minutes)
```bash
# Backup current production
cp -r /path/to/production /path/to/production.backup.$(date +%Y%m%d)

# Backup database (if using MySQL)
mysqldump -u root lifeos_dev > lifeos_backup_$(date +%Y%m%d_%H%M%S).sql
```

### Step 2: Deploy Code (5 minutes)
```bash
# Navigate to project
cd /path/to/LifeOS

# Pull latest code
git pull origin main  # or your branch

# Or copy files manually if not using git
cp -r /path/to/new/code/* /path/to/production/
```

### Step 3: Install Dependencies (2 minutes)
```bash
# Activate virtual environment
source venv/bin/activate  # Linux/Mac
.\venv\Scripts\activate   # Windows

# Install any new dependencies
pip install -r requirements.txt
```

### Step 4: Restart Application (2 minutes)
```bash
# Stop current Flask app
# (kill the process or use your deployment manager)

# Restart Flask
python start_app.py

# Or if using Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 run:app
```

### Step 5: Verify Deployment (3 minutes)
```bash
# Check application is running
curl http://localhost:5000/

# Test reports page
curl http://localhost:5000/ai/reports

# Test API endpoint
curl http://localhost:5000/ai/api/report/check-data
```

### Step 6: Manual Testing (5 minutes)
1. Open browser: `http://localhost:5000`
2. Login with test account
3. Add test data (expense, meal, habit)
4. Go to: Dashboard → AI Intelligence → Weekly Reports
5. Click: "Generate New Report"
6. Verify: Report generates successfully

---

## Post-Deployment Tasks

### Monitor First Hour
- [ ] Watch logs for errors
- [ ] Monitor API response times
- [ ] Check database connections
- [ ] Verify no 500 errors

### User Communication
- [ ] Send announcement about new feature
- [ ] Share `QUICK_START_REPORTS.md`
- [ ] Provide support contact info
- [ ] Ask for feedback

### Monitoring Setup (Optional)
```bash
# Watch logs
tail -f /var/log/lifeos_app.log

# Monitor database
SELECT COUNT(*) FROM ai_reports WHERE report_date > DATE_SUB(NOW(), INTERVAL 1 HOUR);

# Check error frequency
grep "ERROR" /var/log/lifeos_app.log | wc -l
```

---

## Rollback Plan (If Needed)

### Quick Rollback (5 minutes)
```bash
# Stop application
kill <flask_process_id>

# Restore backup
rm -rf /path/to/production
mv /path/to/production.backup.YYYYMMDD /path/to/production

# Restart
cd /path/to/production
python start_app.py
```

### Database Rollback (If Needed)
```bash
# No database changes were made, so no rollback needed!
# All data in ai_reports table remains intact
# Previous form-based generation still works
```

---

## Deployment on Different Platforms

### Linux Server
```bash
# Using systemd
sudo systemctl restart lifeos

# Or manual
cd /home/lifeos/LifeOS
source venv/bin/activate
gunicorn -w 4 -b 0.0.0.0:5000 run:app &
```

### Windows Server
```powershell
# Stop current process
Stop-Process -Name "python" -Force

# Start new process
cd C:\LifeOS
.\venv\Scripts\activate
python start_app.py
```

### Docker
```bash
# Rebuild image
docker-compose build

# Restart container
docker-compose up -d

# Check logs
docker-compose logs -f app
```

### Kubernetes
```bash
# Update image
kubectl set image deployment/lifeos-app lifeos-app=lifeos:v2.0

# Check rollout
kubectl rollout status deployment/lifeos-app

# Verify pods
kubectl get pods
```

---

## Health Checks Post-Deployment

### API Endpoints
```bash
# Check main app
curl http://localhost:5000/

# Check reports page
curl http://localhost:5000/ai/reports

# Check data check endpoint
curl http://localhost:5000/ai/api/report/check-data -H "Authorization: Bearer <token>"

# Check recent reports endpoint
curl http://localhost:5000/ai/api/reports/recent -H "Authorization: Bearer <token>"
```

### Database Health
```sql
-- Check if table exists
SELECT TABLE_NAME FROM information_schema.TABLES WHERE TABLE_NAME = 'ai_reports';

-- Check for recent data
SELECT COUNT(*) as report_count FROM ai_reports WHERE report_date > DATE_SUB(NOW(), INTERVAL 24 HOUR);

-- Check for errors
SELECT * FROM ai_reports WHERE content LIKE '%error%';
```

### Application Health
```bash
# Check if Flask is running
ps aux | grep python | grep flask

# Check port 5000 is open
netstat -tlnp | grep 5000

# Check logs for errors
tail -50 /var/log/lifeos_app.log | grep -i error
```

---

## Performance Monitoring

### Metrics to Watch
```sql
-- Average report generation time
SELECT 
  AVG(TIMESTAMPDIFF(SECOND, created_at, updated_at)) as avg_seconds
FROM ai_reports 
WHERE report_date > DATE_SUB(NOW(), INTERVAL 1 DAY);

-- Reports generated per hour
SELECT 
  HOUR(report_date) as hour,
  COUNT(*) as count
FROM ai_reports 
WHERE report_date > DATE_SUB(NOW(), INTERVAL 24 HOUR)
GROUP BY HOUR(report_date);

-- Errors in last 24 hours
SELECT COUNT(*) FROM ai_reports WHERE content LIKE '%error%' 
AND report_date > DATE_SUB(NOW(), INTERVAL 24 HOUR);
```

---

## Common Issues & Solutions

### Issue: "Error loading reports page"
**Solution**: Check if routes are properly registered
```bash
python -c "from app import create_app; app = create_app(); print([str(rule) for rule in app.url_map.iter_rules() if 'ai' in str(rule)])"
```

### Issue: "GEMINI_API_KEY not configured"
**Solution**: Set it in .env
```bash
echo "GEMINI_API_KEY=AIzaSyBxNX7DbiI8OOU8mzw6H0B5QV30bsA7TdA" >> .env
source .env
python start_app.py
```

### Issue: "Reports not generating"
**Solution**: Run debug script
```bash
python test_report_simple.py
cat debug_report.log
```

### Issue: "Database connection error"
**Solution**: Verify DATABASE_URL
```bash
echo $DATABASE_URL
# Should show: sqlite:///lifeos_dev.db or mysql+pymysql://...
```

---

## Optional: Set Up Automatic Reports

After successful deployment, optionally set up automatic scheduling:

### Linux/Mac (Cron Job)
```bash
# Edit crontab
crontab -e

# Add this line (runs every Sunday at midnight)
0 0 * * 0 cd /path/to/LifeOS && python -c "from app.services.report_scheduler import WeeklyReportScheduler; WeeklyReportScheduler.generate_reports_for_all_users()" >> /var/log/lifeos_reports.log 2>&1
```

### Windows (Task Scheduler)
```powershell
# Create scheduled task
$action = New-ScheduledTaskAction -Execute "C:\Python314\python.exe" -Argument "-c 'from app.services.report_scheduler import WeeklyReportScheduler; WeeklyReportScheduler.generate_reports_for_all_users()'" -WorkingDirectory "C:\LifeOS"
$trigger = New-ScheduledTaskTrigger -Weekly -DaysOfWeek Sunday -At 00:00
Register-ScheduledTask -Action $action -Trigger $trigger -TaskName "LifeOS Weekly Reports"
```

See `REPORT_SCHEDULER_GUIDE.md` for more details.

---

## Success Indicators

### Immediately After Deployment
✅ Application loads without errors
✅ Reports page accessible at `/ai/reports`
✅ Can generate sample report
✅ Report displays all sections
✅ No JavaScript errors in console

### First Hour
✅ Users can access feature
✅ Reports generate successfully
✅ No database errors
✅ API endpoints responding
✅ Logs show normal operation

### First Day
✅ Multiple users generated reports
✅ Reports stored in database
✅ No cascade failures
✅ Performance metrics normal
✅ User feedback positive

---

## Support Contacts

### For Technical Issues
- Check: `VERIFICATION_CHECKLIST.md`
- Run: `python test_report_simple.py`
- Review: Log files
- Debug: `python debug_report_generation.py`

### For User Questions
- Share: `QUICK_START_REPORTS.md`
- Refer to: `WEEKLY_REPORTS_GUIDE.md`
- Check: `REPORTS_QUICK_REF.md`

### For Deployment Help
- See: This document
- Review: `WEEKLY_REPORTS_IMPLEMENTATION.md`
- Check: `WEEKLY_REPORTS_SUMMARY.md`

---

## Version Control

```bash
# Tag the release
git tag -a v2.0-weekly-reports -m "Weekly Reports Feature - AJAX redesign, auto-scheduling, comprehensive docs"

# Push tag
git push origin v2.0-weekly-reports

# Create release notes
# (document what changed)
```

---

## Deployment Verification Checklist

### Pre-Deployment
- [ ] All code changes reviewed
- [ ] Tests passed
- [ ] Documentation ready
- [ ] Backup created
- [ ] Environment variables set

### Deployment
- [ ] Code deployed
- [ ] Dependencies installed
- [ ] Application restarted
- [ ] Health checks passed
- [ ] Manual testing successful

### Post-Deployment
- [ ] Monitoring in place
- [ ] Users notified
- [ ] First hour verified
- [ ] Logs monitored
- [ ] Performance normal

### Follow-Up
- [ ] Feedback collected
- [ ] Issues tracked
- [ ] Documentation updated
- [ ] Success celebrated
- [ ] Next phase planned

---

## Deployment Sign-Off

```
Feature: Weekly Reports (Module 4 - AI Intelligence)
Version: 2.0
Date: April 18, 2026
Status: ✅ APPROVED FOR DEPLOYMENT

Reviewed By: [Your Name]
Tested By: [QA Team]
Approved By: [Manager]

Sign-Off: ___________________________  Date: __________
```

---

## Quick Reference Commands

```bash
# Start app
python start_app.py

# Test reports
python test_report_simple.py

# Debug reports
python debug_report_generation.py

# Restart app
kill <pid> && python start_app.py

# View logs
tail -f /var/log/lifeos_app.log

# Check database
sqlite3 instance/lifeos_dev.db "SELECT COUNT(*) FROM ai_reports;"

# Generate reports for all users
python -c "from app.services.report_scheduler import WeeklyReportScheduler; WeeklyReportScheduler.generate_reports_for_all_users()"
```

---

**Deployment Date**: [Fill in date]
**Deployed By**: [Your name]
**Deployment Status**: [Success/Issues]
**Notes**: [Any issues encountered and how they were resolved]

---

*This deployment guide ensures smooth rollout of the Weekly Reports feature.*
*For questions, refer to the comprehensive documentation provided.*

