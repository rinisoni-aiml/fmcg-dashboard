"""Inventory Optimization Page"""
import streamlit as st
import pandas as pd

def show():
    """Display inventory optimization page"""
    
    st.markdown("# 📦 Inventory Optimization")
    
    if not st.session_state.data_uploaded:
        st.warning("⚠️ Please upload data first")
        return
    
    # Stock Status Cards
    st.markdown("### Stock Status Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class='metric-card' style='border-color: #00B050;'>
            <div class='metric-value' style='color: #00B050;'>156</div>
            <div class='metric-label'>Optimal Stock</div>
            <p style='color: #666; font-size: 0.9rem; margin-top: 0.5rem;'>Products well-stocked</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class='metric-card' style='border-color: #FFA500;'>
            <div class='metric-value' style='color: #FFA500;'>34</div>
            <div class='metric-label'>Low Stock</div>
            <p style='color: #666; font-size: 0.9rem; margin-top: 0.5rem;'>Need reordering soon</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class='metric-card' style='border-color: #C00000;'>
            <div class='metric-value' style='color: #C00000;'>12</div>
            <div class='metric-label'>Stockout</div>
            <p style='color: #666; font-size: 0.9rem; margin-top: 0.5rem;'>Immediate action!</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class='metric-card' style='border-color: #2E5C8A;'>
            <div class='metric-value' style='color: #2E5C8A;'>8</div>
            <div class='metric-label'>Overstock</div>
            <p style='color: #666; font-size: 0.9rem; margin-top: 0.5rem;'>Reduce orders</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Inventory Table
    st.markdown("---")
    st.markdown("### Inventory by Warehouse")
    
    # Sample data
    df = pd.DataFrame({
        'Warehouse': ['Delhi', 'Mumbai', 'Bangalore', 'Chennai'],
        'Total Items': [156, 203, 178, 145],
        'Stock Level': ['45% (Low)', '87% (Good)', '62% (Moderate)', '78% (Good)'],
        'Status': ['⚠️ Alert', '✓ OK', '⚡ Monitor', '✓ OK'],
    })
    
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    # Optimization Suggestions
    st.markdown("---")
    st.markdown("### 🎯 Optimization Suggestions")
    
    st.markdown("""
    <div class='alert-info'>
        <strong>📦 Transfer Stock:</strong> Move 100 units of SKU-789 from Mumbai to Delhi
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class='alert-critical'>
        <strong>🔄 Reorder Now:</strong> 500 units of SKU-123 - Will stockout in 3 days
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class='alert-info'>
        <strong>⬇️ Reduce Orders:</strong> SKU-456 overstocked by 20% - Decrease next order
    </div>
    """, unsafe_allow_html=True)
    
    # YOUR ML MODEL INTEGRATION POINT
    st.markdown("---")
    st.info("""
    **🔧 Integration Point:**  
    Replace sample recommendations with your XGBoost model predictions.
    See `utils/ml_models.py` for the integration template.
    """)
