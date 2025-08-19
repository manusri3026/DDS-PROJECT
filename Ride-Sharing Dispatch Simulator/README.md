
# Ride-Sharing Dispatch Simulator
## 📌 Overview

A command-line ride-sharing dispatch system that matches riders to drivers based on proximity (distance) and driver rating. Designed as a Data Structures project using queues for incoming ride requests and priority queues (min-heap) for intelligent driver matching.

---
## 🛠 Features
---
- Assign drivers to riders based on nearest distance first
- Use driver ratings as a tiebreaker for fairness and quality
- Maintain a FIFO queue of incoming rider requests
- Use a priority queue (heap) to find the best available driver
- Track ride history with timestamps and distances
- Mark drivers as available/unavailable after rides
- Simulate ride completion to return drivers to the pool
- Save and extend for real-world use (GPS coordinates, ETA, etc.)

---

## 📂 Data Structures Used
  - **Array of Drivers**-> List
  - **FIFO processing**-> queue.Queue()
  - **Priority queue**-> heapy

---

## 🚀 How to Run
```bash
# Clone the repository
git clone https://github.com/your-username/ride-sharing-simulator.git
cd ride-sharing-simulator/src

# Run the simulator
python ride_sharing_simulator.py
