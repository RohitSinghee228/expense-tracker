"""
Service layer for expense operations
"""
from sqlmodel import Session, select, func
from app.models import Expense, ExpenseCreate, ExpenseSummary, CategorySummary
from typing import Optional
from datetime import date as DateType
import csv
from io import StringIO


class ExpenseService:
    """Service class for managing expenses"""
    
    @staticmethod
    def create_expense(session: Session, expense_data: ExpenseCreate) -> Expense:
        """Create a new expense"""
        expense = Expense.model_validate(expense_data)
        session.add(expense)
        session.commit()
        session.refresh(expense)
        return expense
    
    @staticmethod
    def get_all_expenses(
        session: Session,
        category: Optional[str] = None,
        start_date: Optional[DateType] = None,
        end_date: Optional[DateType] = None
    ) -> list[Expense]:
        """Get all expenses with optional filters"""
        statement = select(Expense).order_by(Expense.date.desc(), Expense.id.desc())
        
        if category:
            statement = statement.where(Expense.category == category)
        if start_date:
            statement = statement.where(Expense.date >= start_date)
        if end_date:
            statement = statement.where(Expense.date <= end_date)
        
        expenses = session.exec(statement).all()
        return expenses
    
    @staticmethod
    def get_expense_by_id(session: Session, expense_id: int) -> Optional[Expense]:
        """Get a single expense by ID"""
        return session.get(Expense, expense_id)
    
    @staticmethod
    def get_summary(
        session: Session,
        category: Optional[str] = None,
        start_date: Optional[DateType] = None,
        end_date: Optional[DateType] = None
    ) -> ExpenseSummary:
        """Get expense summary with category breakdown"""
        # Base query
        base_statement = select(Expense)
        
        # Apply filters
        if category:
            base_statement = base_statement.where(Expense.category == category)
        if start_date:
            base_statement = base_statement.where(Expense.date >= start_date)
        if end_date:
            base_statement = base_statement.where(Expense.date <= end_date)
        
        # Get total expenses and count
        total_statement = select(
            func.sum(Expense.amount).label("total"),
            func.count(Expense.id).label("count")
        )
        if category:
            total_statement = total_statement.where(Expense.category == category)
        if start_date:
            total_statement = total_statement.where(Expense.date >= start_date)
        if end_date:
            total_statement = total_statement.where(Expense.date <= end_date)
        
        result = session.exec(total_statement).first()
        total_expenses = float(result[0] or 0)
        total_count = int(result[1] or 0)
        
        # Get category breakdown
        category_statement = select(
            Expense.category,
            func.sum(Expense.amount).label("total"),
            func.count(Expense.id).label("count")
        ).group_by(Expense.category).order_by(func.sum(Expense.amount).desc())
        
        if category:
            category_statement = category_statement.where(Expense.category == category)
        if start_date:
            category_statement = category_statement.where(Expense.date >= start_date)
        if end_date:
            category_statement = category_statement.where(Expense.date <= end_date)
        
        category_results = session.exec(category_statement).all()
        
        category_breakdown = [
            CategorySummary(category=cat, total=float(total), count=int(count))
            for cat, total, count in category_results
        ]
        
        return ExpenseSummary(
            total_expenses=total_expenses,
            total_count=total_count,
            category_breakdown=category_breakdown
        )
    
    @staticmethod
    def get_all_categories(session: Session) -> list[str]:
        """Get all unique categories"""
        statement = select(Expense.category).distinct().order_by(Expense.category)
        categories = session.exec(statement).all()
        return categories
    
    @staticmethod
    def export_to_csv(session: Session) -> str:
        """Export all expenses to CSV format"""
        expenses = ExpenseService.get_all_expenses(session)
        
        output = StringIO()
        writer = csv.writer(output)
        
        # Write header
        writer.writerow(['ID', 'Date', 'Category', 'Amount', 'Description'])
        
        # Write data
        for expense in expenses:
            writer.writerow([
                expense.id,
                expense.date.strftime('%Y-%m-%d'),
                expense.category,
                f"{expense.amount:.2f}",
                expense.description
            ])
        
        return output.getvalue()

