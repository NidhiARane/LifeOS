# Weekly Reports - QUICK REFERENCE CARD

## For Users: How to Generate Reports

```
1. Go to: Dashboard → AI Intelligence → Weekly Reports
2. Make sure you logged some data (expenses, meals, or habits)
3. Click: "Generate New Report" button
4. Wait: 5-30 seconds (watch the loading spinner)
5. Done! Report appears automatically
```

**URL**: `http://localhost:5000/ai/reports`

---

## For Developers: Files Changed

| File | Change | Lines |
|------|--------|-------|
| `app/routes/ai.py` | Added 3 new API endpoints | +100 |
| `app/templates/ai/reports.html` | Complete AJAX redesign | +150 |
| `app/services/ai_service.py` | Improved error handling | +50 |
| `app/services/report_scheduler.py` | **NEW** - Automatic generation | 200 |

**Total Changes**: 8 new files, 3 modified, 500+ new lines

---

## For Admins: Auto-Generate Reports

```bash
# One-time generation for all users
python -c "from app.services.report_scheduler import WeeklyReportScheduler; WeeklyReportScheduler.generate_reports_for_all_users()"

# Setup cron (Linux/Mac) - every Sunday at midnight
0 0 * * 0 cd /path/to/LifeOS && python -c "from app.services.report_scheduler import WeeklyReportScheduler; WeeklyReportScheduler.generate_reports_for_all_users()"
```

See: `REPORT_SCHEDULER_GUIDE.md` for details

---

## API Endpoints (NEW)

```
POST /ai/api/report/generate
  → Generates a report via AJAX
  → Returns: {status: 'success', report_id: X, redirect: URL}

GET /ai/api/report/check-data
  → Checks if user has data
  → Returns: {expenses: N, meals: N, habits: N, can_generate: true/false}

GET /ai/api/reports/recent?limit=5
  → Gets recent reports
  → Returns: {count: N, reports: [...]}
```

---

## What's In A Report

### Financial Summary
- Total spent (30 days)
- Daily average
- Top categories
- Spending trend

### Health Summary
- Average calories/protein
- Active habits count
- Habit consistency %
- Health status

### Habit Analysis
- Total habits
- Completion rates
- Current streaks
- Individual performance

### AI Insights
- 2-3 paragraph summary
- 3 personalized recommendations
- Expense predictions

---

## Key Improvements

✅ **AJAX Generation**: No page reload
✅ **Real-time Feedback**: Loading spinner + progress
✅ **Data Status**: Shows what data you have
✅ **Error Handling**: Fallback if API fails
✅ **Auto-redirect**: Goes to report automatically
✅ **Scheduler**: Auto-generate for all users
✅ **Documentation**: 5 comprehensive guides

---

## Testing & Verification

### Quick Test (2 minutes)
```bash
# 1. Start app
python start_app.py

# 2. Login and add test data (expenses, meal, habit)

# 3. Go to: http://localhost:5000/ai/reports

# 4. Click "Generate New Report"

# 5. Should succeed in 5-30 seconds
```

### Full Test (5 minutes)
```bash
python test_report_simple.py
# Check: debug_report.log
```

### Debug If Needed
```bash
python debug_report_generation.py
# Check: debug_report.log for detailed output
```

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| "No reports yet" | Click generate button (normal!) |
| Takes too long | Wait 30 sec, it's calling AI |
| "Error generating" | Log some data first, retry |
| Empty report | Shouldn't happen, refresh page |
| API key error | Check `.env` has GEMINI_API_KEY |

---

## Documentation Guide

**For Users**:
- Start: `QUICK_START_REPORTS.md`
- Full: `WEEKLY_REPORTS_GUIDE.md`

**For Developers**:
- Details: `WEEKLY_REPORTS_IMPLEMENTATION.md`
- Tests: `debug_report_generation.py`

**For Ops/Admins**:
- Scheduler: `REPORT_SCHEDULER_GUIDE.md`
- Summary: `WEEKLY_REPORTS_SUMMARY.md`

**Verification**:
- Checklist: `VERIFICATION_CHECKLIST.md`

---

## Environment Setup

```env
# .env file must have:
GEMINI_API_KEY=AIzaSyBxNX7DbiI8OOU8mzw6H0B5QV30bsA7TdA
FLASK_ENV=development
DATABASE_URL=sqlite:///lifeos_dev.db
```

---

## Performance Notes

- **Generation Time**: 5-30 seconds (API dependent)
- **Database**: No schema changes, backward compatible
- **API Calls**: 1 call per report (costs ~$0.002)
- **Storage**: ~5-10 KB per report

---

## Success Indicators

✓ Report generation completes without errors
✓ AI summary is 1000+ characters
✓ Data is accurately collected
✓ No JSON serialization errors
✓ Fallback works if API fails
✓ Database stores reports correctly
✓ Auto-redirect works smoothly

---

## Quick Commands

```bash
# Start app
python start_app.py

# Test reports
python test_report_simple.py

# Debug reports
python debug_report_generation.py

# Generate for all users
python -c "from app.services.report_scheduler import WeeklyReportScheduler; WeeklyReportScheduler.generate_reports_for_all_users()"

# Generate for user ID 1
python -c "from app.services.report_scheduler import WeeklyReportScheduler; print(WeeklyReportScheduler.generate_report_for_user(1))"
```

---

## Status: ✅ COMPLETE & TESTED

**Implementation**: Done
**Testing**: Done  
**Documentation**: Done
**Ready for**: Production

All systems verified working on April 18, 2026.

---

**Need Help?**
1. Check relevant guide (see Documentation Guide above)
2. Run debug script: `python test_report_simple.py`
3. Review logs for error details
4. Check environment variables are set

**Questions?** Refer to the detailed guides - everything is documented!

