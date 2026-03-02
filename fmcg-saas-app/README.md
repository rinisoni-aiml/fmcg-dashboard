# FMCG SaaS Platform - Production Ready

A complete, production-ready FMCG (Fast-Moving Consumer Goods) analytics platform built with Streamlit, featuring real Prophet-based demand forecasting, AI-powered insights, and database persistence.

## 🚀 Features

### Real Machine Learning
- **Prophet Forecasting**: Facebook Prophet for accurate demand prediction with seasonality
- **Confidence Intervals**: 80% prediction intervals with uncertainty quantification
- **Automatic Fallback**: Statistical methods when Prophet unavailable
- **Multi-dimensional**: Forecast by product, region, or aggregate

### AI-Powered Analytics
- **Groq LLM Integration**: Fast, accurate responses using Llama 3.1
- **Context-Aware**: Chatbot understands your actual data
- **Actionable Insights**: Specific recommendations based on your metrics
- **Smart Fallbacks**: Works even without API key

### Database Persistence
- **PostgreSQL**: Full support for Supabase, Neon, or self-hosted
- **Company Profiles**: Store onboarding and settings
- **Forecast History**: Track predictions over time
- **Inventory Alerts**: Persistent stockout warnings
- **Session Fallback**: Works without database

### Professional UI
- **Modern Design**: Clean, intuitive interface
- **Interactive Charts**: Plotly visualizations
- **Responsive**: Works on desktop and mobile
- **Real-time Updates**: Live data processing

## 📊 Screenshots

### Dashboard
Real-time KPIs, alerts, and insights from your data

### Forecasting
Prophet-based demand predictions with confidence intervals

### Inventory Management
Stockout alerts and reorder recommendations

### AI Assistant
Context-aware chatbot for operational insights

## 🎯 Quick Start

### Deploy to Streamlit Cloud (5 minutes)

1. **Fork this repository**

2. **Get API Keys** (both free):
   - Groq: [console.groq.com](https://console.groq.com)
   - Supabase: [supabase.com](https://supabase.com) (optional)

3. **Deploy**:
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Click "New app"
   - Select your repo, set main file: `fmcg-saas-app/app.py`
   - Add secrets (see below)
   - Deploy!

4. **Streamlit Secrets** (Advanced Settings):
```toml
GROQ_API_KEY = "your_groq_api_key"
GROQ_MODEL = "llama-3.1-8b-instant"
DATABASE_URL = "postgresql://postgres:[PASSWORD]@db.[PROJECT].supabase.co:5432/postgres"
```

5. **Upload Sample Data**:
   - Use `data/sales_orders_complete.csv`
   - Map columns automatically
   - Start analyzing!

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions.

### Local Development

```bash
# Clone and setup
git clone <your-repo>
cd fmcg-saas-app
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Configure
cp .env.example .env
# Edit .env with your API keys

# Run
streamlit run app.py
```

## 📁 Project Structure

```
fmcg-saas-app/
├── app.py                 # Main application entry
├── pages/                 # Streamlit pages
│   ├── landing.py        # Landing page
│   ├── onboarding.py     # Company registration
│   ├── services.py       # Service selection
│   ├── upload_data.py    # Data upload & mapping
│   ├── dashboard.py      # Main dashboard
│   ├── forecasting.py    # Demand forecasting
│   ├── inventory.py      # Inventory management
│   ├── chatbot.py        # AI assistant
│   └── settings.py       # User settings
├── utils/                 # Core utilities
│   ├── analytics.py      # Data processing & KPIs
│   ├── ml_models.py      # Prophet & forecasting
│   ├── chatbot.py        # Groq integration
│   ├── database.py       # PostgreSQL/Supabase
│   └── session.py        # Session management
├── data/                  # Sample datasets
│   ├── sales_orders_complete.csv
│   ├── inventory.csv
│   └── ...
├── .streamlit/
│   └── config.toml       # Streamlit configuration
├── requirements.txt       # Python dependencies
├── .env.example          # Environment template
├── DEPLOYMENT.md         # Deployment guide
└── README.md             # This file
```

## 🔧 Configuration

### Environment Variables

```env
# Required for AI features
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=llama-3.1-8b-instant

# Optional but recommended for persistence
DATABASE_URL=postgresql://user:pass@host:5432/dbname

# Optional
DEBUG=True
```

### Data Format

Upload CSV/XLSX files with these columns (auto-mapped):

| Column | Description | Required |
|--------|-------------|----------|
| order_id | Unique order identifier | Yes |
| order_date | Order date (YYYY-MM-DD) | Yes |
| product_id | Product/SKU code | Yes |
| region | Sales region/warehouse | Yes |
| quantity | Order quantity | Yes |
| unit_price | Price per unit | Yes |
| total_amount | Total order value | Yes |
| customer_id | Customer identifier | Optional |
| discount_percent | Discount percentage | Optional |

## 🎓 How It Works

### 1. Onboarding Flow
```
Landing → Onboarding → Services → Upload Data → Dashboard
```

### 2. Data Processing
- Auto-detect column mappings
- Normalize to standard schema
- Validate and clean data
- Merge multiple files

### 3. Forecasting Pipeline
```
Historical Data → Prophet Model → Seasonality Detection → 
Trend Analysis → Confidence Intervals → Predictions
```

### 4. AI Context Building
```
Raw Data → KPIs → Insights → Alerts → 
Context Payload → LLM → Actionable Response
```

## 📈 Use Cases

### Demand Forecasting
- Predict demand for next 7/30/90 days
- Identify seasonal patterns
- Plan inventory replenishment
- Optimize production schedules

### Inventory Optimization
- Stockout risk alerts
- Reorder point calculations
- Safety stock recommendations
- Overstock identification

### Sales Analytics
- Revenue tracking by product/region
- Top performer identification
- Trend analysis
- Performance insights

### Operational Intelligence
- AI-powered Q&A on your data
- Natural language queries
- Automated recommendations
- Real-time alerts

## 🛠️ Technology Stack

- **Frontend**: Streamlit 1.31
- **ML/Forecasting**: Prophet 1.1.5, XGBoost 2.0
- **AI/LLM**: Groq (Llama 3.1)
- **Database**: PostgreSQL (Supabase/Neon)
- **Visualization**: Plotly 5.18
- **Data Processing**: Pandas 2.1, NumPy 1.26

## 🔒 Security & Privacy

- No data leaves your control (except LLM API calls)
- Database credentials encrypted in Streamlit secrets
- Session-based authentication
- Optional database persistence
- HTTPS by default on Streamlit Cloud

## 📊 Sample Data

Included sample datasets in `data/`:
- `sales_orders_complete.csv` - 1000+ orders across products/regions
- `inventory.csv` - Current stock levels
- `warehouses.csv` - Warehouse information
- `suppliers.csv` - Supplier data
- And more...

## 🚀 Roadmap

- [ ] Multi-user authentication
- [ ] Role-based access control
- [ ] Email alerts for stockouts
- [ ] PDF report generation
- [ ] API endpoints
- [ ] Mobile app
- [ ] Advanced ML models (LSTM, Transformer)
- [ ] Real-time data streaming

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📝 License

MIT License - feel free to use for commercial projects

## 💡 Support

- **Documentation**: See [DEPLOYMENT.md](DEPLOYMENT.md)
- **Issues**: Open a GitHub issue
- **Questions**: Check existing issues first

## 🎉 Acknowledgments

- Facebook Prophet for forecasting
- Groq for fast LLM inference
- Streamlit for the amazing framework
- Supabase for database hosting

---

**Ready to deploy?** See [DEPLOYMENT.md](DEPLOYMENT.md) for step-by-step instructions.

**Need help?** Open an issue or check the troubleshooting section in DEPLOYMENT.md.
