
# Python imports
from typing import List
from typing import Set

# Package imports
from .sign import sign

class DIRECTIONS():

    # The QRS directions in terms of XYZ
    Q = (0, 1, -1)
    R = (1, 0, -1)
    S = (-1, 1, 0)

    # Map the maximum xyz index to the two QRS vectors which need to be used.
    # Each element of the map looks like this
        #   ( ( QRSIndex1, QRSVector1, PositiveDirection1 ) , ( QRSIndex2, QRSVector2, PositiveDirection2 ) )
    MAX_MAP = {
        0 : ((1, R,  1), (2, S, -1)),
        1 : ((0, Q,  1), (2, S,  1)),
        2 : ((0, Q, -1), (1, R, -1))
    }


class HexLocation():
    '''
    Class for storing hexgrid locations
    '''

    @staticmethod
    def createFromXY(x: int, y: int) -> "HexLocation":
        '''
        Create a hex location from an x and y value.
        '''

        # Create a new hex location
        hexLocation = HexLocation()

        # First determine the x, y, and z values
        hexLocation.xyz[0] = x
        hexLocation.xyz[1] = y
        hexLocation.xyz[2] = -(x + y)

        # Then determine the q, r, and s values
        hexLocation.setQRS()

        return hexLocation
    
    @staticmethod
    def createFromQRS(q: int, r: int, s: int) -> "HexLocation":
        '''
        Create a hex location from a given q, r, and s value. 
        These values are restricted such that at least one == 0
        '''

        # Create new HexLocation
        hexLocation = HexLocation()

        # Just copy over the qrs values
        hexLocation.qrs[0] = q
        hexLocation.qrs[1] = r
        hexLocation.qrs[2] = s

        # Set the xyz values from the qrs values
        hexLocation.setXYZ()

        return hexLocation

    def __init__(self):

        self.qrs: List[int] = [0, 0, 0]
        self.xyz: List[int] = [0, 0, 0]

    def __repr__(self):
        '''
        Create the representation of this object
        '''

        locationString = ""

        # First show the qrs values
        locationString += f"QRS ({self.qrs[0]}, {self.qrs[1]}, {self.qrs[2]}) | "

        # Then show the xyz values
        locationString += f"XYZ ({self.xyz[0]}, {self.xyz[1]}, {self.xyz[2]})"

        return locationString

    def setQRS(self) -> None:
        '''
        Assuming x, y, and z are already set appropriately, determine Q R and S.
        '''

        # First find the direction with the highest absolute value.
        # This will determine which two vectors from Q, R, and S are used.
        maxValue, maxIndex = 0, 0
        for index in range(3):
            if abs(self.xyz[index]) > abs(maxValue):
                maxValue = self.xyz[index]
                maxIndex = index
        
        # Once the maximum index and value has been found, we need to determine which two vectors from Q, R, and S will be used for the decomposition
        # Each element of vector info looks like this
        #   ( ( QRSIndex1, QRSVector1, PositiveDirection1 ) , ( QRSIndex2, QRSVector2, PositiveDirection2 ) )
        vectorInfo = DIRECTIONS.MAX_MAP[maxIndex]

        # Extract the indices from the info
        vector1Index = vectorInfo[0][0]
        vector2Index = vectorInfo[1][0]

        # Now extract the vectors
        vector1 = vectorInfo[0][1]
        vector2 = vectorInfo[1][1]

        # And extract their default signs
        maxSign = sign(maxValue)
        vector1Sign = vectorInfo[0][2] * maxSign
        vector2Sign = vectorInfo[1][2] * maxSign
        
        # Adjust each vector according to whether or not the max value was positive or negative
        
        vector1 = (vector1[0] * vector1Sign, vector1[1] * vector1Sign, vector1[2] * vector1Sign)
        vector2 = (vector2[0] * vector2Sign, vector2[1] * vector2Sign, vector2[2] * vector2Sign)

        # Determine how many of each of the vectors are needed.
        vector1Count, vector2Count = 0, 0
        for dimensionIndex in range(3):
            if dimensionIndex != maxIndex:

                # Determine which vector is the relevant vector
                if vector1[dimensionIndex] != 0:
                    vector1Count = abs(self.xyz[dimensionIndex])
                    vector2Count = abs(maxValue) - vector1Count
                    break

                if vector2[dimensionIndex] != 0:
                    vector2Count = abs(self.xyz[dimensionIndex])
                    vector1Count = abs(maxValue) - vector2Count
                    break

        # Now assign the QRS values
        self.qrs[vector1Index] = vector1Count * vector1Sign
        self.qrs[vector2Index] = vector2Count * vector2Sign

    def setXYZ(self) -> None:
        '''
        Assuming q, r, and s are already set appropriately, determine x, y, and z.
        '''

        self.xyz[0] = DIRECTIONS.Q[0] * self.qrs[0] + DIRECTIONS.R[0] * self.qrs[1] + DIRECTIONS.S[0] * self.qrs[2]
        self.xyz[1] = DIRECTIONS.Q[1] * self.qrs[0] + DIRECTIONS.R[1] * self.qrs[1] + DIRECTIONS.S[1] * self.qrs[2]
        self.xyz[2] = DIRECTIONS.Q[2] * self.qrs[0] + DIRECTIONS.R[2] * self.qrs[1] + DIRECTIONS.S[2] * self.qrs[2]
    
    def mag(self) -> int:
        '''
        Returns the magnitude of the hexLocations
        '''

        return abs(self.qrs[0]) + abs(self.qrs[1]) + abs(self.qrs[2])
    

    ######################
    # OPERATOR OVERLOADS #
    ######################
    def __add__(self, other: "HexLocation") -> "HexLocation":
        '''
        Add two locations together
        '''

        # Just add the x and y components together
        newX = self.xyz[0] + other.xyz[0]
        newY = self.xyz[1] + other.xyz[1]

        return HexLocation.createFromXY(newX, newY)
    
    def __iadd__(self, other: "HexLocation") -> "HexLocation":
        '''
        In place add operator
        '''

        self.xyz[0] += other.xyz[0]
        self.xyz[1] += other.xyz[1]
        self.xyz[2] += other.xyz[2]

        self.setQRS()

        return self

    def __sub__(self, other: "HexLocation") -> "HexLocation":
        '''
        Subtract two locations together
        '''

        # Just sub the x and y components together
        newX = self.xyz[0] - other.xyz[0]
        newY = self.xyz[1] - other.xyz[1]

        return HexLocation.createFromXY(newX, newY)
    
    def __isub__(self, other: "HexLocation") -> "HexLocation":
        '''
        In place subtract operator
        '''

        self.xyz[0] -= other.xyz[0]
        self.xyz[1] -= other.xyz[1]
        self.xyz[2] -= other.xyz[2]

        self.setQRS()

        return self
    
    def __eq__(self, other: "HexLocation") -> bool:
        '''
        Equality comparator
        '''

        return self.xyz[0] == other.xyz[0] and self.xyz[1] == other.xyz[1] and self.xyz[2] == other.xyz[2]

    def __hash__(self):
        '''
        Basic hashing method
        '''
        return tuple.__hash__((self.xyz[0], self.xyz[1], self.xyz[2]))

class HexGrid:
    '''
    Class for managing many hexLocations.

    Parameters
    ----------
    radius - Number of hexes away from the the origin
    '''

    def __init__(self, radius: int):
        
        # Grid locations stored as a set for easy access
        self.grid: Set[HexLocation] = set()

        # Create all the hex locations for the grid
        for x in range(-radius, radius + 1):
            for y in range(-radius, radius + 1):
                hexLocation = HexLocation.createFromXY(x, y)
                if abs(hexLocation.qrs[0]) + abs(hexLocation.qrs[1]) + abs(hexLocation.qrs[2]) <= radius:
                    self.grid.add(hexLocation)
                
        
        print(self.grid)
        print(len(self.grid))
        