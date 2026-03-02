"""Main dashboard."""

from __future__ import annotations

from datetime import datetime

import plotly.graph_objects as go
import streamlit as st

from utils.analytics import collect_normalized_data, dashboard_payload
from utils.session import navigate_to


def show() -> None:
    st.markdown(
        f"""
        <div class="hero-banner">
            <h2>Welcome back, {st.session_state.company_name}</h2>
            <p>Live operations overview for demand, inventory risk, and revenue performance.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.caption(f"Updated at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    if not st.session_state.data_uploaded:
        st.warning("No processed data available yet. Complete data upload to unlock analytics.")
        if st.button("Go to data upload", type="primary"):
            navigate_to("upload")
        return

    df = collect_normalized_data(st.session_state.uploaded_files)
    if df.empty:
        st.error("Data was uploaded but no valid rows are available after normalization.")
        if st.button("Review upload mapping"):
            navigate_to("upload")
        return

    payload = dashboard_payload(df)
    _render_alerts(payload["alerts"])
    _render_insights(payload["insights"])
    _render_kpis(payload["kpis"])
    _render_charts(payload)


def _render_alerts(alerts: list[dict]) -> None:
    st.markdown("### Critical alerts")
    for alert in alerts:
        severity = alert.get("severity", "info")
        title = alert.get("title", "Alert")
        message = alert.get("message", "")
        if severity == "critical":
            st.error(f"{title}: {message}")
        elif severity == "warning":
            st.warning(f"{title}: {message}")
        else:
            st.success(f"{title}: {message}")


def _render_insights(insights: list[str]) -> None:
    st.markdown("### AI-generated operational insights")
    if not insights:
        st.info("No insights available yet.")
        return
    for insight in insights:
        st.info(insight)


def _render_kpis(kpis: dict[str, float]) -> None:
    st.markdown("### Key metrics")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        _kpi_tile("Total revenue", f"${kpis['total_revenue']:,.0f}", "#0f4c81")
    with c2:
        _kpi_tile("Active products", f"{kpis['active_products']:,}", "#0f766e")
    with c3:
        _kpi_tile("Stockout alerts", f"{kpis['stockout_alerts']:,}", "#b91c1c")
    with c4:
        _kpi_tile("Forecast accuracy", f"{kpis['forecast_accuracy']:.1f}%", "#b45309")


def _render_charts(payload: dict[str, object]) -> None:
    st.markdown("### Analytics")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Demand forecast - next 30 days")
        hist = payload["forecast_history"]
        pred = payload["forecast_30"]
        fig = go.Figure()
        if not hist.empty:
            fig.add_trace(
                go.Scatter(
                    x=hist["date"],
                    y=hist["demand"],
                    mode="lines",
                    name="Historical",
                    line=dict(color="#0f4c81", width=2.4),
                )
            )
        if not pred.empty:
            fig.add_trace(
                go.Scatter(
                    x=pred["date"],
                    y=pred["predicted_demand"],
                    mode="lines",
                    name="Forecast",
                    line=dict(color="#f97316", width=2.4, dash="dash"),
                )
            )
            fig.add_trace(
                go.Scatter(
                    x=pred["date"].tolist() + pred["date"].tolist()[::-1],
                    y=pred["upper_bound"].tolist() + pred["lower_bound"].tolist()[::-1],
                    fill="toself",
                    fillcolor="rgba(15,76,129,0.12)",
                    line=dict(color="rgba(255,255,255,0)"),
                    name="Confidence",
                )
            )
        fig.update_layout(height=350, margin=dict(l=0, r=0, t=5, b=0), hovermode="x unified")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("#### Demand by region")
        region_frame = payload["region_frame"]
        bar = go.Figure(
            data=[
                go.Bar(
                    x=region_frame["region"],
                    y=region_frame["total_quantity"],
                    marker_color=["#1f6fb2", "#3b82f6", "#f97316", "#0ea5e9", "#0f766e"][: len(region_frame)],
                )
            ]
        )
        bar.update_layout(
            height=350,
            margin=dict(l=0, r=0, t=5, b=0),
            xaxis_title="Region",
            yaxis_title="Quantity",
        )
        st.plotly_chart(bar, use_container_width=True)


def _kpi_tile(label: str, value: str, accent: str) -> None:
    st.markdown(
        f"""
        <div class="tile" style="border-top:4px solid {accent};">
            <div class="tile-label">{label}</div>
            <div class="tile-value">{value}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
