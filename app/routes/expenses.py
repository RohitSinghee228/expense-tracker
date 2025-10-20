"""
API routes for expense operations
"""
from fastapi import APIRouter, Depends, HTTPException, Request, Query
from fastapi.responses import HTMLResponse, Response
from fastapi.templating import Jinja2Templates
from sqlmodel import Session
from typing import Optional
from datetime import date as DateType

from app.database import get_session
from app.models import Expense, ExpenseCreate, ExpenseSummary
from app.services import ExpenseService

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
async def home(
    request: Request,
    category: Optional[str] = Query(None, description="Filter by category"),
    start_date: Optional[DateType] = Query(None, description="Filter by start date"),
    end_date: Optional[DateType] = Query(None, description="Filter by end date"),
    session: Session = Depends(get_session)
):
    """Home page with expense list and add form"""
    expenses = ExpenseService.get_all_expenses(session, category, start_date, end_date)
    categories = ExpenseService.get_all_categories(session)
    
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "expenses": expenses,
            "categories": categories,
            "selected_category": category,
            "start_date": start_date,
            "end_date": end_date
        }
    )


@router.get("/summary", response_class=HTMLResponse)
async def summary_page(
    request: Request,
    category: Optional[str] = Query(None, description="Filter by category"),
    start_date: Optional[DateType] = Query(None, description="Filter by start date"),
    end_date: Optional[DateType] = Query(None, description="Filter by end date"),
    session: Session = Depends(get_session)
):
    """Summary page with expense analytics"""
    summary = ExpenseService.get_summary(session, category, start_date, end_date)
    categories = ExpenseService.get_all_categories(session)
    
    return templates.TemplateResponse(
        "summary.html",
        {
            "request": request,
            "summary": summary,
            "categories": categories,
            "selected_category": category,
            "start_date": start_date,
            "end_date": end_date
        }
    )


@router.post("/add_expense")
async def add_expense(
    expense: ExpenseCreate,
    session: Session = Depends(get_session)
):
    """Add a new expense (API endpoint)"""
    try:
        new_expense = ExpenseService.create_expense(session, expense)
        return {
            "success": True,
            "message": "Expense added successfully",
            "expense": new_expense
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/expenses")
async def get_expenses(
    category: Optional[str] = Query(None),
    start_date: Optional[DateType] = Query(None),
    end_date: Optional[DateType] = Query(None),
    session: Session = Depends(get_session)
) -> list[Expense]:
    """Get all expenses (API endpoint)"""
    return ExpenseService.get_all_expenses(session, category, start_date, end_date)


@router.get("/api/summary")
async def get_summary(
    category: Optional[str] = Query(None),
    start_date: Optional[DateType] = Query(None),
    end_date: Optional[DateType] = Query(None),
    session: Session = Depends(get_session)
) -> ExpenseSummary:
    """Get expense summary (API endpoint)"""
    return ExpenseService.get_summary(session, category, start_date, end_date)


@router.get("/export")
async def export_expenses(session: Session = Depends(get_session)):
    """Export all expenses as CSV"""
    csv_content = ExpenseService.export_to_csv(session)
    
    return Response(
        content=csv_content,
        media_type="text/csv",
        headers={
            "Content-Disposition": "attachment; filename=expenses.csv"
        }
    )

