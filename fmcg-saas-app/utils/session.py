"""Session state helpers and app-flow utilities."""

from __future__ import annotations

import copy
import streamlit as st


DEFAULT_SERVICES = {
    "forecasting": True,
    "inventory": True,
    "chatbot": True,
}


def init_session_state() -> None:
    """Initialize all expected session keys."""
    defaults = {
        "authenticated": False,
        "company_id": None,
        "company_name": None,
        "contact_name": None,
        "email": None,
        "phone": None,
        "industry": None,
        "services": copy.deepcopy(DEFAULT_SERVICES),
        "services_configured": False,
        "data_uploaded": False,
        "uploaded_files": {},
        "current_page": "landing",
        "chat_history": [],
        "db_ready": False,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def navigate_to(page: str) -> None:
    """Navigate to a page and rerun."""
    st.session_state.current_page = page
    st.rerun()


def reset_user_session() -> None:
    """Reset user-specific session state values for logout."""
    st.session_state.authenticated = False
    st.session_state.company_id = None
    st.session_state.company_name = None
    st.session_state.contact_name = None
    st.session_state.email = None
    st.session_state.phone = None
    st.session_state.industry = None
    st.session_state.services = copy.deepcopy(DEFAULT_SERVICES)
    st.session_state.services_configured = False
    st.session_state.data_uploaded = False
    st.session_state.uploaded_files = {}
    st.session_state.chat_history = []
    st.session_state.current_page = "landing"


def get_onboarding_step() -> tuple[int, str]:
    """Return current onboarding step to keep the flow coherent."""
    if not st.session_state.authenticated:
        return 1, "Account setup"
    if not st.session_state.services_configured:
        return 2, "Select services"
    if not st.session_state.data_uploaded:
        return 3, "Connect data"
    return 4, "Operational"


def enforce_flow_guard(page: str) -> str:
    """Redirect users to the next required step if they skip prerequisite screens."""
    public_pages = {"landing", "onboarding"}
    data_required_pages = {"dashboard", "forecasting", "inventory", "chatbot"}

    if not st.session_state.authenticated:
        if page not in public_pages:
            return "onboarding"
        return page

    if page in public_pages:
        return "dashboard" if st.session_state.data_uploaded else "services"

    if not st.session_state.services_configured and page not in {"services", "settings"}:
        return "services"

    if not st.session_state.data_uploaded and page in data_required_pages:
        return "upload"

    if page in {"forecasting", "inventory", "chatbot"} and not st.session_state.services.get(page, False):
        return "services"

    return page
