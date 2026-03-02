"""FMCG SaaS Platform - Streamlit application shell."""

from __future__ import annotations

import streamlit as st
from dotenv import load_dotenv

from pages import chatbot, dashboard, forecasting, inventory, landing, onboarding, services, settings, upload_data
from utils.database import db_service
from utils.session import enforce_flow_guard, get_onboarding_step, init_session_state, navigate_to, reset_user_session


st.set_page_config(
    page_title="FMCG Analytics Platform",
    page_icon="F",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={"About": "FMCG Analytics Platform"},
)

load_dotenv()


def apply_theme() -> None:
    """Inject app-level CSS tokens and component styles."""
    st.markdown(
        """
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&family=Space+Grotesk:wght@500;600;700&display=swap');

            :root {
                --ink-900: #0f172a;
                --ink-700: #334155;
                --ink-500: #64748b;
                --surface-0: #f8fafc;
                --surface-1: #eef2ff;
                --brand-600: #0f4c81;
                --brand-500: #1f6fb2;
                --brand-400: #4f9fdf;
                --accent-500: #f97316;
                --ok-600: #15803d;
                --warn-600: #b45309;
                --danger-600: #b91c1c;
                --border-200: #dbe1ea;
                --shadow-1: 0 10px 28px rgba(15, 23, 42, 0.08);
            }

            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            section[data-testid="stSidebarNav"] {display: none;}
            div[data-testid="stSidebarNav"] {display: none;}
            div[data-testid="stSidebarNavSeparator"] {display: none;}

            html, body, [class*="css"] {
                font-family: "Manrope", "Segoe UI", "Trebuchet MS", sans-serif;
            }

            h1, h2, h3, h4 {
                font-family: "Space Grotesk", "Manrope", sans-serif !important;
                letter-spacing: -0.02em;
                color: var(--ink-900) !important;
            }

            .stApp {
                background:
                    radial-gradient(circle at 10% -10%, #dbeafe 0%, transparent 38%),
                    radial-gradient(circle at 95% 0%, #ffe4cc 0%, transparent 32%),
                    linear-gradient(160deg, rgba(15, 76, 129, 0.05) 0%, rgba(79, 159, 223, 0.04) 45%, rgba(249, 115, 22, 0.06) 100%),
                    var(--surface-0);
                color: var(--ink-900);
            }

            .block-container {
                padding-top: 1.4rem;
                padding-bottom: 2rem;
            }

            .app-shell-title {
                background: linear-gradient(135deg, #0f4c81 0%, #1f6fb2 55%, #3b82f6 100%);
                border-radius: 14px;
                color: white;
                padding: 1rem;
                margin-bottom: 0.75rem;
                box-shadow: 0 12px 28px rgba(15, 76, 129, 0.25);
            }

            .panel-card {
                border: 1px solid var(--border-200);
                border-radius: 12px;
                background: white;
                padding: 1rem;
                box-shadow: var(--shadow-1);
            }

            .status-pill {
                display: inline-block;
                border-radius: 999px;
                padding: 0.25rem 0.7rem;
                font-size: 0.75rem;
                font-weight: 700;
                letter-spacing: 0.02em;
                color: white;
            }
            .status-ok { background: var(--ok-600); }
            .status-warn { background: var(--warn-600); }

            .stButton > button {
                border-radius: 10px;
                border: none;
                background: linear-gradient(135deg, var(--brand-600) 0%, var(--brand-400) 100%);
                color: white;
                font-weight: 600;
                transition: transform .1s ease, box-shadow .2s ease, background .2s ease;
            }
            .stButton > button:hover {
                box-shadow: 0 12px 22px rgba(15, 76, 129, 0.28);
                transform: translateY(-1px);
            }
            .stButton > button:disabled {
                opacity: 0.45;
                transform: none;
                box-shadow: none;
                border-color: #94a3b8;
            }

            .stAlert {
                border-radius: 12px;
                border: 1px solid var(--border-200);
            }

            .stMarkdown p, .stMarkdown li, .stMarkdown span, .stCaption {
                color: var(--ink-700);
            }
            label, .stSelectbox label, .stTextInput label, .stFileUploader label, .stNumberInput label {
                color: var(--ink-700) !important;
                font-weight: 600 !important;
            }
            [data-testid="stDataFrame"] * {
                color: var(--ink-900) !important;
            }

            [data-testid="stMetric"] {
                border: 1px solid var(--border-200);
                border-radius: 14px;
                padding: 0.75rem 0.9rem;
                background: linear-gradient(160deg, #ffffff 0%, #f8fbff 100%);
                box-shadow: var(--shadow-1);
            }
            [data-testid="stMetricLabel"] p {
                color: var(--ink-700) !important;
                font-weight: 700 !important;
                font-size: 0.92rem !important;
            }
            [data-testid="stMetricValue"] {
                color: var(--ink-900) !important;
                font-family: "Space Grotesk", "Manrope", sans-serif !important;
                font-weight: 700 !important;
                font-size: 2rem !important;
                line-height: 1.1;
            }
            [data-testid="stMetricDelta"] {
                color: var(--ink-500) !important;
            }

            .hero-banner {
                border-radius: 16px;
                padding: 1.1rem 1.2rem;
                color: white;
                background:
                    radial-gradient(circle at 90% 0%, rgba(255,255,255,0.28) 0%, rgba(255,255,255,0) 40%),
                    linear-gradient(130deg, #0f4c81 0%, #1f6fb2 56%, #3b82f6 100%);
                box-shadow: 0 18px 30px rgba(15, 76, 129, 0.26);
                margin-bottom: 0.8rem;
            }
            .hero-banner h2 {
                margin: 0;
                color: white !important;
            }
            .hero-banner p {
                margin: 0.35rem 0 0 0;
                opacity: 0.95;
            }

            .tile {
                border: 1px solid var(--border-200);
                border-radius: 14px;
                background: white;
                padding: 0.95rem 1rem;
                box-shadow: var(--shadow-1);
            }
            .tile .tile-label {
                color: var(--ink-700);
                font-weight: 700;
                font-size: 0.95rem;
                margin-bottom: 0.35rem;
            }
            .tile .tile-value {
                color: var(--ink-900);
                font-family: "Space Grotesk", "Manrope", sans-serif;
                font-size: 2rem;
                font-weight: 700;
                line-height: 1.05;
            }

            .streamlit-expanderHeader, .stTabs [data-baseweb="tab"] {
                font-weight: 600;
            }

            .chat-shell {
                border: 1px solid var(--border-200);
                border-radius: 14px;
                background: white;
                padding: 0.7rem;
            }
            .chat-user {
                background: #0b3b62;
                color: #ffffff;
                border-radius: 12px 12px 2px 12px;
                padding: 0.7rem 0.9rem;
            }
            .chat-assistant {
                background: #ecfeff;
                color: #0f172a;
                border: 1px solid #a5f3fc;
                border-radius: 12px 12px 12px 2px;
                padding: 0.7rem 0.9rem;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_sidebar() -> None:
    """Render authenticated side navigation."""
    with st.sidebar:
        st.markdown(
            f"""
            <div class="app-shell-title">
                <h3 style="margin:0;">FMCG Analytics</h3>
                <p style="margin:0.2rem 0 0 0; opacity:0.92;">{st.session_state.company_name or "Workspace"}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        step_num, step_label = get_onboarding_step()
        st.caption(f"Flow step: {step_num}/4 - {step_label}")

        nav_items = [
            ("dashboard", "Dashboard", False),
            ("services", "Services", False),
            ("upload", "Data Upload", False),
            ("forecasting", "Forecasting", not st.session_state.services.get("forecasting", False)),
            ("inventory", "Inventory", not st.session_state.services.get("inventory", False)),
            ("chatbot", "AI Assistant", not st.session_state.services.get("chatbot", False)),
            ("settings", "Settings", False),
        ]

        for key, label, force_disabled in nav_items:
            blocked_by_flow = (
                not st.session_state.data_uploaded
                and key in {"dashboard", "forecasting", "inventory", "chatbot"}
            )
            disabled = force_disabled or blocked_by_flow
            if st.button(label, key=f"nav_{key}", use_container_width=True, disabled=disabled):
                navigate_to(key)

        st.markdown("---")
        if st.session_state.data_uploaded:
            st.markdown('<span class="status-pill status-ok">DATA CONNECTED</span>', unsafe_allow_html=True)
        else:
            st.markdown('<span class="status-pill status-warn">DATA REQUIRED</span>', unsafe_allow_html=True)

        if st.session_state.db_ready:
            st.caption("Database: Connected")
        else:
            st.caption("Database: Not configured")

        st.markdown("---")
        if st.button("Logout", use_container_width=True):
            reset_user_session()
            st.rerun()


def render_public_page(page_key: str) -> None:
    if page_key == "landing":
        landing.show()
    else:
        onboarding.show()


def render_private_page(page_key: str) -> None:
    if page_key == "dashboard":
        dashboard.show()
    elif page_key == "services":
        services.show()
    elif page_key == "upload":
        upload_data.show()
    elif page_key == "forecasting":
        forecasting.show()
    elif page_key == "inventory":
        inventory.show()
    elif page_key == "chatbot":
        chatbot.show()
    elif page_key == "settings":
        settings.show()
    else:
        dashboard.show()


def main() -> None:
    apply_theme()
    init_session_state()

    page = enforce_flow_guard(st.session_state.current_page)
    st.session_state.current_page = page

    if not st.session_state.authenticated:
        render_public_page(page)
        return

    render_sidebar()
    render_private_page(page)


if __name__ == "__main__":
    main()
