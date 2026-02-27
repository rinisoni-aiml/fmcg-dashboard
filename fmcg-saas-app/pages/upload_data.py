"""Data Upload Page with Schema Mapping"""
import streamlit as st
import pandas as pd
import json

def show():
    """Display data upload page"""
    
    st.markdown("# 📤 Upload Your Data")
    st.markdown(f"**Company:** {st.session_state.company_name}")
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        show_file_upload()
    
    with col2:
        show_api_integration()

def show_file_upload():
    """File upload interface"""
    
    st.markdown("""
    <div class='feature-card'>
        <span class='badge-active'>✅ AVAILABLE</span>
        <div style='font-size: 3rem; text-align: center;'>📁</div>
        <h3>Upload Excel/CSV Files</h3>
        <p>Upload your historical sales, inventory, and product data</p>
    </div>
    """, unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader(
        "Choose Excel or CSV file",
        type=['csv', 'xlsx', 'xls'],
        help="Upload sales orders, inventory, or product data"
    )
    
    if uploaded_file:
        try:
            # Read file
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
            
            st.success(f"✅ File loaded: {len(df)} rows, {len(df.columns)} columns")
            
            # Show preview
            with st.expander("📋 Data Preview"):
                st.dataframe(df.head(10))
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total Rows", len(df))
                with col2:
                    st.metric("Columns", len(df.columns))
                with col3:
                    null_pct = (df.isnull().sum().sum() / (len(df) * len(df.columns)) * 100)
                    st.metric("Missing %", f"{null_pct:.1f}%")
            
            # Schema mapping
            show_schema_mapping(df, uploaded_file.name)
            
        except Exception as e:
            st.error(f"Error reading file: {str(e)}")

def show_schema_mapping(df, filename):
    """Schema mapping interface"""
    
    st.markdown("---")
    st.markdown("### 🗺️ Map Your Columns to Standard Schema")
    st.info("Match your column names to our standard format")
    
    # Define standard schema
    standard_schema = {
        'order_id': 'Unique order identifier',
        'order_date': 'Order date',
        'product_id': 'Product/SKU identifier',
        'customer_id': 'Customer identifier',
        'quantity': 'Order quantity',
        'unit_price': 'Unit price',
        'discount_percent': 'Discount percentage',
        'total_amount': 'Total amount',
    }
    
    mapping = {}
    
    st.markdown("#### Column Mapping")
    
    for std_field, description in standard_schema.items():
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown(f"**{std_field}**")
            st.caption(description)
        
        with col2:
            # Try to auto-detect
            suggestions = [col for col in df.columns if std_field.replace('_', '').lower() in col.lower().replace('_', '')]
            default_idx = df.columns.tolist().index(suggestions[0]) + 1 if suggestions else 0
            
            selected = st.selectbox(
                f"Select column for {std_field}",
                options=["-- Skip --"] + df.columns.tolist(),
                index=default_idx,
                key=f"map_{std_field}",
                label_visibility="collapsed"
            )
            
            if selected != "-- Skip --":
                mapping[std_field] = selected
    
    # Validation
    st.markdown("---")
    st.markdown("### ✅ Validation Results")
    
    valid_rows = len(df)
    issues = []
    
    # Check for nulls in mapped columns
    for std_field, user_col in mapping.items():
        null_count = df[user_col].isnull().sum()
        if null_count > 0:
            issues.append(f"⚠️ {null_count} missing values in {std_field}")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Valid Rows", valid_rows, delta=None)
    with col2:
        st.metric("Issues Found", len(issues))
    with col3:
        status = "✅ PASS" if len(issues) == 0 else "⚠️ WARNING"
        st.metric("Status", status)
    
    if issues:
        with st.expander("⚠️ View Issues"):
            for issue in issues:
                st.warning(issue)
    
    # Save button
    if st.button("💾 Save and Process Data", use_container_width=True, type="primary"):
        # Store in session state
        st.session_state.uploaded_files[filename] = {
            'data': df,
            'mapping': mapping,
            'timestamp': pd.Timestamp.now().isoformat()
        }
        st.session_state.data_uploaded = True
        
        st.success("✅ Data saved successfully!")
        st.balloons()
        st.info("👉 Go to Dashboard to see insights")

def show_api_integration():
    """API integration interface (disabled for now)"""
    
    st.markdown("""
    <div class='feature-card disabled'>
        <span class='badge-soon'>🚧 COMING SOON</span>
        <div style='font-size: 3rem; text-align: center;'>🔌</div>
        <h3>Connect via API</h3>
        <p>Integrate with your ERP/CRM system</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("**Supported systems:**")
    st.markdown("• SAP S/4HANA")
    st.markdown("• Oracle NetSuite")
    st.markdown("• Microsoft Dynamics")
    st.markdown("• Salesforce CRM")
    
    st.text_input("API Endpoint URL", disabled=True)
    st.text_input("API Key", type="password", disabled=True)
    st.button("🔗 Connect", disabled=True, use_container_width=True)
