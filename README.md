# 💰 Expense Tracker

A modern, full-stack expense tracking web application built with FastAPI and featuring a beautiful, responsive UI.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## 📋 Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [Testing](#testing)
- [Screenshots](#screenshots)

## ✨ Features

### Core Features
- ➕ **Add Expenses**: Record expenses with amount, category, date, and description
- 📊 **View All Expenses**: See all your expenses in a clean, organized table
- 📈 **Summary Dashboard**: View total spending and category-wise breakdown
- 💾 **SQLite Database**: Persistent local storage for all expense data

### Bonus Features
- 🔍 **Advanced Filtering**: Filter expenses by category and date range
- 📥 **CSV Export**: Download all expenses as a CSV file
- 📱 **Responsive Design**: Beautiful UI that works on all devices
- 🎨 **Modern UI**: Clean, gradient-based design with smooth animations
- ✅ **Full Test Coverage**: Comprehensive pytest test suite

## 🛠️ Tech Stack

- **Backend**: FastAPI (Python)
- **Frontend**: HTML5 + Jinja2 Templates + CSS3
- **Database**: SQLite with SQLModel ORM
- **Server**: Uvicorn (ASGI server)
- **Testing**: pytest + httpx
- **Environment**: Python virtual environment (conda/venv)

## 📁 Project Structure

```
expense-tracker/
├── app/
│   ├── __init__.py              # Application initialization
│   ├── main.py                  # FastAPI application entry point
│   ├── models.py                # SQLModel database models
│   ├── database.py              # Database configuration
│   ├── routes/
│   │   ├── __init__.py
│   │   └── expenses.py          # API routes for expenses
│   ├── services/
│   │   ├── __init__.py
│   │   └── expense_service.py   # Business logic layer
│   ├── templates/
│   │   ├── base.html            # Base template
│   │   ├── index.html           # Home page with expense form
│   │   └── summary.html         # Summary page
│   └── static/
│       └── styles.css           # Modern CSS styles
├── tests/
│   ├── __init__.py
│   └── test_expenses.py         # Test suite
├── .env                         # Environment variables
├── .gitignore                   # Git ignore rules
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- conda (recommended) or venv

### Step 1: Clone or Download the Project

```bash
cd expense-tracker
```

### Step 2: Create Virtual Environment

#### Using conda (Recommended):
```bash
conda create -n expense-tracker python=3.10
conda activate expense-tracker
```

#### Using venv:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Environment Setup

The `.env` file is already configured with default settings:
```env
DATABASE_PATH=expenses.db
HOST=0.0.0.0
PORT=8000
ENVIRONMENT=development
```

You can modify these settings if needed.

## 💻 Usage

### Starting the Application

Run the application using uvicorn:

```bash
uvicorn app.main:app --reload
```

Or directly with Python:

```bash
python -m app.main
```

The application will start on `http://localhost:8000`

### Accessing the Application

- **Home Page (Dashboard)**: `http://localhost:8000/`
- **Summary Page**: `http://localhost:8000/summary`
- **CSV Export**: `http://localhost:8000/export`
- **API Documentation**: `http://localhost:8000/docs` (Swagger UI)
- **Alternative API Docs**: `http://localhost:8000/redoc`

## 📡 API Documentation

### Endpoints

#### 1. Add Expense
```http
POST /add_expense
Content-Type: application/json

{
  "amount": 50.00,
  "category": "Food",
  "date": "2025-10-20",
  "description": "Lunch at restaurant"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Expense added successfully",
  "expense": {
    "id": 1,
    "amount": 50.00,
    "category": "Food",
    "date": "2025-10-20",
    "description": "Lunch at restaurant"
  }
}
```

#### 2. Get All Expenses
```http
GET /expenses?category=Food&start_date=2025-10-01&end_date=2025-10-31
```

**Query Parameters:**
- `category` (optional): Filter by category
- `start_date` (optional): Filter by start date (YYYY-MM-DD)
- `end_date` (optional): Filter by end date (YYYY-MM-DD)

#### 3. Get Summary
```http
GET /api/summary?category=Food&start_date=2025-10-01&end_date=2025-10-31
```

**Response:**
```json
{
  "total_expenses": 180.00,
  "total_count": 3,
  "category_breakdown": [
    {
      "category": "Food",
      "total": 80.00,
      "count": 2
    },
    {
      "category": "Transport",
      "total": 100.00,
      "count": 1
    }
  ]
}
```

#### 4. Export to CSV
```http
GET /export
```

Downloads a CSV file with all expenses.

## 🧪 Testing

Run the test suite:

```bash
pytest
```

Run with coverage:

```bash
pytest --cov=app tests/
```

Run verbose mode:

```bash
pytest -v
```

### Test Coverage

The test suite includes:
- ✅ Adding expenses (valid and invalid)
- ✅ Retrieving all expenses
- ✅ Filtering by category
- ✅ Filtering by date range
- ✅ Summary calculations
- ✅ CSV export functionality
- ✅ Page rendering
- ✅ Model validation

## 🎨 Features Walkthrough

### Adding an Expense

1. Navigate to the home page
2. Fill in the form with:
   - Amount (required, must be positive)
   - Category (required, autocomplete from existing categories)
   - Date (required, defaults to today)
   - Description (optional)
3. Click "Add Expense"
4. See instant feedback and the new expense in the table

### Filtering Expenses

1. Use the filter section on the home page
2. Select a category from the dropdown
3. Choose start and/or end dates
4. Click "Apply Filters"
5. View filtered results
6. Click "Clear Filters" to reset

### Viewing Summary

1. Navigate to the Summary page
2. See total expenses, transaction count, and category count
3. View detailed category breakdown with percentages
4. See visual distribution bars
5. Apply filters to analyze specific periods or categories

### Exporting Data

1. Click "Export CSV" button in the header
2. Download a CSV file with all expense data
3. Open in Excel, Google Sheets, or any spreadsheet application

## 🎯 Learning Outcomes

This project demonstrates:

1. **Project Structure**: Clean, modular organization with separation of concerns
2. **FastAPI Integration**: RESTful API development with automatic documentation
3. **Database Management**: SQLite integration with SQLModel ORM
4. **Template Rendering**: Server-side rendering with Jinja2
5. **Frontend Development**: Modern, responsive UI with CSS3
6. **Testing**: Comprehensive test coverage with pytest
7. **Dependency Management**: Professional Python project setup
8. **Environment Configuration**: Using .env files for configuration

## 🔧 Configuration

### Database

By default, the application creates `expenses.db` in the project root. To change the database location, modify the `DATABASE_PATH` in the `.env` file.

### Server Settings

Modify these in `.env`:
- `HOST`: Server host (default: 0.0.0.0)
- `PORT`: Server port (default: 8000)

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests

## 📝 License

This project is open source and available under the MIT License.

## 👤 Author

Created as an intern assignment project to demonstrate full-stack development skills.

## 🙏 Acknowledgments

- FastAPI for the excellent web framework
- SQLModel for the intuitive ORM
- The Python community for amazing tools and libraries

---

**Happy Expense Tracking! 💰📊**

