import psutil


def collect_cpu_metrics():
    """
  This uses psutil, 
  which basicaly lets me see see basic information about your computer's operating system.
    """

    
    cpu_usage = psutil.cpu_percent(interval=1)

   
    logical_cores = psutil.cpu_count(logical=True)


    physical_cores = psutil.cpu_count(logical=False)


    freq = psutil.cpu_freq()
    frequency_mhz = freq.current if freq else None

    return {
        "cpu_percent": cpu_usage,
        "logical_cores": logical_cores,
        "physical_cores": physical_cores,
        "frequency_mhz": frequency_mhz,
    }
