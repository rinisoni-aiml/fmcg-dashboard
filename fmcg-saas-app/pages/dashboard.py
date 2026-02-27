"""Main Dashboard - AI Insights and Alerts"""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta

def show():
    """Display main dashboard"""
    
    st.markdown(f"# Welcome back, {st.session_state.company_name}!")
    st.caption(f"Last updated: {datetime.now().strftime('%H:%M:%S')}")
    
    if not st.session_state.data_uploaded:
        st.warning("⚠️ No data uploaded yet. Please upload your data to see insights.")
        if st.button("Upload Data Now →"):
            st.session_state.current_page = 'upload'
            st.rerun()
        return
    
    # Critical Alerts
    st.markdown("---")
    show_critical_alerts()
    
    # AI Insights
    st.markdown("---")
    show_ai_insights()
    
    # Key Metrics
    st.markdown("---")
    show_key_metrics()
    
    # Charts
    st.markdown("---")
    show_charts()

def show_critical_alerts():
    """Display critical alerts"""
    
    st.markdown("## 🚨 Critical Alerts")
    
    alerts = [
        ("⚠️", "Low Stock", "Product SKU-123 in Delhi warehouse - Reorder NOW", "critical"),
        ("⚠️", "High Demand", "Product SKU-456 in Mumbai - Increase stock by 40%", "warning"),
        ("✅", "Optimal", "Bangalore region - All systems normal", "success"),
    ]
    
    for icon, title, message, alert_type in alerts:
        if alert_type == "critical":
            st.markdown(f"""
            <div class='alert-critical'>
                <strong>{icon} {title}:</strong> {message}
            </div>
            """, unsafe_allow_html=True)
        elif alert_type == "warning":
            st.markdown(f"""
            <div class='alert-critical' style='background-color: #fff3cd; border-left-color: #E46C0A;'>
                <strong>{icon} {title}:</strong> {message}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class='alert-success'>
                <strong>{icon} {title}:</strong> {message}
            </div>
            """, unsafe_allow_html=True)

def show_ai_insights():
    """Display AI-powered insights"""
    
    st.markdown("## 💡 AI-Powered Insights")
    
    insights = [
        "📈 Demand for 'Product A' expected to increase 25% next week due to upcoming festival",
        "📦 Reduce inventory in West region by 15% - overstocked based on forecast",
        "✅ Your forecast accuracy improved to 93% this month (+5%)",
    ]
    
    for insight in insights:
        st.markdown(f"""
        <div class='alert-info'>
            {insight}
        </div>
        """, unsafe_allow_html=True)

def show_key_metrics():
    """Display key metrics"""
    
    st.markdown("## 📊 Key Metrics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Total Revenue",
            "₹12.5M",
            delta="+8%",
            delta_color="normal"
        )
    
    with col2:
        st.metric(
            "Active Products",
            "234",
            delta="+12",
            delta_color="normal"
        )
    
    with col3:
        st.metric(
            "Stockout Alerts",
            "23",
            delta="-5",
            delta_color="inverse"
        )
    
    with col4:
        st.metric(
            "Forecast Accuracy",
            "92%",
            delta="+3%",
            delta_color="normal"
        )

def show_charts():
    """Display charts"""
    
    st.markdown("## 📈 Analytics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Demand Forecast - Next 30 Days")
        
        # Generate sample data
        dates = pd.date_range(start=datetime.now(), periods=30, freq='D')
        historical = [100 + i*2 + (i%7)*10 for i in range(30)]
        forecast = [historical[-1] + i*2.5 + (i%7)*8 for i in range(30)]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=dates, y=historical,
            mode='lines',
            name='Historical',
            line=dict(color='#2E5C8A', width=2)
        ))
        fig.add_trace(go.Scatter(
            x=dates, y=forecast,
            mode='lines',
            name='Forecast',
            line=dict(color='#E46C0A', width=2, dash='dash')
        ))
        fig.update_layout(
            height=300,
            margin=dict(l=0, r=0, t=0, b=0),
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### Inventory Levels by Region")
        
        regions = ['North', 'South', 'East', 'West']
        stock_levels = [850, 920, 780, 690]
        
        fig = go.Figure(data=[
            go.Bar(
                x=regions,
                y=stock_levels,
                marker_color=['#00B050', '#00B050', '#E46C0A', '#C00000']
            )
        ])
        fig.update_layout(
            height=300,
            margin=dict(l=0, r=0, t=0, b=0),
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)
