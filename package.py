from datetime import timedelta


class Package:
    # Initializes all the data the Package object needs created.
    # Time Complexity O(1)
    # Space Complexity O(1)
    def __init__(self, package_id, address, city, state, zip_code, deadline, weight, notes):
        self.package_id = package_id
        self.original_address = address
        self.updated_address = None
        self.updated_zip = None
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
        self.delivery_time = None

        # "Special" method that tells the program how to print the object.
    # Time Complexity O(1)
    # Space Complexity O(1)
    def __str__(self):
        return (f"Package {self.package_id}: {self.address}, {self.city}, {self.state} {self.zip_code} | "
                f"Deadline: {self.deadline}, Weight: {self.weight}, Notes: {self.notes} | "
                f"Status: {self.status}, Delivery Time: {self.delivery_time}, Truck ID: {self.truck_id}")

    # Updates the status of a package and optionally records the delivery time if the package has been delivered.
    # Time Complexity O(1)
    # Space Complexity O(1)
    def update_status(self, new_status, time=None):
        self.status = new_status
        if new_status == "Delivered":
            self.delivery_time = time

    def get_current_address(self, current_time):
        if self.package_id == 9 and current_time >= timedelta(hours=10, minutes=20):
            return "410 S State St"
        return self.address


    def print_status(self, user_time):
        temp_delivery_time = ''

        if user_time > self.delivery_time:
            temp_status = "Delivered"
            temp_delivery_time = self.delivery_time
        elif user_time < self.departure_time:
            temp_status = "At the Hub"
        else:
            temp_status = "En route"

    #
    #
        address = self.original_address
        zip_code = self.zip_code

        if self.package_id == 9:
            if user_time >= timedelta(hours=10, minutes=20):
                address = self.updated_address
                zip_code = self.updated_zip

        return (
            f"{'Package ID:':<15} {self.package_id:<20} {'Truck:':<10} {self.truck_id}\n"
            f"{'Address:':<15} {address:<20} {'City:':<10} {self.city}\n"
            f"{'Zip Code:':<15} {zip_code:<20} {'Deadline:':<10} {self.deadline}\n"
            f"{'Weight:':<15} {str(self.weight) + ' lbs':<20} {'Status:':<10} {temp_status}\n"
            f"{'Delivery Time:':<15} {str(temp_delivery_time):<20} {'Notes:':<10} {self.notes}\n"
            f"{'-' * 80}"
        )


        # return (f"Package {self.package_id} (Truck {self.truck_id}): {address}, {self.city}, {zip_code} | "
        #         f"Deadline: {self.deadline}, Weight: {self.weight}, Notes: {self.notes} | "
        #         f"Status: {temp_status}, Delivery Time: {temp_delivery_time}")



