import csv
from hash import ChainedHashTable

class Package:
    # constructor
    def __init__(self, package_id, address, city, state, zip, delivery_deadline, weight, notes, status, depart_time, deliver_time):
        self.deliver_time = deliver_time
        self.depart_time = depart_time
        self.notes = notes
        self.package_id = package_id
        self.address = address
        self.city = city
        self.state = state
        self.zip = zip
        self.delivery_deadline = delivery_deadline
        self.weight = weight
        self.status = status


    def __str__ (self):
        return "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s" % (self.package_id, self.address, self.city, self.state, self.zip,
                                                      self.delivery_deadline, self.weight, self.status, self.notes, self.depart_time, self.deliver_time)



    def status_update(self, datetime):
        if (datetime < self.depart_time):
            self.status = "at the hub"
        elif (datetime > self.deliver_time):
            self.status = f"Delivered at {self.deliver_time}"
        else:
            self.status = "en route"
