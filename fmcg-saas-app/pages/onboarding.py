"""Onboarding and login flow with premium UI and DB persistence."""

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

    # Record login event in database
    db_service.save_login_event(company_name, email, login_type="signup")

    navigate_to("services")


def show() -> None:
    st.markdown(
        """
        <div class="hero-banner" style="text-align:center;">
            <h2>🏢  Company Onboarding</h2>
            <p>Create your workspace or login to an existing one</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Progress indicator
    st.markdown(
        """
        <div style="display:flex;justify-content:center;gap:1.5rem;margin-bottom:1.5rem;">
            <div style="display:flex;align-items:center;gap:0.4rem;">
                <div style="width:30px;height:30px;border-radius:50%;background:linear-gradient(135deg,#0f4c81,#3b8ad9);color:white;display:flex;align-items:center;justify-content:center;font-size:0.75rem;font-weight:700;">1</div>
                <span style="font-weight:600;color:#0f4c81;">Account</span>
            </div>
            <div style="width:40px;height:2px;background:#cbd5e1;margin-top:14px;"></div>
            <div style="display:flex;align-items:center;gap:0.4rem;">
                <div style="width:30px;height:30px;border-radius:50%;background:#e2e8f0;color:#64748b;display:flex;align-items:center;justify-content:center;font-size:0.75rem;font-weight:700;">2</div>
                <span style="color:#94a3b8;font-weight:500;">Services</span>
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

    if db_service.is_connected():
        st.success("✅  Database connected — company records will be persisted to Supabase.")
    else:
        st.info("💡  Database not configured. Running in session-only mode. Add `DATABASE_URL` to `.env` for persistence.")

    tab1, tab2 = st.tabs(["🆕  New Company", "🔑  Existing Company"])

    with tab1:
        _show_signup()
    with tab2:
        _show_login()


def _show_signup() -> None:
    st.markdown("#### Create your workspace")
    selected_industry = st.selectbox("Industry vertical", INDUSTRIES, index=0)

    with st.form("onboarding_form"):
        col1, col2 = st.columns(2)
        with col1:
            company_name = st.text_input("Company name *", placeholder="ABC Foods Pvt Ltd")
            contact_name = st.text_input("Contact person *", placeholder="John Doe")
            email = st.text_input("Work email *", placeholder="ops@company.com")
        with col2:
            phone = st.text_input("Phone", placeholder="+1-555-0100")
            num_products = st.number_input("Products in catalog", min_value=1, value=100)
            num_warehouses = st.number_input("Warehouses / regions", min_value=1, value=4)

        submitted = st.form_submit_button("Continue to Services  →", type="primary", use_container_width=True)

    if not submitted:
        return

    if not company_name or not contact_name or not email:
        st.error("⚠️  Please fill all required fields.")
        return

    company_id = f"COMP-{uuid.uuid4().hex[:10].upper()}"

    # Save to database if connected
    if db_service.is_connected():
        company_data = {
            "company_name": company_name,
            "industry": selected_industry,
            "contact_email": email,
            "contact_phone": phone,
            "contact_name": contact_name,
            "services": [],
        }
        if db_service.save_company(company_data):
            st.success("✅  Company saved to Supabase")
        else:
            st.warning("⚠️  Could not save to database. Continuing in session mode.")

    st.session_state.org_profile = {
        "num_products": int(num_products),
        "num_warehouses": int(num_warehouses),
    }
    _set_authenticated_state(company_id, company_name, contact_name, email, phone, selected_industry)


def _show_login() -> None:
    st.markdown("#### Login to existing workspace")
    company_name_input = st.text_input("Company name", key="login_company", placeholder="ABC Foods Pvt Ltd")
    email = st.text_input("Work email (optional)", key="login_email", placeholder="ops@company.com")

    if not st.button("Login  →", use_container_width=True):
        return

    if not company_name_input:
        st.error("⚠️  Company name is required.")
        return

    # Try to load from database
    if db_service.is_connected():
        company_data = db_service.get_company(company_name_input)
        if company_data:
            db_service.save_login_event(company_name_input, email or company_data.get("contact_email", ""), "login")
            _set_authenticated_state(
                company_id=f"COMP-{company_data['id']}",
                company_name=company_data["company_name"],
                contact_name=company_data.get("contact_name", "User"),
                email=company_data.get("contact_email", email or "user@company.com"),
                phone=company_data.get("contact_phone", ""),
                industry=company_data.get("industry", "FMCG"),
            )
            st.success("✅  Loaded company from database")
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
    st.info("🔄  Logged in with session mode (company not found in database)")
