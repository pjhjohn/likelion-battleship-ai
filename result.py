class Result:
    """

    """
    def __init__( self, board ):
        self.board = board
        self.history = []

    def get_history( self, last_count ):
        history_count = len(self.history)
        if history_count < last_count :
            return None
        else:
            return self.history.pop( (history_count - last_count) )

    def get_board( self ):
        return self.board

    def get_coordinate( self, x, y ):
        return self.board[y][x]

    def get_remaining_ships( self ):
        pass

    def get_sank_locations_and_ships_info( self ):
        pass

    def get_sank_location_by_ship_id( self, ship_id ):
        pass

    def update_board( self, board ):
        self.board = board

    def update_history( self, last_result ):
        self.history.append(last_result)

    def update_result( self, board, last_result):
        self.update_board(board)
        self.update_history(last_result)
