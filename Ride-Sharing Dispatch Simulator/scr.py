import heapq
import queue
import math
from datetime import datetime
from typing import List, Optional

# -----------------------------
# Data Classes
# -----------------------------

class Driver:
    def __init__(self, driver_id: int, location: tuple, rating: float):
        self.driver_id = driver_id
        self.location = location  # (x, y) coordinates
        self.rating = rating
        self.available = True

    def __repr__(self):
        return f"Driver(id={self.driver_id}, loc={self.location}, rating={self.rating})"

class Rider:
    def __init__(self, rider_id: int, location: tuple):
        self.rider_id = rider_id
        self.location = location  # (x, y) coordinates

    def __repr__(self):
        return f"Rider(id={self.rider_id}, loc={self.location})"

class RideMatch:
    def __init__(self, rider: Rider, driver: Driver, timestamp: datetime, distance: float):
        self.rider = rider
        self.driver = driver
        self.timestamp = timestamp
        self.distance = distance

    def __repr__(self):
        return (f"Ride(rider={self.rider.rider_id}, driver={self.driver.driver_id}, "
                f"dist={self.distance:.2f}, time={self.timestamp.strftime('%H:%M:%S')})")

# -----------------------------
# Core Simulator
# -----------------------------

class RideSharingSimulator:
    def __init__(self):
        # Queue for incoming ride requests (FIFO)
        self.request_queue = queue.Queue()
        # List of available drivers
        self.drivers: List[Driver] = []
        # History of completed rides
        self.ride_history: List[RideMatch] = []

    def add_driver(self, driver: Driver):
        """Add a driver to the system."""
        self.drivers.append(driver)

    def add_rider_request(self, rider: Rider):
        """Add a rider to the request queue."""
        self.request_queue.put(rider)

    def calculate_distance(self, loc1: tuple, loc2: tuple) -> float:
        """Calculate Euclidean distance between two points."""
        return math.sqrt((loc1[0] - loc2[0])**2 + (loc1[1] - loc2[1])**2)

    def dispatch_rides(self):
        """Process all pending ride requests."""
        while not self.request_queue.empty():
            rider = self.request_queue.get()
            match = self._find_best_driver(rider)
            if match:
                self.ride_history.append(match)
                print(f"✅ Matched: {match}")
            else:
                print(f"❌ No driver available for Rider {rider.rider_id}")

    def _find_best_driver(self, rider: Rider) -> Optional[RideMatch]:
        """Find the nearest available driver using a priority queue."""
        if not self.drivers:
            return None

        # Min-heap (priority queue) based on (distance, -rating, driver_id)
        pq = []
        for driver in self.drivers:
            if not driver.available:
                continue
            dist = self.calculate_distance(rider.location, driver.location)
            # Use -rating because heapq is a min-heap; we want higher rating first
            heapq.heappush(pq, (dist, -driver.rating, driver.driver_id, driver))

        if pq:
            dist, neg_rating, driver_id, driver = heapq.heappop(pq)
            driver.available = False  # Assign driver
            return RideMatch(rider, driver, datetime.now(), dist)
        return None

    def complete_ride(self, driver_id: int):
        """Mark a driver as available after ride completion."""
        for driver in self.drivers:
            if driver.driver_id == driver_id:
                driver.available = True
                print(f"🔁 Driver {driver_id} is now available.")
                break

    def show_ride_history(self):
        """Display all completed rides."""
        print("\n📋 Ride History:")
        if not self.ride_history:
            print("No rides yet.")
        for ride in self.ride_history:
            print(ride)

    def show_available_drivers(self):
        """Display currently available drivers."""
        available = [d for d in self.drivers if d.available]
        print(f"\n🟢 Available Drivers: {available}")

# -----------------------------
# Example Usage
# -----------------------------

def main():
    simulator = RideSharingSimulator()

    # Add drivers: (id, (x, y), rating)
    simulator.add_driver(Driver(1, (0, 0), 4.8))
    simulator.add_driver(Driver(2, (3, 4), 4.2))
    simulator.add_driver(Driver(3, (1, 1), 4.9))
    simulator.add_driver(Driver(4, (10, 10), 4.5))  # Far away

    # Add riders
    simulator.add_rider_request(Rider(101, (0, 1)))   # Close to Driver 1 and 3
    simulator.add_rider_request(Rider(102, (2, 2)))   # Closer to Driver 3
    simulator.add_rider_request(Rider(103, (0, 0)))   # Right at Driver 1
    simulator.add_rider_request(Rider(104, (8, 9)))   # Close to Driver 4

    print("🚀 Starting ride dispatch...\n")
    simulator.dispatch_rides()

    # Show status
    simulator.show_ride_history()
    simulator.show_available_drivers()

    # Complete a ride and free up driver
    print("\n--- Completing ride for Driver 1 ---")
    simulator.complete_ride(1)
    simulator.show_available_drivers()

if __name__ == "__main__":
    main()
