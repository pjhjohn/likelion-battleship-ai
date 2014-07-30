class Result:
    """
    keys in history element
    "guess" : (dict) x, y coordinate {"x":, "y":}
    "result" : (int) guess result -2 ~ 3
    "sink" : (int) sank ship_id
    """
    def __init__( self, board ):
        self.board = board
        self.history = []

    def get_last_result(self):
        """
        return the last result dict
        """
        if len(self.history) > 0:
            return self.history[len(self.history)-1]
        else:
            return {}

    def get_history( self, last_n ):
        """
        return last nth result
        """
        history_count = len(self.history)
        if history_count < last_n :
            return {}
        else:
            return self.history[(history_count - last_n)]

    def get_board( self ):
        """
        return current board status
        """
        return self.board

    def get_coordinate( self, x, y ):
        """
        return the status of certain coordinate
        """
        return int(self.board[y][x])

    def get_remaining_ships( self ):
        """
        return the list of remaining battleships
        """
        remaining = [1, 2, 3, 4, 5]
        for result in self.history:
            if result["result"] == 2:
                remaining.remove(result["sink"])
        return remaining

    def get_sinking_locations_and_ships_info( self ):
        """
        return all sinking locations of ships
        return : (dict)"location": {"x":,"y"}, "sink": sinking ship id
        """
        sink = []
        for result in self.history:
            if result["result"] == 2:
                sink.append({"location":result["guess"], "sink":result["sink"]})
        return sink

    def get_sinking_location_by_ship_id( self, ship_id ):
        """
        return the last hit location of the ship by ship_id.
        If ship is still alive, return empty dict.
        """
        for result in self.history:
            if result["sink"] == ship_id:
                return result["guess"]
        else:
            {}

    def update_board( self, board ):
        self.board = board

    def update_history( self, last_result ):
        self.history.append(last_result)

    def update_result( self, board, last_result):
        self.update_board(board)
        self.update_history(last_result)
