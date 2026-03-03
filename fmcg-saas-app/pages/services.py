"""Services configuration page — premium module selection."""

from __future__ import annotations

import streamlit as st

from utils.session import navigate_to


MODULE_INFO = {
    "forecasting": {
        "title": "Demand Forecasting",
        "icon": "🔮",
        "desc": "Project 7–90 day demand by product and region with Prophet ML models and confidence intervals.",
        "color": "#0f4c81",
    },
    "inventory": {
        "title": "Inventory Optimization",
        "icon": "📦",
        "desc": "Prioritize low cover products, detect stockout risks, and generate replenishment actions.",
        "color": "#15803d",
    },
    "chatbot": {
        "title": "AI Assistant",
        "icon": "🤖",
        "desc": "Ask operational questions against your data powered by Groq LLMs. Get instant insights.",
        "color": "#ea580c",
    },
}


def show() -> None:
    st.markdown(
        """
        <div class="hero-banner" style="text-align:center;">
            <h2>⚙️  Configure Services</h2>
            <p>Choose which analytics modules to activate for your workspace</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Progress bar
    st.markdown(
        """
        <div style="display:flex;justify-content:center;gap:1.5rem;margin-bottom:1.5rem;">
            <div style="display:flex;align-items:center;gap:0.4rem;">
                <div style="width:30px;height:30px;border-radius:50%;background:#22c55e;color:white;display:flex;align-items:center;justify-content:center;font-size:0.75rem;font-weight:700;">✓</div>
                <span style="font-weight:500;color:#22c55e;">Account</span>
            </div>
            <div style="width:40px;height:2px;background:#22c55e;margin-top:14px;"></div>
            <div style="display:flex;align-items:center;gap:0.4rem;">
                <div style="width:30px;height:30px;border-radius:50%;background:linear-gradient(135deg,#0f4c81,#3b8ad9);color:white;display:flex;align-items:center;justify-content:center;font-size:0.75rem;font-weight:700;">2</div>
                <span style="font-weight:600;color:#0f4c81;">Services</span>
            </div>
            <div style="width:40px;height:2px;background:#cbd5e1;margin-top:14px;"></div>
            <div style="display:flex;align-items:center;gap:0.4rem;">
                <div style="width:30px;height:30px;border-radius:50%;background:#e2e8f0;color:#64748b;display:flex;align-items:center;justify-content:center;font-size:0.75rem;font-weight:700;">3</div>
                <span style="color:#94a3b8;font-weight:500;">Data</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <div class="panel-card" style="margin-bottom:1rem;">
            <strong>Workspace:</strong> {st.session_state.company_name or "N/A"}<br>
            <span style="color:#475569;font-size:0.88rem;">Toggle modules on or off. You can change these later in Settings.</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### Active Modules")
    cols = st.columns(3)
    for (key, info), col in zip(MODULE_INFO.items(), cols):
        with col:
            _module_card(key=key, **info)

    st.markdown("---")
    st.markdown("### Roadmap")
    future_modules = [
        ("📈", "Sales Optimization", "Conversion and territory optimization from sales funnel performance."),
        ("💰", "P&L Insights", "Margin and profitability diagnostics across SKUs and regions."),
        ("🏷️", "Autonomous Pricing", "Price sensitivity-aware recommendations based on demand and stock."),
    ]
    cols = st.columns(3)
    for (icon, name, description), col in zip(future_modules, cols):
        with col:
            st.markdown(
                f"""
                <div class="panel-card" style="opacity:0.60;min-height:140px;">
                    <div style="font-size:1.3rem;margin-bottom:0.3rem;">{icon}</div>
                    <strong>{name}</strong><br>
                    <span style="color:#475569;font-size:0.85rem;">{description}</span><br>
                    <span style="font-size:0.75rem;color:#94a3b8;font-weight:600;text-transform:uppercase;letter-spacing:0.03em;">Coming Soon</span>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown("---")
    enabled_count = sum(bool(v) for v in st.session_state.services.values())
    st.caption(f"Active modules: **{enabled_count}** / {len(MODULE_INFO)}")

    col1, col2 = st.columns([2, 1])
    with col2:
        if st.button("Next: Upload Data  →", type="primary", use_container_width=True):
            if enabled_count == 0:
                st.error("⚠️  Enable at least one module before continuing.")
                return
            st.session_state.services_configured = True
            navigate_to("upload")


def _module_card(key: str, title: str, icon: str, desc: str, color: str) -> None:
    with st.container(border=True):
        st.markdown(
            f"""
            <div style="display:flex;align-items:center;gap:0.5rem;margin-bottom:0.3rem;">
                <span style="font-size:1.3rem;">{icon}</span>
                <span style="font-weight:700;font-size:1rem;">{title}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown(f'<p style="font-size:0.85rem;color:#475569;margin:0 0 0.5rem 0;">{desc}</p>', unsafe_allow_html=True)
        st.session_state.services[key] = st.toggle(
            "Enabled",
            value=bool(st.session_state.services.get(key, True)),
            key=f"service_toggle_{key}",
        )
