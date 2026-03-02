"""Landing page."""

from __future__ import annotations

import streamlit as st

from utils.session import navigate_to


def show() -> None:
    st.markdown(
        """
        <div style="border:1px solid #dbe1ea;border-radius:14px;padding:2.2rem;background:linear-gradient(130deg,#0f4c81 0%,#1f6fb2 58%,#60a5fa 100%);color:white;">
            <div style="display:flex;justify-content:space-between;gap:1rem;align-items:flex-start;flex-wrap:wrap;">
                <div>
                    <p style="opacity:0.85;margin:0;">FMCG SaaS Platform</p>
                    <h1 style="margin:0.4rem 0 0.8rem 0;color:white !important;">AI-Powered Operations Intelligence</h1>
                    <p style="max-width:760px;margin:0;opacity:0.92;">
                        Connect sales and inventory data, forecast demand, detect stock risk early,
                        and manage operations from one production-grade interface.
                    </p>
                </div>
                <div style="text-align:right;">
                    <div style="font-size:0.86rem;opacity:0.9;">Delivery flow</div>
                    <div style="font-weight:700;">1. Onboard</div>
                    <div style="font-weight:700;">2. Select services</div>
                    <div style="font-weight:700;">3. Upload data</div>
                    <div style="font-weight:700;">4. Operate</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    cta_col1, cta_col2, _ = st.columns([1.2, 1.1, 2.2])
    with cta_col1:
        if st.button("Start Free Trial", type="primary", use_container_width=True):
            navigate_to("onboarding")
    with cta_col2:
        if st.button("Login", use_container_width=True):
            navigate_to("onboarding")

    st.markdown("### Built for modern operations teams")
    industries = [
        ("FMCG", "Forecast demand, optimize inventory, and reduce stockout events."),
        ("Healthcare", "Plan critical supplies and control replenishment risks."),
        ("Education", "Improve resource planning using demand and trend analytics."),
        ("Fintech", "Track usage trends and forecast capacity requirements."),
        ("Logistics", "Optimize route-linked inventory and fulfillment timing."),
        ("Cyber Security", "Model incident volume trends and staffing demand."),
    ]

    col1, col2, col3 = st.columns(3)
    cols = [col1, col2, col3]
    for i, (name, desc) in enumerate(industries):
        with cols[i % 3]:
            st.markdown(
                f"""
                <div class="panel-card" style="height:170px;">
                    <h4 style="margin:0 0 0.55rem 0;">{name}</h4>
                    <p style="margin:0;color:#475569;">{desc}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown("### Core capabilities")
    m1, m2, m3 = st.columns(3)
    with m1:
        st.markdown("**Demand Forecasting**  \nModel 7-90 day demand and likely trend breaks.")
    with m2:
        st.markdown("**Inventory Optimization**  \nDetect low cover risk and prioritize replenishment actions.")
    with m3:
        st.markdown("**AI Copilot**  \nAsk operations questions and get context-aware recommendations.")
