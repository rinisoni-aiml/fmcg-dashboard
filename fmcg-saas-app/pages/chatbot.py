"""AI assistant page — premium chat using native st.chat_message."""

from __future__ import annotations

import streamlit as st

from utils.analytics import build_chat_context, collect_normalized_data, dashboard_payload
from utils.chatbot import chatbot_service
from utils.database import db_service


def show() -> None:
    st.markdown(
        """
        <div class="hero-banner">
            <h2>🤖  AI Assistant</h2>
            <p>Ask operations questions based on your uploaded data — powered by Groq</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Initialize chat history
    if "chat_history" not in st.session_state or not st.session_state.chat_history:
        # Try to load from DB
        loaded = []
        if db_service.is_connected() and st.session_state.company_name:
            loaded = db_service.get_chat_history(st.session_state.company_name, limit=30)

        if loaded:
            st.session_state.chat_history = loaded
        else:
            st.session_state.chat_history = [
                {
                    "role": "assistant",
                    "content": (
                        "👋 Hi! I'm your FMCG analytics assistant. I can help with:\n\n"
                        "• **Demand forecasting** — trends, predictions, and recommendations\n"
                        "• **Inventory optimization** — stockout risks, reorder points\n"
                        "• **Sales analysis** — top products, regional performance\n"
                        "• **Operational insights** — actionable recommendations from your data\n\n"
                        "Ask me anything about your data!"
                    ),
                }
            ]

    df = collect_normalized_data(st.session_state.uploaded_files)

    # Build comprehensive context
    if not df.empty:
        full_payload = dashboard_payload(df)
        context = build_chat_context(
            company_name=st.session_state.company_name or "Unknown",
            industry=st.session_state.industry or "FMCG",
            df=df,
        )
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
            "alerts": [],
        }

    if df.empty:
        st.warning("📂  No processed data found. Upload data first for detailed insights.")

    # Quick question buttons
    st.markdown("### ⚡  Quick Questions")
    q1, q2, q3, q4 = st.columns(4)
    with q1:
        if st.button("📦  Low Stock Alerts", use_container_width=True):
            _process_query("Which products are at risk of stockout? Give me specific product IDs and recommendations.", context)
            st.rerun()
    with q2:
        if st.button("📈  Top Performers", use_container_width=True):
            _process_query("Show me the top selling products and regions by revenue. Include specific numbers.", context)
            st.rerun()
    with q3:
        if st.button("🔮  Demand Forecast", use_container_width=True):
            _process_query("What's the demand forecast for the next 7 days? Any trends I should know about?", context)
            st.rerun()
    with q4:
        if st.button("💡  Key Insights", use_container_width=True):
            _process_query("Give me the top 3 actionable insights from my current data with specific recommendations.", context)
            st.rerun()

    st.markdown("---")

    # Chat messages using native Streamlit chat
    for message in st.session_state.chat_history:
        role = message["role"]
        with st.chat_message(role, avatar="🤖" if role == "assistant" else "👤"):
            st.markdown(message["content"])

    # Chat input
    user_input = st.chat_input("Ask about inventory, forecasts, sales, or any operational question...")
    if user_input:
        _process_query(user_input, context)
        st.rerun()

    # Status
    st.markdown("---")
    status_cols = st.columns(3)
    with status_cols[0]:
        if chatbot_service.client:
            st.success(f"✅  AI powered by Groq ({chatbot_service.model})")
        else:
            st.info("💡  Add `GROQ_API_KEY` to `.env` for AI-powered responses")
    with status_cols[1]:
        if db_service.is_connected():
            st.success("✅  Chat history saved to Supabase")
        else:
            st.info("💾  Session-only chat (add `DATABASE_URL` for persistence)")
    with status_cols[2]:
        msg_count = len(st.session_state.chat_history)
        st.caption(f"💬  {msg_count} messages in conversation")


def _process_query(query: str, context: dict) -> None:
    """Process a user query and get AI response."""
    st.session_state.chat_history.append({"role": "user", "content": query})

    # Save user message to DB
    if db_service.is_connected() and st.session_state.company_name:
        db_service.save_chat_message(st.session_state.company_name, "user", query)

    history = st.session_state.chat_history[:-1]
    response = chatbot_service.get_response(query, company_data=context, history=history)

    st.session_state.chat_history.append({"role": "assistant", "content": response})

    # Save assistant response to DB
    if db_service.is_connected() and st.session_state.company_name:
        db_service.save_chat_message(st.session_state.company_name, "assistant", response)
