# Testing Guide

## Quick Test (5 minutes)

### 1. Start the App

```bash
streamlit run app.py
```

### 2. Complete Onboarding

1. Click "Get Started"
2. Fill in company details:
   - Company: "Test FMCG Co"
   - Contact: "Test User"
   - Email: "test@example.com"
   - Industry: FMCG
3. Click "Continue to Services"

### 3. Select Services

Select all services:
- ✅ Demand Forecasting
- ✅ Inventory Optimization
- ✅ AI Assistant

Click "Save & Continue"

### 4. Upload Sample Data

1. Click "Browse files"
2. Select `data/sales_orders_complete.csv`
3. Verify auto-mapping (should detect all columns)
4. Click "Process & Continue"

### 5. Test Dashboard

Verify you see:
- ✅ Total Revenue (should be > $0)
- ✅ Active Products count
- ✅ Stockout Alerts
- ✅ Forecast Accuracy %
- ✅ Charts and visualizations

### 6. Test Forecasting

1. Go to "Forecasting" page
2. Select:
   - Product: "All Products"
   - Region: "All Regions"
   - Horizon: "Next 30 Days"
3. Click "Generate"

Verify you see:
- ✅ Historical data line (blue)
- ✅ Forecast line (orange, dashed)
- ✅ Confidence interval (shaded area)
- ✅ Summary cards (Next 7/30/90 days)
- ✅ Action recommendations

### 7. Test Inventory

1. Go to "Inventory" page
2. Verify you see:
   - ✅ Status cards (Optimal, Low Stock, etc.)
   - ✅ Inventory table with products
   - ✅ Action recommendations

### 8. Test AI Chatbot

1. Go to "AI Assistant" page
2. Try quick questions:
   - Click "📦 Low stock alerts"
   - Click "📈 Top performers"
   - Click "🔮 Demand forecast"

3. Try custom questions:
   - "What are my top 3 products by revenue?"
   - "Which regions have the highest demand?"
   - "Show me stockout risks"

Verify:
- ✅ Responses are relevant to your data
- ✅ Numbers match dashboard KPIs
- ✅ Recommendations are actionable

## Detailed Testing

### Test Prophet Forecasting

```python
# In Python console or notebook
import pandas as pd
from utils.ml_models import demand_forecaster
from utils.analytics import collect_normalized_data

# Load data
df = pd.read_csv('data/sales_orders_complete.csv')

# Prepare data
df['OrderDate'] = pd.to_datetime(df['OrderDate'])
df = df.rename(columns={
    'OrderDate': 'order_date',
    'ProductID': 'product_id',
    'Region': 'region',
    'Quantity': 'quantity'
})

# Test forecast
history, forecast, confidence = demand_forecaster.predict(
    df, horizon_days=30
)

print(f"History shape: {history.shape}")
print(f"Forecast shape: {forecast.shape}")
print(f"Confidence: {confidence}%")
print("\nForecast preview:")
print(forecast.head())
```

Expected output:
- History: 100+ rows
- Forecast: 30 rows
- Confidence: 70-95%
- Forecast has columns: date, predicted_demand, lower_bound, upper_bound

### Test Database Connection

```python
from utils.database import db_service

# Check connection
print(f"Database connected: {db_service.is_connected()}")

# Test save company
company_data = {
    "company_name": "Test Company",
    "industry": "FMCG",
    "contact_email": "test@example.com",
    "contact_phone": "+1234567890",
    "services": ["forecasting", "inventory"]
}

success = db_service.save_company(company_data)
print(f"Save successful: {success}")

# Test retrieve company
company = db_service.get_company("Test Company")
print(f"Retrieved: {company}")
```

Expected output:
- Connection: True (if DATABASE_URL set)
- Save: True
- Retrieved: Dict with company data

### Test Chatbot

```python
from utils.chatbot import chatbot_service

# Check API connection
print(f"Groq client available: {chatbot_service.client is not None}")

# Test response
context = {
    "company_name": "Test Co",
    "industry": "FMCG",
    "rows": 1000,
    "kpis": {
        "total_revenue": 1000000,
        "active_products": 50,
        "stockout_alerts": 3,
        "forecast_accuracy": 92.5
    },
    "insights": ["Demand trending up 15%"],
    "top_regions": [
        {"region": "North", "total_quantity": 5000, "total_revenue": 500000}
    ]
}

response = chatbot_service.get_response(
    "What are my top performing regions?",
    company_data=context
)

print(f"Response: {response}")
```

Expected output:
- Client available: True (if GROQ_API_KEY set)
- Response: Mentions "North" region with specific numbers

## Performance Testing

### Load Test with Large Dataset

```python
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Generate large dataset
n_rows = 10000
dates = pd.date_range(end=datetime.now(), periods=n_rows, freq='H')

large_df = pd.DataFrame({
    'order_id': [f'ORD{i:06d}' for i in range(n_rows)],
    'order_date': dates,
    'product_id': np.random.choice([f'SKU{i:03d}' for i in range(100)], n_rows),
    'region': np.random.choice(['North', 'South', 'East', 'West'], n_rows),
    'quantity': np.random.randint(1, 100, n_rows),
    'unit_price': np.random.uniform(10, 1000, n_rows),
    'total_amount': np.random.uniform(100, 10000, n_rows)
})

# Save and test
large_df.to_csv('data/large_test.csv', index=False)
print(f"Generated {n_rows} rows")

# Upload this file in the app and verify:
# - Upload completes in < 30 seconds
# - Dashboard loads in < 10 seconds
# - Forecasting completes in < 60 seconds
```

### Memory Usage Test

```python
import psutil
import os

process = psutil.Process(os.getpid())

# Before loading data
mem_before = process.memory_info().rss / 1024 / 1024
print(f"Memory before: {mem_before:.2f} MB")

# Load large dataset
df = pd.read_csv('data/large_test.csv')

# After loading
mem_after = process.memory_info().rss / 1024 / 1024
print(f"Memory after: {mem_after:.2f} MB")
print(f"Memory increase: {mem_after - mem_before:.2f} MB")

# Expected: < 500MB for 10k rows
```

## Error Testing

### Test Missing API Key

1. Remove GROQ_API_KEY from .env
2. Restart app
3. Go to AI Assistant
4. Verify: Fallback responses work
5. Verify: Message shows "Add GROQ_API_KEY"

### Test Missing Database

1. Remove DATABASE_URL from .env
2. Restart app
3. Complete onboarding
4. Verify: App works in session mode
5. Verify: Message shows "Running in session-only mode"

### Test Invalid Data

1. Create CSV with missing columns:
```csv
OrderID,Date,Product
1,2025-01-01,SKU001
```

2. Upload to app
3. Verify: Auto-mapping detects available columns
4. Verify: Missing columns show as "Not mapped"
5. Verify: Error message if required columns missing

### Test Empty Data

1. Create empty CSV (headers only)
2. Upload to app
3. Verify: Error message shown
4. Verify: App doesn't crash

## Integration Testing

### End-to-End Flow

1. **Fresh Start**
   - Clear browser cache
   - Restart app
   - Verify landing page loads

2. **Onboarding**
   - Complete registration
   - Verify redirect to services

3. **Services**
   - Select all services
   - Verify redirect to upload

4. **Upload**
   - Upload sample data
   - Verify processing completes
   - Verify redirect to dashboard

5. **Dashboard**
   - Verify all KPIs populated
   - Verify charts render
   - Verify alerts shown

6. **Forecasting**
   - Generate forecast
   - Verify chart renders
   - Verify recommendations shown

7. **Inventory**
   - View inventory table
   - Verify status colors
   - Verify recommendations

8. **Chatbot**
   - Ask 3 different questions
   - Verify responses relevant
   - Verify conversation history

9. **Settings**
   - Update company info
   - Verify changes saved

### Multi-File Upload

1. Upload `sales_orders_complete.csv`
2. Process and continue
3. Go back to upload page
4. Upload another CSV file
5. Verify: Both files merged
6. Verify: Dashboard shows combined data
7. Verify: No duplicate orders

## Browser Testing

Test on:
- ✅ Chrome (latest)
- ✅ Firefox (latest)
- ✅ Safari (latest)
- ✅ Edge (latest)

Verify:
- All pages load correctly
- Charts render properly
- Forms submit successfully
- No console errors

## Mobile Testing

Test on mobile devices:
- ✅ iPhone (Safari)
- ✅ Android (Chrome)

Verify:
- Responsive layout
- Touch interactions work
- Charts are readable
- Forms are usable

## Deployment Testing

### Streamlit Cloud

1. Deploy to Streamlit Cloud
2. Wait for deployment
3. Open public URL
4. Run all tests above
5. Verify:
   - App loads in < 10 seconds
   - All features work
   - No errors in logs

### Environment Variables

Verify all secrets are set:
```bash
# In Streamlit Cloud logs
echo $GROQ_API_KEY  # Should show key
echo $DATABASE_URL  # Should show URL
```

## Automated Testing

### Unit Tests (Future)

```python
# tests/test_forecasting.py
import pytest
from utils.ml_models import demand_forecaster

def test_forecast_with_valid_data():
    # Test implementation
    pass

def test_forecast_with_empty_data():
    # Test implementation
    pass
```

### Run Tests

```bash
pytest tests/
```

## Troubleshooting Tests

### If Forecasting Fails

1. Check Prophet installation:
```python
import prophet
print(prophet.__version__)
```

2. Check data format:
```python
print(df['order_date'].dtype)  # Should be datetime64
print(df['quantity'].dtype)     # Should be numeric
```

3. Check data size:
```python
print(len(df))  # Should be > 30 rows
```

### If Chatbot Fails

1. Check API key:
```python
import os
print(os.getenv('GROQ_API_KEY'))  # Should show key
```

2. Test API directly:
```python
from groq import Groq
client = Groq(api_key="your_key")
response = client.chat.completions.create(
    model="llama-3.1-8b-instant",
    messages=[{"role": "user", "content": "Hello"}]
)
print(response.choices[0].message.content)
```

### If Database Fails

1. Check connection string:
```python
import os
print(os.getenv('DATABASE_URL'))
```

2. Test connection:
```python
from sqlalchemy import create_engine
engine = create_engine(os.getenv('DATABASE_URL'))
with engine.connect() as conn:
    result = conn.execute("SELECT 1")
    print(result.fetchone())
```

## Test Checklist

Before deployment:
- [ ] All pages load without errors
- [ ] Sample data uploads successfully
- [ ] Forecasting generates predictions
- [ ] Inventory shows recommendations
- [ ] Chatbot responds to questions
- [ ] Database saves company data
- [ ] Charts render correctly
- [ ] Mobile layout works
- [ ] No console errors
- [ ] Performance is acceptable

## Reporting Issues

If you find bugs:
1. Note the exact steps to reproduce
2. Check browser console for errors
3. Check Streamlit logs
4. Include sample data (if possible)
5. Open GitHub issue with details

---

**Ready to test?** Start with the Quick Test section above!
