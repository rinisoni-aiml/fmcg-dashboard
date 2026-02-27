"""Demand Forecasting Page"""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta

def show():
    """Display demand forecasting page"""
    
    st.markdown("# 📈 Demand Forecasting")
    
    if not st.session_state.data_uploaded:
        st.warning("⚠️ Please upload data first")
        return
    
    # Filters
    st.markdown("### Filters")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        product = st.selectbox("Product", ["All Products", "Product A", "Product B", "Product C"])
    with col2:
        region = st.selectbox("Region", ["All Regions", "North", "South", "East", "West"])
    with col3:
        period = st.selectbox("Forecast Period", ["Next 7 Days", "Next 30 Days", "Next 90 Days"])
    with col4:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Generate Forecast", type="primary", use_container_width=True):
            st.success("✅ Forecast generated!")
    
    st.markdown("---")
    
    # Forecast Chart
    st.markdown("### Demand Forecast Chart")
    
    days = 30 if "30" in period else (7 if "7" in period else 90)
    dates = pd.date_range(start=datetime.now(), periods=days, freq='D')
    
    # Historical data (past 30 days)
    hist_dates = pd.date_range(end=datetime.now(), periods=30, freq='D')
    historical = [100 + i*2 + (i%7)*10 for i in range(30)]
    
    # Forecast data
    forecast = [historical[-1] + i*2.5 + (i%7)*8 for i in range(days)]
    lower_bound = [f * 0.9 for f in forecast]
    upper_bound = [f * 1.1 for f in forecast]
    
    fig = go.Figure()
    
    # Historical
    fig.add_trace(go.Scatter(
        x=hist_dates, y=historical,
        mode='lines',
        name='Historical',
        line=dict(color='#2E5C8A', width=3)
    ))
    
    # Forecast
    fig.add_trace(go.Scatter(
        x=dates, y=forecast,
        mode='lines',
        name='Forecast',
        line=dict(color='#E46C0A', width=3, dash='dash')
    ))
    
    # Confidence interval
    fig.add_trace(go.Scatter(
        x=dates.tolist() + dates.tolist()[::-1],
        y=upper_bound + lower_bound[::-1],
        fill='toself',
        fillcolor='rgba(228, 108, 10, 0.2)',
        line=dict(color='rgba(255,255,255,0)'),
        showlegend=True,
        name='Confidence Interval'
    ))
    
    fig.update_layout(
        height=400,
        xaxis_title="Date",
        yaxis_title="Demand (units)",
        hovermode='x unified'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Metrics
    st.markdown("---")
    st.markdown("### Forecast Summary")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Next 7 Days", "1,234 units")
    with col2:
        st.metric("Next 30 Days", "5,678 units")
    with col3:
        st.metric("Next 90 Days", "18,456 units")
    with col4:
        st.metric("Confidence Level", "89%")
    
    # Recommendations
    st.markdown("---")
    st.markdown("### 📋 Action Recommendations")
    
    st.markdown("""
    <div class='alert-info'>
        <strong>✓ Increase stock by 30% in North region</strong><br>
        Based on forecast, demand will spike in Week 2
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class='alert-info'>
        <strong>✓ Prepare for 2x demand in Week 3</strong><br>
        Festival season - historical patterns show 2x increase
    </div>
    """, unsafe_allow_html=True)
    
    # YOUR ML MODEL INTEGRATION POINT
    st.markdown("---")
    st.info("""
    **🔧 Integration Point:**  
    Replace the sample data above with your actual Prophet/LSTM model predictions.
    See `utils/ml_models.py` for the integration template.
    """)
