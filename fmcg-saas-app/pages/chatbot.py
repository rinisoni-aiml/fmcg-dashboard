"""AI Chatbot Interface"""
import streamlit as st
from datetime import datetime

def show():
    """Display AI chatbot interface"""
    
    st.markdown("# 🤖 AI Assistant")
    st.markdown("Ask me anything about your data!")
    
    if not st.session_state.data_uploaded:
        st.warning("⚠️ Please upload data first to get data-specific insights")
    
    # Initialize chat history
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = [
            {"role": "assistant", "content": "Hi! I'm your AI assistant. Ask me anything about your data."}
        ]
    
    # Quick action buttons
    st.markdown("### Quick Questions")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📦 Low stock products?"):
            process_query("Which products are low in stock?")
    
    with col2:
        if st.button("📈 Top sellers?"):
            process_query("Show me top selling products")
    
    with col3:
        if st.button("🎯 Forecast accuracy?"):
            process_query("What's my forecast accuracy?")
    
    st.markdown("---")
    
    # Chat history
    chat_container = st.container()
    with chat_container:
        for message in st.session_state.chat_history:
            if message["role"] == "user":
                st.markdown(f"""
                <div style='background: #E8F0F7; padding: 1rem; border-radius: 8px; margin: 0.5rem 0; margin-left: 3rem;'>
                    <strong>You:</strong><br>{message["content"]}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style='background: white; border: 1px solid #ddd; padding: 1rem; border-radius: 8px; margin: 0.5rem 0; margin-right: 3rem;'>
                    <strong>🤖 AI Assistant:</strong><br>{message["content"]}
                </div>
                """, unsafe_allow_html=True)
    
    # Chat input
    st.markdown("---")
    col1, col2 = st.columns([5, 1])
    
    with col1:
        user_input = st.text_input("Type your question...", key="chat_input", label_visibility="collapsed")
    
    with col2:
        send_button = st.button("Send", type="primary", use_container_width=True)
    
    if send_button and user_input:
        process_query(user_input)
        st.rerun()
    
    # Voice input placeholder
    st.markdown("---")
    st.info("🎤 Voice input coming soon!")
    
    # YOUR CLAUDE API INTEGRATION POINT
    st.markdown("---")
    st.info("""
    **🔧 Integration Point:**  
    Replace mock responses with actual Claude API calls.
    See `utils/chatbot.py` for the integration template.
    Add your ANTHROPIC_API_KEY to .env file.
    """)

def process_query(query):
    """Process user query"""
    # Add user message
    st.session_state.chat_history.append({"role": "user", "content": query})
    
    # Mock response - REPLACE WITH CLAUDE API
    if "low stock" in query.lower():
        response = """I found 12 products that need immediate attention:
        
1. Product A (SKU-123) - 5 units left in Delhi
2. Product B (SKU-456) - Stockout in Mumbai
3. Product C (SKU-789) - Below reorder point in Bangalore

Would you like me to create reorder recommendations?"""
    
    elif "top sell" in query.lower():
        response = """Here are your top 5 selling products this month:
        
1. Product X - ₹2.5M revenue (↑15%)
2. Product Y - ₹1.8M revenue (↑8%)
3. Product Z - ₹1.2M revenue (↓3%)
4. Product A - ₹950K revenue (↑12%)
5. Product B - ₹780K revenue (↑5%)

Would you like detailed insights on any product?"""
    
    elif "forecast accuracy" in query.lower():
        response = """Your current forecast accuracy is **92%** (MAPE: 8%).

📈 Performance trends:
- Last month: 89% (improved by 3%)
- Best performing: North region (95%)
- Needs improvement: West region (87%)

Your models are performing well! The 92% accuracy is above industry standard."""
    
    else:
        response = f"I understand you're asking about: {query}\n\nI'm currently in demo mode. In production, I'll provide detailed insights based on your actual data using Claude AI."
    
    # Add assistant response
    st.session_state.chat_history.append({"role": "assistant", "content": response})
