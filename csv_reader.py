import csv
from hash_map import HashTable
from package import Package

#Function to import addresses from csv file to my hashtable
#Time Complexity O(n)
#Space Complexity O(n)
def import_addresses(filename):
    addresses = []
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            address = row[2].strip()
            addresses.append(address)
    return addresses

#Creates my distance matrix
#Time Complexity O(n^2)
#Space Complexity O(n^2)
def import_distances(filename):
    distances = []
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            distance_row = [float(val) if val else 0.0 for val in row]
            distances.append(distance_row)
    return distances

#Function to import packages from csv file to my hashtable
#Time Complexity O(n)
#Space Complexity O(n)
def import_packages(filename):
    hash_table = HashTable() #local variable
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            package_id = int(row[0])
            package = Package(
                package_id=package_id,
                address=row[1],
                city=row[2],
                state=row[3],
                zip_code=row[4],
                deadline=row[5],
                weight=row[6],
                notes=row[7]
            )
            hash_table.insert(package_id, package)
    return hash_table

#Used to get the distance between two addresses
#Time Complexity O(n)
#Space Complexity O(1)
def get_distance(start_address, end_address, address_list, distance_matrix):
    try:
        start_index = address_list.index(start_address)
        end_index = address_list.index(end_address)
    except ValueError:
        raise Exception("One of the addresses was not found in the address list.")

    # Use symmetry
    if start_index > end_index:
        return distance_matrix[start_index][end_index]
    else:
        return distance_matrix[end_index][start_index]

