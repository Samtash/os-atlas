import argparse
import sys
import logging
from pathlib import Path
from os_atlas.collectors.metrics import collect_cpu_metrics



def setup_logging(verbose=False):
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s | %(levelname)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        force=True,  # <-- this is the fix
    )


def validate_output_file(filepath):
    path = Path(filepath)
    if path.suffix.lower() not in [".json", ".csv"]:
        raise argparse.ArgumentTypeError(
            f"Output file must be .json or .csv, got: {path.suffix}"
        )
    return filepath


def handle_snapshot(args):
    logging.info("Taking system snapshot...")

    cpu = collect_cpu_metrics()

    logging.info("CPU Metrics:")
    logging.info(f"  Usage: {cpu['cpu_percent']}%")
    logging.info(f"  Logical cores: {cpu['logical_cores']}")
    logging.info(f"  Physical cores: {cpu['physical_cores']}")
    logging.info(f"  Frequency: {cpu['frequency_mhz']} MHz")

    logging.info("Snapshot completed")



def handle_watch(args):
    logging.info(f"Starting watch mode (interval: {args.interval}s)")
    logging.info("Press Ctrl+C to stop")
    logging.info("Watch mode active (implementation pending)")


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
