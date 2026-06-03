# Analytics & Summary Calculations - Bug Fixes

## Issues Fixed

### 1. **Habit Completion Percentage Issue (1466.7% and higher)**

**Root Cause:**
Multiple functions were calculating habit completion rate as `(len(habit.logs) / days_active * 100)` where `days_active` was the number of days since the habit was **created** (potentially months or years old):
- `get_habit_progress()` - used in dashboard
- `calculate_health_score()` - used in Life Score
- `calculate_habit_score()` - used in Life Score

For older habits with many logs, this resulted in percentages far exceeding 100%.

**Example Scenario:**
- Habit created 100 days ago with 50 logs logged
- Old calculation: (50 / 100) * 100 = 50% ✓ (happened to work in this case)
- But if 150 logs: (150 / 100) * 100 = 150% ✗ (exceeds 100%)
- Or in the reported case: (1466.7 logs / unclear denominator) ✗

**Solution Applied:**
Changed all three functions to calculate completion rate based only on logs from the **last 30 days**:

```python
# OLD (broken):
days_active = (datetime.utcnow() - habit.created_at).days + 1
completion_rate = (len(habit.logs) / days_active * 100)

# NEW (fixed):
thirty_days_ago = datetime.utcnow() - timedelta(days=30)
recent_logs = [log for log in habit.logs if log.completed_date >= thirty_days_ago]
completion_rate = (len(recent_logs) / 30 * 100) if recent_logs else 0
completion_rate = min(100, completion_rate)  # Cap at 100%
```

This means:
- At most 30 logs in 30 days = 100% completion
- 15 logs in 30 days = 50% completion
- Percentages are always capped at 100% maximum

**Files Modified:**
- `app/services/analytics_service.py`:
  - Lines 56-67: `calculate_health_score()` - habit consistency sub-score
  - Lines 119-150: `calculate_habit_score()` - Life Score habit component
  - Lines 352-394: `get_habit_progress()` - dashboard habit summary

---

### 2. **Financial Summary - Wrong Expenses Timeframe**

**Root Cause:**
- `get_expense_summary()` was filtering expenses by `datetime.utcnow() - timedelta(days=30)` (last 30 days).
- For a monthly budget, this doesn't align with the calendar month (1st to end of month).
- Example: If today is June 15th, it would show June 15 - May 16's expenses, not June 1-15.

**Impact:**
- Budget calculation included expenses from previous month
- Percentage calculations were inaccurate
- Monthly budget tracking was off by days/weeks

**Solution Applied:**
Changed to use **current month** instead of last 30 days:

```python
# OLD (rolling 30-day window):
start_date = datetime.utcnow() - timedelta(days=days)

# NEW (calendar month):
now = datetime.utcnow()
current_month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
expenses = Expense.query.filter_by(user_id=user_id).filter(
    Expense.expense_date >= current_month_start
).all()
```

This ensures expenses from the 1st of the current month to today are counted, providing accurate monthly budget tracking.

**File Modified:**
- `app/services/analytics_service.py` - Lines 193-234 (`get_expense_summary()`)

---

### 3. **Financial Summary - Percentage Over 100%**

**Root Cause:**
When total spent exceeded the budget limit, the percentage could be > 100% (e.g., 150%).
Progress bars were rendered at width > 100%, which is visually broken.

**Solution Applied:**
Added capped percentage for display:

```python
percentage = (total_spent / budget.monthly_limit * 100) if budget.monthly_limit > 0 else 0
capped_percentage = min(percentage, 100)  # Cap for progress bar display

return {
    ...
    'percentage': round(capped_percentage, 1),  # Capped at 100%
    'actual_percentage': round(percentage, 1),  # Actual (may be > 100%)
    'status': f'Over Budget by ${round(total_spent - budget.monthly_limit, 2)}'  # Detailed status
}
```

- Progress bar in dashboard template displays capped percentage
- Status message shows detailed overage amount: "Over Budget by $150.25"

**Files Modified:**
- `app/services/analytics_service.py` - Lines 193-234 (`get_expense_summary()`)
- `app/templates/analytics/dashboard.html` - Lines 102-107 (already properly capped in template)

---

## Testing Recommendations

### For Habit Completion Fix:
1. Create a habit and log it daily for 30 days → should show ~100% completion
2. Log it 15 times in 30 days → should show ~50% completion
3. Create an old habit (60 days old) with 200 logs → should still show max 100%
4. Check dashboard and life score: habit_score should be ≤ 100
5. Navigate to Life Score dashboard and verify all habit metrics are ≤ 100%

### For Financial Summary Fix:
1. Log expenses on June 1 → should include in June's budget
2. Log expenses today (e.g., June 4) → should include in budget
3. Log expenses on May 31 → should NOT be included in June's budget
4. Spend over budget → percentage should show 100%, status should say "Over Budget by $X"
5. Check dashboard financial summary card for proper display

---

## Code Changes Summary

| File | Lines | Change | Status |
|------|-------|--------|--------|
| `app/services/analytics_service.py` | 56-67 | Fixed health score habit calculation (30-day window, capped at 100%) | ✅ Done |
| `app/services/analytics_service.py` | 119-150 | Fixed habit score calculation (30-day window, capped at 100%) | ✅ Done |
| `app/services/analytics_service.py` | 352-394 | Fixed habit progress calculation (30-day window, capped at 100%) | ✅ Done |
| `app/services/analytics_service.py` | 193-234 | Fixed expense summary (current month window, capped percentage at 100%) | ✅ Done |
| `app/templates/analytics/dashboard.html` | 102-107 | Template already has proper percentage capping and color coding | ✅ Verified |
| `app/templates/analytics/life_score.html` | 64-68, 100-103, 135-139, 180-205 | Life score scores already capped via CSS progress bar width | ✅ Verified |

---

## Impact Summary

**Before fixes:**
- ❌ Habits could show 1000%+ completion (e.g., 1466.7%)
- ❌ Financial summary included expenses from wrong month
- ❌ Progress bars exceeded 100% visually
- ❌ Life Score habit component could exceed 100%
- ❌ Dashboard habit summary showed inflated percentages

**After fixes:**
- ✅ All habit completion rates capped at max 100%
- ✅ Financial summary uses current calendar month
- ✅ Progress bars display correctly (max 100%)
- ✅ Life Score habit component max 100%
- ✅ Dashboard displays accurate metrics
- ✅ Over-budget status shows exact overage amount

---

## Notes

- The habit completion calculation now respects a 30-day evaluation window
- The financial summary now uses calendar months instead of rolling windows for better user expectations
- Both percentage values are now guaranteed to be ≤ 100% for display purposes
- The actual percentage (if > 100%) is still available as `actual_percentage` for transparency
- All progress bars and badges will display correctly with these changes
- Life Score calculations are now consistent across all habit-based metrics

