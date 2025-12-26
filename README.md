# OS Atlas
## What is OS Atlas?

**OS Atlas** is a **system-level analyzer** that observes how an operating system behaves under real workloads. Instead of only reporting raw metrics, it interprets CPU, memory, and process activity to surface meaningful system states such as pressure, starvation risk, and overall health.

In short: **OS Atlas explains what your system is doing—and why it matters.**

---

## Why This Project Is Needed

Modern operating systems expose a large number of metrics, but metrics alone rarely tell the full story. High CPU usage, low available memory, or many running processes do not automatically indicate that a system is unhealthy.

OS Atlas bridges this gap by connecting low-level signals to higher-level interpretations, allowing system behavior to be *reasoned about*, not just observed.

This approach mirrors how operating systems are studied in academia and analyzed in real-world engineering environments.

---

## Project Overview

OS Atlas continuously collects system information and applies lightweight analysis to detect patterns such as:

- Rising CPU load over time  
- Sustained memory pressure  
- Processes receiving consistently low CPU time  
- Symptoms resembling deadlock-like behavior  

The project supports both **CLI-based monitoring** and a **simple GUI**, making it suitable for experimentation, demonstrations, and learning.

---

## Key Features

- Real-time CPU and memory analysis  
- Short-term trend detection  
- Heuristic-based starvation detection at the process level  
- Deadlock-like behavior identification using behavioral signals  
- System health evaluation combining multiple indicators  
- Modular architecture for easy extension  

---

## Operating System Concepts Covered

This project demonstrates core operating system concepts through practical analysis:

### CPU Scheduling & Load Analysis
Observes scheduling pressure and rising CPU trends over time.

### Process Management
Tracks active processes and highlights resource-dominant behavior.

### Memory Management & Pressure
Evaluates memory usage, availability, and sustained stress conditions.

### Starvation Detection (Heuristic-Based)
Identifies processes that receive persistently low CPU time across samples.

### Deadlock-like Behavior Detection
Flags lack of forward progress using observable behavioral symptoms rather than strict locking models.

### System Health Evaluation
Synthesizes multiple OS signals into an overall health assessment.

---

## Skills Demonstrated

The project applies each skill as follows:

### Operating System Fundamentals
**Where:** `collectors/`, `analyzers/`  
**Used to:** Apply OS concepts such as CPU scheduling, memory pressure, process states, starvation, and deadlock behavior.

### System-Level Reasoning & Diagnostics
**Where:** `analyzers/starvation.py`, `analyzers/deadlock_like.py`, `analyzers/health.py`  
**Used to:** Interpret raw metrics to diagnose system behavior over time.

### Python System Programming
**Where:** `collectors/`, `main.py`  
**Used to:** Gather CPU, memory, and process data using Python system interfaces.

### Modular & Extensible Software Design
**Where:** Entire folder structure (`collectors/`, `analyzers/`, `explainers/`)  
**Used to:** Isolate responsibilities, allowing easy extension with new analyzers or metrics.

### Real-Time Data Analysis
**Where:** `cli/watch.py`, `storage/` snapshot comparison  
**Used to:** Detect trends like rising CPU load or sustained memory pressure.

### Building CLI Tools
**Where:** `cli/`, `main.py`  
**Used to:** Provide live monitoring and interval-based analysis via the command line.

### Building a GUI
**Where:** `dashboard.py`  
**Used to:** Make system behavior accessible visually while preserving underlying reasoning.

### Translating Metrics into Meaningful Insights
**Where:** `explainers/`, health summaries  
**Used to:** Convert raw metrics into actionable, human-readable insights.

### Analyzer-Oriented Thinking
**Where:** Entire project  
**Used to:** Focus on *why* behavior is happening, not just *what* the numbers are.

---

## Project Structure

```text
os_atlas/
├── collectors/        # CPU, memory, and process data collection
├── analyzers/         # Starvation, deadlock-like analysis, health evaluation
├── explainers/        # Human-readable explanations of system behavior
├── storage/           # Snapshot persistence
├── cli/               # Command-line interface handlers
├── dashboard.py             # GUI entry point
└── main.py            # CLI entry point
