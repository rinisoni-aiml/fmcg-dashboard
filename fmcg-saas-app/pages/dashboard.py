"""Main dashboard — premium analytics overview."""

from __future__ import annotations

from datetime import datetime

import plotly.graph_objects as go
import streamlit as st

from utils.analytics import collect_normalized_data, dashboard_payload
from utils.session import navigate_to


PLOTLY_LAYOUT_DEFAULTS = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter, sans-serif", color="#334155"),
    margin=dict(l=0, r=0, t=20, b=0),
    hovermode="x unified",
    hoverlabel=dict(bgcolor="white", font_size=12, font_family="Inter"),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font_size=11),
    xaxis=dict(gridcolor="rgba(226,232,240,0.6)", zerolinecolor="rgba(226,232,240,0.8)"),
    yaxis=dict(gridcolor="rgba(226,232,240,0.6)", zerolinecolor="rgba(226,232,240,0.8)"),
)


def show() -> None:
    st.markdown(
        f"""
        <div class="hero-banner">
            <h2>📈  Welcome back, {st.session_state.company_name}</h2>
            <p>Live operations overview · demand · inventory risk · revenue performance</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.caption(f"Last refreshed: {datetime.now().strftime('%B %d, %Y at %H:%M')}")

    if not st.session_state.data_uploaded:
        st.warning("No processed data available yet. Complete data upload to unlock analytics.")
        if st.button("📁  Go to Data Upload", type="primary"):
            navigate_to("upload")
        return

    df = collect_normalized_data(st.session_state.uploaded_files)
    if df.empty:
        st.error("Data was uploaded but no valid rows are available after normalization.")
        if st.button("🔄  Review upload mapping"):
            navigate_to("upload")
        return

    with st.spinner("Building dashboard..."):
        payload = dashboard_payload(df)

    _render_kpis(payload["kpis"])
    _render_alerts(payload["alerts"])
    _render_insights(payload["insights"])
    _render_charts(payload, df)


def _render_kpis(kpis: dict[str, float]) -> None:
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        _kpi_tile("Total Revenue", f"${kpis['total_revenue']:,.0f}", "#0f4c81")
    with c2:
        _kpi_tile("Active Products", f"{kpis['active_products']:,}", "#15803d")
    with c3:
        _kpi_tile("Stockout Alerts", f"{kpis['stockout_alerts']:,}", "#dc2626")
    with c4:
        _kpi_tile("Forecast Accuracy", f"{kpis['forecast_accuracy']:.1f}%", "#d97706")


def _render_alerts(alerts: list[dict]) -> None:
    if not alerts:
        return

    st.markdown("### 🚨  Alerts")
    for alert in alerts:
        severity = alert.get("severity", "info")
        title = alert.get("title", "Alert")
        message = alert.get("message", "")
        if severity == "critical":
            st.error(f"**{title}:** {message}")
        elif severity == "warning":
            st.warning(f"**{title}:** {message}")
        else:
            st.success(f"**{title}:** {message}")


def _render_insights(insights: list[str]) -> None:
    if not insights:
        return

    st.markdown("### 💡  AI-Generated Insights")
    cols = st.columns(min(len(insights), 3))
    for i, insight in enumerate(insights):
        with cols[i % len(cols)]:
            st.markdown(
                f"""
                <div class="panel-card" style="border-left:4px solid #0f4c81;min-height:80px;">
                    <p style="margin:0;font-size:0.88rem;">{insight}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )


def _render_charts(payload: dict[str, object], df) -> None:
    st.markdown("### 📊  Analytics")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Demand Forecast — Next 30 Days")
        hist = payload["forecast_history"]
        pred = payload["forecast_30"]
        fig = go.Figure()
        if not hist.empty:
            fig.add_trace(
                go.Scatter(
                    x=hist["date"], y=hist["demand"],
                    mode="lines", name="Historical",
                    line=dict(color="#0f4c81", width=2.5),
                    fill="tozeroy", fillcolor="rgba(15,76,129,0.06)",
                )
            )
        if not pred.empty:
            fig.add_trace(
                go.Scatter(
                    x=pred["date"], y=pred["predicted_demand"],
                    mode="lines", name="Forecast",
                    line=dict(color="#f97316", width=2.5, dash="dash"),
                )
            )
            fig.add_trace(
                go.Scatter(
                    x=pred["date"].tolist() + pred["date"].tolist()[::-1],
                    y=pred["upper_bound"].tolist() + pred["lower_bound"].tolist()[::-1],
                    fill="toself", fillcolor="rgba(249,115,22,0.10)",
                    line=dict(color="rgba(255,255,255,0)"),
                    name="Confidence Band",
                )
            )
        fig.update_layout(height=380, **PLOTLY_LAYOUT_DEFAULTS)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("#### Demand by Region")
        region_frame = payload["region_frame"]
        palette = ["#0f4c81", "#1a6bb5", "#3b8ad9", "#7cb8ec", "#bcdcf7", "#f97316", "#fb923c"]
        bar = go.Figure(
            data=[
                go.Bar(
                    x=region_frame["region"],
                    y=region_frame["total_quantity"],
                    marker=dict(color=palette[:len(region_frame)], cornerradius=4),
                )
            ]
        )
        bar.update_layout(
            height=380, **PLOTLY_LAYOUT_DEFAULTS,
            xaxis_title="Region", yaxis_title="Quantity",
        )
        st.plotly_chart(bar, use_container_width=True)

    # Second row: Revenue over time & Top products
    col3, col4 = st.columns(2)

    with col3:
        st.markdown("#### Revenue Over Time")
        monthly_rev = (
            df.groupby(df["order_date"].dt.to_period("M"))["total_amount"]
            .sum()
            .reset_index()
        )
        monthly_rev["order_date"] = monthly_rev["order_date"].dt.to_timestamp()
        fig_rev = go.Figure(
            go.Scatter(
                x=monthly_rev["order_date"], y=monthly_rev["total_amount"],
                mode="lines+markers", name="Revenue",
                line=dict(color="#15803d", width=2.5),
                marker=dict(size=6, color="#15803d"),
                fill="tozeroy", fillcolor="rgba(21,128,61,0.06)",
            )
        )
        fig_rev.update_layout(
            height=340, **PLOTLY_LAYOUT_DEFAULTS,
            yaxis_title="Revenue ($)",
        )
        st.plotly_chart(fig_rev, use_container_width=True)

    with col4:
        st.markdown("#### Top 10 Products by Revenue")
        top_products = (
            df.groupby("product_id", as_index=False)["total_amount"]
            .sum()
            .sort_values("total_amount", ascending=True)
            .tail(10)
        )
        fig_prod = go.Figure(
            go.Bar(
                y=top_products["product_id"],
                x=top_products["total_amount"],
                orientation="h",
                marker=dict(
                    color=top_products["total_amount"],
                    colorscale=[[0, "#bcdcf7"], [0.5, "#3b8ad9"], [1, "#0f4c81"]],
                    cornerradius=4,
                ),
            )
        )
        fig_prod.update_layout(
            height=340, **PLOTLY_LAYOUT_DEFAULTS,
            xaxis_title="Revenue ($)",
        )
        st.plotly_chart(fig_prod, use_container_width=True)


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
