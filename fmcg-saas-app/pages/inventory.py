"""Inventory optimization page."""

from __future__ import annotations

import streamlit as st

from utils.analytics import collect_normalized_data, inventory_overview
from utils.session import navigate_to


def show() -> None:
    st.markdown(
        """
        <div class="hero-banner">
            <h2>Inventory Optimization</h2>
            <p>Track stock risk across regions and prioritize replenishment actions with better visibility.</p>
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
        st.error("No valid inventory-driving data found.")
        return

    payload = inventory_overview(df)
    cards = payload["cards"]
    table = payload["table"]
    recommendations = payload["recommendations"]

    st.markdown("### Stock status")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        _stock_tile("Optimal", cards.get("optimal", 0), "#15803d")
    with c2:
        _stock_tile("Low Stock", cards.get("low_stock", 0), "#b45309")
    with c3:
        _stock_tile("Stockout Risk", cards.get("stockout", 0), "#b91c1c")
    with c4:
        _stock_tile("Overstock", cards.get("overstock", 0), "#0f4c81")

    st.markdown("---")
    st.markdown("### Product and region inventory view")
    if table.empty:
        st.info("No inventory rows available.")
    else:
        display_df = table[
            [
                "product_id",
                "region",
                "estimated_stock",
                "reorder_point",
                "safety_stock",
                "days_of_cover",
                "status",
                "action",
            ]
        ].copy()
        display_df = display_df.rename(
            columns={
                "product_id": "Product",
                "region": "Region",
                "estimated_stock": "Estimated Stock",
                "reorder_point": "Reorder Point",
                "safety_stock": "Safety Stock",
                "days_of_cover": "Days of Cover",
                "status": "Status",
                "action": "Action",
            }
        )
        st.dataframe(display_df, use_container_width=True, hide_index=True)

    st.markdown("---")
    st.markdown("### Recommendations")
    if not recommendations:
        st.info("No specific inventory action detected right now.")
    for rec in recommendations:
        st.info(rec)


def _stock_tile(label: str, value: int, accent: str) -> None:
    st.markdown(
        f"""
        <div class="tile" style="border-top:4px solid {accent};">
            <div class="tile-label">{label}</div>
            <div class="tile-value">{value:,}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
