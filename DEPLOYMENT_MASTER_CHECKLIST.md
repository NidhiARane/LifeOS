# DEPLOYMENT MASTER CHECKLIST - Weekly Reports Feature

## Pre-Deployment Phase

### Code Review & Testing
- [ ] Read `IMPLEMENTATION_COMPLETE_SUMMARY.md`
- [ ] Review changes in `app/routes/ai.py`
- [ ] Review changes in `app/templates/ai/reports.html`
- [ ] Review changes in `app/services/ai_service.py`
- [ ] Review new file `app/services/report_scheduler.py`
- [ ] Run `python test_report_simple.py`
- [ ] Verify `debug_report.log` shows success
- [ ] Test report generation manually in development
- [ ] Test all 3 new API endpoints
- [ ] Test error scenarios (no data, API down, etc.)

### Configuration Check
- [ ] Verify `.env` has `GEMINI_API_KEY`
- [ ] Verify `.env` has `FLASK_ENV=production` (if applicable)
- [ ] Verify `.env` has `DATABASE_URL` set correctly
- [ ] Verify `SECRET_KEY` is configured
- [ ] Verify database connection works
- [ ] Verify all dependencies in `requirements.txt` are installed

### Documentation Review
- [ ] Read `DEPLOYMENT_GUIDE.md`
- [ ] Read `VERIFICATION_CHECKLIST.md`
- [ ] Prepare `QUICK_START_REPORTS.md` for user distribution
- [ ] Review `REPORTS_QUICK_REF.md` for admin reference
- [ ] Have `WEEKLY_REPORTS_GUIDE.md` ready for support
- [ ] Prepare user communication/announcement

### Backup & Rollback
- [ ] Create full database backup
- [ ] Create full code backup
- [ ] Document rollback procedure
- [ ] Test rollback procedure (dry run)
- [ ] Document rollback contact information

### Security Review
- [ ] Verify no API keys exposed in code
- [ ] Verify no passwords in configuration
- [ ] Verify input validation on all endpoints
- [ ] Verify CSRF protection is enabled
- [ ] Verify user data isolation is enforced
- [ ] Run security scan (if available)

---

## Deployment Phase

### Day Before Deployment
- [ ] Notify stakeholders of scheduled deployment
- [ ] Confirm backup systems are ready
- [ ] Confirm rollback procedure is documented
- [ ] Brief support team on new feature
- [ ] Verify deployment window is clear
- [ ] Have all documentation printed/accessible

### Deployment Day - Preparation (30 minutes before)
- [ ] Stop accepting new requests (if applicable)
- [ ] Wait for existing requests to complete
- [ ] Create final backup
- [ ] Verify all systems are stable
- [ ] Have rollback procedure ready
- [ ] Test internet/connectivity one final time

### Step 1: Backup (5 minutes)
```bash
[ ] Backup database
    Command: mysqldump -u root lifeos_dev > lifeos_backup_$(date +%Y%m%d_%H%M%S).sql
    Verify: ls -lh lifeos_backup_*.sql

[ ] Backup application code
    Command: cp -r /path/to/production /path/to/production.backup.$(date +%Y%m%d)
    Verify: ls -d /path/to/production.backup.*

[ ] Backup current configuration
    Command: cp .env .env.backup.$(date +%Y%m%d)
    Verify: ls -l .env.backup.*
```

### Step 2: Stop Application (2 minutes)
- [ ] Stop Flask server
  ```bash
  kill <process_id>
  # or
  sudo systemctl stop lifeos
  # or use your deployment manager
  ```
- [ ] Verify application stopped
  ```bash
  ps aux | grep python | grep flask
  # Should show no results
  ```
- [ ] Verify port is free
  ```bash
  netstat -tlnp | grep 5000
  # Should show nothing
  ```

### Step 3: Deploy Code (5 minutes)
- [ ] Navigate to project directory
  ```bash
  cd /path/to/LifeOS
  ```

- [ ] Deploy code changes
  ```bash
  [ ] If using Git:
      git pull origin main
      git log --oneline -5
  
  [ ] If manual:
      cp -r /path/to/new/app/* /path/to/production/app/
      cp -r /path/to/new/app/services/report_scheduler.py /path/to/production/app/services/
  ```

- [ ] Verify files are in place
  ```bash
  [ ] ls -la app/routes/ai.py
  [ ] ls -la app/templates/ai/reports.html
  [ ] ls -la app/services/ai_service.py
  [ ] ls -la app/services/report_scheduler.py
  ```

### Step 4: Install Dependencies (2 minutes)
- [ ] Activate virtual environment
  ```bash
  [ ] Linux/Mac: source venv/bin/activate
  [ ] Windows: .\venv\Scripts\activate
  ```

- [ ] Install requirements
  ```bash
  pip install -r requirements.txt
  ```

- [ ] Verify no errors
  ```bash
  pip list | grep -E "Flask|SQLAlchemy|google"
  ```

### Step 5: Start Application (2 minutes)
- [ ] Start Flask server
  ```bash
  [ ] python start_app.py
  [ ] OR: python run.py
  [ ] OR: gunicorn -w 4 -b 0.0.0.0:5000 run:app
  ```

- [ ] Wait for application to fully start
  - [ ] Watch for "Running on..." message
  - [ ] Wait 30 seconds for full initialization
  - [ ] Verify no immediate errors

- [ ] Verify application is running
  ```bash
  ps aux | grep python | grep flask
  # Should show running process
  ```

### Step 6: Health Checks (3 minutes)
- [ ] Check main application
  ```bash
  curl http://localhost:5000/
  # Should return 200 or redirect
  ```

- [ ] Check reports page
  ```bash
  curl http://localhost:5000/ai/reports
  # Should return 200
  ```

- [ ] Check API endpoint
  ```bash
  curl http://localhost:5000/ai/api/report/check-data
  # Should return 401 (no auth) or JSON data
  ```

- [ ] Check database connection
  ```bash
  [ ] Login to app
  [ ] Navigate to /ai/reports
  [ ] Should load without errors
  ```

### Step 7: Manual Testing (5 minutes)
- [ ] Open browser: `http://localhost:5000`
- [ ] Login with test account
- [ ] Add test data:
  - [ ] Log an expense
  - [ ] Log a meal
  - [ ] Create a habit
- [ ] Navigate to: Dashboard → AI Intelligence → Weekly Reports
- [ ] Click "Generate New Report"
- [ ] Verify:
  - [ ] Loading spinner appears
  - [ ] Progress bar animates
  - [ ] Status message updates
  - [ ] Report generates successfully
  - [ ] Auto-redirect works
  - [ ] Report displays all sections
  - [ ] No JavaScript errors (F12)

---

## Post-Deployment Phase

### Immediate (First 5 minutes)
- [ ] Monitor application logs
  ```bash
  tail -f /var/log/lifeos_app.log
  # Watch for any errors
  ```

- [ ] Check error tracking (if available)
  - [ ] Sentry/New Relic/similar
  - [ ] No new errors reported

- [ ] Verify API endpoints are responding
  - [ ] All 3 new endpoints
  - [ ] Return correct status codes
  - [ ] Response times acceptable

### First Hour
- [ ] Monitor system resources
  - [ ] CPU usage normal
  - [ ] Memory usage normal
  - [ ] Disk I/O normal
  - [ ] Network latency acceptable

- [ ] Watch for user errors
  - [ ] Check support tickets
  - [ ] Monitor error logs
  - [ ] No cascading failures

- [ ] Verify database operations
  ```bash
  [ ] Check if reports are storing
  [ ] Check query performance
  [ ] Check for locks/deadlocks
  ```

- [ ] Test with real users (if available)
  - [ ] Have beta users test feature
  - [ ] Gather initial feedback
  - [ ] Watch for any issues

### First Day
- [ ] Review error logs
  ```bash
  grep "ERROR" /var/log/lifeos_app.log | wc -l
  # Should be minimal or zero
  ```

- [ ] Check report generation stats
  ```sql
  SELECT COUNT(*) FROM ai_reports WHERE report_date > NOW() - INTERVAL 24 HOUR;
  ```

- [ ] Monitor performance metrics
  - [ ] Response times
  - [ ] Error rates
  - [ ] User satisfaction

- [ ] Collect initial feedback
  - [ ] Email surveys
  - [ ] Support tickets
  - [ ] User comments

### First Week
- [ ] Verify sustained stability
  - [ ] No memory leaks
  - [ ] No recurring errors
  - [ ] Normal performance
  
- [ ] Check user adoption
  - [ ] How many users generated reports
  - [ ] Report success rate
  - [ ] User engagement

- [ ] Gather detailed feedback
  - [ ] User experience feedback
  - [ ] Feature requests
  - [ ] Bug reports

---

## Rollback Plan (If Needed)

### Quick Rollback Procedure (5 minutes)
```bash
[ ] Stop application
    kill <process_id>

[ ] Restore code backup
    rm -rf /path/to/production
    mv /path/to/production.backup.YYYYMMDD /path/to/production

[ ] Restart application
    cd /path/to/production
    python start_app.py

[ ] Verify rollback
    curl http://localhost:5000/
    # Should be accessible

[ ] Verify database still works
    # Login and navigate - should work

[ ] Notify stakeholders
    Feature has been rolled back
```

### Database Rollback
**NOTE**: No database changes were made, so no rollback needed!
- Reports stay in database
- Previous form-based generation still works
- Users can continue using old method if needed

---

## Communication

### Pre-Deployment Communication
- [ ] Notify users of upcoming feature
- [ ] Explain what the feature does
- [ ] Share QUICK_START_REPORTS.md
- [ ] Ask for feedback after deployment

### Deployment Communication
- [ ] Notify stakeholders deployment started
- [ ] Update status as deployment progresses
- [ ] Notify when deployment complete
- [ ] Provide support contact information

### Post-Deployment Communication
- [ ] Announce feature is live
- [ ] Share user guide links
- [ ] Offer support and feedback channel
- [ ] Celebrate successful deployment

---

## Success Criteria

### Must Have ✅
- [ ] Application loads without errors
- [ ] Reports page is accessible
- [ ] Can generate sample report
- [ ] Report displays all sections
- [ ] No database errors
- [ ] No JavaScript errors
- [ ] API endpoints working
- [ ] Logs show normal operation

### Should Have ✅
- [ ] Positive user feedback
- [ ] Performance is acceptable
- [ ] No error spikes
- [ ] Multiple users testing successfully
- [ ] All documented features working

### Nice to Have ✅
- [ ] Users generating many reports
- [ ] Good engagement metrics
- [ ] Feature adoption is high
- [ ] Zero support issues

---

## Deployment Sign-Off

```
DEPLOYMENT RECORD

Feature:        Weekly Reports (Module 4 - AI Intelligence)
Version:        2.0
Deployment:     April 18, 2026 (Actual: ___________)
Environment:    Production / Development / Staging
Developer:      ____________________________
QA Approved:    ____________________________
Manager:        ____________________________

DEPLOYMENT STATUS
Code Deployed:          [ ] Success  [ ] Issues
Tests Passed:           [ ] Success  [ ] Issues
Health Checks:          [ ] Success  [ ] Issues
Manual Testing:         [ ] Success  [ ] Issues
User Communication:     [ ] Complete [ ] Partial
Support Briefed:        [ ] Yes      [ ] No

FINAL STATUS:           [ ] SUCCESS  [ ] ROLLED BACK

Issues Encountered:
_________________________________________________________________
_________________________________________________________________

Notes:
_________________________________________________________________
_________________________________________________________________

Approved By: ________________________  Date: __________
```

---

## Maintenance & Monitoring

### Daily Monitoring
- [ ] Check application health
- [ ] Review error logs
- [ ] Monitor API response times
- [ ] Check database performance

### Weekly Monitoring
- [ ] Review user feedback
- [ ] Check feature usage stats
- [ ] Monitor API costs
- [ ] Plan improvements

### Monthly Monitoring
- [ ] User engagement metrics
- [ ] Performance trends
- [ ] Feature adoption rate
- [ ] Plan Phase 2 features

---

## Contact & Support

### During Deployment
- **Tech Lead**: [Contact info]
- **Database Admin**: [Contact info]
- **System Admin**: [Contact info]

### After Deployment
- **User Support**: [Contact info]
- **Bug Reports**: [Contact info]
- **Feature Requests**: [Contact info]

---

## Quick Reference

**Start Application**: `python start_app.py`
**Test Feature**: `python test_report_simple.py`
**Debug Issues**: `python debug_report_generation.py`
**Deployment Guide**: See `DEPLOYMENT_GUIDE.md`
**Verification**: See `VERIFICATION_CHECKLIST.md`

---

## Deployment Notes

**Estimated Duration**: 30 minutes
**Rollback Time**: 5 minutes
**Expected Downtime**: <5 minutes
**Risk Level**: Low
**Backward Compatible**: Yes
**Database Changes**: None
**New Dependencies**: None

---

✅ **This checklist ensures a smooth, successful deployment!**

When all items are checked, you're ready to deploy the Weekly Reports feature.

For questions or issues during deployment, refer to:
- DEPLOYMENT_GUIDE.md
- VERIFICATION_CHECKLIST.md
- WEEKLY_REPORTS_IMPLEMENTATION.md

Good luck with the deployment! 🚀

