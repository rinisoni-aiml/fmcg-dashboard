"""Demand forecasting page."""

from __future__ import annotations

import plotly.graph_objects as go
import streamlit as st

from utils.analytics import collect_normalized_data, generate_forecast
from utils.session import navigate_to


def show() -> None:
    st.markdown(
        """
        <div class="hero-banner">
            <h2>Demand Forecasting</h2>
            <p>Project near-term demand and act early on trend shifts with confidence intervals.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if not st.session_state.data_uploaded:
        st.warning("Upload and process data first.")
        if st.button("Go to upload", type="primary"):
            navigate_to("upload")
        return

    df = collect_normalized_data(st.session_state.uploaded_files)
    if df.empty:
        st.error("No valid data available after mapping.")
        return

    product_options = ["All Products"] + sorted(df["product_id"].astype(str).unique().tolist())
    region_options = ["All Regions"] + sorted(df["region"].astype(str).unique().tolist())

    st.markdown("### Filters")
    c1, c2, c3, c4 = st.columns([1.5, 1.3, 1.2, 1])
    with c1:
        product = st.selectbox("Product", product_options)
    with c2:
        region = st.selectbox("Region", region_options)
    with c3:
        horizon_label = st.selectbox("Horizon", ["Next 7 Days", "Next 30 Days", "Next 90 Days"], index=1)
    with c4:
        st.markdown("<div style='height:1.9rem;'></div>", unsafe_allow_html=True)
        run = st.button("Generate", type="primary", use_container_width=True)

    if not run and "forecast_result" not in st.session_state:
        st.session_state.forecast_result = None

    horizon_days = 7 if "7" in horizon_label else (30 if "30" in horizon_label else 90)
    if run or st.session_state.forecast_result is None:
        st.session_state.forecast_result = generate_forecast(
            df, horizon_days=horizon_days, product_id=product, region=region
        )

    result = st.session_state.forecast_result
    if result is None or result.forecast.empty:
        st.warning("No forecast available for the selected filter.")
        return

    st.markdown("---")
    _render_forecast_chart(result)
    _render_summary_cards(result)
    _render_recommendations(result)


def _render_forecast_chart(result) -> None:
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=result.history["date"],
            y=result.history["demand"],
            mode="lines",
            name="Historical",
            line=dict(color="#0f4c81", width=2.5),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=result.forecast["date"],
            y=result.forecast["predicted_demand"],
            mode="lines",
            name="Forecast",
            line=dict(color="#f97316", width=2.5, dash="dash"),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=result.forecast["date"].tolist() + result.forecast["date"].tolist()[::-1],
            y=result.forecast["upper_bound"].tolist() + result.forecast["lower_bound"].tolist()[::-1],
            fill="toself",
            fillcolor="rgba(15,76,129,0.12)",
            line=dict(color="rgba(255,255,255,0)"),
            name="Confidence interval",
        )
    )
    fig.update_layout(height=430, margin=dict(l=0, r=0, t=20, b=0), hovermode="x unified")
    st.plotly_chart(fig, use_container_width=True)


def _render_summary_cards(result) -> None:
    fc = result.forecast
    next_7 = float(fc.head(7)["predicted_demand"].sum())
    next_30 = float(fc.head(min(30, len(fc)))["predicted_demand"].sum())
    next_90 = float(fc.head(min(90, len(fc)))["predicted_demand"].sum())

    st.markdown("### Forecast summary")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        _summary_tile("Next 7 days", f"{next_7:,.0f}", "#0f4c81")
    with c2:
        _summary_tile("Next 30 days", f"{next_30:,.0f}", "#0f766e")
    with c3:
        _summary_tile("Next 90 days", f"{next_90:,.0f}", "#334155")
    with c4:
        _summary_tile("Confidence level", f"{result.confidence_level:.1f}%", "#b45309")


def _render_recommendations(result) -> None:
    fc = result.forecast.copy()
    early_avg = float(fc.head(max(3, min(7, len(fc))))["predicted_demand"].mean())
    late_avg = float(fc.tail(max(3, min(7, len(fc))))["predicted_demand"].mean())
    trend_pct = ((late_avg - early_avg) / (early_avg + 1e-6)) * 100

    st.markdown("### Action recommendations")
    if trend_pct > 12:
        st.info("Demand is trending up strongly. Increase replenishment buffers for top SKUs.")
    elif trend_pct < -12:
        st.info("Demand trend is softening. Reduce purchase quantities to avoid overstock.")
    else:
        st.info("Demand trend is stable. Maintain current inventory policy with weekly monitoring.")

    spread = (fc["upper_bound"] - fc["lower_bound"]).mean()
    if spread > fc["predicted_demand"].mean() * 0.6:
        st.warning("Forecast uncertainty is elevated. Consider more granular product or region filters.")


def _summary_tile(label: str, value: str, accent: str) -> None:
    st.markdown(
        f"""
        <div class="tile" style="border-top:4px solid {accent};">
            <div class="tile-label">{label}</div>
            <div class="tile-value">{value}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
