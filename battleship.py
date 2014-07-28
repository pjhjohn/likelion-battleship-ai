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
            for i in range(0, size-1):
                location[ direction ] += 1
                coordinates.append(dict(location))
        else:
            print "wrong direction!"

        self.coordinates = coordinates # list of coordinates that the battleship occupies