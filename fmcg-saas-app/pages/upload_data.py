"""Data upload and schema mapping page."""

from __future__ import annotations

from datetime import datetime

import pandas as pd
import streamlit as st

from utils.analytics import (
    STANDARD_SCHEMA,
    auto_map_schema,
    collect_normalized_data,
    get_quality_summary,
    normalize_dataset,
)
from utils.session import navigate_to


MAX_UPLOAD_FILES = 10


def show() -> None:
    st.markdown("## Data upload and mapping")
    st.caption("Step 3 of 3 - upload files and map to the platform schema")

    left, right = st.columns([1.35, 1])

    with left:
        _render_upload_panel()
    with right:
        _render_status_panel()


def _render_upload_panel() -> None:
    st.markdown("### Upload files")
    uploaded_files = st.file_uploader(
        f"Accepted formats: CSV, XLSX, XLS (max {MAX_UPLOAD_FILES} files)",
        type=["csv", "xlsx", "xls"],
        accept_multiple_files=True,
        help="Upload up to 10 files per batch.",
    )

    if not uploaded_files:
        return

    if len(uploaded_files) > MAX_UPLOAD_FILES:
        st.error(f"You selected {len(uploaded_files)} files. Only the first {MAX_UPLOAD_FILES} will be shown.")
        uploaded_files = uploaded_files[:MAX_UPLOAD_FILES]
    else:
        st.caption(f"{len(uploaded_files)} file(s) selected.")

    for idx, uploaded_file in enumerate(uploaded_files, start=1):
        _render_single_file_block(uploaded_file, idx)

    if st.session_state.uploaded_files and st.button("Continue to dashboard", use_container_width=True):
        navigate_to("dashboard")


def _render_single_file_block(uploaded_file, index: int) -> None:
    key_prefix = _safe_key(uploaded_file.name, index)
    with st.expander(f"{index}. {uploaded_file.name}", expanded=(index == 1)):
        raw_df = _read_file(uploaded_file)
        if raw_df is None:
            return

        if raw_df.empty:
            st.error("The uploaded file is empty.")
            return

        st.success(f"Loaded `{uploaded_file.name}` with {len(raw_df):,} rows and {len(raw_df.columns)} columns.")
        st.dataframe(raw_df.head(20), use_container_width=True)

        default_mapping = auto_map_schema(raw_df)
        mapping = _render_mapping_editor(raw_df, key_prefix, default_mapping)

        col1, col2 = st.columns([1, 1])
        with col1:
            process_clicked = st.button(
                f"Process {uploaded_file.name}",
                type="primary",
                use_container_width=True,
                key=f"process_{key_prefix}",
            )
        with col2:
            if st.button("Reset mapping", use_container_width=True, key=f"reset_{key_prefix}"):
                for schema_col in STANDARD_SCHEMA:
                    st.session_state.pop(f"map_{key_prefix}_{schema_col}", None)
                st.rerun()

        if not process_clicked:
            return

        normalized = normalize_dataset(raw_df, mapping)
        quality = get_quality_summary(normalized)
        storage_key = _get_storage_key(uploaded_file.name)
        st.session_state.uploaded_files[storage_key] = {
            "data": raw_df,
            "mapping": mapping,
            "normalized_data": normalized,
            "quality": quality,
            "original_name": uploaded_file.name,
            "timestamp": datetime.utcnow().isoformat(),
        }
        st.session_state.data_uploaded = True
        st.success(f"Processed and saved `{storage_key}`.")


def _read_file(uploaded_file) -> pd.DataFrame | None:
    try:
        if uploaded_file.name.endswith(".csv"):
            return pd.read_csv(uploaded_file)
        return pd.read_excel(uploaded_file)
    except Exception as exc:
        st.error(f"Unable to read file `{uploaded_file.name}`: {exc}")
        return None


def _safe_key(file_name: str, index: int) -> str:
    clean = "".join(ch if ch.isalnum() else "_" for ch in file_name)
    return f"{index}_{clean}"


def _get_storage_key(file_name: str) -> str:
    if file_name not in st.session_state.uploaded_files:
        return file_name
    counter = 2
    while f"{file_name} ({counter})" in st.session_state.uploaded_files:
        counter += 1
    return f"{file_name} ({counter})"


def _render_mapping_editor(raw_df: pd.DataFrame, file_name: str, default_mapping: dict[str, str]) -> dict[str, str]:
    st.markdown("### Schema mapping")
    st.caption("Map your columns to platform fields. Leave optional fields as `-- Skip --`.")
    mapping: dict[str, str] = {}

    available_cols = ["-- Skip --"] + raw_df.columns.tolist()
    for std_field, description in STANDARD_SCHEMA.items():
        key = f"map_{file_name}_{std_field}"
        if key not in st.session_state:
            st.session_state[key] = default_mapping.get(std_field, "-- Skip --")

        col1, col2 = st.columns([1.2, 2.8])
        with col1:
            st.markdown(f"**{std_field}**")
            st.caption(description)
        with col2:
            default_value = st.session_state.get(key, "-- Skip --")
            if default_value not in available_cols:
                default_value = "-- Skip --"
            selected = st.selectbox(
                f"Map {std_field}",
                options=available_cols,
                index=available_cols.index(default_value),
                label_visibility="collapsed",
                key=key,
            )
            if selected != "-- Skip --":
                mapping[std_field] = selected

    required = {"order_date", "product_id", "quantity"}
    missing_required = required.difference(set(mapping.keys()))
    if missing_required:
        st.warning(f"Missing required mappings: {', '.join(sorted(missing_required))}")
    else:
        st.success("Required fields mapped.")

    return mapping


def _render_status_panel() -> None:
    st.markdown("### Workspace ingestion status")
    if not st.session_state.uploaded_files:
        st.info("No processed files yet.")
        return

    combined = collect_normalized_data(st.session_state.uploaded_files)
    quality = get_quality_summary(combined)

    mc1, mc2 = st.columns(2)
    with mc1:
        st.metric("Rows", f"{quality['rows']:,}")
        st.metric("Coverage days", quality["date_coverage_days"])
    with mc2:
        st.metric("Columns", quality["columns"])
        st.metric("Missing %", f"{quality['missing_percent']:.1f}%")

    st.markdown("---")
    st.markdown("#### Processed files")
    for filename, meta in st.session_state.uploaded_files.items():
        rows = len(meta.get("normalized_data", []))
        timestamp = meta.get("timestamp", "")[:19].replace("T", " ")
        st.markdown(
            f"""
            <div class="panel-card" style="margin-bottom:0.55rem;">
                <strong>{filename}</strong><br>
                <span style="color:#475569;">Rows: {rows:,} | Processed: {timestamp} UTC</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
