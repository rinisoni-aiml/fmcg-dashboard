"""AI assistant page."""

from __future__ import annotations

import html

import streamlit as st

from utils.analytics import build_chat_context, collect_normalized_data
from utils.chatbot import chatbot_service


def show() -> None:
    st.markdown("## AI assistant")
    st.caption("Ask operations questions based on your current workspace data.")

    if "chat_history" not in st.session_state or not st.session_state.chat_history:
        st.session_state.chat_history = [
            {
                "role": "assistant",
                "content": (
                    "I'm your FMCG analytics assistant. I can help you with demand forecasting, "
                    "inventory optimization, sales analysis, and operational insights. "
                    "Ask me anything about your data!"
                ),
            }
        ]

    df = collect_normalized_data(st.session_state.uploaded_files)
    
    # Build comprehensive context with all data
    from utils.analytics import dashboard_payload
    
    if not df.empty:
        full_payload = dashboard_payload(df)
        context = build_chat_context(
            company_name=st.session_state.company_name or "Unknown",
            industry=st.session_state.industry or "FMCG",
            df=df,
        )
        # Add inventory and alerts to context
        context["inventory"] = full_payload.get("inventory", {})
        context["alerts"] = full_payload.get("alerts", [])
    else:
        context = {
            "company_name": st.session_state.company_name or "Unknown",
            "industry": st.session_state.industry or "FMCG",
            "rows": 0,
            "kpis": {},
            "top_regions": [],
            "insights": [],
            "inventory": {},
            "alerts": []
        }

    if df.empty:
        st.warning("No processed data found. Upload data to get detailed insights.")

    st.markdown("### Quick Questions")
    quick_col1, quick_col2, quick_col3, quick_col4 = st.columns(4)
    with quick_col1:
        if st.button("📦 Low stock alerts", use_container_width=True):
            _process_query("Which products are at risk of stockout? Give me specific recommendations.", context)
    with quick_col2:
        if st.button("📈 Top performers", use_container_width=True):
            _process_query("Show me the top selling products and regions by revenue.", context)
    with quick_col3:
        if st.button("🔮 Demand forecast", use_container_width=True):
            _process_query("What's the demand forecast for the next 7 days? Any trends I should know?", context)
    with quick_col4:
        if st.button("💡 Key insights", use_container_width=True):
            _process_query("Give me the top 3 actionable insights from my current data.", context)

    st.markdown("---")
    st.markdown('<div class="chat-shell">', unsafe_allow_html=True)
    for message in st.session_state.chat_history:
        safe_content = html.escape(message["content"]).replace("\n", "<br>")
        if message["role"] == "user":
            st.markdown(f'<div class="chat-user"><strong>You</strong><br>{safe_content}</div>', unsafe_allow_html=True)
        else:
            st.markdown(
                f'<div class="chat-assistant"><strong>Assistant</strong><br>{safe_content}</div>',
                unsafe_allow_html=True,
            )
    st.markdown("</div>", unsafe_allow_html=True)

    user_input = st.chat_input("Ask about inventory, forecasts, sales, or any operational question...")
    if user_input:
        _process_query(user_input, context)
        st.rerun()

    if chatbot_service.client:
        st.success(f"✓ AI Powered by Groq ({chatbot_service.model})")
    else:
        st.info("💡 Add GROQ_API_KEY to .env for AI-powered responses")


def _process_query(query: str, context: dict) -> None:
    st.session_state.chat_history.append({"role": "user", "content": query})
    history = st.session_state.chat_history[:-1]
    response = chatbot_service.get_response(query, company_data=context, history=history)
    st.session_state.chat_history.append({"role": "assistant", "content": response})
