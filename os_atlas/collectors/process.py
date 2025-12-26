import psutil


def collect_top_processes(limit=5):
    processes = []

    for proc in psutil.process_iter(attrs=["pid", "name", "cpu_percent", "memory_info"]):
        try:
            info = proc.info
            processes.append({
                "pid": info["pid"],
                "name": info["name"],
                "cpu_percent": info["cpu_percent"],
                "memory_mb": round(info["memory_info"].rss / (1024 * 1024), 1)
            })
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    processes.sort(key=lambda p: p["cpu_percent"], reverse=True)
    return processes[:limit]
