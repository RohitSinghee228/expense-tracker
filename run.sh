#!/bin/bash

# Expense Tracker Startup Script

echo "🚀 Starting Expense Tracker Application..."
echo ""

# Check if conda environment exists
if conda env list | grep -q "expense-tracker"; then
    echo "✓ Conda environment 'expense-tracker' found"
else
    echo "❌ Conda environment not found. Creating it..."
    conda create -n expense-tracker python=3.10 -y
    source "$(conda info --base)/etc/profile.d/conda.sh"
    conda activate expense-tracker
    pip install -r requirements.txt
fi

# Activate environment
echo "Activating conda environment..."
source "$(conda info --base)/etc/profile.d/conda.sh"
conda activate expense-tracker

# Check if dependencies are installed
if ! python -c "import fastapi" 2>/dev/null; then
    echo "Installing dependencies..."
    pip install -r requirements.txt
fi

echo ""
echo "✓ Environment ready!"
echo ""
echo "📊 Starting server at http://localhost:8000"
echo "📈 Summary page: http://localhost:8000/summary"
echo "📥 Export CSV: http://localhost:8000/export"
echo "📚 API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Start the application
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

