import time


class StarvationTracker:
    def __init__(self, window=6, min_cpu=0.3):
        self.window = int(window)
        self.min_cpu = float(min_cpu)
        self._history = {}

    def update(self, processes):
        now = time.time()
        for p in processes:
            pid = p.get("pid")
            if pid is None:
                continue

            cpu = float(p.get("cpu_percent", 0.0))
            entry = self._history.get(pid)
            if entry is None:
                self._history[pid] = {"name": p.get("name", ""), "samples": [(now, cpu)]}
                continue

            entry["name"] = p.get("name", entry.get("name", ""))
            entry["samples"].append((now, cpu))
            if len(entry["samples"]) > self.window:
                entry["samples"] = entry["samples"][-self.window :]

        live = {p.get("pid") for p in processes if p.get("pid") is not None}
        for pid in list(self._history.keys()):
            if pid not in live:
                self._history.pop(pid, None)

    def get_starved(self):
        flagged = []
        for pid, entry in self._history.items():
            samples = entry.get("samples", [])
            if len(samples) < self.window:
                continue

            avg_cpu = sum(v for _, v in samples) / len(samples)
            if avg_cpu < self.min_cpu:
                flagged.append(
                    {
                        "pid": pid,
                        "name": entry.get("name", ""),
                        "avg_cpu": round(avg_cpu, 2),
                        "window": len(samples),
                    }
                )

        flagged.sort(key=lambda x: x["avg_cpu"])
        return flagged
