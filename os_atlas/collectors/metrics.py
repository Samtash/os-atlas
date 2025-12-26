import psutil


def collect_cpu_metrics():
    """
    Collect basic CPU metrics using user-level OS APIs.
    Returns a dictionary with raw CPU data.
    """

    cpu_usage = psutil.cpu_percent(interval=1)

    return {
        "cpu_percent": cpu_usage,
        "logical_cores": psutil.cpu_count(logical=True),
        "physical_cores": psutil.cpu_count(logical=False),
        "frequency_mhz": psutil.cpu_freq().current if psutil.cpu_freq() else None,
    }
