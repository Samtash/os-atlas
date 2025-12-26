import psutil
def analyze_memory():
    """
    by using ths functionn we're basically retrieving
      basic CPU information from the system.
    """

    mem = psutil.virtual_memory()

    pressure = "normal"

    # its greater than 80 ,thatll mean high memory pressure is very much possible
    if mem.percent > 80 and mem.available < 500 * 1024 * 1024:
        pressure = "high"

    return {
        "total_mb": round(mem.total / (1024 * 1024), 1),
        "used_mb": round(mem.used / (1024 * 1024), 1),
        "available_mb": round(mem.available / (1024 * 1024), 1),
        "percent_used": mem.percent,
        "pressure": pressure,
    }
