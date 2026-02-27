"""Services Selection Page"""
import streamlit as st

def show():
    """Display services selection page"""
    
    st.markdown("# FMCG Analytics Services")
    st.markdown("Select the services you need for your business")
    
    st.markdown("---")
    
    # Active features
    st.markdown("## ✅ Active Features")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class='feature-card'>
            <span class='badge-active'>✅ ACTIVE</span>
            <div style='font-size: 3rem; text-align: center; margin: 1rem 0;'>📈</div>
            <h3>Demand Forecasting</h3>
            <p>Predict demand 7-90 days ahead with 90%+ accuracy using AI models</p>
        </div>
        """, unsafe_allow_html=True)
        st.checkbox("Select", value=True, key="sel_forecast")
    
    with col2:
        st.markdown("""
        <div class='feature-card'>
            <span class='badge-active'>✅ ACTIVE</span>
            <div style='font-size: 3rem; text-align: center; margin: 1rem 0;'>📦</div>
            <h3>Inventory Optimization</h3>
            <p>Optimize stock levels, reduce waste, prevent stockouts</p>
        </div>
        """, unsafe_allow_html=True)
        st.checkbox("Select", value=True, key="sel_inventory")
    
    with col3:
        st.markdown("""
        <div class='feature-card'>
            <span class='badge-active'>✅ ACTIVE</span>
            <div style='font-size: 3rem; text-align: center; margin: 1rem 0;'>🤖</div>
            <h3>AI Assistant</h3>
            <p>Chat/voice bot - Ask questions, get instant insights</p>
        </div>
        """, unsafe_allow_html=True)
        st.checkbox("Select", value=True, key="sel_chatbot")
    
    st.markdown("---")
    st.markdown("## 🚧 Coming Soon")
    
    coming_soon = [
        ("💹", "Sales Optimization", "Optimize sales strategies and improve conversion rates", "Q2 2024"),
        ("💰", "Profit & Loss Insights", "AI-powered P&L analysis and recommendations", "Q2 2024"),
        ("🏷️", "Autonomous Pricing Agent", "Dynamic pricing based on demand, competition", "Q3 2024"),
        ("🎯", "Autonomous Sales Agent", "AI agent that identifies opportunities", "Q3 2024"),
        ("🔗", "Supply Chain Analytics", "End-to-end supply chain visibility", "Q3 2024"),
        ("✅", "Quality Control AI", "Automated quality monitoring", "Q4 2024"),
    ]
    
    col1, col2, col3 = st.columns(3)
    cols = [col1, col2, col3]
    
    for i, (icon, name, desc, timeline) in enumerate(coming_soon):
        with cols[i % 3]:
            st.markdown(f"""
            <div class='feature-card disabled'>
                <span class='badge-soon'>🚧 COMING SOON</span>
                <div style='font-size: 3rem; text-align: center; margin: 1rem 0;'>{icon}</div>
                <h3>{name}</h3>
                <p>{desc}</p>
                <p style='color: #999; font-size: 0.9rem;'>Available {timeline}</p>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("Next: Upload Data →", use_container_width=True, type="primary"):
            st.session_state.current_page = 'upload'
            st.rerun()
