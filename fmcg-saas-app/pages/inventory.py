"""Inventory optimization page — premium design."""

from __future__ import annotations

import plotly.graph_objects as go
import streamlit as st

from utils.analytics import collect_normalized_data, inventory_overview
from utils.session import navigate_to


def show() -> None:
    st.markdown(
        """
        <div class="hero-banner">
            <h2>📦  Inventory Optimization</h2>
            <p>Track stock risk across regions and prioritize replenishment actions</p>
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
        st.error("No valid inventory-driving data found.")
        return

    payload = inventory_overview(df)
    cards = payload["cards"]
    table = payload["table"]
    recommendations = payload["recommendations"]

    # Status cards
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        _stock_tile("Optimal", cards.get("optimal", 0), "#15803d", "✅")
    with c2:
        _stock_tile("Low Stock", cards.get("low_stock", 0), "#d97706", "⚠️")
    with c3:
        _stock_tile("Stockout Risk", cards.get("stockout", 0), "#dc2626", "🔴")
    with c4:
        _stock_tile("Overstock", cards.get("overstock", 0), "#0f4c81", "📦")

    # Distribution chart
    st.markdown("### Stock Distribution")
    fig = go.Figure(
        go.Pie(
            labels=["Optimal", "Low Stock", "Stockout Risk", "Overstock"],
            values=[cards.get("optimal", 0), cards.get("low_stock", 0), cards.get("stockout", 0), cards.get("overstock", 0)],
            hole=0.55,
            marker=dict(colors=["#22c55e", "#eab308", "#ef4444", "#3b82f6"]),
            textinfo="label+percent",
            textfont=dict(size=12, family="Inter"),
        )
    )
    fig.update_layout(
        height=300,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        showlegend=False,
        margin=dict(l=20, r=20, t=10, b=10),
    )
    st.plotly_chart(fig, use_container_width=True)

    # Data table
    st.markdown("### 📋  Product & Region Inventory View")
    if table.empty:
        st.info("No inventory rows available.")
    else:
        display_df = table[
            [
                "product_id", "region", "estimated_stock", "reorder_point",
                "safety_stock", "days_of_cover", "status", "action",
            ]
        ].copy()
        display_df = display_df.rename(
            columns={
                "product_id": "Product",
                "region": "Region",
                "estimated_stock": "Est. Stock",
                "reorder_point": "Reorder Point",
                "safety_stock": "Safety Stock",
                "days_of_cover": "Days of Cover",
                "status": "Status",
                "action": "Action",
            }
        )
        st.dataframe(display_df, use_container_width=True, hide_index=True)

    # Recommendations
    st.markdown("### ⚡  Recommendations")
    if not recommendations:
        st.success("✅  No immediate inventory actions required. All stock levels are healthy.")
    for rec in recommendations:
        st.info(f"💡  {rec}")


def _stock_tile(label: str, value: int, accent: str, icon: str) -> None:
    st.markdown(
        f"""
        <div class="tile" style="border-top:4px solid {accent};">
            <div class="tile-label">{icon}  {label}</div>
            <div class="tile-value">{value:,}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
