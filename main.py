                                #Author: Brittany McGuire
                                #Student ID#: 011067208
                                #Title: WGUPS Routing program
import datetime
from truck import Truck
from csv_reader import import_addresses, import_distances, import_packages, get_distance


print("Welcome to WGUPS Routing!\n")
print("Starting program.\n")
print("Delivering packages...\n")

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
    print(f"\nTruck {truck.truck_id} left WGU at {truck.depart_time}.\n")
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
        next_pkg.update_status("Delivered", truck.time)
        package_table.insert(next_pkg.package_id, next_pkg)
        truck.end_time = truck.time

        print(f"Truck {truck.truck_id} delivered package {next_pkg.package_id} to {next_pkg.address} at {truck.time}")
        truck.packages.append(next_pkg.package_id)
        # Removes the delivered package from pending
        # Updates the current location so the next delivery is calculated from here
        pending.remove(next_pkg)
        current_location = next_pkg.address

    # Return to the hub
    return_distance = get_distance(current_location, "4001 South 700 East", address_list, distance_matrix)
    truck.time += datetime.timedelta(hours=return_distance / truck.speed)
    truck.mileage += return_distance
    print(f"\nTruck {truck.truck_id} returned to WGU at {truck.time}.\n")
    print(f"Total distance traveled for truck {truck.truck_id} was {round(truck.mileage, 1)} miles.\n")




# Set up trucks
#Time Complexity O(n)
#Space Complexity O(n)
truck1 = Truck(1, ["15", "13", "14", "16", "1", "19", "20", "29", "31", "34", "40"], "4001 South 700 East", datetime.timedelta(hours=8))
truck2 = Truck(2, ["3 ", "6", "25", "26", "28", "30", "32", "33", "35", "36", "37", "38", "39"], "4001 South 700 East", datetime.timedelta(hours=9, minutes=5))
truck3 = Truck(3, ["2", "4", "5", "7", "8", "9", "10", "11", "12", "17", "18", "21", "22", "23", "24", "27"], "4001 South 700 East", None)


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
#truck 3 does not leave until one of the trucks get back
truck3.depart_time = min(truck1.time, truck2.time)
truck3.time = truck3.depart_time
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
        if requested_time < pkg.departure_time:
            status = "At hub"
        elif requested_time < pkg.delivery_time:
            status = "En route"
        else:
            status = f"Delivered at {pkg.delivery_time}"
        if package_id in truck1.packages:
            truck_number = 1
        elif package_id in truck2.packages:
            truck_number = 2
        elif package_id in truck3.packages:
            truck_number = 3
        else:
            truck_number = "Unknown"
        result += f"Package {package_id} (Truck {truck_number}): {status}\n"
    return result


# Main user interaction

total_miles = truck1.mileage + truck2.mileage + truck3.mileage

while True:
    print("="  * 40)

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
    if option == 1:
        for package_id in range(1, 41):
            pkg = package_table.lookup(package_id)
            print(pkg) #prints all package info
        print(f"\nTotal mileage traveled by all trucks: {total_miles:.1f} miles\n")
    elif option == 2:
        user_inp = input("Enter the package id: ")
        response = input("Enter a time to view package status (HH:MM): ")
        try:
            (h, m) = map(int, response.strip().split(":"))
            user_time = datetime.timedelta(hours=h, minutes=m)
            package = package_table.lookup(int(user_inp))

            #Compares input to package times and gives the status of the package
            if user_time < package.departure_time:
                status = "At hub"
            elif user_time < package.delivery_time:
                status = "En route"
            else:
                status = f"Delivered at {package.delivery_time}"

            #Returns what truck the package is in/scheduled to be in
            if package.package_id in truck1.packages:
                truck_id = 1
            elif package.package_id in truck2.packages:
                truck_id = 2
            elif package.package_id in truck3.packages:
                truck_id = 3
            else:
                truck_id = "Unknown"

            print()
            print(f"Package ID: {package.package_id}")
            if package.package_id == 9:
                if user_time < datetime.timedelta(hours=10, minutes=20):
                    print(f"Address: {package.original_address}")
                else:
                    print(f"Address: {package.updated_address}")
            else:
                print(f"Address: {package.address}")
            print(f"Deadline: {package.deadline}")
            print(f"Status: {status}\n")
            print(f"Truck ID: {truck_id}\n")
        except Exception as e:
            print(f"Error: {str(e)}")
            print("Invalid time format.")
    elif option == 3:
        response = input("Enter a time to view package status (HH:MM): ")
        try:
            (h, m) = map(int, response.strip().split(":"))
            user_time = datetime.timedelta(hours=h, minutes=m)
            print(f"\n--- Package Status at {response} ---\n")
            print(print_package_status_at_time(user_time))
            #print(f"\nTotal mileage traveled by all trucks: {total_miles:.1f} miles\n")
        except:
            print("Invalid time format.")
        #Calculate the mileage of each truck at a given time
        mileage1 = truck1.mileage if user_time >= truck1.end_time else truck1.mileage_at_time(user_time, package_table, address_list, distance_matrix)
        mileage2 = truck2.mileage if user_time >= truck2.end_time else truck2.mileage_at_time(user_time, package_table, address_list, distance_matrix)
        mileage3 = truck3.mileage if user_time >= truck3.end_time else truck3.mileage_at_time(user_time, package_table, address_list, distance_matrix)
        total_mileage = mileage1 + mileage2 + mileage3

        print(f"\nMileage at {str(user_time)}:")
        print(f"Truck 1: {round(mileage1,2)} miles")
        print(f"Truck 2: {round(mileage2,2)} miles")
        print(f"Truck 3: {round(mileage3, 2)} miles")
        print(f"Total: {round(total_mileage, 2)} miles\n")

    elif option == 4:
        break