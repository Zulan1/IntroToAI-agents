from __future__ import annotations
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
        self._dropOffMaxTime = int(params[6])

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
    def dropOffMaxTime(self) -> int:
        """return dropoff max time

        Returns:
            int: time
        """
        return self._dropOffMaxTime
    
    def __eq__(self, other: Package) -> bool:
        """checks if two packages are equal

        Args:
            other (Package): other package

        Returns:
            bool: True if equal, False otherwise
        """
        return all([self.pickupLoc == other.pickupLoc,
                    self.dropoffLoc == other.dropoffLoc,
                    self.pickupTime == other.pickupTime,
                    self.dropOffMaxTime == other.dropOffMaxTime])
