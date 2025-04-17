from csv_reader import get_distance
import datetime

# Initializes all the data the Package object needs created.
# Time Complexity O(1)
# Space Complexity O(1)
class Truck:
    def __init__(self, truck_id, package_ids, address='4001 South 700 East', depart_time=None, capacity=16, speed=18):
        self.truck_id = truck_id
        self.package_ids = package_ids  # store string IDs initially
        self.capacity = capacity
        self.speed = speed
        self.load = 0
        self.packages = []
        self.mileage = 0.0
        self.address = address
        self.depart_time = depart_time
        self.time = depart_time
        self.end_time = None

    # "Special" method that tells the program how to print the object.
    # Time Complexity O(1)
    # Space Complexity O(1)
    def __str__(self):
        return (f"Truck at {self.address} | Departed at {self.depart_time} | "
                f"Packages: {len(self.packages)} | Mileage: {self.mileage:.2f}")

    # Function to calculate mileage of trucks at specific time at option 3.
    # Time Complexity O(n^2)
    # Space Complexity O(1)
    def mileage_at_time(self, requested_time, package_table, address_list, distance_matrix):
        total = 0
        current_time = self.depart_time
        current_location = "4001 South 700 East"

        for pkg_id in self.packages:
            pkg = package_table.lookup(pkg_id)
            travel_distance = get_distance(current_location, pkg.address, address_list, distance_matrix)
            travel_time = datetime.timedelta(hours=travel_distance / self.speed)

            if current_time + travel_time <= requested_time:
                total += travel_distance
                current_time += travel_time
                current_location = pkg.address
            else:
                break

        return round(total, 2)
