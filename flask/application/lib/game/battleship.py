class Battleship:
    """
    size : (int) size of battleship (2,3,4,5)
    location : (dic) starting point of the battleship
    direction : x or y  
    """
    def __init__( self, size, direction, location, ship_id ):
        self.size = size
        self.health = size
        self.direction = direction
        self.ship_id = ship_id

        coordinates = []

        if direction == 'x' or direction == 'y':
            coordinates.append(dict(location))
            for i in range(0, size-2):
                location[ direction ] += 1

                if location[direction] > 9:
                    raise ValueError("Battleship #%d location out of bound." %self.ship_id)

                coordinates.append(dict(location))
        else:
            raise ValueError("Invalid Direction")


        self.coordinates = coordinates # list of coordinates that the battleship occupies