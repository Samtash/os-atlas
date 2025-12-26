import json
import time
from pathlib import Path

HISTORY_FILE = Path("os_storage/snapshot_history.jsonl")


def load_latest_snapshot():
    if not HISTORY_FILE.exists():
        print("No snapshot history found. Run watch mode first.")
        return None

    with HISTORY_FILE.open("r") as f:
        lines = f.readlines()
        if not lines:
            return None
        return json.loads(lines[-1])


def render(record):
    # support both raw snapshot and wrapped history format
    snap = record.get("snapshot", record)

    cpu = snap["cpu"]
    mem = snap.get("memory", snap.get("mem", {}))
    procs = snap.get("top_processes", [])

    print("\n=== SYSTEM SNAPSHOT ===\n")

    print("CPU")
    print(f"  Usage: {cpu.get('cpu_percent')}%")
    print(
        f"  Cores: {cpu.get('logical_cores')} logical / "
        f"{cpu.get('physical_cores')} physical"
    )
    print(f"  Frequency: {cpu.get('frequency_mhz')} MHz\n")

    print("Memory")
    print(f"  Used: {mem.get('percent_used')}%")
    print(f"  Available: {mem.get('available_mb')} MB")
    print(f"  Pressure: {mem.get('pressure')}\n")

    if procs:
        print("Top Processes (CPU)")
        for p in procs[:5]:
            print(
                f"  PID {p.get('pid')} | {p.get('name')} | "
                f"CPU: {p.get('cpu_percent')}% | MEM: {p.get('memory_mb')} MB"
            )

    print("\n=======================\n")


def main():
    while True:
        record = load_latest_snapshot()
        if record:
            render(record)
        time.sleep(2)


if __name__ == "__main__":
    main()
