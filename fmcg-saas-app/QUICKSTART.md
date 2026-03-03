# Quick Start Guide (5 Minutes)

## 🎯 Goal
Get the app running locally in 5 minutes.

## 📋 Prerequisites
- Python 3.9 or higher installed
- Internet connection
- Text editor (VS Code, Notepad++, etc.)

## 🚀 Steps

### 1. Download/Clone the Code (30 seconds)

If you have Git:
```bash
git clone <your-repository-url>
cd fmcg-saas-app
```

If you don't have Git:
- Download ZIP from GitHub
- Extract to a folder
- Open terminal/command prompt in that folder

### 2. Run Setup Script (2 minutes)

**On Windows:**
```bash
setup.bat
```

**On Mac/Linux:**
```bash
chmod +x setup.sh
./setup.sh
```

This will:
- Create virtual environment
- Install all dependencies
- Create .env file

### 3. Get API Key (1 minute)

1. Go to [console.groq.com](https://console.groq.com)
2. Sign up (free, no credit card)
3. Click "API Keys"
4. Click "Create API Key"
5. Copy the key

### 4. Configure Environment (30 seconds)

Open `.env` file in text editor and replace:
```env
GROQ_API_KEY=your_groq_api_key_here
```

With your actual key:
```env
GROQ_API_KEY=gsk_abc123xyz...
```

Save the file.

### 5. Run the App (30 seconds)

**On Windows:**
```bash
venv\Scripts\activate
streamlit run app.py
```

**On Mac/Linux:**
```bash
source venv/bin/activate
streamlit run app.py
```

Browser will open automatically at `http://localhost:8501`

### 6. Test with Sample Data (30 seconds)

1. Click "Get Started"
2. Fill in any company details
3. Select all services
4. Upload `data/sales_orders_complete.csv`
5. Click "Process & Continue"

Done! You should see the dashboard with real data.

## 🎉 Success!

You should now see:
- Dashboard with KPIs
- Charts and visualizations
- Forecasting page
- Inventory insights
- AI chatbot

## 🔧 Troubleshooting

### "Python not found"
Install Python from [python.org](https://python.org)

### "pip not found"
```bash
python -m ensurepip --upgrade
```

### "streamlit not found"
```bash
pip install streamlit
```

### "Prophet installation failed"
The app will work with statistical fallback. To fix:
```bash
pip install prophet
```

### "Port 8501 already in use"
```bash
streamlit run app.py --server.port 8502
```

## 📚 Next Steps

### Learn More
- Read [README.md](README.md) for full overview
- Check [DEPLOYMENT.md](DEPLOYMENT.md) to deploy online
- See [CHATBOT_GUIDE.md](CHATBOT_GUIDE.md) for AI features

### Deploy Online (Free)
1. Push code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect repository
4. Add API key in secrets
5. Deploy!

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed steps.

### Add Database (Optional)
1. Create free account at [supabase.com](https://supabase.com)
2. Create new project
3. Copy connection string
4. Add to `.env`:
```env
DATABASE_URL=postgresql://postgres:password@db.project.supabase.co:5432/postgres
```
5. Restart app

## 💡 Tips

### Use Sample Data
The `data/` folder has ready-to-use CSV files:
- `sales_orders_complete.csv` - Main sales data
- `inventory.csv` - Stock levels
- `warehouses.csv` - Locations

### Try the Chatbot
Ask questions like:
- "Which products are low in stock?"
- "Show me top sellers"
- "What's the demand forecast?"

### Explore Features
- **Dashboard**: Overview of all metrics
- **Forecasting**: Predict future demand
- **Inventory**: Stockout alerts
- **AI Assistant**: Ask questions

## 🆘 Need Help?

### Documentation
- [README.md](README.md) - Overview
- [DEPLOYMENT.md](DEPLOYMENT.md) - Deploy online
- [DATA_GUIDE.md](DATA_GUIDE.md) - Prepare your data
- [TESTING.md](TESTING.md) - Test everything
- [CHATBOT_GUIDE.md](CHATBOT_GUIDE.md) - Use AI features

### Common Issues
- **App won't start**: Check Python version (3.9+)
- **No data showing**: Upload CSV file first
- **Chatbot not working**: Add GROQ_API_KEY to .env
- **Charts not rendering**: Clear browser cache

### Still Stuck?
1. Check error message in terminal
2. Read relevant documentation
3. Search GitHub issues
4. Open new issue with details

## ✅ Checklist

Before showing to others:
- [ ] App runs locally
- [ ] Sample data uploaded
- [ ] Dashboard shows metrics
- [ ] Forecasting works
- [ ] Chatbot responds
- [ ] No errors visible

## 🎯 What's Next?

### For Demo
1. Upload your company's actual data
2. Customize company name in onboarding
3. Test all features
4. Prepare talking points

### For Production
1. Deploy to Streamlit Cloud (free)
2. Add database for persistence
3. Share URL with team
4. Gather feedback
5. Iterate and improve

## 📊 Expected Results

After following this guide:
- ✅ App running locally
- ✅ Dashboard with real data
- ✅ Forecasting with Prophet ML
- ✅ AI chatbot working
- ✅ Ready to demo

**Time taken**: ~5 minutes
**Cost**: $0
**Difficulty**: Easy

---

**Congratulations!** 🎉 You now have a working FMCG analytics platform.

**Next**: Deploy online with [DEPLOYMENT.md](DEPLOYMENT.md) or customize with your data using [DATA_GUIDE.md](DATA_GUIDE.md).
