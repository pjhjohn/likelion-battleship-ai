from application.lib.attrdict import attrdict_const
class Record : 
    """
    <Keys in History element>
    'guess' : (dict) x, y coordinate as {"x": (int), "y": (int)}
    'result': (int)  guess result from -2 to 3
    'sink'  : (int)  Sank ship.id
    """
    # API STARTS
    Status = attrdict_const(INVALID=-2, TWICE=-1, MISSED=0, HIT=1, SINK=2, WIN=3)
    def __init__(self, board) :
        self.board = board
        self.history = []

    def get_latest(self) :
        """
        (dict) return the latst result
        """
        if len(self.history) > 0 :
            return dict(self.history[len(self.history) - 1])
        else :
            return {}
    
    def get_history_at(self, index, direction='FORWARD') :
        if 0 <= index < len(self.history) :
            if direction == 'FORWARD' :
                return dict(self.history[index])
            elif direction == 'BACKWARD' :
                return dict(self.history[len(self.history) - 1 - index])
            else : 
                raise ValueError('dir should be FORWARD or BACKWARD. You used %s' % direction)
        else :
            return {}

    def get_board(self) :
        return list(self.board)

    def get_status_at(self, x, y) : 
        return int(self.board[x][y])

    def get_remaining_ships(self) : 
        ship_ids = [1, 2, 3, 4, 5]
        for record in self.history :
            if record['result'] == 2 :
                remaining.remove(result['sink'])
        return remaining

    def get_sink_info(self, ship_id=None) : 
        sinks = []
        for record in self.history :
            if record['result'] == 2 :
                sinks.append({'location' : record['guess'], 'sink' : record['sink']})
        if ship_id == None :
            return sinks
        elif type(ship_id) == int and 0 < ship_id < 5 :
            for sink in sinks :
                if record['sink'] == ship_id :
                    return dict(sink['location'])
        else :
            return {}
    # API ENDS

    def update_board(self, board ):
        self.board = board

    def update_history(self, last_result ):
        self.history.append(last_result)

    def update_result(self, board, last_result):
        self.update_board(board)
        self.update_history(last_result)