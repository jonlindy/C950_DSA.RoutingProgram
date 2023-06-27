import csv
from hash import ChainedHashTable

class Package:
    # constructor
    def __init__(self, package_id, address, city, state, zip, delivery_deadline, weight, notes, status):
        self.notes = notes
        self.package_id = package_id
        self.address = address
        self.city = city
        self.state = state
        self.zip = zip
        self.delivery_deadline = delivery_deadline
        self.weight = weight
        self.status = status

# method to load package data into hashtable from CSV
def load_packagedata():
    with open("WGUPS_package.csv", 'r') as infile:
        reader = csv.reader(infile, delimiter=",")

        # read each line into new package object
        for row in reader:
            package_id = row[0]
            address = row[1]
            city = row[2]
            state = row[3]
            zip = row[4]
            delivery_deadline = row[5]
            weight = row[6]
            notes = row[7]
            status = 'Processing'

            package = Package(package_id, address, city, state, zip, delivery_deadline, weight, notes, status)

            packageHT.insert(package_id, package)

packageHT = ChainedHashTable()

