from application.lib.attrdict import attrdict_const
class Board(object) :
    # Tile Status on the Board. occupied ship id in [1,2,3,4,5]
    Status = attrdict_const(MISSED=-2, HIT=-1, EMPTY=0)
    # Constructor
    def __init__(self, ships) :
        self.ships = ships
        # remaining numbers of battleships' tiles
        self.remaining = 17
        # Generate Board        
        self.board = []
        for i in range(10) : self.board.append([0]*10)
        for ship in ships :
            for coord in ship.coordinates :
                if self.board[coord['x']][coord['y']] > 0 :
                    raise ValueError("ship#%d overlaps at (%d,%d)." % (ship.id, coord['x'], coord['y']))
                else :
                    self.board[coord['x']][coord['y']] = ship.id

    # Hit Calculation : Check whether player's guess is hit
    def hit(self, player, guess) :
        x, y = guess['x'], guess['y']
        if x not in range(10) or y not in range(10) :
            return {"player" : player, "guess" : {'x' : x, 'y' : y}, 'result' : -2, 'sink' : None}
        status = self.board[x][y]
        if status < 0 :
            return {"player" : player, "guess" : {'x' : x, 'y' : y}, 'result' : -1, 'sink' : None}
        elif status == 0 : 
            self.board[x][y] = -2
            return {"player" : player, "guess" : {'x' : x, 'y' : y}, 'result' : 0, 'sink' : None}
        elif status > 0 : 
            ship_id = self.board[x][y]
            self.board[x][y] = -1
            self.remaining -= 1
            self.ships[ship_id - 1].health -= 1
            if self.ships[ship_id - 1].health == 0 :
                return {"player" : player, "guess" : {'x' : x, 'y' : y}, 'result' : [2, 3][self.remaining==0], 'sink' : ship_id}
            else :
                return {"player" : player, "guess" : {'x' : x, 'y' : y}, 'result' : 1, 'sink' : None}

    def print_ships(self) :
        for ship in self.ships :
            print "%d sized ship #%d has %d health" %(ship.id, ship.size, ship.health)

    def show(self) :
        for row in self.board :
            for element in row :
                if element >= 0 : print ' ' + str(element),
                else : print element,
            print

    def convert(self) :
        copy = []
        for row in self.board :
            copy.append([[item, 0][item > 0] for item in row])
        return copy