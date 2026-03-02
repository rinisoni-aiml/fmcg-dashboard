# AI Chatbot Guide

## Overview

The AI Assistant uses Groq's Llama 3.1 model to provide intelligent, context-aware responses based on your actual FMCG data. It can answer questions about inventory, forecasting, sales, and provide actionable recommendations.

## Setup

### Get Groq API Key (Free)

1. Go to [console.groq.com](https://console.groq.com)
2. Sign up or log in
3. Navigate to "API Keys"
4. Click "Create API Key"
5. Copy the key
6. Add to `.env`:
```env
GROQ_API_KEY=your_key_here
GROQ_MODEL=llama-3.1-8b-instant
```

### Free Tier Limits

- **Requests**: 30 requests/minute
- **Tokens**: 6,000 tokens/minute
- **Cost**: $0 (completely free for testing)

## How It Works

### 1. Context Building

The chatbot receives rich context about your business:

```
Company: Your Company Name
Industry: FMCG
Dataset: 1,234 orders

KPIs:
- Total Revenue: $1,234,567
- Active Products: 50
- Stockout Alerts: 3
- Forecast Accuracy: 92.5%

Top Regions:
1. North: 5,000 units, $500,000
2. South: 3,500 units, $350,000

Alerts:
- [CRITICAL] SKU001 in North: 2 days of cover
- [HIGH] SKU045 in South: 4 days of cover

Insights:
- Expected demand over next 7 days: 1,250 units
- Top product: SKU001 ($125,000 revenue)
```

### 2. Response Generation

The AI:
- Analyzes your specific data
- Provides concrete numbers
- Gives actionable recommendations
- References actual products/regions
- Never invents data

### 3. Fallback Mode

Without API key, the chatbot:
- Uses rule-based responses
- References your actual KPIs
- Provides basic insights
- Suggests adding API key for full features

## Example Questions

### Inventory Management

**Question**: "Which products are at risk of stockout?"

**Response**:
```
Based on your current data, you have 3 products at stockout risk:

1. SKU001 in North region - Only 2 days of cover remaining
   Recommendation: Immediate reorder of 500 units

2. SKU045 in South region - 4 days of cover
   Recommendation: Schedule reorder within 48 hours

3. SKU089 in East region - 5 days of cover
   Recommendation: Monitor daily, reorder in 2-3 days

Priority action: Focus on SKU001 as it's critical.
```

**Question**: "What's my current inventory status?"

**Response**:
```
Your inventory health:
- Optimal Stock: 35 products (70%)
- Low Stock: 10 products (20%)
- Stockout Risk: 3 products (6%)
- Overstock: 2 products (4%)

Overall: Healthy inventory with a few attention areas.
Focus on the 3 stockout risks mentioned above.
```

### Demand Forecasting

**Question**: "What's the demand forecast for next week?"

**Response**:
```
Next 7 days forecast:
- Total predicted demand: 1,250 units
- Confidence level: 92.5%
- Trend: Increasing by 8% vs last week

Key insights:
- Monday-Wednesday: Higher demand (200+ units/day)
- Thursday-Friday: Moderate (150-180 units/day)
- Weekend: Lower demand (100-120 units/day)

Recommendation: Ensure stock levels are 15% above forecast
to maintain 95% service level.
```

**Question**: "Which products will have highest demand?"

**Response**:
```
Top 5 products by forecasted demand (next 30 days):

1. SKU001: 850 units (confidence: 94%)
2. SKU023: 720 units (confidence: 91%)
3. SKU045: 680 units (confidence: 89%)
4. SKU012: 590 units (confidence: 92%)
5. SKU078: 540 units (confidence: 88%)

Recommendation: Prioritize procurement for SKU001 and SKU023.
```

### Sales Analysis

**Question**: "Show me top performing products"

**Response**:
```
Top 5 products by revenue:

1. SKU001: $125,450 (15% of total)
   - Sold in: North, South, East
   - Avg price: $45.50
   - Volume: 2,756 units

2. SKU023: $98,230 (12% of total)
   - Sold in: All regions
   - Avg price: $38.20
   - Volume: 2,571 units

3. SKU045: $87,650 (10% of total)
   - Sold in: North, West
   - Avg price: $52.30
   - Volume: 1,676 units

Insight: Top 3 products account for 37% of revenue.
Focus marketing and inventory on these SKUs.
```

**Question**: "Which regions are performing best?"

**Response**:
```
Regional performance:

1. North: $500,000 (40% of revenue)
   - 5,000 units sold
   - Top product: SKU001
   - Growth: +12% vs last month

2. South: $350,000 (28% of revenue)
   - 3,500 units sold
   - Top product: SKU023
   - Growth: +8% vs last month

3. East: $250,000 (20% of revenue)
   - 2,800 units sold
   - Top product: SKU045
   - Growth: +5% vs last month

Recommendation: North region is your strongest market.
Consider expanding distribution there.
```

### Operational Insights

**Question**: "Give me top 3 actionable insights"

**Response**:
```
Top 3 priorities for this week:

1. URGENT: Reorder SKU001 for North region
   - Current stock: 2 days of cover
   - Recommended order: 500 units
   - Lead time: 7 days
   - Action: Place order today

2. HIGH: Optimize inventory for SKU045
   - Currently overstocked in West (45 days cover)
   - Understocked in South (4 days cover)
   - Action: Transfer 200 units West → South

3. MEDIUM: Capitalize on demand trend
   - Overall demand up 8% this week
   - Forecast shows continued growth
   - Action: Increase safety stock by 10%

Expected impact: Prevent 3 stockouts, improve service level to 98%
```

**Question**: "What should I focus on today?"

**Response**:
```
Today's priorities:

Morning:
1. Review and approve reorder for SKU001 (critical)
2. Check inventory levels for 3 at-risk products
3. Verify supplier lead times for urgent orders

Afternoon:
4. Analyze forecast accuracy for last week
5. Review regional performance trends
6. Plan next week's procurement

Evening:
7. Update safety stock levels based on new forecast
8. Prepare stockout risk report for management

Most critical: SKU001 reorder - don't delay!
```

### Trend Analysis

**Question**: "Are there any concerning trends?"

**Response**:
```
Trend analysis (last 30 days):

⚠️ Concerns:
1. Stockout frequency increased 25%
   - From 2 to 3 products at risk
   - Mainly in North region
   - Action: Review reorder points

2. Forecast accuracy dropped 3%
   - From 95.5% to 92.5%
   - Due to unexpected demand spike
   - Action: Recalibrate model with recent data

✅ Positive trends:
1. Revenue up 12% month-over-month
2. Order frequency increased 8%
3. Customer base grew by 15 new accounts

Overall: Strong growth but inventory management needs attention.
```

## Quick Questions (Buttons)

The chatbot page includes quick-access buttons:

### 📦 Low stock alerts
Instantly shows products at risk with specific recommendations

### 📈 Top performers
Lists top products and regions by revenue

### 🔮 Demand forecast
Shows next 7-day forecast with trends

### 💡 Key insights
Provides top 3 actionable insights

## Advanced Usage

### Multi-turn Conversations

The chatbot remembers context:

**You**: "Which products are low in stock?"
**AI**: "You have 3 products at stockout risk: SKU001, SKU045, SKU089..."

**You**: "Tell me more about SKU001"
**AI**: "SKU001 details: Currently in North region with 2 days of cover..."

**You**: "What's the reorder quantity?"
**AI**: "For SKU001, recommended reorder quantity is 500 units..."

### Specific Queries

Be specific for better answers:

❌ "Tell me about sales"
✅ "What are my top 5 products by revenue in the North region?"

❌ "Inventory status"
✅ "Which products in the South region need reordering this week?"

❌ "Forecast"
✅ "What's the 30-day demand forecast for SKU001 with confidence level?"

### Comparative Analysis

**Question**: "Compare North and South region performance"

**Response**:
```
North vs South comparison:

Revenue:
- North: $500,000 (40% of total) ✓
- South: $350,000 (28% of total)
- Difference: +43% in favor of North

Volume:
- North: 5,000 units ✓
- South: 3,500 units
- Difference: +43% in favor of North

Growth:
- North: +12% vs last month ✓
- South: +8% vs last month
- North growing faster

Top Products:
- North: SKU001 ($125k)
- South: SKU023 ($98k)

Recommendation: North is your strongest market.
Consider replicating North's strategy in South.
```

## Best Practices

### Do's ✅

- Ask specific questions with product IDs or regions
- Request actionable recommendations
- Ask for comparisons and trends
- Use follow-up questions for details
- Request prioritized action items

### Don'ts ❌

- Don't ask about data not uploaded
- Don't expect predictions beyond your data range
- Don't ask for external market data
- Don't request features not in the app
- Don't ask personal or non-business questions

## Limitations

### What the Chatbot CAN Do

✅ Analyze your uploaded data
✅ Provide insights from your KPIs
✅ Reference specific products/regions
✅ Give actionable recommendations
✅ Explain trends in your data
✅ Answer operational questions
✅ Prioritize actions

### What the Chatbot CANNOT Do

❌ Access external market data
❌ Predict beyond your data patterns
❌ Modify your data
❌ Place actual orders
❌ Access other companies' data
❌ Provide financial advice
❌ Make business decisions for you

## Troubleshooting

### "Add GROQ_API_KEY to enable full features"

**Solution**: Add your Groq API key to `.env` file

### Responses seem generic

**Possible causes**:
1. No data uploaded yet → Upload sales data first
2. API key not set → Add GROQ_API_KEY
3. Data too small → Upload at least 30 days of data

### "I don't have that information"

**Possible causes**:
1. Question about data not uploaded
2. Asking for external information
3. Question too vague

**Solution**: Be more specific and ensure data is uploaded

### Slow responses

**Possible causes**:
1. Large dataset (>10k rows)
2. Complex query
3. API rate limits

**Solution**: 
- Simplify question
- Wait a few seconds
- Check API rate limits

## Privacy & Security

### Data Privacy

- Your data never leaves your control (except API calls)
- Groq processes queries but doesn't store your data
- Database credentials are encrypted
- No data shared between companies

### API Security

- API keys stored in environment variables
- Never committed to version control
- Transmitted over HTTPS only
- Rotatable at any time

## Cost Management

### Free Tier (Groq)

- 30 requests/minute
- 6,000 tokens/minute
- Sufficient for 100+ questions/day
- No credit card required

### Monitoring Usage

Check your usage at [console.groq.com](https://console.groq.com)

### Optimizing Costs

- Use quick question buttons (pre-optimized)
- Ask specific questions (fewer tokens)
- Avoid very long conversations
- Use fallback mode for simple queries

## Future Enhancements

Coming soon:
- Voice input/output
- Multi-language support
- Custom report generation
- Email alerts integration
- Scheduled insights
- Comparison with industry benchmarks

---

**Ready to chat?** Go to the AI Assistant page and start asking questions!

**Need help?** Try the quick question buttons first to see examples.
