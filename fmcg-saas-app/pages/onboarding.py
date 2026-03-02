"""Onboarding and login flow."""

from __future__ import annotations

import uuid

import streamlit as st

from utils.database import db_service
from utils.session import navigate_to


INDUSTRIES = [
    "FMCG",
    "Healthcare",
    "Education",
    "Fintech",
    "Logistics",
    "Cyber Security",
]


def _set_authenticated_state(
    company_id: str,
    company_name: str,
    contact_name: str,
    email: str,
    phone: str,
    industry: str,
) -> None:
    st.session_state.company_id = company_id
    st.session_state.company_name = company_name
    st.session_state.contact_name = contact_name
    st.session_state.email = email
    st.session_state.phone = phone
    st.session_state.industry = industry
    st.session_state.authenticated = True
    st.session_state.services_configured = False
    st.session_state.data_uploaded = False
    navigate_to("services")


def show() -> None:
    st.markdown("## Company onboarding")
    st.caption("Step 1 of 3 - create account or login")

    if db_service.is_connected():
        st.success("✓ Database connected. Company records will be persisted.")
    else:
        st.info("💡 Database not configured. Running in session-only mode. Add DATABASE_URL to .env for persistence.")

    tab1, tab2 = st.tabs(["New Company", "Existing Company"])

    with tab1:
        _show_signup()
    with tab2:
        _show_login()


def _show_signup() -> None:
    st.markdown("### Create workspace")
    selected_industry = st.selectbox("Industry", INDUSTRIES, index=0)

    with st.form("onboarding_form"):
        col1, col2 = st.columns(2)
        with col1:
            company_name = st.text_input("Company name *", placeholder="ABC Foods Pvt Ltd")
            contact_name = st.text_input("Contact person *", placeholder="Operations lead")
            email = st.text_input("Work email *", placeholder="ops@company.com")
        with col2:
            phone = st.text_input("Phone", placeholder="+1-555-0100")
            num_products = st.number_input("Products in catalog", min_value=1, value=100)
            num_warehouses = st.number_input("Warehouses / regions", min_value=1, value=4)

        submitted = st.form_submit_button("Continue to Services", type="primary", use_container_width=True)

    if not submitted:
        return

    if not company_name or not contact_name or not email:
        st.error("Fill all required fields.")
        return

    company_id = f"COMP-{uuid.uuid4().hex[:10].upper()}"
    
    # Save to database if connected
    if db_service.is_connected():
        company_data = {
            "company_name": company_name,
            "industry": selected_industry,
            "contact_email": email,
            "contact_phone": phone,
            "services": []
        }
        if db_service.save_company(company_data):
            st.success("✓ Company saved to database")
        else:
            st.warning("Failed to save to database. Continuing in session mode.")

    st.session_state.org_profile = {
        "num_products": int(num_products),
        "num_warehouses": int(num_warehouses),
    }
    _set_authenticated_state(company_id, company_name, contact_name, email, phone, selected_industry)


def _show_login() -> None:
    st.markdown("### Login")
    company_name_input = st.text_input("Company name", key="login_company", placeholder="ABC Foods Pvt Ltd")
    email = st.text_input("Work email (optional)", key="login_email", placeholder="ops@company.com")

    if not st.button("Login", use_container_width=True):
        return

    if not company_name_input:
        st.error("Company name is required.")
        return

    # Try to load from database
    if db_service.is_connected():
        company_data = db_service.get_company(company_name_input)
        if company_data:
            _set_authenticated_state(
                company_id=f"COMP-{company_data['id']}",
                company_name=company_data["company_name"],
                contact_name="User",
                email=company_data.get("contact_email", email or "user@company.com"),
                phone=company_data.get("contact_phone", ""),
                industry=company_data.get("industry", "FMCG"),
            )
            st.success("✓ Loaded company from database")
            return

    # Fallback to session mode
    _set_authenticated_state(
        company_id=f"COMP-{uuid.uuid4().hex[:10].upper()}",
        company_name=company_name_input,
        contact_name="Session User",
        email=email or "session@local",
        phone="",
        industry="FMCG",
    )
    st.info("Logged in with session mode (company not found in database)")
