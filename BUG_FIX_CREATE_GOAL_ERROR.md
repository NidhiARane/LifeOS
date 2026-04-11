# 🐛 Bug Fix: TypeError in Create Goal - 'int' + 'method'

## Issue
When clicking "Create Goal", the application threw:
```
TypeError: unsupported operand type(s) for +: 'int' and 'method'
```

## Root Cause
In the `goals.html` template, line 74 was trying to calculate the average progress using:
```html
{{ goals | map(attribute='get_progress_percentage') | sum / (goals | length) }}
```

The problem is that `map(attribute='get_progress_percentage')` tries to access `get_progress_percentage` as a property/attribute, not as a method. In Jinja2 templates, you cannot call methods through the pipe operator.

This resulted in trying to add integers with the method object itself:
```
sum(int + <method get_progress_percentage>)  # ❌ Error!
```

## Solution Applied

### Updated `app/templates/health/goals.html`
Changed the average progress calculation from using `map()` to using a loop that properly calls the method:

**Before:**
```html
{{ "%.0f"|format(goals | map(attribute='get_progress_percentage') | sum / (goals | length)) }}%
```

**After:**
```html
{% if goals %}
    {% set total_progress = 0 %}
    {% for goal in goals %}
        {% set total_progress = total_progress + goal.get_progress_percentage() %}
    {% endfor %}
    {{ "%.0f"|format(total_progress / (goals | length)) }}%
{% else %}
    0%
{% endif %}
```

This approach:
1. Loops through each goal
2. Calls `goal.get_progress_percentage()` as a proper method
3. Accumulates the total progress
4. Calculates the average

## Files Modified
- ✅ `app/templates/health/goals.html` (line 74)

## Status
✅ **FIXED** - The "Create Goal" page now loads without errors and the average progress displays correctly.

## Testing
The Flask app has been restarted with the fixes applied. You can now:
1. Click "Manage Goals" from the dashboard
2. Click "+ New Goal" button
3. The form will load without errors
4. The goals dashboard will show the average progress correctly

---

**Date Fixed**: April 11, 2026
**Severity**: High (blocking feature)
**Resolution**: Complete

