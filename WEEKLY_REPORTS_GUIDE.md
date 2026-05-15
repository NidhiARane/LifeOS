# Weekly Reports Generation Guide - LifeOS

## Overview
Weekly reports are AI-generated summaries of your life management data across financial, health, and habit tracking. They're generated on-demand and stored for your future reference.

## How to Generate Weekly Reports

### Method 1: From Dashboard
1. Go to **Dashboard** (home page after login)
2. Look for **AI Intelligence** card on the right side
3. Click **Weekly Reports** button
4. You'll see the Reports page

### Method 2: Direct Navigation
1. Click on **AI** in the main navigation
2. Select **Weekly Reports**

### Method 3: From Report Page
1. Navigate to the Reports page
2. Click the **Generate New Report** button (green button with + icon)

## What Gets Included in Reports

### Financial Summary
- **Total Spent**: Sum of all expenses in the last 30 days
- **Daily Average**: Average daily spending
- **Top Categories**: Your top 5 spending categories
- **Spending Trend**: Whether spending is increasing, moderate, or stable

### Health Summary
- **Average Daily Calories**: Average calorie intake from logged meals
- **Average Daily Protein**: Average protein consumption
- **Active Habits**: Number of active habits being tracked
- **Habit Consistency**: Percentage of days habits were completed
- **Health Status**: Overall health assessment

### Habit Analysis
- **Total Habits**: Number of habits you're tracking
- **Average Completion Rate**: Percentage of days all habits are completed
- **Individual Habit Performance**:
  - Completion rate percentage
  - Current streak (days)
  - Status (Excellent, Good, Fair, Needs Work)

### AI Summary & Recommendations
- Personalized summary of your week
- Areas of strength to build on
- 3 specific, actionable recommendations for improvement

### Expense Prediction
- Predicted daily expense for the next 30 days
- Based on your historical spending data
- Prediction confidence level

## Important Notes

### Data Requirements
To generate meaningful reports, you need:
- **At least 10 expense records** for accurate expense predictions
- **30+ days of expense data** for higher confidence predictions
- **At least 1 meal logged** for health data
- **At least 1 habit created** for habit analysis

### Report Generation Time
- Reports are generated on-demand (instantly when you click the button)
- If you have limited data, a simplified report will be generated
- Reports with minimal data will show a confidence level indicator

### What Happens if You Have Limited Data?
- Financial insights will still show your recent spending
- Health insights may show as "Fair" or "Needs Improvement"
- Habit analysis will include only the habits you've created
- The AI may provide fallback recommendations if API is unavailable

## Viewing Reports

### List All Reports
1. Go to the **Weekly Reports** page
2. You'll see all your generated reports in a grid layout
3. Each report shows:
   - Title (with date)
   - Week covered
   - Report type
   - Preview of the content

### View Full Report
1. Click **"View Full Report"** on any report card
2. Or click **"View Full Report"** button on the report preview

The full report page shows:
- Complete AI summary
- Detailed financial breakdown
- Complete health metrics
- Individual habit performance table
- Expense predictions
- Report metadata

## Managing Reports

### Delete a Report
1. Go to the **Weekly Reports** page
2. Find the report you want to delete
3. Click the trash icon button on the report card
4. Confirm the deletion

Or from the full report view:
1. Click the **Delete** button in the top right
2. Confirm the deletion

### Export/Save Reports
Currently, reports are stored in the database. To save them:
1. Take a screenshot of the report page
2. Or manually copy the information

## Troubleshooting

### "Error generating report" message
**Solution**: This usually means:
1. You don't have any expense, meal, or habit data logged
2. The AI API is temporarily unavailable
3. Try again in a few moments

### Report shows only partial data
**Reason**: You may not have logged enough data in one or more areas
**Solution**: Log expenses, meals, and habits, then generate another report

### Reports page is empty
**Reason**: You haven't generated any reports yet
**Solution**: Click "Generate Your First Report" button to create one

### Report takes too long to load
**Reason**: The AI API might be slow or the report has lots of data
**Solution**: Wait a moment and refresh the page, or try again later

## Best Practices

1. **Log Data Consistently**
   - Log expenses daily for accurate tracking
   - Log meals to get accurate nutrition insights
   - Complete habits daily for consistency scoring

2. **Generate Reports Weekly**
   - Generate reports at the same time each week (e.g., Sunday)
   - This helps track progress over time

3. **Review and Act**
   - Read the AI recommendations carefully
   - Implement the suggested improvements
   - Review the next week's report to see progress

4. **Use Multiple Reports**
   - Compare reports week-to-week to see trends
   - Identify which recommendations were most helpful
   - Adjust your goals based on patterns

## Technical Details

### Report Storage
- Reports are stored in the `ai_reports` database table
- Each report includes JSON-formatted summaries of financial, health, and habit data
- Reports are linked to your user account and private to you

### Data Freshness
- Reports use data up to the moment of generation
- Expenses from the last 30 days are included
- Meals from the last 7 days are included
- All habits are included

### AI Model
- Reports use Google Gemini 2.5 Flash Lite model
- The model is configured to provide personalized, encouraging advice
- If the API is unavailable, fallback recommendations are provided

## Related Features

- **Chat with AI**: Have real-time conversations for quick insights
- **Analytics Dashboard**: View detailed charts and metrics
- **Life Score**: See your overall personal discipline score
- **Insights Dashboard**: Get specific insights for finance, health, and habits

---

**Last Updated**: April 18, 2026
**Version**: 1.0

