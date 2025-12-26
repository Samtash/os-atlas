import argparse
import sys
import logging
from pathlib import Path
from os_atlas.collectors.metrics import collect_cpu_metrics
from os_atlas.analyzers.memory import analyze_memory
from os_atlas.explainers.snapshot_explainer import explain_snapshot
from os_atlas.collectors.process import collect_top_processes
import time
from collections import deque
from os_atlas.storage.history_writer import write_snapshot
from os_atlas.analyzers.starvation import StarvationTracker
from os_atlas.explainers.starvation_explainer import explain_starvation
from os_atlas.analyzers.deadlock import DeadlockDetector
from os_atlas.explainers.system_health import evaluate_system_health



def setup_logging(verbose=False):
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s | %(levelname)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        force=True,
    )


def validate_output_file(filepath):
    path = Path(filepath)
    if path.suffix.lower() not in [".json", ".csv"]:
        raise argparse.ArgumentTypeError(
            f"Output file must be .json or .csv, got: {path.suffix}"
        )
    return filepath


def evaluate_system_health(cpu, mem, starved, suspects):
    """
    Evaluate overall system health based on metrics.
    Returns: (status_string, list_of_reasons)
    """
    status = "normal"
    reasons = []
    
    # Check CPU
    if cpu["cpu_percent"] > 80:
        status = "warning"
        reasons.append(f"High CPU usage: {cpu['cpu_percent']}%")
    
    # Check memory
    if mem["percent_used"] > 85:
        status = "critical" if mem["percent_used"] > 95 else "warning"
        reasons.append(f"High memory usage: {mem['percent_used']}%")
    
    if mem["pressure"] == "high":
        status = "warning"
        reasons.append("Memory pressure is high")
    
    # Check starvation
    if starved:
        status = "warning"
        reasons.append(f"{len(starved)} process(es) starving")
    
    # Check deadlock suspects
    if suspects:
        status = "warning"
        reasons.append(f"{len(suspects)} possible deadlock suspect(s)")
    
    if not reasons:
        reasons.append("All metrics within normal ranges")
    
    return status, reasons


def handle_snapshot(args):
    logging.info("Taking system snapshot in REAL time")

    cpu = collect_cpu_metrics()
    mem = analyze_memory()
    procs = collect_top_processes()

    logging.info("CPU Metrics:")
    logging.info(f" Usage: {cpu['cpu_percent']}%")
    logging.info(f" Logical cores: {cpu['logical_cores']}")
    logging.info(f" Physical cores: {cpu['physical_cores']}")
    logging.info(f" Frequency: {cpu['frequency_mhz']} MHz")

    logging.info("Memory Metrics:")
    logging.info(f" Used: {mem['used_mb']} MB / {mem['total_mb']} MB")
    logging.info(f" Available: {mem['available_mb']} MB")
    logging.info(f" Usage: {mem['percent_used']}%")
    logging.info(f" Pressure level: {mem['pressure']}")

    logging.info("Top Processes (by CPU usage):")
    for p in procs:
        logging.info(
            f" PID {p['pid']} | {p['name']} | CPU: {p['cpu_percent']}% | MEM: {p['memory_mb']} MB"
        )

    explanations = explain_snapshot(cpu, mem, procs)

    logging.info("System Interpretation:")
    for line in explanations:
        logging.info(f" - {line}")

    # Evaluate system health (FIX: define status and reasons)
    status, reasons = evaluate_system_health(cpu, mem, [], [])
    
    logging.info(f"System Health: {status}")
    for reason in reasons:
        logging.info(f" - {reason}")

    snapshot = {
        "cpu": cpu,
        "memory": mem,
        "top_processes": procs,
        "system_health": {
            "status": status,
            "reasons": reasons
        }
    }
    write_snapshot(snapshot)

    logging.info("Snapshot completed")

def handle_watch(args):
    logging.info(f"Starting watch mode (interval: {args.interval}s)")
    logging.info("Press Ctrl+C to stop")

    history = deque(maxlen=5)

    tracker = StarvationTracker(window=6, min_cpu=0.3)
    deadlock = DeadlockDetector(window=6, min_cpu=0.2)

    try:
        while True:
            cpu = collect_cpu_metrics()
            mem = analyze_memory()
            procs = collect_top_processes(limit=10)

            history.append({"cpu": cpu, "mem": mem})

            logging.info(
                "CPU: %s%% | MEM: %s%% (%s)",
                cpu["cpu_percent"],
                mem["percent_used"],
                mem["pressure"],
            )

            # ---- Short-term trends ----
            if len(history) >= 2:
                prev, curr = history[-2], history[-1]

                if curr["cpu"]["cpu_percent"] > prev["cpu"]["cpu_percent"] + 10:
                    logging.info("Trend: CPU load increasing")

                if curr["mem"]["percent_used"] > prev["mem"]["percent_used"] + 5:
                    logging.info("Trend: memory usage increasing")

                if curr["mem"]["pressure"] == prev["mem"]["pressure"] == "high":
                    logging.info("Trend: sustained memory pressure")

            # ---- Starvation ----
            tracker.update(procs)
            starved = tracker.get_starved()

            if starved:
                logging.info("Starvation detected:")
                for p in starved[:5]:
                    logging.info(
                        " PID %s | %s | avg CPU: %.2f%%",
                        p["pid"], p["name"], p["avg_cpu"]
                    )

                for line in explain_starvation(starved, cpu):
                    logging.info(" - %s", line)

            # ---- Deadlock ----
            deadlock.update(procs)
            suspects = deadlock.get_suspects()

            if suspects:
                logging.info("Possible deadlock-like processes:")
                for p in suspects[:5]:
                    logging.info(
                        " PID %s | %s | avg CPU: %.2f%% | mem growth: %.2f MB",
                        p["pid"], p["name"], p["avg_cpu"], p["mem_growth_mb"]
                    )

            # ---- System health ----
            status, reasons = evaluate_system_health(cpu, mem, starved, suspects)
            logging.info("SYSTEM HEALTH: %s", status)
            for r in reasons:
                logging.info(" - %s", r)

            # ---- Write snapshot ----
            snapshot = {
                "timestamp": time.time(),
                "cpu": cpu,
                "memory": mem,
                "processes": procs,
                "health": {
                    "status": status,
                    "reasons": reasons
                }
            }
            write_snapshot(snapshot)

            time.sleep(args.interval)

    except KeyboardInterrupt:
        logging.info("Watch stopped by user")
def handle_report(args):
    logging.info(f"Generating system report: {args.out}")
    logging.info("Report completed (implementation pending)")


def build_parser():
    parser = argparse.ArgumentParser(
        prog="os-atlas",
        description="User-level system monitor with OS-aware explanations",
    )

    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose logging",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    snapshot = subparsers.add_parser("snapshot", help="Take a system snapshot")
    snapshot.set_defaults(func=handle_snapshot)

    watch = subparsers.add_parser("watch", help="Continuously monitor the system")
    watch.add_argument(
        "--interval",
        type=int,
        default=2,
        help="Polling interval in seconds",
    )
    watch.set_defaults(func=handle_watch)

    report = subparsers.add_parser("report", help="Generate a system report")
    report.add_argument(
        "--out",
        required=True,
        type=validate_output_file,
        help="Output file (.json or .csv)",
    )
    report.set_defaults(func=handle_report)

    return parser


def main():
    try:
        parser = build_parser()
        args = parser.parse_args()
        setup_logging(verbose=getattr(args, "verbose", False))
        args.func(args)
    except KeyboardInterrupt:
        logging.info("Interrupted by user")
        sys.exit(0)
    except Exception as e:
        logging.error(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
  main()