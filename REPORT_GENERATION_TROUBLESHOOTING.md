# Report Generation Troubleshooting Guide

## Error: "An error occurred while generating the report"

### Quick Diagnosis Steps

#### Step 1: Check Your Data
Before generating a report, you need at least some data:
```
✓ Log at least 1 expense
✓ OR log at least 1 meal
✓ OR create at least 1 habit
```

**To add data**:
- **Expenses**: Dashboard → Finance → Log Expense
- **Meals**: Dashboard → Health → Log Meal
- **Habits**: Dashboard → Health → Manage Habits → Create Habit

#### Step 2: Check Internet Connection
Report generation requires an internet connection to call the Gemini API.

**Verify**:
- [ ] Can you access other websites?
- [ ] Is your internet stable?
- [ ] Try again in a moment (API might be slow)

#### Step 3: Clear Browser Cache
Sometimes browser cache can cause issues.

**How to clear**:
- Press `Ctrl + Shift + Delete` (Chrome/Edge)
- Or `Cmd + Shift + Delete` (Mac)
- Select "All time"
- Clear cache

#### Step 4: Refresh Page
```
Press F5 or Ctrl + R to refresh the page
Wait for it to fully load
Try generating again
```

---

## Common Errors & Solutions

### Error 1: "No data available for report"
**Cause**: You haven't logged any expenses, meals, or habits
**Solution**: 
1. Go to Dashboard
2. Log at least one of:
   - Expense (Finance module)
   - Meal (Health module)
   - Habit (Health module)
3. Try generating report again

### Error 2: "API Error - GEMINI_API_KEY not configured"
**Cause**: The Gemini API key is not set in the system
**Solution**:
1. Contact your system administrator
2. They need to set GEMINI_API_KEY in .env file
3. Restart the application

### Error 3: "Request timeout - API not responding"
**Cause**: Gemini API is slow or unreachable
**Solution**:
1. Wait 30-60 seconds
2. Try again
3. If it keeps happening, try later

### Error 4: "Database error - Unable to save report"
**Cause**: Database connection issue
**Solution**:
1. Refresh page
2. Try again
3. Contact administrator if persists

### Error 5: "Invalid data format"
**Cause**: Data in database is corrupted or in wrong format
**Solution**:
1. Delete problematic expense/meal/habit
2. Re-enter the data
3. Try generating report again

---

## Troubleshooting Checklist

- [ ] Do I have data logged (expenses, meals, or habits)?
- [ ] Is my internet connection working?
- [ ] Have I refreshed the page (F5)?
- [ ] Have I cleared browser cache?
- [ ] Is the application running without errors?
- [ ] Has it been more than 30 seconds since I clicked generate?

---

## Debug Information

If none of the above helps, collect this information:

### 1. What error message do you see exactly?
Write down the exact error text

### 2. What steps did you take before the error?
- [ ] Logged in
- [ ] Added data
- [ ] Clicked "Generate New Report"
- [ ] Anything else?

### 3. Check browser console for errors
1. Press F12 to open Developer Tools
2. Click "Console" tab
3. Copy any red error messages

### 4. Check application logs
Run the diagnostic script:
```bash
python diagnose_report_error.py
```

### 5. Report findings to support
Include:
- Exact error message
- Steps you took
- Browser console errors
- Diagnostic output

---

## Advanced Troubleshooting

### For Administrators

#### Check Database
```sql
-- Check if reports table exists
SELECT TABLE_NAME FROM information_schema.TABLES WHERE TABLE_NAME = 'ai_reports';

-- Check recent reports
SELECT * FROM ai_reports ORDER BY created_at DESC LIMIT 5;

-- Check for errors in reports
SELECT * FROM ai_reports WHERE content LIKE '%error%';
```

#### Check Application Logs
```bash
# Watch live logs
tail -f /var/log/lifeos_app.log

# Search for errors
grep "ERROR" /var/log/lifeos_app.log

# Get last 50 lines
tail -50 /var/log/lifeos_app.log
```

#### Verify Configuration
```bash
# Check if GEMINI_API_KEY is set
echo $GEMINI_API_KEY

# Verify database connection
python -c "from app import db; print('Database OK')"

# Test API key
python -c "import google.generativeai as genai; print('Gemini OK')"
```

#### Run Full Diagnostic
```bash
python diagnose_report_error.py
```

---

## Getting Help

**If you see an error**:
1. Take a screenshot
2. Note the exact error message
3. Tell us:
   - What you were doing
   - What error appeared
   - What browser you're using
   - Any additional info

**Contact Support**:
- Share diagnostic output: `python diagnose_report_error.py`
- Include browser console errors (F12 → Console)
- Provide exact error message

---

## Success Indicators

### Report Generated Successfully
- ✅ Loading spinner appears
- ✅ Progress bar animates
- ✅ Page redirects to new report
- ✅ Report shows all sections
- ✅ No error messages

### Common Misconceptions
❌ "The report is loading forever" = Normal (5-30 seconds is OK)
❌ "I got redirected but no report" = Refresh page, it should appear
❌ "I see JSON/data instead of report" = Refresh, browser cache issue
✅ "I see a beautiful formatted report" = Success!

---

## Prevention Tips

1. **Keep data up-to-date**: Log expenses, meals, and habits regularly
2. **Refresh occasionally**: Keep browser fresh
3. **Stable internet**: Ensure good connection
4. **Check API status**: Gemini API is usually very stable
5. **One report per week**: Generating multiple daily is unnecessary

---

## Still Having Issues?

**Run this**:
```bash
python diagnose_report_error.py
```

**Then**:
1. Check output for any errors
2. Share the output with support
3. Include exact error message from your screen

The diagnostic will test every component and identify the exact problem!

---

**Last Updated**: April 18, 2026
**Status**: Updated for v2.0 Weekly Reports Feature

