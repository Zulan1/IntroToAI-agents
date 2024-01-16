from type_aliases import Node

class Package:
    """class for packages on the grid
    """
    def __init__(self, params: list[str]):
        """creates new package

        Args:
            params (list[str]): package parameters
        """
        self._pickupLoc = (int(params[0]), int(params[1]))
        self._pickupTime = int(params[2])
        self._dropoffLoc = (int(params[4]), int(params[5]))
        self._dropoffMaxtime = int(params[6])

    @property
    def pickupLoc(self) -> Node:
        """return pickup location

        Returns:
            Node: location
        """
        return self._pickupLoc

    @property
    def dropoffLoc(self) -> Node:
        """return dropoff location

        Returns:
            Node: location
        """
        return self._dropoffLoc

    @property
    def pickupTime(self) -> int:
        """return pickup time

        Returns:
            int: time
        """
        return self._pickupTime

    @property
    def dropoffMaxtime(self) -> int:
        """return dropoff max time

        Returns:
            int: time
        """
        return self._dropoffMaxtime
