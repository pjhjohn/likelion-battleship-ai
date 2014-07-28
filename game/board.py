class Board:
    """
    battleships : (list) list of battleships
    """
    def __init__( self, battleships ):
        self.battleships = battleships
        self.remaining = 17  # remaining numbers of battleships' tiles
        self.board = [] # status of each tile on the board. 0 = empty, 1 = occupied, -1 = hit, -2 = missed
        
        for x in range(10): 
            self.board.append( [0] * 10 )

        for battleship in battleships:
            for coordinate in battleship.coordinates:
                if self.board[ coordinate['y'] ][ coordinate['x'] ] > 0 :
                    print "battleships overlap!"
                else:
                    self.board[ coordinate['y'] ][ coordinate['x'] ] = battleship.ship_id # change occupied tile to 1

    def win(self):  
        print "You won!"

    def lose(self):
        print "You lost!"

    def hit( self, player, guess ):
        """
        check if guess hit
        guess : (dic) guess location
        """
        if ( guess['x'] > 9 or guess['x'] < 0 ) or ( guess['y'] > 9 or guess['y'] < 0 ):
            print "Player%d, invalid guess" %(player,guess['x'],guess['y'])
            return (player, (guess['x'],guess['y']), -2, None)

        else:
            coordinate = self.board[ guess['y'] ][ guess['x'] ]
            if coordinate < 0:
                print "Player%d, guessed already (%d,%d)" %(player,guess['x'],guess['y'])
                return (player, (guess['x'],guess['y']), -1, None)

            elif coordinate == 0:
                self.board[ guess['y'] ][ guess['x'] ] = -2
                print "Player%d, missed (%d,%d)" %(player,guess['x'],guess['y'])
                return (player, (guess['x'],guess['y']), 0, None)

            elif coordinate > 0 :
                hit_ship_id = self.board[ guess['y'] ][ guess['x'] ]

                self.board[ guess['y'] ][ guess['x'] ] = -1
                self.remaining -= 1
                print 'Hit Ship ID %d' %(hit_ship_id)
                print 'battleships' + str(self.battleships)
                self.battleships[ ( hit_ship_id - 1 ) ].health -= 1
                print 'Hit Ship Health : %d' %self.battleships[(hit_ship_id-1)].health
                if self.battleships[ ( hit_ship_id - 1 ) ].health == 0:
                    print "Player%d, Ship size %d has sank. (%d,%d)" % (player, self.battleships[ ( hit_ship_id - 1) ].size, guess['x'], guess['y'])
                    if self.remaining == 0:
                        self.win()
                        return (player, (guess['x'],guess['y']), 2, hit_ship_id)
                    else:
                        return (player, (guess['x'],guess['y']), 1, hit_ship_id)

                else:
                    print "Player%d, Hit Ship%d! (%d, %d)" %(player, hit_ship_id, guess['x'], guess['y'])
                    return (player, (guess['x'],guess['y']), 1, None)

                    
            else:
                print "WHAT?!"