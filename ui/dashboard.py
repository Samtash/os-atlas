import json
import time
from pathlib import Path

import streamlit as st

DATA_FILE = Path("os_storage/snapshot_history.jsonl")  # Changed to .jsonl

st.set_page_config(
    page_title="OS Atlas Dashboard",
    layout="wide"
)

st.title("🧠 OS Atlas – System Monitor")

def load_snapshots():
    if not DATA_FILE.exists():
        return []
    
    snapshots = []
    with open(DATA_FILE, "r") as f:
        for line in f:
            if line.strip():
                snapshots.append(json.loads(line))
    return snapshots

refresh = st.sidebar.slider(
    "Refresh interval (seconds)",
    min_value=1,
    max_value=10,
    value=2
)

placeholder = st.empty()

while True:
    snapshots = load_snapshots()

    if not snapshots:
        st.warning("No snapshots yet. Run watch mode first.")
        time.sleep(refresh)
        continue

    latest = snapshots[-1]
    cpu = latest["snapshot"]["cpu"]
    mem = latest["snapshot"]["memory"]
    health = latest["snapshot"].get("health", {})

    with placeholder.container():
        col1, col2, col3 = st.columns(3)

        col1.metric(
            "CPU Usage",
            f"{cpu['cpu_percent']}%"
        )

        col2.metric(
            "Memory Usage",
            f"{mem['percent_used']}%"
        )

        status = health.get("status", "unknown")
        col3.metric(
            "System Health",
            status.upper()
        )

        st.subheader("Top Processes")
        st.table(latest["snapshot"]["processes"])

    time.sleep(refresh)