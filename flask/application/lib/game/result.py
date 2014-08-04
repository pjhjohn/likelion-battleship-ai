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
        self.data = {}

    def get_last_log(self):
        """
        return the last result dict
        """
        if len(self.history) > 0:
            return dict(self.history[len(self.history)-1])
        else:
            return {}

    def get_last_nth_log( self, last_n ):
        """
        return last nth result
        """
        history_count = len(self.history)
        if not last_n.isdigit():
            return {}
        elif history_count < last_n or last_n < 1:
            return {}
        else:
            return dict(self.history[(history_count - last_n)])

    def get_history():
        return list(self.history)

    def get_board( self ):
        """
        return current board status
        """
        return list(self.board)

    def get_coordinate_status( self, x, y ):
        """
        return the status of certain coordinate
        """
        if not x.isdigit() or not y.isdigit():
            return []
        elif not ((0 <= x < 10) and (0 <= y < 10)):
            return []

        return int(self.board[x][y])

    def get_remaining_ships( self ):
        """
        return the list of remaining battleships
        """
        remaining = [1, 2, 3, 4, 5]
        for result in self.history:
            if result["result"] == 2:
                remaining.remove(result["sink"])
        return remaining

    def get_sinking_locations_and_ships( self ):
        """
        return all sinking locations of ships
        return : (dict)"location": {"x":,"y"}, "id": sinking ship id
        """
        sink = []
        for result in self.history:
            if result["result"] == 2:
                sink.append({"location":result["guess"], "id":result["sink"]})
        return sink

    def get_sinking_location_by_ship_id( self, ship_id ):
        """
        return the last hit location of the ship by ship_id.
        If ship is still alive, return empty dict.
        """
        if not ship_id.isdigit():
            return {}
        elif not ( 1 <= ship_id <= 5 ):
            return {}
        else:
            for result in self.history:
                if result["sink"] == ship_id:
                    return dict(result["guess"])
        return {}

    def update_board( self, board ):
        self.board = board

    def update_history( self, last_result ):
        self.history.append(last_result)

    def update_result( self, board, last_result):
        self.update_board(board)
        self.update_history(last_result)
