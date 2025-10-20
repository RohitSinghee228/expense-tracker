# 🚀 Quick Start Guide - Expense Tracker

## Prerequisites
- Python 3.10+
- Conda (Anaconda/Miniconda)

## Installation & Setup (5 minutes)

### Step 1: Open Terminal
Navigate to the project directory:
```bash
cd "/Users/rohit/Desktop/Syren/Assignment /expense-tracker"
```

### Step 2: Create & Activate Environment
```bash
# Create conda environment
conda create -n expense-tracker python=3.10 -y

# Activate environment
conda activate expense-tracker

# Install dependencies
pip install -r requirements.txt
```

### Step 3: Start the Application
```bash
uvicorn app.main:app --reload
```

**OR** use the convenience script:
```bash
./run.sh
```

### Step 4: Open Your Browser
Go to: **http://localhost:8000**

## 📸 What You'll See

### Dashboard (Home Page)
- ➕ **Add Expense Form** - Enter amount, category, date, description
- 🔍 **Filter Section** - Filter by category and date range
- 📋 **Expenses Table** - View all your expenses with totals

### Summary Page
Go to: **http://localhost:8000/summary**
- 💵 **Total Expenses** - Overall spending
- 📊 **Transaction Count** - Number of expenses
- 🏷️ **Categories** - Unique categories
- 📈 **Category Breakdown** - Detailed analytics with percentages

### Export Data
Go to: **http://localhost:8000/export**
- Downloads CSV file with all expenses

## 🎯 Try These Actions

### 1. Add an Expense
```
Amount: 50.00
Category: Food
Date: (today's date)
Description: Lunch at restaurant
```
Click "Add Expense" ✅

### 2. Add More Expenses
```
Amount: 100.00
Category: Transport
Date: Yesterday
Description: Taxi
```

```
Amount: 30.00
Category: Food
Date: Two days ago
Description: Groceries
```

### 3. Use Filters
- Select "Food" from category dropdown
- Click "Apply Filters"
- See only Food expenses

### 4. View Summary
- Click "📈 Summary" in header
- See category breakdown
- View visual distribution

### 5. Export Data
- Click "📥 Export CSV"
- Opens CSV file with all data

## 🧪 Run Tests

```bash
# Activate environment
conda activate expense-tracker

# Run all tests
pytest -v

# Expected: 10 passed ✅
```

## 🌐 API Documentation

FastAPI provides automatic interactive API docs:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 📊 Sample API Usage

### Add Expense via API
```bash
curl -X POST "http://localhost:8000/add_expense" \
  -H "Content-Type: application/json" \
  -d '{
    "amount": 50.00,
    "category": "Food",
    "date": "2025-10-20",
    "description": "Lunch"
  }'
```

### Get All Expenses
```bash
curl "http://localhost:8000/expenses"
```

### Get Summary
```bash
curl "http://localhost:8000/api/summary"
```

### Filter by Category
```bash
curl "http://localhost:8000/expenses?category=Food"
```

## 🎨 UI Features to Explore

1. **Auto-complete Categories** - Type in category field to see suggestions
2. **Date Picker** - Click date field for calendar
3. **Responsive Design** - Try resizing browser window
4. **Visual Analytics** - Check the progress bars in summary
5. **Smooth Animations** - Notice hover effects and transitions
6. **Empty States** - See helpful messages when no data

## ⚡ Keyboard Shortcuts

- **Tab** - Navigate between form fields
- **Enter** - Submit form (when in text field)
- **Esc** - Clear current input (browser default)

## 🛠️ Troubleshooting

### Port Already in Use
```bash
# Kill process on port 8000
lsof -ti:8000 | xargs kill -9

# Or use different port
uvicorn app.main:app --port 8001
```

### Dependencies Not Found
```bash
# Reinstall
pip install -r requirements.txt --force-reinstall
```

### Database Issues
```bash
# Delete and recreate
rm expenses.db
# Restart app - it will recreate
```

## 📝 Notes

- Database file (`expenses.db`) is created automatically
- All data persists between sessions
- Environment variables in `.env` file
- Logs appear in terminal

## 🎓 Next Steps

1. ✅ Add your real expenses
2. ✅ Explore filtering options
3. ✅ Check out the summary analytics
4. ✅ Export your data
5. ✅ Review the API docs at /docs
6. ✅ Examine the code structure
7. ✅ Run the test suite

## 💡 Tips

- Use descriptive categories for better analytics
- Add descriptions to track details
- Export data regularly for backup
- Use date filters to analyze spending periods
- Check summary page for spending insights

---

**Need Help?** Check README.md for detailed documentation!

**Enjoy tracking your expenses! 💰📊**

