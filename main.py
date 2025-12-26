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





def setup_logging(verbose=False):
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s | %(levelname)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        force=True,  # forces the program to handover the mic
    )


def validate_output_file(filepath):
    path = Path(filepath)
    if path.suffix.lower() not in [".json", ".csv"]:
        raise argparse.ArgumentTypeError(
            f"Output file must be .json or .csv, got: {path.suffix}"
        )
    return filepath



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

    snapshot = {
        "cpu": cpu,
        "memory": mem,
        "top_processes": procs
    }

    write_snapshot(snapshot)    

    logging.info("Snapshot completed")





def handle_watch(args):
    logging.info(f"Starting watch mode (interval: {args.interval}s)")
    logging.info("Press Ctrl+C to stop")

    history = deque(maxlen=5)  # short-term trend window

    tracker = StarvationTracker(
        window=6,
        min_cpu=0.3
    )

    deadlock = DeadlockDetector(
        window=6,
        min_cpu=0.2
    )

  try:
    while True:
        cpu = collect_cpu_metrics()
        mem = analyze_memory()
        procs = collect_top_processes(limit=10)

        snapshot = {
            "cpu": cpu,
            "mem": mem,
        }
        history.append(snapshot)

        logging.info(
            "CPU: %s%% | MEM: %s%% (%s)",
            cpu["cpu_percent"],
            mem["percent_used"],
            mem["pressure"]
        )

        # ---- Short-term trend detection ----
        if len(history) >= 2:
            prev = history[-2]
            curr = history[-1]

            if curr["cpu"]["cpu_percent"] > prev["cpu"]["cpu_percent"] + 10:
                logging.info("Trend: CPU load increasing")

            if curr["mem"]["percent_used"] > prev["mem"]["percent_used"] + 5:
                logging.info("Trend: memory usage increasing")

            if (
                curr["mem"]["pressure"] == "high"
                and prev["mem"]["pressure"] == "high"
            ):
                logging.info("Trend: sustained memory pressure")

        # ---- Starvation detection ----
        tracker.update(procs)
        starved = tracker.get_starved()

        if starved:
            logging.info("Starvation detected (low CPU over time):")
            for p in starved[:5]:
                logging.info(
                    " PID %s | %s | avg CPU: %.2f%%",
                    p["pid"],
                    p["name"],
                    p["avg_cpu"]
                )

            explanations = explain_starvation(starved, cpu)
            if explanations:
                logging.info("Starvation explanation:")
                for line in explanations:
                    logging.info(" - %s", line)

        # ---- Deadlock detection ----
        deadlock.update(procs)
        suspects = deadlock.get_suspects()

        if suspects:
            logging.info("Possible deadlock-like processes detected:")
            for p in suspects[:5]:
                logging.info(
                    " PID %s | %s | avg CPU: %.2f%% | mem growth: %.2f MB",
                    p["pid"],
                    p["name"],
                    p["avg_cpu"],
                    p["mem_growth_mb"]
                )

        # ---- System health evaluation ----
        status, reasons = evaluate_system_health(cpu, mem, starved, suspects)

        logging.info("SYSTEM HEALTH: %s", status)
        for r in reasons:
            logging.info(" - %s", r)

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
