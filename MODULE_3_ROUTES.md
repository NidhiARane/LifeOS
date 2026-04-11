# Module 3: Routes & Endpoints Reference

## Complete Routes Listing

### 🍽️ MEAL ROUTES

#### Dashboard & Display
```
GET /health/meals
├─ Purpose: View meals dashboard with daily summary
├─ Auth: Required (login_required)
├─ Parameters: page (int) - pagination
├─ Response: meals.html template
└─ Features: Daily stats, meal history, pagination
```

#### Log Meal
```
GET /health/meal/log
├─ Purpose: Display meal logging form
├─ Auth: Required
└─ Response: log_meal.html template

POST /health/meal/log
├─ Purpose: Create new meal entry
├─ Auth: Required
├─ Form Data:
│  ├─ meal_name (string, required)
│  ├─ description (string, optional)
│  ├─ meal_type (breakfast|lunch|dinner|snack, required)
│  ├─ calories (float, required)
│  ├─ protein (float, required)
│  ├─ carbs (float, optional)
│  ├─ fat (float, optional)
│  └─ meal_date (ISO datetime, required)
├─ Response: Redirect to meals_dashboard
└─ Success Flash: "Meal '{name}' logged successfully!"
```

#### Delete Meal
```
POST /health/meal/<meal_id>/delete
├─ Purpose: Delete a meal entry
├─ Auth: Required
├─ Authorization: User must own the meal
├─ Response: Redirect to meals_dashboard
└─ Success Flash: "Meal '{name}' deleted successfully!"
```

#### Meal Summary API
```
GET /health/api/meals-summary
├─ Purpose: Get meal data for last 7 days (API)
├─ Auth: Required
├─ Response Type: JSON
├─ Response Format:
│  {
│    "2025-04-10": {
│      "calories": 2150,
│      "protein": 85,
│      "carbs": 250,
│      "fat": 65,
│      "meals": [...]
│    }
│  }
└─ Use: AJAX calls, integrations
```

---

### 🏃 HABIT ROUTES

#### Habits Dashboard
```
GET /health/habits
├─ Purpose: View all habits with consistency scores
├─ Auth: Required
├─ Response: habits.html template
└─ Features: Habit list, streaks, consistency scores
```

#### Create Habit Form
```
GET /health/habit/create
├─ Purpose: Display habit creation form
├─ Auth: Required
└─ Response: create_habit.html template
```

#### Create Habit
```
POST /health/habit/create
├─ Purpose: Create new habit
├─ Auth: Required
├─ Form Data:
│  ├─ habit_name (string, required)
│  ├─ description (string, optional)
│  ├─ category (string, optional)
│  │  └─ Options: health|productivity|learning|wellness|social|finance|other
│  ├─ frequency (string, required)
│  │  └─ Options: daily|weekly|custom
│  └─ target (int, default: 1)
├─ Response: Redirect to habits_dashboard
└─ Success Flash: "Habit '{name}' created successfully!"
```

#### Check In Habit (AJAX)
```
POST /health/habit/<habit_id>/checkin
├─ Purpose: Daily habit check-in with streak tracking
├─ Auth: Required
├─ Authorization: User must own the habit
├─ Content-Type: application/json
├─ Response Type: JSON
├─ Success Response:
│  {
│    "status": "success",
│    "current_streak": 5,
│    "longest_streak": 7
│  }
├─ Error Response:
│  {
│    "error": "Already checked in today" (HTTP 400)
│  }
└─ Features: Automatic streak calculation, daily limit
```

#### Delete Habit
```
POST /health/habit/<habit_id>/delete
├─ Purpose: Delete a habit
├─ Auth: Required
├─ Authorization: User must own the habit
├─ Response: Redirect to habits_dashboard
└─ Success Flash: "Habit '{name}' deleted successfully!"
```

#### Habits Summary API
```
GET /health/api/habits-summary
├─ Purpose: Get habit statistics (API)
├─ Auth: Required
├─ Response Type: JSON
├─ Response Format:
│  {
│    "total_habits": 5,
│    "active_habits": 4,
│    "habits": [...]
│  }
└─ Use: Dashboard widgets, analytics
```

---

### 🎯 GOAL ROUTES

#### Goals Dashboard
```
GET /health/goals
├─ Purpose: View all goals organized by category
├─ Auth: Required
├─ Response: goals.html template
└─ Features: Category organization, progress tracking
```

#### Create Goal Form
```
GET /health/goal/create
├─ Purpose: Display goal creation form
├─ Auth: Required
└─ Response: create_goal.html template
```

#### Create Goal
```
POST /health/goal/create
├─ Purpose: Create new goal
├─ Auth: Required
├─ Form Data:
│  ├─ goal_title (string, required)
│  ├─ description (string, optional)
│  ├─ category (string, required)
│  │  └─ Options: health|financial|learning|fitness|career|social|personal
│  ├─ target_value (float, required)
│  ├─ unit (string, required)
│  │  └─ Examples: kg, $, books, km, hours
│  ├─ target_date (ISO date, optional)
│  └─ priority (string, default: medium)
│     └─ Options: low|medium|high
├─ Response: Redirect to goals_dashboard
└─ Success Flash: "Goal '{title}' created successfully!"
```

#### Update Goal Progress (AJAX)
```
POST /health/goal/<goal_id>/update-progress
├─ Purpose: Update goal progress (AJAX)
├─ Auth: Required
├─ Authorization: User must own the goal
├─ Content-Type: application/json
├─ Request Body:
│  {
│    "current_value": 7.5
│  }
├─ Response Type: JSON
├─ Success Response:
│  {
│    "status": "success",
│    "current_value": 7.5,
│    "progress": 75.0
│  }
├─ Error Response:
│  {
│    "error": "Error message" (HTTP 500)
│  }
└─ Features: Auto completion detection, progress calculation
```

#### Delete Goal
```
POST /health/goal/<goal_id>/delete
├─ Purpose: Delete a goal
├─ Auth: Required
├─ Authorization: User must own the goal
├─ Response: Redirect to goals_dashboard
└─ Success Flash: "Goal '{title}' deleted successfully!"
```

#### Goals Summary API
```
GET /health/api/goals-summary
├─ Purpose: Get goal statistics (API)
├─ Auth: Required
├─ Response Type: JSON
├─ Response Format:
│  {
│    "total_goals": 8,
│    "completed_goals": 2,
│    "goals": [...]
│  }
└─ Use: Analytics, dashboard widgets
```

---

## 🔐 Authentication & Authorization

### Authentication
- All routes require `@login_required` decorator
- Uses Flask-Login session management
- Redirects to login page if not authenticated

### Authorization
- User can only access their own data
- User ID validation on all operations
- Returns 403 Forbidden if unauthorized

---

## 📡 API Response Patterns

### Success Response (AJAX)
```json
{
  "status": "success",
  "data": {}
}
```

### Error Response (AJAX)
```json
{
  "error": "Error message"
}
```

### HTTP Status Codes
- **200 OK**: Success
- **400 Bad Request**: Validation error
- **403 Forbidden**: Unauthorized
- **404 Not Found**: Resource not found
- **500 Internal Server Error**: Server error

---

## 🧪 Testing Routes

### Using cURL (Command Line)

#### Get Meals
```bash
curl -X GET http://localhost:5000/health/meals \
  -H "Content-Type: application/json"
```

#### Check In Habit
```bash
curl -X POST http://localhost:5000/health/habit/1/checkin \
  -H "Content-Type: application/json"
```

#### Update Goal
```bash
curl -X POST http://localhost:5000/health/goal/1/update-progress \
  -H "Content-Type: application/json" \
  -d '{"current_value": 7.5}'
```

#### Get Meals Summary
```bash
curl -X GET http://localhost:5000/health/api/meals-summary
```

---

## 📊 URL Patterns Summary

### Pattern Base
```
/health/[resource]/[action]
```

### Examples
```
/health/meals                          - GET, display meals
/health/meal/log                       - GET (form), POST (submit)
/health/meal/1/delete                  - POST
/health/habits                         - GET
/health/habit/create                   - GET, POST
/health/habit/1/checkin                - POST
/health/habit/1/delete                 - POST
/health/goals                          - GET
/health/goal/create                    - GET, POST
/health/goal/1/update-progress         - POST
/health/goal/1/delete                  - POST
/health/api/meals-summary              - GET
/health/api/habits-summary             - GET
/health/api/goals-summary              - GET
```

---

## 🔄 Data Flow Examples

### Meal Logging Flow
```
1. User clicks "Log Meal"
2. GET /health/meal/log → Display form
3. User fills form → POST /health/meal/log
4. Backend creates Meal record
5. Redirect to GET /health/meals
6. Display updated meal list with daily stats
```

### Habit Check-in Flow
```
1. User clicks "Check In Today" button
2. AJAX POST /health/habit/1/checkin
3. Backend creates HabitLog entry
4. Backend calculates streak
5. Return JSON with new streak values
6. JavaScript updates UI with toast notification
7. Page auto-refreshes (optional)
```

### Goal Progress Update Flow
```
1. User clicks "Update Progress"
2. Modal opens with current value
3. User enters new value
4. JavaScript AJAX POST /health/goal/1/update-progress
5. Backend calculates progress percentage
6. Backend updates is_completed if >= 100%
7. Return JSON with new progress
8. JavaScript closes modal
9. Page reloads to show updated goal
```

---

## 🛡️ Error Handling

### Common Errors

#### 400 Bad Request
- **Cause**: Missing required fields, invalid data type
- **Example**: POST meal without calories
- **Response**: Flash message, form stays open

#### 403 Forbidden
- **Cause**: Trying to modify someone else's data
- **Example**: Delete another user's meal
- **Response**: Redirect with error flash

#### 404 Not Found
- **Cause**: Resource doesn't exist
- **Example**: GET /health/meal/999 (doesn't exist)
- **Response**: 404 template displayed

#### 500 Internal Server Error
- **Cause**: Database error, unexpected exception
- **Response**: 500 template, error logged

---

## 📝 Form Field Validation

### Meal Form
- meal_name: Required, string, max 200 chars
- meal_type: Required, from predefined list
- calories: Required, float > 0
- protein: Required, float >= 0
- carbs: Optional, float >= 0
- fat: Optional, float >= 0
- meal_date: Required, valid datetime

### Habit Form
- habit_name: Required, string, max 200 chars
- description: Optional, text
- category: Optional, from predefined list
- frequency: Required, from predefined list
- target: Optional, integer >= 1

### Goal Form
- goal_title: Required, string, max 200 chars
- description: Optional, text
- category: Required, from predefined list
- target_value: Required, float > 0
- unit: Required, string, max 50 chars
- target_date: Optional, valid date
- priority: Optional, from predefined list

---

**Last Updated**: April 11, 2026
**Module**: 3 - Health, Meal & Habit Management
**Status**: Complete ✅

