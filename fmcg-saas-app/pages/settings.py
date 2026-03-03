"""Settings page — fixed with proper DB methods."""

from __future__ import annotations

import streamlit as st

from utils.database import db_service
from utils.session import navigate_to


def show() -> None:
    st.markdown(
        """
        <div class="hero-banner">
            <h2>🛠  Settings</h2>
            <p>Manage your profile, company, data sources, and integrations</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    tabs = st.tabs(["👤  Profile", "🏢  Company", "📁  Data Sources", "🔗  Integrations"])
    with tabs[0]:
        _show_profile()
    with tabs[1]:
        _show_company()
    with tabs[2]:
        _show_data_sources()
    with tabs[3]:
        _show_integrations()


def _show_profile() -> None:
    st.markdown("### User Profile")
    industries = ["FMCG", "Healthcare", "Education", "Fintech", "Logistics", "Cyber Security"]
    current_industry = st.session_state.industry if st.session_state.industry in industries else "FMCG"
    with st.form("profile_form"):
        c1, c2 = st.columns(2)
        with c1:
            name = st.text_input("Contact name", value=st.session_state.contact_name or "")
            email = st.text_input("Email", value=st.session_state.email or "")
        with c2:
            phone = st.text_input("Phone", value=st.session_state.phone or "")
            industry = st.selectbox(
                "Industry",
                industries,
                index=industries.index(current_industry),
            )
        save = st.form_submit_button("💾  Save Profile", type="primary", width="stretch")

    if save:
        st.session_state.contact_name = name
        st.session_state.email = email
        st.session_state.phone = phone
        st.session_state.industry = industry
        st.success("✅  Profile updated")


def _show_company() -> None:
    st.markdown("### Company")
    company_name = st.text_input("Company name", value=st.session_state.company_name or "")
    st.text_input("Company ID", value=st.session_state.company_id or "", disabled=True)

    st.markdown("### Enabled Modules")
    for module_key in ["forecasting", "inventory", "chatbot"]:
        icons = {"forecasting": "🔮", "inventory": "📦", "chatbot": "🤖"}
        st.session_state.services[module_key] = st.checkbox(
            f"{icons.get(module_key, '')}  {module_key.capitalize()}",
            value=bool(st.session_state.services.get(module_key, True)),
            key=f"settings_module_{module_key}",
        )

    if st.button("💾  Save Company Settings", type="primary"):
        st.session_state.company_name = company_name

        if db_service.is_connected() and st.session_state.email:
            result = db_service.upsert_company(
                company_name=company_name,
                contact_name=st.session_state.contact_name or "User",
                email=st.session_state.email,
                phone=st.session_state.phone or "",
                industry=st.session_state.industry or "FMCG",
            )
            if result:
                st.session_state.company_id = f"COMP-{result.id}"
                st.success("✅  Saved to Supabase PostgreSQL")
            else:
                st.warning("⚠️  Could not persist to database — session values updated only.")
        else:
            st.success("✅  Saved in current session")


def _show_data_sources() -> None:
    st.markdown("### Connected Files")
    if not st.session_state.uploaded_files:
        st.markdown(
            """
            <div class="panel-card" style="text-align:center;padding:1.5rem;">
                <div style="font-size:2rem;margin-bottom:0.3rem;">📂</div>
                <p style="margin:0;color:#64748b;">No files processed yet</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        for name, meta in st.session_state.uploaded_files.items():
            rows = len(meta.get("normalized_data", []))
            ts = meta.get("timestamp", "")[:19].replace("T", " ")
            st.markdown(
                f"""
                <div class="panel-card" style="margin-bottom:0.55rem;">
                    <div style="display:flex;justify-content:space-between;align-items:center;">
                        <strong>📄  {name}</strong>
                        <span style="font-size:0.75rem;color:#15803d;font-weight:600;">✅ ACTIVE</span>
                    </div>
                    <span style="color:#475569;font-size:0.82rem;">{rows:,} rows · {ts} UTC</span>
                </div>
                """,
                unsafe_allow_html=True,
            )
    if st.button("📁  Add Data Source", width="stretch"):
        navigate_to("upload")


def _show_integrations() -> None:
    st.markdown("### Integration Status")

    from utils.chatbot import chatbot_service
    integrations = [
        ("DATABASE_URL", "PostgreSQL / Supabase", db_service.is_connected()),
        ("GROQ_API_KEY", "AI Chatbot (Groq LLM)", chatbot_service.client is not None),
    ]

    for env_key, label, connected in integrations:
        status_icon = "🟢" if connected else "🔴"
        status_text = "Connected" if connected else "Not configured"
        status_color = "#15803d" if connected else "#dc2626"
        st.markdown(
            f"""
            <div class="panel-card" style="margin-bottom:0.55rem;">
                <div style="display:flex;justify-content:space-between;align-items:center;">
                    <div>
                        <strong>{label}</strong><br>
                        <code style="font-size:0.78rem;color:#64748b;">{env_key}</code>
                    </div>
                    <div style="text-align:right;">
                        <span style="font-size:1.1rem;">{status_icon}</span>
                        <span style="font-size:0.82rem;color:{status_color};font-weight:600;margin-left:0.3rem;">{status_text}</span>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("---")
    st.markdown("#### Configuration Reference")
    st.markdown(
        """
        | Variable | Purpose | Required |
        |---|---|---|
        | `DATABASE_URL` | PostgreSQL connection string for Supabase | Recommended |
        | `GROQ_API_KEY` | API key for Groq-hosted LLMs | For AI Assistant |
        | `GROQ_MODEL` | Model override (default: `llama-3.1-8b-instant`) | Optional |
        """
    )
