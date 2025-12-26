def explain_snapshot(cpu, mem,procs):
    explanations = []

    if cpu["cpu_percent"] > 80:
        explanations.append("CPU usage is high, system may be under heavy load.")
    else:
        explanations.append("CPU usage is within normal range.")

    if mem["pressure"] == "high":
        explanations.append("Memory pressure is high; system may start swapping.")
    else:
        explanations.append("Memory usage looks stable.")

    return explanations
