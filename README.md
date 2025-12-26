# OS Atlas — Operating System Analyzer

OS Atlas is a user-level **operating system analyzer**.

It does not simply show CPU or memory numbers.  
It continuously observes how system resources behave over time and explains what the operating system is experiencing in practical terms.

This project combines a real-time analyzer (CLI) with a live graphical dashboard (GUI) to make OS behavior visible and understandable.

---

## What This Tool Does

OS Atlas analyzes system behavior by observing:

- CPU load and scheduling pressure  
- Memory usage and memory stress  
- Top processes competing for resources  
- Short-term trends such as rising CPU load  
- Overall system health derived from OS signals  

The analyzer stores this information as snapshots and visualizes it through a live dashboard.

---

## Why This Matters

Operating systems rarely fail suddenly.  
They show **signals** first.

OS Atlas focuses on those signals:

- sustained CPU pressure  
- growing memory usage  
- process dominance  
- starvation risk  

This project is designed to demonstrate how **operating system concepts appear in real systems**, not just how to print metrics.

---

## Architecture Overview

OS Atlas is intentionally modular:

- **Collectors** gather raw OS data  
- **Analyzers** interpret system behavior  
- **Explainers** convert signals into human-readable meaning  
- **Storage** persists system snapshots  
- **UI** visualizes the live system state  

This mirrors how real observability and monitoring systems are built.

---

## Project Structure
os-atlas/
├── collectors/ # CPU, memory, and process data
├── analyzers/ # system health, starvation, deadlock logic
├── explainers/ # human-readable explanations
├── storage/ # snapshot persistence
├── ui/ # Streamlit dashboard
├── main.py # analyzer entry point
└── README.md

