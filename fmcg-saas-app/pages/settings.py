"""Settings Page"""
import streamlit as st

def show():
    """Display settings page"""
    
    st.markdown("# ⚙️ Settings")
    
    tab1, tab2, tab3 = st.tabs(["Profile", "Company", "Data Sources"])
    
    with tab1:
        show_profile()
    
    with tab2:
        show_company()
    
    with tab3:
        show_data_sources()

def show_profile():
    """Profile settings"""
    
    st.markdown("### User Profile")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.text_input("Name", value="John Doe")
        st.text_input("Email", value="john@company.com")
    
    with col2:
        st.text_input("Phone", value="+91 1234567890")
        st.selectbox("Role", ["Admin", "Manager", "Analyst"])
    
    if st.button("Save Profile", type="primary"):
        st.success("✅ Profile updated!")

def show_company():
    """Company settings"""
    
    st.markdown("### Company Details")
    
    st.text_input("Company Name", value=st.session_state.company_name, disabled=True)
    st.text_input("Industry", value=st.session_state.industry or "FMCG", disabled=True)
    
    st.markdown("---")
    st.markdown("### Notification Preferences")
    
    st.checkbox("Email alerts for critical issues", value=True)
    st.checkbox("Daily summary reports", value=True)
    st.checkbox("Weekly performance digest", value=False)
    
    if st.button("Save Settings", type="primary"):
        st.success("✅ Settings saved!")

def show_data_sources():
    """Data sources"""
    
    st.markdown("### Connected Data Sources")
    
    if st.session_state.uploaded_files:
        for filename, info in st.session_state.uploaded_files.items():
            st.markdown(f"""
            <div class='feature-card'>
                <strong>📁 {filename}</strong><br>
                Uploaded: {info['timestamp'][:10]}<br>
                Rows: {len(info['data'])}
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No data sources connected yet")
    
    if st.button("➕ Add New Source"):
        st.session_state.current_page = 'upload'
        st.rerun()
