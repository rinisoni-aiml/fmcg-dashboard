"""Onboarding Flow - Industry Selection"""
import streamlit as st
import uuid
from datetime import datetime

def show():
    """Display onboarding/login page"""
    
    st.markdown("### 🏢 Company Onboarding")
    
    tab1, tab2 = st.tabs(["New Company", "Existing Company"])
    
    with tab1:
        show_industry_selection()
    
    with tab2:
        show_login()

def show_industry_selection():
    """Industry selection for new companies"""
    
    st.markdown("""
    <div style='text-align: center; margin: 2rem 0;'>
        <p style='color: #999;'>Step 1 of 3</p>
        <h2>Welcome! Let\'s Get Started</h2>
        <p style='color: #666;'>First, tell us about your industry</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    industries = {
        "FMCG": ("🛒", "Fast-Moving Consumer Goods including food, beverages, personal care"),
        "Healthcare": ("🏥", "Hospitals, clinics, medical supplies, pharmaceuticals"),
        "Education": ("🎓", "Schools, universities, e-learning platforms"),
        "Fintech": ("💰", "Banking, payments, lending, insurance"),
        "Logistics": ("🚚", "Shipping, warehousing, supply chain"),
        "Cyber Security": ("🔒", "Network security, threat detection, compliance"),
    }
    
    selected_industry = None
    
    for i, (industry, (icon, desc)) in enumerate(industries.items()):
        col = [col1, col2, col3][i % 3]
        with col:
            if st.button(
                f"{icon}\n\n**{industry}**\n\n{desc}",
                key=f"ind_{industry}",
                use_container_width=True
            ):
                selected_industry = industry
    
    if selected_industry:
        st.session_state.industry = selected_industry
        show_company_details()

def show_company_details():
    """Collect company details"""
    
    st.markdown("---")
    st.markdown("### Company Information")
    
    with st.form("company_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            company_name = st.text_input("Company Name *", placeholder="ABC Foods Pvt Ltd")
            contact_name = st.text_input("Contact Person *", placeholder="Your name")
            email = st.text_input("Email *", placeholder="name@company.com")
        
        with col2:
            phone = st.text_input("Phone", placeholder="+91 1234567890")
            num_products = st.number_input("Number of Products", min_value=1, value=100)
            num_warehouses = st.number_input("Number of Warehouses", min_value=1, value=5)
        
        submitted = st.form_submit_button("Complete Onboarding →", use_container_width=True)
        
        if submitted:
            if company_name and contact_name and email:
                # Create company
                company_id = f"COMP{str(uuid.uuid4())[:8].upper()}"
                
                st.session_state.company_id = company_id
                st.session_state.company_name = company_name
                st.session_state.authenticated = True
                st.session_state.current_page = 'services'
                
                st.success(f"✅ Welcome aboard, {company_name}!")
                st.balloons()
                st.rerun()
            else:
                st.error("Please fill all required fields (*)")

def show_login():
    """Login for existing companies"""
    
    st.markdown("### Login to Existing Account")
    
    # For demo, just create a quick login
    company_name = st.text_input("Company Name")
    
    if st.button("Login", use_container_width=True):
        if company_name:
            company_id = f"COMP{str(uuid.uuid4())[:8].upper()}"
            st.session_state.company_id = company_id
            st.session_state.company_name = company_name
            st.session_state.industry = "FMCG"
            st.session_state.authenticated = True
            st.session_state.current_page = 'dashboard'
            st.rerun()
        else:
            st.error("Please enter company name")
