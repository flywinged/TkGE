
# Python imports
from typing import List

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
        0 : ((1, R, 1), (2, S, -1)),
        1 : ((0, Q, 1), (2, S, 1)),
        2 : ((0, Q, -1), (1, R, -1))
    }

class HexLocation():
    '''
    Class for storing hexgrid locations
    '''

    def __init__(self):

        self.qrs: List[int] = [0, 0, 0]
        self.xyz: List[int] = [0, 0, 0]
    
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


    def setQRS(self) -> None:
        '''
        Assuming x, y, and z are already set appropriately, determine Q R and S.
        '''

        # First find the direction with the highest absolute value.
        # This will determine which two vectors from Q, R, and S are used.
        maxValue, maxIndex = 0, 0
        for index in range(3):
            if abs(self.xyz[index]) > maxIndex:
                maxValue = abs(self.xyz[index])
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
        vector1Sign = vectorInfo[0][2]
        vector2Sign = vectorInfo[1][2]
        
        # Adjust each vector according to whether or not the max value was positive or negative
        maxSign = sign(maxValue)
        vector1 = (vector1[0] * vector1Sign * maxSign, vector1[1] * vector1Sign * maxSign, vector1[2] * vector1Sign * maxSign)
        vector2 = (vector2[0] * vector2Sign * maxSign, vector2[1] * vector2Sign * maxSign, vector2[2] * vector2Sign * maxSign)

h = HexLocation.createFromXY(2, 2)