"""
AI Suggestions Service
Business logic for AI-powered recommendations
"""
from datetime import datetime, timedelta
from app.services.finance_service import FinanceService


class AISuggestionsService:
    """Service for AI-powered suggestions and insights"""

    @staticmethod
    def get_saving_suggestions(user_id):
        """
        Generate saving suggestions based on spending patterns

        Args:
            user_id: User ID

        Returns:
            List of suggestions
        """
        suggestions = []

        try:
            # Get last 3 months spending
            trends = FinanceService.get_spending_trends(user_id, months=3)
            category_breakdown = FinanceService.get_category_breakdown(user_id)

            # Analyze spending patterns - improved to work with minimal data
            if trends and len(trends) > 0:
                # Filter out zero values for better average
                non_zero_spending = [t['total'] for t in trends if t['total'] > 0]

                if non_zero_spending:
                    avg_spending = sum(non_zero_spending) / len(non_zero_spending)
                    current_month = trends[-1]['total']

                    # Suggest if spending is above average (only if we have data)
                    if current_month > 0 and avg_spending > 0 and current_month > avg_spending * 1.2:
                        suggestions.append({
                            'type': 'spending_spike',
                            'title': 'High Spending Detected',
                            'message': f'Your spending is {((current_month / avg_spending - 1) * 100):.1f}% above your average. Consider reviewing your expenses.',
                            'severity': 'warning'
                        })
                    elif current_month > 0 and avg_spending > 0:
                        # Add positive feedback if spending is normal
                        suggestions.append({
                            'type': 'spending_normal',
                            'title': 'On Track',
                            'message': f'Your spending is normal. You\'ve spent ${current_month:.2f} this month, consistent with your habits.',
                            'severity': 'success'
                        })

            # Analyze category spending
            if category_breakdown:
                sorted_categories = sorted(category_breakdown.items(), key=lambda x: x[1], reverse=True)
                top_category = sorted_categories[0]

                if top_category[1] > 0:
                    total_spending = sum(category_breakdown.values())
                    percentage = (top_category[1] / total_spending) * 100 if total_spending > 0 else 0

                    if percentage > 40:
                        suggestions.append({
                            'type': 'category_high',
                            'title': f'High {top_category[0]} Spending',
                            'message': f'{top_category[0]} accounts for {percentage:.1f}% of your spending. Look for ways to optimize.',
                            'severity': 'info'
                        })
            else:
                # No spending data yet - provide helpful message
                if not suggestions:
                    suggestions.append({
                        'type': 'no_data',
                        'title': 'Get Started',
                        'message': 'Log more expenses to get personalized recommendations and insights about your spending patterns.',
                        'severity': 'info'
                    })

            return suggestions
        except Exception as e:
            return []

    @staticmethod
    def get_budget_insights(user_id):
        """
        Get budget-related insights

        Args:
            user_id: User ID

        Returns:
            Budget insights dictionary
        """
        try:
            budget_status = FinanceService.check_budget_status(user_id)

            if not budget_status:
                return None

            insights = {
                'current_status': budget_status,
                'recommendations': []
            }

            # Generate recommendations based on budget status
            if budget_status['is_over_budget']:
                insights['recommendations'].append({
                    'type': 'over_budget',
                    'message': f"You've exceeded your monthly budget by ${abs(budget_status['remaining']):.2f}",
                    'severity': 'danger'
                })
            elif budget_status['percentage_used'] > 80:
                insights['recommendations'].append({
                    'type': 'near_budget_limit',
                    'message': f'You have only {100 - budget_status["percentage_used"]:.1f}% of your budget remaining',
                    'severity': 'warning'
                })
            else:
                insights['recommendations'].append({
                    'type': 'good_spending',
                    'message': 'Great job! You are within your budget.',
                    'severity': 'success'
                })

            return insights
        except Exception as e:
            return None

    @staticmethod
    def get_ai_message(suggestion_type):
        """
        Get AI-generated message for a suggestion

        Args:
            suggestion_type: Type of suggestion

        Returns:
            AI message (placeholder for Gemini API integration)
        """
        messages = {
            'spending_spike': 'Consider analyzing your recent purchases to identify unnecessary expenses.',
            'category_high': 'Try reducing discretionary spending in this category by 10-15%.',
            'over_budget': 'Review your recent transactions and identify items to return or cancel.',
            'near_budget_limit': 'Plan your remaining expenses carefully for the rest of the month.',
            'good_spending': 'Maintain this spending pattern to achieve your financial goals!'
        }

        return messages.get(suggestion_type, 'Keep tracking your expenses to get better insights.')

    @staticmethod
    def get_expense_prediction(user_id, months_ahead=1):
        """
        Predict future expenses based on historical data

        Args:
            user_id: User ID
            months_ahead: Number of months to predict

        Returns:
            Predicted spending
        """
        try:
            # Get last 6 months of data
            trends = FinanceService.get_spending_trends(user_id, months=6)

            if not trends or len(trends) < 3:
                return None

            # Simple average prediction
            totals = [t['total'] for t in trends[-3:]]  # Last 3 months
            predicted_avg = sum(totals) / len(totals)

            predictions = []
            for i in range(1, months_ahead + 1):
                date = datetime.utcnow() + timedelta(days=30 * i)
                predictions.append({
                    'year': date.year,
                    'month': date.month,
                    'month_name': date.strftime('%B'),
                    'predicted_spending': predicted_avg,
                    'confidence': 0.65  # Simple confidence score
                })

            return predictions
        except Exception as e:
            return None

