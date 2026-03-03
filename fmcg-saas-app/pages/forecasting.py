"""Demand forecasting page — premium design with diagnostics."""

from __future__ import annotations

import plotly.graph_objects as go
import streamlit as st

from utils.analytics import collect_normalized_data, generate_forecast
from utils.database import db_service
from utils.session import navigate_to


PLOTLY_LAYOUT = dict(
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
        """
        <div class="hero-banner">
            <h2>🔮  Demand Forecasting</h2>
            <p>Project near-term demand with Prophet ML models and confidence intervals</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if not st.session_state.data_uploaded:
        st.warning("Upload and process data first.")
        if st.button("📁  Go to Upload", type="primary"):
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
        run = st.button("⚡  Generate", type="primary", use_container_width=True)

    if not run and "forecast_result" not in st.session_state:
        st.session_state.forecast_result = None

    horizon_days = 7 if "7" in horizon_label else (30 if "30" in horizon_label else 90)
    if run or st.session_state.forecast_result is None:
        with st.spinner("🔮  Running Prophet ML forecast..."):
            st.session_state.forecast_result = generate_forecast(
                df, horizon_days=horizon_days, product_id=product, region=region
            )

        # Save to DB
        result = st.session_state.forecast_result
        if result and not result.forecast.empty and db_service.is_connected():
            db_service.save_forecast({
                "company_name": st.session_state.company_name or "Unknown",
                "product_id": product,
                "region": region,
                "horizon_days": horizon_days,
                "forecast": result.forecast[["date", "predicted_demand"]].assign(
                    date=result.forecast["date"].astype(str)
                ).to_dict(orient="records"),
                "confidence_level": result.confidence_level,
                "model_type": result.diagnostics.get("model_type", "prophet"),
                "diagnostics": result.diagnostics,
            })

    result = st.session_state.forecast_result
    if result is None or result.forecast.empty:
        st.warning("No forecast available for the selected filter. Try different product/region.")
        return

    st.markdown("---")
    _render_forecast_chart(result)
    _render_diagnostics(result)
    _render_summary_cards(result)
    _render_recommendations(result)


def _render_forecast_chart(result) -> None:
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=result.history["date"], y=result.history["demand"],
            mode="lines", name="Historical",
            line=dict(color="#0f4c81", width=2.5),
            fill="tozeroy", fillcolor="rgba(15,76,129,0.06)",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=result.forecast["date"], y=result.forecast["predicted_demand"],
            mode="lines", name="Forecast",
            line=dict(color="#f97316", width=2.5, dash="dash"),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=result.forecast["date"].tolist() + result.forecast["date"].tolist()[::-1],
            y=result.forecast["upper_bound"].tolist() + result.forecast["lower_bound"].tolist()[::-1],
            fill="toself", fillcolor="rgba(249,115,22,0.10)",
            line=dict(color="rgba(255,255,255,0)"),
            name="Confidence Band",
        )
    )
    fig.update_layout(height=450, **PLOTLY_LAYOUT)
    st.plotly_chart(fig, use_container_width=True)


def _render_diagnostics(result) -> None:
    diag = result.diagnostics or {}
    if not diag:
        return

    st.markdown("### 🔍  Model Diagnostics")
    cols = st.columns(4)

    trend = diag.get("trend_direction", "unknown")
    trend_icon = "📈" if trend == "upward" else ("📉" if trend == "downward" else "➡️")
    trend_color = "#15803d" if trend == "upward" else ("#dc2626" if trend == "downward" else "#d97706")

    with cols[0]:
        st.markdown(
            f"""
            <div class="panel-card" style="text-align:center;">
                <div style="font-size:1.5rem;">{trend_icon}</div>
                <div style="font-weight:700;color:{trend_color};font-size:0.95rem;text-transform:capitalize;">{trend}</div>
                <div style="font-size:0.75rem;color:#94a3b8;">Trend Direction</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with cols[1]:
        change = diag.get("trend_change_pct", 0)
        st.markdown(
            f"""
            <div class="panel-card" style="text-align:center;">
                <div style="font-size:1.3rem;font-weight:700;color:{trend_color};">{change:+.1f}%</div>
                <div style="font-size:0.75rem;color:#94a3b8;margin-top:0.2rem;">Trend Change</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with cols[2]:
        seasonality = "✅ Yes" if diag.get("has_seasonality") else "❌ No"
        st.markdown(
            f"""
            <div class="panel-card" style="text-align:center;">
                <div style="font-size:1rem;font-weight:700;">{seasonality}</div>
                <div style="font-size:0.75rem;color:#94a3b8;margin-top:0.2rem;">Seasonality Detected</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with cols[3]:
        dp = diag.get("data_points", 0)
        model_type = diag.get("model_type", "unknown")
        st.markdown(
            f"""
            <div class="panel-card" style="text-align:center;">
                <div style="font-size:1rem;font-weight:700;">{dp:,}</div>
                <div style="font-size:0.75rem;color:#94a3b8;margin-top:0.2rem;">Data Points ({model_type})</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def _render_summary_cards(result) -> None:
    fc = result.forecast
    next_7 = float(fc.head(7)["predicted_demand"].sum())
    next_30 = float(fc.head(min(30, len(fc)))["predicted_demand"].sum())
    next_90 = float(fc.head(min(90, len(fc)))["predicted_demand"].sum())

    st.markdown("### 📋  Forecast Summary")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        _summary_tile("Next 7 Days", f"{next_7:,.0f}", "#0f4c81")
    with c2:
        _summary_tile("Next 30 Days", f"{next_30:,.0f}", "#15803d")
    with c3:
        _summary_tile("Next 90 Days", f"{next_90:,.0f}", "#334155")
    with c4:
        _summary_tile("Confidence", f"{result.confidence_level:.1f}%", "#d97706")


def _render_recommendations(result) -> None:
    fc = result.forecast.copy()
    early_avg = float(fc.head(max(3, min(7, len(fc))))["predicted_demand"].mean())
    late_avg = float(fc.tail(max(3, min(7, len(fc))))["predicted_demand"].mean())
    trend_pct = ((late_avg - early_avg) / (early_avg + 1e-6)) * 100

    st.markdown("### ⚡  Recommendations")
    if trend_pct > 12:
        st.info("📈  **Demand trending up strongly.** Increase replenishment buffers for top SKUs to avoid stockouts.")
    elif trend_pct < -12:
        st.info("📉  **Demand trending down.** Reduce purchase quantities to avoid overstock and free cash.")
    else:
        st.info("➡️  **Demand is stable.** Maintain current inventory policy. Review weekly for changes.")

    spread = (fc["upper_bound"] - fc["lower_bound"]).mean()
    if spread > fc["predicted_demand"].mean() * 0.6:
        st.warning("⚠️  **High forecast uncertainty detected.** Try filtering by specific product or region for sharper predictions.")


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
