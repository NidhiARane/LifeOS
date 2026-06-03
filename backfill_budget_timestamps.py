#!/usr/bin/env python
"""
Backfill Script for UserBudget updated_at Timestamps
Fixes any NULL updated_at values in user_budgets table
"""

import sys
from datetime import datetime
from app import create_app, db
from app.models.analytics import UserBudget

def backfill_updated_at():
    """Backfill NULL updated_at values in user_budgets table"""
    app = create_app()
    
    with app.app_context():
        try:
            # Find all UserBudget rows with NULL updated_at
            null_count = UserBudget.query.filter(UserBudget.updated_at == None).count()
            
            if null_count == 0:
                print("✅ No NULL updated_at values found. Database is clean!")
                return True
            
            print(f"🔧 Found {null_count} records with NULL updated_at")
            print("🔄 Backfilling with created_at or current time...")
            
            # Update all NULL updated_at with created_at (or current time if created_at is also NULL)
            budgets = UserBudget.query.filter(UserBudget.updated_at == None).all()
            
            for budget in budgets:
                if budget.created_at:
                    budget.updated_at = budget.created_at
                else:
                    budget.updated_at = datetime.utcnow()
            
            # Commit changes
            db.session.commit()
            
            print(f"✅ Successfully backfilled {null_count} records!")
            
            # Verify the fix
            remaining_null = UserBudget.query.filter(UserBudget.updated_at == None).count()
            if remaining_null == 0:
                print("✅ Verification passed: All updated_at values are now set!")
                return True
            else:
                print(f"⚠️  Warning: {remaining_null} records still have NULL updated_at")
                return False
                
        except Exception as e:
            print(f"❌ Error during backfill: {str(e)}")
            db.session.rollback()
            return False

if __name__ == '__main__':
    success = backfill_updated_at()
    sys.exit(0 if success else 1)

