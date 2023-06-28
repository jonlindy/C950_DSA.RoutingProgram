class Truck:
    def __init__(self, truckID, capacity, start, driverID):
        self.driverID = driverID
        self.start = start
        self.capacity = capacity
        self.truckID = truckID
        
        
class Driver:
    def __init__(self, driverID, truckID):
        self.truckID = truckID
        self.driverID = driverID