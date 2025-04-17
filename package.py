class Package:
    # Initializes all the data the Package object needs created.
    # Time Complexity O(1)
    # Space Complexity O(1)
    def __init__(self, package_id, address, city, state, zip_code, deadline, weight, notes):
        self.package_id = package_id
        self.original_address = address
        self.updated_address = '410 S State St'
        self.address = address
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.deadline = deadline
        self.weight = weight
        self.notes = notes
        self.truck_id = None
        self.status = 'At Hub'
        self.departure_time = None

    # "Special" method that tells the program how to print the object.
    # Time Complexity O(1)
    # Space Complexity O(1)
    def __str__(self):
        return (f"Package {self.package_id}: {self.address}, {self.city}, {self.state} {self.zip_code} | "
                f"Deadline: {self.deadline}, Weight: {self.weight}, Notes: {self.notes} | "
                f"Status: {self.status}, Delivery Time: {self.delivery_time}")

    # Updates the status of a package and optionally records the delivery time if the package has been delivered.
    # Time Complexity O(1)
    # Space Complexity O(1)
    def update_status(self, new_status, time=None):
        self.status = new_status
        if new_status == "Delivered":
            self.delivery_time = time


    # def print_status(self, user_time, truck1, truck2, truck3):
    #     temp_delivery_time = ''
    #
    #     if user_time > self.delivery_time:
    #         temp_status = "Delivered"
    #         temp_delivery_time = self.delivery_time
    #     elif user_time < self.departure_time:
    #         temp_status = "At the Hub"
    #     else:
    #         temp_status = "En route"
    #     if self.package_id in truck1.packages:
    #         truck_number = 1
    #     elif self.package_id in truck2.packages:
    #         truck_number = 2
    #     elif self.package_id in truck3.packages:
    #         truck_number = 3
    #     else:
    #         truck_number = "Unknown"
    #
    #     return (f"Package {self.package_id} (Truck {truck_number}): {self.address}, {self.city}, {self.state} {self.zip_code} | "
    #             f"Deadline: {self.deadline}, Weight: {self.weight}, Notes: {self.notes} | "
    #             f"Status: {temp_status}, Delivery Time: {temp_delivery_time}")



