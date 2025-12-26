def evaluate_system_health(cpu, mem, starved, deadlocked):
    issues = []

    if cpu["cpu_percent"] > 80:
        issues.append("high CPU load")

    if mem["pressure"] == "high":
        issues.append("memory pressure")

    if starved:
        issues.append("process starvation")

    if deadlocked:
        issues.append("possible deadlock → resource wait")

    if not issues:
        return "HEALTHY", ["System operating within normal limits"]

    if "possible deadlock → resource wait" in issues and len(issues) >= 2:
        return "CRITICAL", issues

    return "DEGRADED", issues
