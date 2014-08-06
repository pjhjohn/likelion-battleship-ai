class Ship :
    """
    size     : (int) size of battleship whthin (2, 3, 4, 5)
    location : (dict) starting point of the battleship
    direction: (str) x or y
    """
    def __init__(self, size, location, direction, ship_id) :
        self.size = size
        self.health = size
        self.direction = direction
        self.id = ship_id
        coord = []
        if direction in ['x', 'y'] :
            coord.append(dict(location))
            for i in range(size-1) :
                location[direction] += 1
                if location[direction] > 9 :
                    raise ValueError("Location of Ship#%d is out of bound."%self.id)
                coord.append(dict(location))
        else :
            raise ValueError("Invalid Direction : %s" % direction)

        # List of Coord that is occupied by battleship itself
        self.coordinates = coord