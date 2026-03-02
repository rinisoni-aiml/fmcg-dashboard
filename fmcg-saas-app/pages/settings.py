"""Settings page."""

from __future__ import annotations

import streamlit as st

from utils.database import db_service
from utils.session import navigate_to


def show() -> None:
    st.markdown("## Settings")
    tabs = st.tabs(["Profile", "Company", "Data Sources", "Integrations"])
    with tabs[0]:
        _show_profile()
    with tabs[1]:
        _show_company()
    with tabs[2]:
        _show_data_sources()
    with tabs[3]:
        _show_integrations()


def _show_profile() -> None:
    st.markdown("### User profile")
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
        save = st.form_submit_button("Save profile", type="primary", use_container_width=True)

    if save:
        st.session_state.contact_name = name
        st.session_state.email = email
        st.session_state.phone = phone
        st.session_state.industry = industry
        st.success("Profile updated in session.")


def _show_company() -> None:
    st.markdown("### Company")
    company_name = st.text_input("Company name", value=st.session_state.company_name or "")
    st.text_input("Company ID", value=st.session_state.company_id or "", disabled=True)
    st.markdown("### Enabled modules")

    for module_key in ["forecasting", "inventory", "chatbot"]:
        st.session_state.services[module_key] = st.checkbox(
            module_key.capitalize(),
            value=bool(st.session_state.services.get(module_key, True)),
            key=f"settings_module_{module_key}",
        )

    if st.button("Save company settings", type="primary"):
        st.session_state.company_name = company_name
        if st.session_state.db_ready and st.session_state.email:
            record = db_service.upsert_company(
                company_name=company_name,
                contact_name=st.session_state.contact_name or "User",
                email=st.session_state.email,
                phone=st.session_state.phone,
                industry=st.session_state.industry or "FMCG",
            )
            if record:
                st.session_state.company_id = record.company_uid
                st.success("Saved to PostgreSQL.")
            else:
                st.warning("Could not persist to PostgreSQL. Session values were updated only.")
        else:
            st.success("Saved in current session.")


def _show_data_sources() -> None:
    st.markdown("### Connected files")
    if not st.session_state.uploaded_files:
        st.info("No files processed yet.")
    else:
        for name, meta in st.session_state.uploaded_files.items():
            rows = len(meta.get("normalized_data", []))
            ts = meta.get("timestamp", "")[:19].replace("T", " ")
            st.markdown(
                f"""
                <div class="panel-card" style="margin-bottom:0.5rem;">
                    <strong>{name}</strong><br>
                    <span style="color:#475569;">Rows: {rows:,} | Processed: {ts} UTC</span>
                </div>
                """,
                unsafe_allow_html=True,
            )
    if st.button("Add source", use_container_width=True):
        navigate_to("upload")


def _show_integrations() -> None:
    st.markdown("### Integration readiness")
    st.markdown(
        """
        - `DATABASE_URL`: PostgreSQL connection string used for company/user persistence.
        - `GROQ_API_KEY`: API key for Groq-hosted open models.
        - `GROQ_MODEL`: Optional override. Default is `llama-3.1-8b-instant`.
        """
    )
    if st.session_state.db_ready:
        st.success("Database: connected")
    else:
        st.warning("Database: not connected (configure `DATABASE_URL`).")
