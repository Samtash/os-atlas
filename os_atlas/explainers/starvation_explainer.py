def explain_starvation(starved, cpu):
    explanations = []

    if not starved:
        return explanations

    if cpu["cpu_percent"] > 70:
        explanations.append(
            "System CPU load is high. This will increase the competition among processes."
        )

    explanations.append(
        "Starved processes are recieving consistently low CPU time despite being active."
    )

    explanations.append(
        "This usually happens because the scheduler favors certain tasks or the CPU is too busy."
    )

    explanations.append(
        "Starvation is decided by looking at what the program is experiencing"
    )

    return explanations
