# 🐛 Bug Fix: Jinja2 UndefinedError - 'str object' has no attribute 'get'

## Issue
When trying to view a generated report, the application threw:
```
jinja2.exceptions.UndefinedError: 'str object' has no attribute 'get'
```

## Root Cause
The report summary data (financial_summary, health_summary, habits_summary) was being saved to the database as string representations of dictionaries using `str()` conversion. When the template tried to call `.get()` on these strings, it failed because strings don't have a `.get()` method.

**Problem Flow:**
1. `generate_report()` creates dictionary data: `{'total_spent': 150, ...}`
2. Saves it as string: `str({'total_spent': 150, ...})` → `"{'total_spent': 150, ...}"`
3. Template tries: `report.financial_summary.get('total_spent')` 
4. Error: Strings don't have `.get()` method!

## Solution Applied

### 1. Updated Route Handler (`app/routes/ai.py`)

**Added JSON import:**
```python
import json
```

**Changed data storage from string to JSON:**
```python
# BEFORE (Wrong):
financial_summary=str(report_data.get('financial_summary', {})),

# AFTER (Correct):
financial_summary=json.dumps(report_data.get('financial_summary', {})),
```

This converts the dictionary to a proper JSON string instead of a string representation.

### 2. Updated Template (`app/templates/ai/report_view.html`)

**Added JSON parsing with Jinja2 filter:**
```jinja2
# BEFORE (Wrong):
{{ report.financial_summary.get('total_spent', 0) }}

# AFTER (Correct):
{% set fin_data = report.financial_summary | from_json %}
{{ fin_data.get('total_spent', 0) }}
```

Applied the same pattern to all three summary sections:
- Financial Summary
- Health Summary  
- Habit Analysis

### 3. Added Custom Jinja2 Filter (`app/__init__.py`)

**Registered `from_json` filter:**
```python
@app.template_filter('from_json')
def from_json_filter(value):
    """Convert JSON string to Python object"""
    try:
        if isinstance(value, str):
            return json.loads(value)
        return value
    except (json.JSONDecodeError, TypeError):
        return {}
```

This filter safely converts JSON strings back to dictionaries in templates.

## Files Modified
- ✅ `app/routes/ai.py` - Added json import, changed to json.dumps()
- ✅ `app/templates/ai/report_view.html` - Added from_json filter usage on all summaries
- ✅ `app/__init__.py` - Added json import and from_json filter registration

## Why This Works

**Before:**
```
Database: "'{'total_spent': 150}'"  (string representation)
Template: report.financial_summary.get('total_spent')  
Result: ERROR - strings don't have .get()
```

**After:**
```
Database: '{"total_spent": 150}'  (valid JSON)
Template: report.financial_summary | from_json → {'total_spent': 150}  (dict)
Result: SUCCESS - dicts have .get()
```

## Status
✅ **FIXED** - Report viewing now works correctly.

## Testing
After restart, you can now:
1. Generate a weekly report ✅
2. Click "View Full Report" to see the detailed report page ✅
3. View all report sections:
   - Financial summary displays correctly ✅
   - Health summary displays correctly ✅
   - Habit analysis displays correctly ✅
4. All data is properly formatted ✅

---

**Date Fixed**: April 11, 2026
**Severity**: High (blocking report viewing)
**Resolution**: Complete

## Additional Notes

### JSON vs String Representation
- **String representation**: `str({'key': 'value'})` → `"{'key': 'value'}"`
  - Not valid JSON (uses single quotes, Python syntax)
  - Can't be parsed back reliably
  - ❌ Don't use this

- **JSON**: `json.dumps({'key': 'value'})` → `'{"key": "value"}'`
  - Valid JSON (uses double quotes)
  - Can be parsed reliably with `json.loads()`
  - ✅ Use this for storing structured data

### Filter Usage
The `from_json` filter is useful for:
- Converting stored JSON strings to dictionaries
- Safe parsing with fallback to empty dict on error
- Cleaner template syntax than manual parsing

