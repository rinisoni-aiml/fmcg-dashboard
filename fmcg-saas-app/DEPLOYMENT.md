# Deployment Guide - FMCG SaaS Platform

## Quick Deploy to Streamlit Cloud (Free)

### Prerequisites
1. GitHub account
2. Streamlit Cloud account (sign up at [share.streamlit.io](https://share.streamlit.io))
3. Groq API key (get free at [console.groq.com](https://console.groq.com))
4. Supabase or Neon database (optional but recommended)

### Step 1: Prepare Your Repository

1. Push your code to GitHub:
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/yourusername/fmcg-saas-app.git
git push -u origin main
```

### Step 2: Set Up Database (Recommended)

#### Option A: Supabase (Recommended)

1. Go to [supabase.com](https://supabase.com) and create a free account
2. Create a new project
3. Go to Project Settings → Database
4. Copy the connection string (URI format)
5. It will look like: `postgresql://postgres:[YOUR-PASSWORD]@db.[PROJECT-REF].supabase.co:5432/postgres`

#### Option B: Neon

1. Go to [neon.tech](https://neon.tech) and create a free account
2. Create a new project
3. Copy the connection string
4. It will look like: `postgresql://[user]:[password]@[host]/[database]?sslmode=require`

### Step 3: Deploy to Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click "New app"
3. Select your GitHub repository
4. Set:
   - Main file path: `fmcg-saas-app/app.py`
   - Python version: 3.11

5. Click "Advanced settings" and add these secrets:

```toml
# Groq API for AI Chatbot (Required)
GROQ_API_KEY = "your_groq_api_key_here"
GROQ_MODEL = "llama-3.1-8b-instant"

# Database (Recommended - use Supabase or Neon)
DATABASE_URL = "postgresql://postgres:[PASSWORD]@db.[PROJECT-REF].supabase.co:5432/postgres"

# Optional
DEBUG = "False"
```

6. Click "Deploy"
7. Wait 2-3 minutes for deployment

### Step 4: Get Your API Keys

#### Groq API Key (Free - Required for AI features)
1. Go to [console.groq.com](https://console.groq.com)
2. Sign up/Login
3. Go to API Keys section
4. Create new API key
5. Copy and paste into Streamlit secrets

### Step 5: Test Your Deployment

1. Once deployed, click the app URL
2. Complete onboarding with your company details
3. Upload sample data from `data/sales_orders_complete.csv`
4. Test forecasting, inventory, and chatbot features

## Local Development

### Setup

```bash
cd fmcg-saas-app
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Configure Environment

Create `.env` file:

```env
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=llama-3.1-8b-instant
DATABASE_URL=postgresql://postgres:password@localhost:5432/fmcg_saas
DEBUG=True
```

### Run Locally

```bash
streamlit run app.py
```

## Database Schema

The app automatically creates these tables:

### companies
- id (Primary Key)
- company_name (Unique)
- industry
- contact_email
- contact_phone
- services (JSON)
- created_at
- updated_at

### forecast_history
- id (Primary Key)
- company_name
- product_id
- region
- forecast_date
- horizon_days
- forecast_data (JSON)
- confidence_level
- model_type

### inventory_alerts
- id (Primary Key)
- company_name
- product_id
- warehouse_id
- alert_type
- current_stock
- recommended_action
- priority
- is_resolved
- created_at
- resolved_at

## Features

### ✅ Real Prophet Forecasting
- Uses Facebook Prophet for time series forecasting
- Automatic seasonality detection
- Confidence intervals
- Fallback to statistical methods if Prophet unavailable

### ✅ AI-Powered Chatbot
- Groq-powered LLM (Llama 3.1)
- Context-aware responses based on your data
- Inventory, forecast, and sales insights
- Fallback responses when API unavailable

### ✅ Database Persistence
- Company profiles
- Forecast history
- Inventory alerts
- Works with Supabase, Neon, or any PostgreSQL

### ✅ Production-Ready UI
- Modern, responsive design
- Interactive charts with Plotly
- Real-time data processing
- Mobile-friendly

## Troubleshooting

### Prophet Installation Issues

If Prophet fails to install on Streamlit Cloud, it will automatically fall back to statistical forecasting. To ensure Prophet works:

1. Make sure `requirements.txt` has: `prophet==1.1.5`
2. Streamlit Cloud uses Ubuntu, which should support Prophet

### Database Connection Issues

1. Ensure your DATABASE_URL includes `?sslmode=require` for Supabase/Neon
2. Check that your database allows connections from Streamlit Cloud IPs
3. Verify the connection string format is correct

### Groq API Issues

1. Verify your API key is correct
2. Check you haven't exceeded free tier limits
3. The app will work with fallback responses if API is unavailable

## Cost Breakdown (Free Tier)

- **Streamlit Cloud**: Free (1 app, public)
- **Supabase**: Free (500MB database, 2GB bandwidth)
- **Neon**: Free (3GB storage, 1 project)
- **Groq API**: Free (generous limits for testing)

**Total Cost: $0/month** for development and demo purposes

## Upgrading for Production

When ready for production:

1. **Streamlit Cloud**: $20/month for private apps
2. **Supabase**: $25/month for Pro (8GB database)
3. **Groq**: Pay-as-you-go for higher limits
4. Add authentication (Auth0, Supabase Auth)
5. Add monitoring (Sentry, LogRocket)

## Support

For issues:
1. Check Streamlit Cloud logs
2. Verify all environment variables are set
3. Test database connection separately
4. Ensure sample data is uploaded correctly
