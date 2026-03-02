"""Services configuration page."""

from __future__ import annotations

import streamlit as st

from utils.session import navigate_to


def show() -> None:
    st.markdown("## Services")
    st.caption("Step 2 of 3 - choose enabled modules for this workspace")

    st.markdown(
        """
        <div class="panel-card" style="margin-bottom:0.75rem;">
            <strong>Workspace:</strong> {company}<br>
            <span style="color:#475569;">Turn modules on/off now. You can edit this again in Settings.</span>
        </div>
        """.format(company=st.session_state.company_name or "N/A"),
        unsafe_allow_html=True,
    )

    c1, c2, c3 = st.columns(3)
    with c1:
        _module_card(
            key="forecasting",
            title="Demand Forecasting",
            desc="Project 7-90 day demand by product and region with confidence ranges.",
        )
    with c2:
        _module_card(
            key="inventory",
            title="Inventory Optimization",
            desc="Prioritize low cover products and operational replenishment actions.",
        )
    with c3:
        _module_card(
            key="chatbot",
            title="AI Assistant",
            desc="Ask operational questions against your data with Groq-hosted models.",
        )

    st.markdown("---")
    st.markdown("### Roadmap modules")
    future_modules = [
        ("Sales Optimization", "Conversion and territory optimization from sales funnel performance."),
        ("P&L Insights", "Margin and profitability diagnostics across SKUs and regions."),
        ("Autonomous Pricing", "Price sensitivity-aware recommendations based on demand and stock."),
    ]
    for name, description in future_modules:
        st.markdown(
            f"""
            <div class="panel-card" style="opacity:0.72;">
                <strong>{name}</strong><br>
                <span style="color:#475569;">{description}</span><br>
                <span style="font-size:0.8rem;color:#64748b;">Status: Coming soon</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("---")
    enabled_count = sum(bool(v) for v in st.session_state.services.values())
    st.caption(f"Enabled modules: {enabled_count}")

    col1, col2 = st.columns([2, 1])
    with col2:
        if st.button("Next: Upload data", type="primary", use_container_width=True):
            if enabled_count == 0:
                st.error("Enable at least one active module before continuing.")
                return
            st.session_state.services_configured = True
            navigate_to("upload")


def _module_card(key: str, title: str, desc: str) -> None:
    with st.container(border=True):
        st.markdown(f"#### {title}")
        st.markdown(desc)
        st.session_state.services[key] = st.toggle(
            "Enabled",
            value=bool(st.session_state.services.get(key, True)),
            key=f"service_toggle_{key}",
        )
