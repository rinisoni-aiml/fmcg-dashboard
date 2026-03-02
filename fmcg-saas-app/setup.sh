#!/bin/bash

# FMCG SaaS Platform - Quick Setup Script

echo "🚀 FMCG SaaS Platform Setup"
echo "================================"
echo ""

# Check Python version
echo "📋 Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Python $python_version detected"
echo ""

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv
echo "✓ Virtual environment created"
echo ""

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate
echo "✓ Virtual environment activated"
echo ""

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip > /dev/null 2>&1
echo "✓ Pip upgraded"
echo ""

# Install dependencies
echo "📚 Installing dependencies (this may take a few minutes)..."
pip install -r requirements.txt
echo "✓ Dependencies installed"
echo ""

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file..."
    cp .env.example .env
    echo "✓ .env file created"
    echo ""
    echo "⚠️  IMPORTANT: Edit .env file and add your API keys:"
    echo "   - GROQ_API_KEY (get from https://console.groq.com)"
    echo "   - DATABASE_URL (optional, get from https://supabase.com)"
    echo ""
else
    echo "✓ .env file already exists"
    echo ""
fi

echo "================================"
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env file with your API keys"
echo "2. Run: streamlit run app.py"
echo "3. Open browser at http://localhost:8501"
echo ""
echo "For deployment to Streamlit Cloud, see DEPLOYMENT.md"
echo "================================"
