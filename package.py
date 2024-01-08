class Package:
    """class for packages on the grid
    """
    def __init__(self, params: list[str]):
        """creates new package

        Args:
            params (list[str]): package parameters
        """
        self.pickupLoc = (int(params[0]), params[1])
        self.dropoffLoc = int(params[2])
        self.pickupTime = (int(params[4]), params[5])
        self.dropoffMaxtime = int(params[6])

    def GetPickupLoc(self) -> (int, int):
        """return pickup location

        Returns:
            (int, int): location
        """
        return self.pickupLoc

    def GetDropoffLoc(self) -> (int, int):
        """return dropoff location

        Returns:
            (int, int): location
        """
        return self.dropoffLoc

    def GetPickupTime(self) -> int:
        """return pickup time

        Returns:
            int: time
        """
        return self.pickupTime

    def GetDropoffMaxtime(self) -> int:
        """return dropoff max time

        Returns:
            int: time
        """
        return self.dropoffMaxtime

    # def pickup(self):
    #     if self.status == "not picked up":
    #         self.status = "picked up"
    #         print("Package has been picked up.")
    #     else:
    #         print("Package is already picked up.")

    # def dropoff(self):
    #     if self.status == "picked up":
    #         self.status = "dropped off"
    #         print("Package has been dropped off.")
    #     elif self.status == "not picked up":
    #         print("Cannot drop off. Package has not been picked up yet.")
    #     else:
    #         print("Package has already been dropped off.")
