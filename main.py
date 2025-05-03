                                #Author: Brittany McGuire
                                #Title: WGUPS Routing program
import datetime
from truck import Truck
from csv_reader import import_addresses, import_distances, import_packages, get_distance


print("Welcome to WGUPS Routing!\n")
# print("Starting program.\n")
# print("Delivering packages...\n")

#The overall program has a Space and Time complexity of O(n^2)

# Load data
address_list = import_addresses("data/WGUPS_addresses.csv")
distance_matrix = import_distances("data/WGUPS_distances.csv") #Time and space complexity O(n^2)
package_table = import_packages("data/WGUPS_packages.csv")

# This function prints a message showing what time the truck left the hub to start deliveries.
# Uses truck.truck_id (the truck number) and truck.depart_time (when it left).
# It also sets the current location/starting location to hub address.
# 'pending' stores list of all the actual Package objects.
#Time Complexity O(n^2)
#Space Complexity O(n)
def nearest_neighbor_algorithm(truck):
    # print(f"\nTruck {truck.truck_id} left WGU at {truck.depart_time}.\n")
    current_location = "4001 South 700 East"
    pending = [package_table.lookup(package_id) for package_id in truck.packages]
    for pkg in pending:
        pkg.departure_time = truck.depart_time
    truck.packages.clear()

    # This starts a loop that continues until all packages in pending are delivered.
    while pending:
        next_pkg = None #will hold the package that should be delivered next.
        min_distance = float("inf") #min_distance is set to infinity at the start. This is used to find the package that is closest to the current location.
        # checks each package still pending and calculates the distance from the current location to that package’s address.
        # get_distance() is a function that finds that distance using your address list and distance matrix.
        for pkg in pending:
            pkg.address = pkg.get_current_address(truck.time)
            dist = get_distance(current_location, pkg.address, address_list, distance_matrix)
            # If the distance to the current package is less than the minimum distance found so far, this becomes the next package to deliver.
            if dist < min_distance:
                min_distance = dist
                next_pkg = pkg

        # Increases the truck’s current time by how long it took to travel the distance.
        # This uses the truck’s speed (in miles per hour) to calculate travel time.
        # Adds that travel distance to the truck’s total mileage.
        # Updates the truck’s current address to the destination it just arrived at.
        truck.time += datetime.timedelta(hours=min_distance / truck.speed)
        truck.mileage += min_distance
        truck.address = next_pkg.address

        # Updates the package
        # Used the helper to mark delivered
        next_pkg.delivery_time = truck.time
        next_pkg.truck_id = truck.truck_id
        next_pkg.update_status("Delivered", truck.time)
        package_table.insert(next_pkg.package_id, next_pkg)
        truck.end_time = truck.time


        # print(f"Truck {truck.truck_id} delivered package {next_pkg.package_id} to {next_pkg.address}, {next_pkg.state}, {next_pkg.zip_code}  at {truck.time}")
        truck.packages.append(next_pkg.package_id)

        # Removes the delivered package from pending
        # Updates the current location so the next delivery is calculated from here
        pending.remove(next_pkg)
        current_location = next_pkg.address

    # Return to the hub
    return_distance = get_distance(current_location, "4001 South 700 East", address_list, distance_matrix)
    truck.time += datetime.timedelta(hours=return_distance / truck.speed)
    truck.mileage += return_distance
    # print(f"\nTruck {truck.truck_id} returned to WGU at {truck.time}.\n")
    # print(f"Total distance traveled for truck {truck.truck_id} was {round(truck.mileage, 1)} miles.\n")

# Set up trucks
#Time Complexity O(n)
#Space Complexity O(n)
truck1 = Truck(1, ["15", "13", "14", "16", "1", "19", "20", "23", "24", "27", "29", "31", "34", "40"], "4001 South 700 East", datetime.timedelta(hours=8))
truck2 = Truck(2, ["3 ", "6", "18", "25", "26", "28", "30", "32", "33", "35", "36", "37", "38", "39"], "4001 South 700 East", datetime.timedelta(hours=9, minutes=5))
truck3 = Truck(3, ["2", "4", "5", "7", "8", "9", "10", "11", "12", "17", "21", "22"], "4001 South 700 East", None)


#Checks package ID on the truck, looks up package info, and adds the confirmed package ID to the truck’s delivery list.
#Time Complexity O(n)
#Space Complexity O(n)
for pkg_id in truck1.package_ids:
    pkg = package_table.lookup(int(pkg_id))
    truck1.packages.append(pkg.package_id)

for pkg_id in truck2.package_ids:
    pkg = package_table.lookup(int(pkg_id))
    truck2.packages.append(pkg.package_id)

for pkg_id in truck3.package_ids:
    pkg = package_table.lookup(int(pkg_id))
    truck3.packages.append(pkg.package_id)

# Deliver packages using Nearest Neighbor
nearest_neighbor_algorithm(truck1)
nearest_neighbor_algorithm(truck2)
truck3.depart_time = min(truck1.time, truck2.time) #truck 3 does not leave until one of the trucks get back
truck3.time = truck3.depart_time
package_9 = package_table.lookup(9)
package_9.updated_address = "410 S State St"
package_9.updated_zip = "84111"
nearest_neighbor_algorithm(truck3)

total_miles = round(truck1.mileage + truck2.mileage + truck3.mileage, 1)
print("All packages have been delivered!\n")
print(f"Total mileage traveled by all trucks: {total_miles} miles\n")


# Print status by time. Determines the package status as well as truck number at given time
#Time Complexity O(n)
#Space Complexity O(1)
def print_package_status_at_time(requested_time):
    result = ""
    for package_id in range(1, 41):
        pkg = package_table.lookup(package_id)
        print(pkg.print_status(requested_time))



# Main user interaction

total_miles = truck1.mileage + truck2.mileage + truck3.mileage

while True:
    print("="  * 40)

    print("Please select an option below:")
    print()
    print("1." "Status of all packages")
    print("2." "Status of a package at a specific time")
    print("3." "Status of all packages at a specific time")
    print("4." "Exit")
    try:
        option = int(input("Enter your choice: "))
    except ValueError:
        print("Invalid input. Please enter a number from 1 to 4.\n")
        continue
    if option == 1: #Option 1 to display all package data
        for package_id in range(1, 41):
            pkg = package_table.lookup(package_id)
            user_time = datetime.timedelta(hours=23, minutes=59)
            print(pkg.print_status(user_time)) #prints all package info
        print(f"\nTotal mileage traveled by all trucks: {total_miles:.1f} miles\n")
    elif option == 2: #Option 2 to see status of a package at specific time
        try:
            user_inp = input("Enter the package id: ")
            response = input("Enter a time to view package status (HH:MM): ")
            # try:
            (h, m) = map(int, response.strip().split(":"))
            user_time = datetime.timedelta(hours=h, minutes=m)
            package = package_table.lookup(int(user_inp))
            print(package.print_status(user_time))
        except:
            print("Invalid input. Try again.\n")

    elif option == 3: #Option 3 to see all packages at specific time
        response = input("Enter a time to view package status (HH:MM): ")
        try:
            (h, m) = map(int, response.strip().split(":"))
            user_time = datetime.timedelta(hours=h, minutes=m)
            print(f"\n--- Package Status at {response} ---\n")
            print_package_status_at_time(user_time)
            #print(f"\nTotal mileage traveled by all trucks: {total_miles:.1f} miles\n")
            print(f"\nMileage at {response}:")
            print(f"Truck 1: {truck1.mileage_at_time(user_time, package_table, address_list, distance_matrix)} miles")
            print(f"Truck 2: {truck2.mileage_at_time(user_time, package_table, address_list, distance_matrix)} miles")
            print(f"Truck 3: {truck3.mileage_at_time(user_time, package_table, address_list, distance_matrix)} miles")

            total = (
                    truck1.mileage_at_time(user_time, package_table, address_list, distance_matrix)
                    + truck2.mileage_at_time(user_time, package_table, address_list, distance_matrix)
                    + truck3.mileage_at_time(user_time, package_table, address_list, distance_matrix)
            )
            print(f"Total: {round(total, 2)} miles\n")

        except:
            print("Invalid time format.")
        #Calculate the mileage of each truck at a given time


    elif option == 4:
        break