"""FMCG SaaS Platform - Streamlit application shell."""

from __future__ import annotations

import streamlit as st
from dotenv import load_dotenv

from pages import chatbot, dashboard, forecasting, inventory, landing, onboarding, services, settings, upload_data
from utils.database import db_service
from utils.session import enforce_flow_guard, get_onboarding_step, init_session_state, navigate_to, reset_user_session


st.set_page_config(
    page_title="FMCG Analytics Platform",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={"About": "FMCG Analytics Platform — AI-Powered Operations Intelligence"},
)

load_dotenv()


def apply_theme() -> None:
    """Inject premium app-level CSS tokens and component styles."""
    st.markdown(
        """
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Space+Grotesk:wght@400;500;600;700&display=swap');

            :root {
                --ink-900: #0f172a;
                --ink-800: #1e293b;
                --ink-700: #334155;
                --ink-600: #475569;
                --ink-500: #64748b;
                --ink-400: #94a3b8;
                --ink-300: #cbd5e1;
                --surface-0: #f8fafc;
                --surface-1: #f1f5f9;
                --surface-2: #e2e8f0;
                --brand-700: #0c3d66;
                --brand-600: #0f4c81;
                --brand-500: #1a6bb5;
                --brand-400: #3b8ad9;
                --brand-300: #7cb8ec;
                --brand-200: #bcdcf7;
                --brand-100: #e8f2fc;
                --accent-600: #ea580c;
                --accent-500: #f97316;
                --accent-400: #fb923c;
                --accent-300: #fdba74;
                --ok-700: #15803d;
                --ok-600: #16a34a;
                --ok-500: #22c55e;
                --ok-100: #dcfce7;
                --warn-600: #d97706;
                --warn-500: #eab308;
                --warn-100: #fef9c3;
                --danger-600: #dc2626;
                --danger-500: #ef4444;
                --danger-100: #fee2e2;
                --border-100: #e2e8f0;
                --border-200: #cbd5e1;
                --radius-sm: 8px;
                --radius-md: 12px;
                --radius-lg: 16px;
                --radius-xl: 20px;
                --shadow-sm: 0 1px 3px rgba(15,23,42,0.06), 0 1px 2px rgba(15,23,42,0.04);
                --shadow-md: 0 4px 12px rgba(15,23,42,0.08), 0 2px 4px rgba(15,23,42,0.04);
                --shadow-lg: 0 12px 32px rgba(15,23,42,0.10), 0 4px 8px rgba(15,23,42,0.06);
                --shadow-xl: 0 20px 48px rgba(15,23,42,0.14), 0 8px 16px rgba(15,23,42,0.08);
            }

            /* --- HIDE STREAMLIT DEFAULTS --- */
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            section[data-testid="stSidebarNav"] {display: none;}
            div[data-testid="stSidebarNav"] {display: none;}
            div[data-testid="stSidebarNavSeparator"] {display: none;}
            header[data-testid="stHeader"] {background: transparent;}

            /* --- TYPOGRAPHY --- */
            html, body, [class*="css"] {
                font-family: "Inter", -apple-system, "Segoe UI", sans-serif;
                -webkit-font-smoothing: antialiased;
            }
            h1, h2, h3, h4 {
                font-family: "Space Grotesk", "Inter", sans-serif !important;
                letter-spacing: -0.025em;
                color: var(--ink-900) !important;
                font-weight: 700 !important;
            }
            h1 { font-size: 2rem !important; }
            h2 { font-size: 1.55rem !important; }
            h3 { font-size: 1.2rem !important; }

            /* --- APP BACKGROUND --- */
            .stApp {
                background:
                    radial-gradient(ellipse at 0% -15%, rgba(15,76,129,0.07) 0%, transparent 50%),
                    radial-gradient(ellipse at 100% 0%, rgba(249,115,22,0.05) 0%, transparent 40%),
                    var(--surface-0);
                color: var(--ink-900);
            }
            .block-container {
                padding-top: 1.2rem;
                padding-bottom: 2rem;
                max-width: 1200px;
            }

            /* --- SIDEBAR --- */
            section[data-testid="stSidebar"] {
                background: linear-gradient(180deg, #0b1e36 0%, #0f2e4e 40%, #143d65 100%) !important;
                border-right: 1px solid rgba(255,255,255,0.06);
            }
            section[data-testid="stSidebar"] * {
                color: rgba(255,255,255,0.88) !important;
            }
            section[data-testid="stSidebar"] .stButton > button {
                background: rgba(255,255,255,0.06) !important;
                border: 1px solid rgba(255,255,255,0.10) !important;
                color: white !important;
                border-radius: var(--radius-sm) !important;
                font-weight: 500 !important;
                transition: all 0.2s ease !important;
                text-align: left !important;
                padding: 0.55rem 0.9rem !important;
            }
            section[data-testid="stSidebar"] .stButton > button:hover {
                background: rgba(255,255,255,0.14) !important;
                border-color: rgba(255,255,255,0.20) !important;
                transform: translateX(2px);
            }
            section[data-testid="stSidebar"] .stButton > button:disabled {
                opacity: 0.35 !important;
                transform: none !important;
            }
            section[data-testid="stSidebar"] .stCaption p,
            section[data-testid="stSidebar"] .stCaption {
                color: rgba(255,255,255,0.50) !important;
            }
            section[data-testid="stSidebar"] hr {
                border-color: rgba(255,255,255,0.10) !important;
            }

            /* --- HERO BANNER --- */
            .hero-banner {
                border-radius: var(--radius-xl);
                padding: 1.5rem 1.6rem;
                color: white;
                background: linear-gradient(135deg, #0b1e36 0%, #0f4c81 45%, #1a6bb5 85%, #3b8ad9 100%);
                box-shadow: var(--shadow-xl), 0 0 0 1px rgba(15,76,129,0.15);
                margin-bottom: 1.2rem;
                position: relative;
                overflow: hidden;
            }
            .hero-banner::before {
                content: '';
                position: absolute;
                top: -50%;
                right: -20%;
                width: 300px;
                height: 300px;
                background: radial-gradient(circle, rgba(255,255,255,0.10) 0%, transparent 70%);
                border-radius: 50%;
            }
            .hero-banner::after {
                content: '';
                position: absolute;
                bottom: -40%;
                left: 10%;
                width: 200px;
                height: 200px;
                background: radial-gradient(circle, rgba(249,115,22,0.12) 0%, transparent 70%);
                border-radius: 50%;
            }
            .hero-banner h2 {
                margin: 0;
                color: white !important;
                font-size: 1.6rem !important;
                position: relative;
                z-index: 1;
            }
            .hero-banner p {
                margin: 0.4rem 0 0 0;
                opacity: 0.88;
                position: relative;
                z-index: 1;
                font-size: 0.95rem;
                color: rgba(255,255,255,0.88) !important;
            }

            /* --- PREMIUM CARDS --- */
            .panel-card {
                border: 1px solid var(--border-100);
                border-radius: var(--radius-md);
                background: white;
                padding: 1rem 1.1rem;
                box-shadow: var(--shadow-sm);
                transition: all 0.2s ease;
            }
            .panel-card:hover {
                box-shadow: var(--shadow-md);
                transform: translateY(-1px);
                border-color: var(--border-200);
            }

            /* --- KPI / METRIC TILES --- */
            .tile {
                border: 1px solid var(--border-100);
                border-radius: var(--radius-lg);
                background: white;
                padding: 1rem 1.1rem;
                box-shadow: var(--shadow-sm);
                transition: all 0.25s ease;
                position: relative;
                overflow: hidden;
            }
            .tile:hover {
                box-shadow: var(--shadow-lg);
                transform: translateY(-2px);
            }
            .tile .tile-label {
                color: var(--ink-600);
                font-weight: 600;
                font-size: 0.82rem;
                text-transform: uppercase;
                letter-spacing: 0.04em;
                margin-bottom: 0.45rem;
            }
            .tile .tile-value {
                color: var(--ink-900);
                font-family: "Space Grotesk", "Inter", sans-serif;
                font-size: 1.85rem;
                font-weight: 700;
                line-height: 1.1;
            }
            .tile .tile-delta {
                font-size: 0.78rem;
                font-weight: 600;
                margin-top: 0.3rem;
            }
            .tile .tile-delta.positive { color: var(--ok-600); }
            .tile .tile-delta.negative { color: var(--danger-600); }

            /* --- NATIVE METRIC STYLING --- */
            [data-testid="stMetric"] {
                border: 1px solid var(--border-100);
                border-radius: var(--radius-lg);
                padding: 0.85rem 1rem;
                background: white;
                box-shadow: var(--shadow-sm);
                transition: all 0.25s ease;
            }
            [data-testid="stMetric"]:hover {
                box-shadow: var(--shadow-md);
                transform: translateY(-1px);
            }
            [data-testid="stMetricLabel"] p {
                color: var(--ink-600) !important;
                font-weight: 700 !important;
                font-size: 0.82rem !important;
                text-transform: uppercase;
                letter-spacing: 0.04em;
            }
            [data-testid="stMetricValue"] {
                color: var(--ink-900) !important;
                font-family: "Space Grotesk", "Inter", sans-serif !important;
                font-weight: 700 !important;
                font-size: 1.8rem !important;
                line-height: 1.1;
            }
            [data-testid="stMetricDelta"] {
                font-weight: 600 !important;
            }

            /* --- BUTTONS --- */
            .stButton > button {
                border-radius: var(--radius-sm) !important;
                border: none !important;
                background: linear-gradient(135deg, var(--brand-600) 0%, var(--brand-400) 100%) !important;
                color: white !important;
                font-weight: 600 !important;
                font-size: 0.88rem !important;
                padding: 0.55rem 1.2rem !important;
                transition: all 0.2s ease !important;
                box-shadow: 0 2px 8px rgba(15,76,129,0.20) !important;
            }
            .stButton > button:hover {
                box-shadow: 0 6px 20px rgba(15,76,129,0.30) !important;
                transform: translateY(-1px) !important;
                filter: brightness(1.05) !important;
            }
            .stButton > button:active {
                transform: translateY(0) !important;
            }
            .stButton > button:disabled {
                opacity: 0.40 !important;
                transform: none !important;
                box-shadow: none !important;
            }

            /* --- TABS --- */
            .stTabs [data-baseweb="tab-list"] {
                gap: 0.25rem;
                background: var(--surface-1);
                border-radius: var(--radius-md);
                padding: 4px;
            }
            .stTabs [data-baseweb="tab"] {
                border-radius: var(--radius-sm);
                font-weight: 600;
                font-size: 0.88rem;
                padding: 0.5rem 1rem;
            }
            .stTabs [aria-selected="true"] {
                background: white !important;
                box-shadow: var(--shadow-sm);
            }

            /* --- ALERTS --- */
            .stAlert {
                border-radius: var(--radius-md);
                border: 1px solid var(--border-100);
            }

            /* --- DATA FRAMES --- */
            [data-testid="stDataFrame"] {
                border-radius: var(--radius-md);
                overflow: hidden;
            }

            /* --- TEXT STYLING --- */
            .stMarkdown p, .stMarkdown li, .stMarkdown span, .stCaption p {
                color: var(--ink-700);
                line-height: 1.6;
            }
            label, .stSelectbox label, .stTextInput label, .stFileUploader label, .stNumberInput label {
                color: var(--ink-700) !important;
                font-weight: 600 !important;
                font-size: 0.88rem !important;
            }

            /* --- EXPANDER / ACCORDION --- */
            .streamlit-expanderHeader {
                font-weight: 600;
                font-size: 0.92rem;
            }

            /* --- STATUS PILLS --- */
            .status-pill {
                display: inline-flex;
                align-items: center;
                gap: 0.35rem;
                border-radius: 999px;
                padding: 0.3rem 0.85rem;
                font-size: 0.73rem;
                font-weight: 700;
                letter-spacing: 0.03em;
                text-transform: uppercase;
            }
            .status-ok {
                background: linear-gradient(135deg, #15803d, #22c55e);
                color: white;
            }
            .status-warn {
                background: linear-gradient(135deg, #d97706, #f59e0b);
                color: white;
            }

            /* --- CHAT ELEMENTS --- */
            .chat-shell {
                border: 1px solid var(--border-100);
                border-radius: var(--radius-lg);
                background: var(--surface-0);
                padding: 0.6rem;
                max-height: 450px;
                overflow-y: auto;
            }
            [data-testid="stChatMessage"] {
                border-radius: var(--radius-md) !important;
                border: 1px solid var(--border-100) !important;
                margin-bottom: 0.4rem !important;
            }

            /* --- SIDEBAR BRAND --- */
            .sidebar-brand {
                background: linear-gradient(135deg, rgba(255,255,255,0.08) 0%, rgba(255,255,255,0.03) 100%);
                border: 1px solid rgba(255,255,255,0.10);
                border-radius: var(--radius-md);
                padding: 1rem;
                margin-bottom: 0.75rem;
                backdrop-filter: blur(8px);
            }
            .sidebar-brand h3 {
                margin: 0;
                color: white !important;
                font-size: 1.15rem !important;
                font-weight: 700 !important;
            }
            .sidebar-brand p {
                margin: 0.25rem 0 0 0;
                opacity: 0.70;
                font-size: 0.82rem;
                color: rgba(255,255,255,0.70) !important;
            }

            /* --- NAV PILL ACTIVE --- */
            .nav-active > button {
                background: rgba(59,138,217,0.20) !important;
                border-color: rgba(59,138,217,0.35) !important;
                color: #7cb8ec !important;
            }

            /* --- FORM INPUTS --- */
            .stTextInput input, .stSelectbox select, .stNumberInput input {
                border-radius: var(--radius-sm) !important;
                border: 1px solid var(--border-200) !important;
                font-size: 0.9rem !important;
            }

            /* --- SCROLLBAR --- */
            ::-webkit-scrollbar { width: 6px; }
            ::-webkit-scrollbar-track { background: transparent; }
            ::-webkit-scrollbar-thumb {
                background: var(--ink-300);
                border-radius: 3px;
            }
            ::-webkit-scrollbar-thumb:hover { background: var(--ink-400); }

            /* --- ANIMATION KEYFRAMES --- */
            @keyframes fadeInUp {
                from { opacity: 0; transform: translateY(12px); }
                to { opacity: 1; transform: translateY(0); }
            }
            .animate-in {
                animation: fadeInUp 0.4s ease-out;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_sidebar() -> None:
    """Render premium side navigation."""
    with st.sidebar:
        st.markdown(
            f"""
            <div class="sidebar-brand">
                <h3>📊 FMCG Analytics</h3>
                <p>{st.session_state.company_name or "Workspace"}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        step_num, step_label = get_onboarding_step()
        st.caption(f"Step {step_num}/4 · {step_label}")

        nav_items = [
            ("dashboard", "📈  Dashboard", False),
            ("services", "⚙️  Services", False),
            ("upload", "📁  Data Upload", False),
            ("forecasting", "🔮  Forecasting", not st.session_state.services.get("forecasting", False)),
            ("inventory", "📦  Inventory", not st.session_state.services.get("inventory", False)),
            ("chatbot", "🤖  AI Assistant", not st.session_state.services.get("chatbot", False)),
            ("settings", "🛠  Settings", False),
        ]

        current_page = st.session_state.current_page
        for key, label, force_disabled in nav_items:
            blocked_by_flow = (
                not st.session_state.data_uploaded
                and key in {"dashboard", "forecasting", "inventory", "chatbot"}
            )
            disabled = force_disabled or blocked_by_flow
            is_active = current_page == key

            # Wrap active nav item for highlighting
            if is_active:
                st.markdown('<div class="nav-active">', unsafe_allow_html=True)
            if st.button(label, key=f"nav_{key}", use_container_width=True, disabled=disabled):
                navigate_to(key)
            if is_active:
                st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("---")
        if st.session_state.data_uploaded:
            st.markdown('<span class="status-pill status-ok">● DATA CONNECTED</span>', unsafe_allow_html=True)
        else:
            st.markdown('<span class="status-pill status-warn">● DATA REQUIRED</span>', unsafe_allow_html=True)

        if db_service.is_connected():
            st.caption("🟢 Database: Connected")
            st.session_state.db_ready = True
        else:
            st.caption("🔴 Database: Not configured")
            st.session_state.db_ready = False

        st.markdown("---")
        if st.button("🚪  Logout", use_container_width=True):
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
