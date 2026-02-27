"""
FMCG SaaS Platform - Main Application
Production-ready Streamlit app matching the wireframe design
"""

import streamlit as st
from pathlib import Path
import sys

# Add project root to path
sys.path.append(str(Path(__file__).parent))

# Page config - MUST be first Streamlit command
st.set_page_config(
    page_title="FMCG Analytics Platform",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': "FMCG Analytics Platform - AI-Powered Insights"
    }
)

# Custom CSS matching wireframe design
st.markdown("""
<style>
    /* Main theme colors */
    :root {
        --primary-blue: #2E5C8A;
        --secondary-orange: #E46C0A;
        --success-green: #00B050;
        --alert-red: #C00000;
        --gray: #999999;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Custom button styles */
    .stButton>button {
        background-color: var(--primary-blue);
        color: white;
        border-radius: 8px;
        padding: 0.5rem 2rem;
        font-weight: 500;
        border: none;
        transition: all 0.3s;
    }
    
    .stButton>button:hover {
        background-color: #1e4c6a;
        box-shadow: 0 4px 12px rgba(46, 92, 138, 0.3);
    }
    
    /* Status badges */
    .badge-active {
        background-color: var(--success-green);
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: bold;
        display: inline-block;
    }
    
    .badge-soon {
        background-color: var(--gray);
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: bold;
        display: inline-block;
    }
    
    /* Alert boxes */
    .alert-critical {
        background-color: #fff3cd;
        border-left: 4px solid var(--alert-red);
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    .alert-info {
        background-color: #e8f0f7;
        border-left: 4px solid var(--primary-blue);
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    .alert-success {
        background-color: #d4edda;
        border-left: 4px solid var(--success-green);
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    /* Cards */
    .feature-card {
        border: 2px solid #ddd;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        transition: all 0.3s;
        background: white;
    }
    
    .feature-card:hover {
        border-color: var(--primary-blue);
        box-shadow: 0 4px 12px rgba(46, 92, 138, 0.2);
        transform: translateY(-2px);
    }
    
    .feature-card.disabled {
        opacity: 0.6;
        cursor: not-allowed;
    }
    
    /* Metrics */
    .metric-card {
        background: white;
        border: 2px solid #ddd;
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: bold;
        color: var(--primary-blue);
        margin-bottom: 0.5rem;
    }
    
    .metric-label {
        color: #666;
        font-size: 0.9rem;
    }
    
    .metric-change {
        color: var(--success-green);
        font-size: 0.8rem;
        margin-top: 0.5rem;
    }
    
    /* Headers */
    h1 {
        color: var(--primary-blue) !important;
    }
    
    h2 {
        color: var(--secondary-orange) !important;
    }
    
    h3 {
        color: var(--primary-blue) !important;
    }
    
    /* Sidebar */
    .css-1d391kg {
        background-color: #f8f9fa;
    }
    
    /* Data editor/dataframe styling */
    .stDataFrame {
        border: 1px solid #ddd;
        border-radius: 8px;
    }
    
    /* File uploader */
    .uploadedFile {
        border: 2px dashed var(--primary-blue);
        border-radius: 8px;
        padding: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
def init_session_state():
    """Initialize all session state variables"""
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'company_id' not in st.session_state:
        st.session_state.company_id = None
    if 'company_name' not in st.session_state:
        st.session_state.company_name = None
    if 'industry' not in st.session_state:
        st.session_state.industry = None
    if 'data_uploaded' not in st.session_state:
        st.session_state.data_uploaded = False
    if 'uploaded_files' not in st.session_state:
        st.session_state.uploaded_files = {}
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'landing'

init_session_state()

# Navigation function
def navigate_to(page):
    """Navigate to a specific page"""
    st.session_state.current_page = page
    st.rerun()

# Main app logic
def main():
    """Main application router"""
    
    # Check if we're on landing page
    if st.session_state.current_page == 'landing':
        from pages import landing
        landing.show()
    
    # Check authentication for protected pages
    elif not st.session_state.authenticated:
        from pages import onboarding
        onboarding.show()
    
    else:
        # Show authenticated app
        show_authenticated_app()

def show_authenticated_app():
    """Show the main authenticated application"""
    
    # Sidebar navigation
    with st.sidebar:
        st.markdown(f"""
        <div style='padding: 1rem; background: linear-gradient(135deg, #2E5C8A 0%, #4472C4 100%); 
                    border-radius: 12px; margin-bottom: 1rem; color: white;'>
            <h2 style='margin: 0; color: white !important;'>📊 FMCG Analytics</h2>
            <p style='margin: 0.5rem 0 0 0; opacity: 0.9;'>{st.session_state.company_name}</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Navigation menu
        menu_items = {
            'dashboard': ('📊', 'Dashboard'),
            'services': ('⚙️', 'Services'),
            'upload': ('📤', 'Upload Data'),
            'forecasting': ('📈', 'Demand Forecasting'),
            'inventory': ('📦', 'Inventory Optimization'),
            'chatbot': ('🤖', 'AI Assistant'),
            'settings': ('⚙️', 'Settings'),
        }
        
        for page_key, (icon, label) in menu_items.items():
            if st.button(f"{icon} {label}", key=f"nav_{page_key}", use_container_width=True):
                navigate_to(page_key)
        
        st.markdown("---")
        
        # Status indicator
        if st.session_state.data_uploaded:
            st.success("✅ Data Connected")
        else:
            st.warning("⚠️ No Data Yet")
        
        st.markdown("---")
        
        # Logout button
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.authenticated = False
            st.session_state.company_id = None
            st.session_state.company_name = None
            navigate_to('landing')
    
    # Main content area - route to appropriate page
    current_page = st.session_state.current_page
    
    if current_page == 'dashboard':
        from pages import dashboard
        dashboard.show()
    elif current_page == 'services':
        from pages import services
        services.show()
    elif current_page == 'upload':
        from pages import upload_data
        upload_data.show()
    elif current_page == 'forecasting':
        from pages import forecasting
        forecasting.show()
    elif current_page == 'inventory':
        from pages import inventory
        inventory.show()
    elif current_page == 'chatbot':
        from pages import chatbot
        chatbot.show()
    elif current_page == 'settings':
        from pages import settings
        settings.show()
    else:
        # Default to dashboard
        from pages import dashboard
        dashboard.show()

if __name__ == "__main__":
    main()
