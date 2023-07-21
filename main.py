import datetime

import package
from hash import *
from package import *
from truck import Truck

# method to load package data into hashtable from CSV
def load_packagedata(ht):
    with open("WGUPS_package.csv", 'r') as infile:
        reader = csv.reader(infile, delimiter=",")
        # read each line into new package object
        for row in reader:
            package_id = int(row[0])
            address = row[1]
            city = row[2]
            state = row[3]
            zip = row[4]
            delivery_deadline = row[5]
            weight = row[6]
            notes = row[7]
            status = 'At Hub'
            depart_time = None
            deliver_time = None

            package_to_load = Package(package_id, address, city, state, zip, delivery_deadline, weight, notes, status, depart_time, deliver_time)

            ht.insert(package_id, package_to_load)

# method to create key:value dictionary from address.csv
def create_address_dict():
    with open("address.csv", 'r', encoding='utf-8-sig') as infile:
            data = csv.reader(infile, delimiter=",")
            dictio = {}
            for row in data:
                key = row[0]
                value = int(row[1])
                dictio[key] = value

            return dictio
# method to create list of lists from distance.csv
def create_distance_matrix():
    with open("distance.csv", 'r', encoding='utf-8-sig') as infile:
            data = csv.reader(infile, delimiter=",")
            matrix = []
            for row in data:
                rowlist = []
                for col in row:
                    rowlist.append(col)
                matrix.append(rowlist)
            return matrix

# method to get distance between two locations using distance matrix
def find_distance(loc1, loc2, matrix):
    if not (matrix[loc1][loc2] == ''):
        return float(matrix[loc1][loc2])
    else:
        return float(matrix[loc2][loc1])

# method implements SpeedyAlgo. Delivers all packages on truck and returns truck to hub.
def delivery(truck):
    # split package list into priority/normal deadlines
    priority_packages = []
    normal_packages = []
    for pkg in truck.packages:
        this_package = packageHT.search(pkg)
        this_package.status = 'en route'
        this_package.depart_time = truck.depart_time
        if this_package.delivery_deadline == "EOD":
            normal_packages.append(this_package)
        else:
            priority_packages.append(this_package)
    truck.packages.clear()

    # loop through priority package list, adding nearest package until list is empty
    while len(priority_packages) > 0:
        next_adrs = 30
        next_pkg = None
        for pkg in priority_packages:
            if find_distance(truck.location, address_dict[pkg.address], distance_matrix) <= next_adrs:
                next_adrs = find_distance(truck.location, address_dict[pkg.address], distance_matrix)
                next_pkg = pkg
        # add nearest package to truck package list
        truck.packages.append(next_pkg)
        # remove package from priority package list
        priority_packages.remove(next_pkg)
        # add mileage to truck
        truck.mileage += next_adrs
        # update truck location
        truck.location = address_dict[next_pkg.address]
        # update truck time
        truck.current_time += datetime.timedelta(hours= next_adrs / 18)
        # timestamp for package delivery
        packageHT.search(next_pkg.package_id).deliver_time = truck.current_time
        packageHT.search(next_pkg.package_id).status = f"Delivered: {truck.current_time}"
        #print(f" Truck {truck.truckID} time: {truck.current_time}")

    while len(normal_packages) > 0:
        next_adrs = 30
        next_pkg = None
        for pkg in normal_packages:
            if find_distance(truck.location, address_dict[pkg.address], distance_matrix) <= next_adrs:
                next_adrs = find_distance(truck.location, address_dict[pkg.address], distance_matrix)
                next_pkg = pkg
        # add nearest package to truck package list
        truck.packages.append(next_pkg)
        # remove package from priority package list
        normal_packages.remove(next_pkg)
        # add mileage to truck
        truck.mileage += next_adrs
        # update truck location
        truck.location = address_dict[next_pkg.address]
        # update truck time
        truck.current_time += datetime.timedelta(hours=next_adrs / 18)
        # timestamp for package delivery
        packageHT.search(next_pkg.package_id).deliver_time = truck.current_time
        packageHT.search(next_pkg.package_id).status = f"Delivered: {truck.current_time}"
        #print(f" Truck {truck.truckID} time: {truck.current_time}")

    #send truck back to hub, add mileage and time
    truck.mileage += find_distance(truck.location, 1, distance_matrix)
    truck.current_time += datetime.timedelta(hours=find_distance(truck.location, 1, distance_matrix) /18)
    truck.location = 1

# create package hash table - load packages into hash table - create address dictionary - create distance matrix
packageHT = ChainedHashTable()
load_packagedata(packageHT)
address_dict = create_address_dict()
distance_matrix = create_distance_matrix()

# load trucks with packages
truck1 = Truck(1, 16, datetime.timedelta(hours=8), datetime.timedelta(hours=8),0,18,0,[1,4,5,13,14,15,16,19,20,21,29,30,31,34,39,40])
truck2 = Truck(2, 16, datetime.timedelta(hours=9, minutes=5), datetime.timedelta(hours=9, minutes=5),0,18,0,[2,3,6,7,10,11,12,17,18,25,28,32,35,36,37,38])
truck3 = Truck(3, 16, datetime.timedelta(hours=10, minutes=20), datetime.timedelta(hours=10, minutes=20),0,18,0,[8,9,22,23,24,26,27,33])

# send out truck1 @ 08:00 and truck2 @ 09:05
delivery(truck1)
delivery(truck2)
# update truck3 depart_time to truck1 current_time. truck3 can't leave until truck1 is back at hub.
truck3.depart_time = truck1.current_time
# update wrong address
packageHT.search(9).address = '410 S State St'
delivery(truck3)

total_mileage = (truck1.mileage + truck2.mileage + truck3.mileage)

# CLI for WGUPS
class Main:
    print(" -- Western Governors University Parcel Service --")
    # print total mileage
    print(f"Total mileage of route: {total_mileage}")
    # user is prompted to start program by entering "status"

    while True:
        start_input = input("Please type 'status' to view route progress --> ")
        # program continues when status is entered
        try:
            if start_input == 'status':
                break
        # if invalid input, prompts user again to type 'status'
        except ValueError:
            print("Invalid input. Please type 'status' to continue. --> ")
    while True:
        # user prompted for a time
        time_input = input("Please enter a time to check package status using format:'HH:MM' --> ")
        try:
            #if input is valid, proceed to ID input
            (hour,min) = time_input.split(':')
            time_in_form = datetime.timedelta(hours=int(hour),minutes=int(min))
            if type(time_in_form) == datetime.timedelta:
                break
        # if invalid input, loops back to prompt user for time
        except ValueError:
            print("Invalid input. Please enter time in 'HH:MM' format. --> ")
    while True:
        # user prompted for package ID
        package_input = input("To view status of a single package, type 'single' "
                              "\n Or type 'all' to view status of all packages --> ")
        try:
            #if input is valid, get package, update status with time, print status
            if package_input == 'single':
                ID_input = input("Please enter a valid package ID (1-40) --> ")
                if int(ID_input) in range(1, 41):
                    # print package data with status at given time
                    package = packageHT.search(int(ID_input))
                    package.status_update(time_in_form)
                    print(f"Package {ID_input} status: {package.status}")
                    break
            elif package_input == 'all':
                for pkg in range(1,41):
                    package = packageHT.search(pkg)
                    package.status_update(time_in_form)
                    print(f"Package {pkg} status: {package.status}")
        # if invalid input, loops back to prompt user for ID
        except ValueError:
            print("Invalid input.")



























