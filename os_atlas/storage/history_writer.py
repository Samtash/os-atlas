import json
import time
from pathlib import Path

DATA_DIR = Path("os_storage")
DATA_DIR.mkdir(exist_ok=True)

HISTORY_FILE = DATA_DIR / "snapshot_history.jsonl"


def write_snapshot(snapshot: dict):
    record = {
        "timestamp": time.time(),
        "snapshot": snapshot
    }

    with HISTORY_FILE.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record) + "\n")
