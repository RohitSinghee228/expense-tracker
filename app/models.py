"""
Database models for the Expense Tracker application
"""
from sqlmodel import SQLModel, Field
from datetime import date as DateType
from typing import Optional


class Expense(SQLModel, table=True):
    """Expense model for storing expense records"""
    
    id: Optional[int] = Field(default=None, primary_key=True)
    amount: float = Field(gt=0, description="Expense amount (must be positive)")
    category: str = Field(min_length=1, max_length=100, description="Expense category")
    date: DateType = Field(description="Date of expense")
    description: str = Field(default="", max_length=500, description="Expense description")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "amount": 50.00,
                "category": "Food",
                "date": "2025-10-20",
                "description": "Lunch at restaurant"
            }
        }
    }


class ExpenseCreate(SQLModel):
    """Model for creating a new expense"""
    
    amount: float = Field(gt=0)
    category: str = Field(min_length=1, max_length=100)
    date: DateType
    description: str = Field(default="", max_length=500)


class CategorySummary(SQLModel):
    """Model for category-wise expense summary"""
    
    category: str
    total: float
    count: int


class ExpenseSummary(SQLModel):
    """Model for overall expense summary"""
    
    total_expenses: float
    total_count: int
    category_breakdown: list[CategorySummary]

