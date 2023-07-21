class Truck:
    def __init__(self, truckID, capacity, depart_time, current_time, location, speed, mileage, packages):

        self.current_time = current_time
        self.depart_time = depart_time
        self.packages = packages
        self.mileage = mileage
        self.speed = speed
        self.location = location
        self.capacity = capacity
        self.truckID = truckID

    def __str__(self):
        return "%s, %s, %s, %s, %s, %s, %s, %s" % (
        self.depart_time, self.current_time, self.packages, self.mileage, self.speed, self.location,
        self.capacity, self.truckID)
