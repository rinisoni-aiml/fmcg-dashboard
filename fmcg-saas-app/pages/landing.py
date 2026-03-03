"""Landing page — premium hero and feature showcase."""

from __future__ import annotations

import streamlit as st

from utils.session import navigate_to


def show() -> None:
    # Hero section
    st.markdown(
        """
        <div style="
            border-radius: 24px;
            padding: 2.8rem 2.2rem;
            background: linear-gradient(135deg, #0b1e36 0%, #0f4c81 40%, #1a6bb5 75%, #3b8ad9 100%);
            color: white;
            position: relative;
            overflow: hidden;
            margin-bottom: 1.5rem;
            box-shadow: 0 20px 48px rgba(15,76,129,0.25);
        ">
            <div style="position:absolute;top:-80px;right:-60px;width:350px;height:350px;background:radial-gradient(circle,rgba(249,115,22,0.15) 0%,transparent 70%);border-radius:50%;"></div>
            <div style="position:absolute;bottom:-100px;left:10%;width:250px;height:250px;background:radial-gradient(circle,rgba(255,255,255,0.08) 0%,transparent 70%);border-radius:50%;"></div>
            <div style="position:relative;z-index:1;">
                <p style="opacity:0.75;margin:0 0 0.3rem 0;font-size:0.82rem;text-transform:uppercase;letter-spacing:0.08em;font-weight:600;">FMCG SaaS Platform</p>
                <h1 style="margin:0 0 0.8rem 0;color:white !important;font-size:2.4rem;font-weight:800;line-height:1.15;letter-spacing:-0.03em;">
                    AI-Powered Operations<br>Intelligence
                </h1>
                <p style="max-width:640px;margin:0;opacity:0.88;font-size:1.05rem;line-height:1.6;">
                    Connect sales and inventory data, forecast demand with Prophet ML models, 
                    detect stock risk early, and chat with an AI assistant — all from one platform.
                </p>
            </div>
            <div style="position:relative;z-index:1;margin-top:1.2rem;display:flex;gap:0.75rem;flex-wrap:wrap;">
                <div style="display:flex;align-items:center;gap:0.4rem;background:rgba(255,255,255,0.12);border-radius:999px;padding:0.35rem 0.75rem;font-size:0.78rem;font-weight:600;">
                    ✅ Real-time data insights
                </div>
                <div style="display:flex;align-items:center;gap:0.4rem;background:rgba(255,255,255,0.12);border-radius:999px;padding:0.35rem 0.75rem;font-size:0.78rem;font-weight:600;">
                    📊 Prophet ML Forecasting
                </div>
                <div style="display:flex;align-items:center;gap:0.4rem;background:rgba(255,255,255,0.12);border-radius:999px;padding:0.35rem 0.75rem;font-size:0.78rem;font-weight:600;">
                    🤖 AI Copilot
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    cta_col1, cta_col2, _ = st.columns([1.2, 1.1, 2.2])
    with cta_col1:
        if st.button("🚀  Start Free Trial", type="primary", use_container_width=True):
            navigate_to("onboarding")
    with cta_col2:
        if st.button("🔑  Login", use_container_width=True):
            navigate_to("onboarding")

    # How it works
    st.markdown("### How it works")
    steps = [
        ("1️⃣", "Onboard", "Register your company and team in under 60 seconds."),
        ("2️⃣", "Upload Data", "Import CSV/Excel files — auto-mapped to our schema."),
        ("3️⃣", "Get Insights", "Dashboard, forecasts, and AI assistant — instantly."),
    ]
    cols = st.columns(3)
    for i, (icon, title, desc) in enumerate(steps):
        with cols[i]:
            st.markdown(
                f"""
                <div class="panel-card" style="text-align:center;padding:1.3rem 1rem;min-height:165px;">
                    <div style="font-size:2rem;margin-bottom:0.4rem;">{icon}</div>
                    <h4 style="margin:0 0 0.4rem 0;">{title}</h4>
                    <p style="margin:0;color:#475569;font-size:0.88rem;">{desc}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown("")

    # Industry cards
    st.markdown("### Built for modern operations teams")
    industries = [
        ("🏭", "FMCG", "Forecast demand, optimize inventory, and reduce stockout events."),
        ("🏥", "Healthcare", "Plan critical supplies and control replenishment risks."),
        ("🎓", "Education", "Improve resource planning using demand and trend analytics."),
        ("💳", "Fintech", "Track usage trends and forecast capacity requirements."),
        ("🚛", "Logistics", "Optimize route-linked inventory and fulfillment timing."),
        ("🔒", "Cyber Security", "Model incident volume trends and staffing demand."),
    ]

    col1, col2, col3 = st.columns(3)
    cols = [col1, col2, col3]
    for i, (icon, name, desc) in enumerate(industries):
        with cols[i % 3]:
            st.markdown(
                f"""
                <div class="panel-card" style="min-height:140px;margin-bottom:0.6rem;">
                    <div style="font-size:1.5rem;margin-bottom:0.3rem;">{icon}</div>
                    <h4 style="margin:0 0 0.4rem 0;font-size:1rem;">{name}</h4>
                    <p style="margin:0;color:#475569;font-size:0.85rem;">{desc}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

    # Core capabilities
    st.markdown("### Core capabilities")
    c1, c2, c3 = st.columns(3)
    capabilities = [
        ("🔮", "Demand Forecasting", "Model 7–90 day demand with Prophet ML and confidence intervals.", "#0f4c81"),
        ("📦", "Inventory Optimization", "Detect low cover risk and prioritize replenishment actions.", "#15803d"),
        ("🤖", "AI Copilot", "Ask operational questions and get data-driven recommendations.", "#ea580c"),
    ]
    for col, (icon, title, desc, color) in zip([c1, c2, c3], capabilities):
        with col:
            st.markdown(
                f"""
                <div class="panel-card" style="border-top:4px solid {color};min-height:140px;">
                    <div style="font-size:1.4rem;margin-bottom:0.35rem;">{icon}</div>
                    <h4 style="margin:0 0 0.4rem 0;">{title}</h4>
                    <p style="margin:0;color:#475569;font-size:0.85rem;">{desc}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
