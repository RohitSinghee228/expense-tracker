"""
Unit tests for expense tracking functionality
"""
import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool
from datetime import date as DateType
from pydantic import ValidationError

from app.main import app
from app.database import get_session
from app.models import Expense


# Create in-memory database for testing
@pytest.fixture(name="session")
def session_fixture():
    """Create a test database session"""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    """Create a test client with test database"""
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


def test_add_expense(client: TestClient):
    """Test adding a new expense"""
    expense_data = {
        "amount": 50.00,
        "category": "Food",
        "date": "2025-10-20",
        "description": "Lunch at restaurant"
    }
    
    response = client.post("/add_expense", json=expense_data)
    assert response.status_code == 200
    
    data = response.json()
    assert data["success"] is True
    assert data["message"] == "Expense added successfully"
    assert data["expense"]["amount"] == 50.00
    assert data["expense"]["category"] == "Food"


def test_add_expense_invalid_amount(client: TestClient):
    """Test adding expense with invalid amount"""
    expense_data = {
        "amount": -10.00,  # Negative amount
        "category": "Food",
        "date": "2025-10-20",
        "description": "Invalid expense"
    }
    
    response = client.post("/add_expense", json=expense_data)
    assert response.status_code == 422  # Validation error


def test_get_expenses(client: TestClient):
    """Test retrieving all expenses"""
    # Add some test expenses
    expenses = [
        {"amount": 50.00, "category": "Food", "date": "2025-10-20", "description": "Lunch"},
        {"amount": 100.00, "category": "Transport", "date": "2025-10-19", "description": "Taxi"},
        {"amount": 30.00, "category": "Food", "date": "2025-10-18", "description": "Groceries"}
    ]
    
    for expense in expenses:
        client.post("/add_expense", json=expense)
    
    response = client.get("/expenses")
    assert response.status_code == 200
    
    data = response.json()
    assert len(data) == 3
    assert data[0]["amount"] == 50.00  # Most recent first


def test_get_expenses_with_category_filter(client: TestClient):
    """Test retrieving expenses filtered by category"""
    # Add test expenses
    expenses = [
        {"amount": 50.00, "category": "Food", "date": "2025-10-20", "description": "Lunch"},
        {"amount": 100.00, "category": "Transport", "date": "2025-10-19", "description": "Taxi"},
        {"amount": 30.00, "category": "Food", "date": "2025-10-18", "description": "Groceries"}
    ]
    
    for expense in expenses:
        client.post("/add_expense", json=expense)
    
    response = client.get("/expenses?category=Food")
    assert response.status_code == 200
    
    data = response.json()
    assert len(data) == 2
    assert all(exp["category"] == "Food" for exp in data)


def test_get_expenses_with_date_filter(client: TestClient):
    """Test retrieving expenses filtered by date range"""
    # Add test expenses
    expenses = [
        {"amount": 50.00, "category": "Food", "date": "2025-10-20", "description": "Lunch"},
        {"amount": 100.00, "category": "Transport", "date": "2025-10-19", "description": "Taxi"},
        {"amount": 30.00, "category": "Food", "date": "2025-10-15", "description": "Groceries"}
    ]
    
    for expense in expenses:
        client.post("/add_expense", json=expense)
    
    response = client.get("/expenses?start_date=2025-10-19&end_date=2025-10-20")
    assert response.status_code == 200
    
    data = response.json()
    assert len(data) == 2


def test_get_summary(client: TestClient):
    """Test getting expense summary"""
    # Add test expenses
    expenses = [
        {"amount": 50.00, "category": "Food", "date": "2025-10-20", "description": "Lunch"},
        {"amount": 100.00, "category": "Transport", "date": "2025-10-19", "description": "Taxi"},
        {"amount": 30.00, "category": "Food", "date": "2025-10-18", "description": "Groceries"}
    ]
    
    for expense in expenses:
        client.post("/add_expense", json=expense)
    
    response = client.get("/api/summary")
    assert response.status_code == 200
    
    data = response.json()
    assert data["total_expenses"] == 180.00
    assert data["total_count"] == 3
    assert len(data["category_breakdown"]) == 2
    
    # Check category breakdown
    food_category = next(cat for cat in data["category_breakdown"] if cat["category"] == "Food")
    assert food_category["total"] == 80.00
    assert food_category["count"] == 2


def test_export_csv(client: TestClient):
    """Test exporting expenses to CSV"""
    # Add test expenses
    expenses = [
        {"amount": 50.00, "category": "Food", "date": "2025-10-20", "description": "Lunch"},
        {"amount": 100.00, "category": "Transport", "date": "2025-10-19", "description": "Taxi"}
    ]
    
    for expense in expenses:
        client.post("/add_expense", json=expense)
    
    response = client.get("/export")
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/csv; charset=utf-8"
    assert "Content-Disposition" in response.headers
    
    csv_content = response.text
    assert "ID,Date,Category,Amount,Description" in csv_content
    assert "Food" in csv_content
    assert "Transport" in csv_content


def test_home_page(client: TestClient):
    """Test home page renders correctly"""
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]


def test_summary_page(client: TestClient):
    """Test summary page renders correctly"""
    response = client.get("/summary")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]


def test_expense_model_validation():
    """Test expense model validation"""
    # Valid expense
    expense = Expense(
        amount=50.00,
        category="Food",
        date=DateType(2025, 10, 20),
        description="Lunch"
    )
    assert expense.amount == 50.00
    assert expense.category == "Food"
    assert expense.description == "Lunch"
    
    # Test expense with empty description (should be allowed)
    expense2 = Expense(
        amount=100.00,
        category="Transport",
        date=DateType(2025, 10, 15),
        description=""
    )
    assert expense2.amount == 100.00
    assert expense2.description == ""

