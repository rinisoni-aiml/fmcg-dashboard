"""Landing Page - Marketing homepage"""
import streamlit as st

def show():
    """Display landing page"""
    
    st.markdown("""
    <div style='text-align: center; padding: 3rem 0;'>
        <h1 style='font-size: 3rem; margin-bottom: 1rem;'>📊 FMCG Analytics Platform</h1>
        <h2 style='font-size: 1.5rem; color: #666; margin-bottom: 2rem;'>
            AI-Powered Analytics for Modern Businesses
        </h2>
        <p style='font-size: 1.1rem; color: #666; max-width: 800px; margin: 0 auto 2rem auto;'>
            Transform your data into actionable insights with demand forecasting, 
            inventory optimization, and intelligent automation
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🚀 Start Free Trial", use_container_width=True, type="primary"):
            st.session_state.current_page = 'onboarding'
            st.rerun()
        if st.button("🔑 Login", use_container_width=True):
            st.session_state.current_page = 'onboarding'
            st.rerun()
    
    st.markdown("---")
    st.markdown("### Built for Every Industry")
    
    col1, col2, col3 = st.columns(3)
    
    industries = [
        ("🛒", "FMCG", "Fast-Moving Consumer Goods"),
        ("🏥", "Healthcare", "Medical supplies & patient flow"),
        ("🎓", "Education", "Student analytics & resources"),
        ("💰", "Fintech", "Transaction analytics & risk"),
        ("🚚", "Logistics", "Route optimization & tracking"),
        ("🔒", "Cyber Security", "Threat detection & response"),
    ]
    
    for i, (icon, name, desc) in enumerate(industries):
        col = [col1, col2, col3][i % 3]
        with col:
            st.markdown(f"""
            <div class='feature-card'>
                <div style='font-size: 3rem; text-align: center;'>{icon}</div>
                <h3 style='text-align: center;'>{name}</h3>
                <p style='text-align: center; color: #666;'>{desc}</p>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### Powerful Features")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        **📈 AI-Powered Forecasting**  
        Predict demand with 90%+ accuracy using machine learning
        """)
    with col2:
        st.markdown("""
        **🚨 Real-Time Alerts**  
        Get instant notifications for critical business events
        """)
    with col3:
        st.markdown("""
        **🤖 Intelligent Automation**  
        Autonomous agents that optimize and take action
        """)
