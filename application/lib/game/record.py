from application.lib.attrdict import attrdict_const
class Record : 
    # API STARTS
    Status = attrdict_const(INVALID=-2, TWICE=-1, MISSED=0, HIT=1, SINK=2, WIN=3)
    def __init__(self, board) :
        self.board = board
        self.history = []
        self.data = {}

    def get_latest(self) :
        if len(self.history) > 0 :
            return dict(self.history[len(self.history) - 1])
        else :
            return {}

    def get_history(self) : 
        print list(self.history)
        return list(self.history)

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
        sink_list = []
        for log in self.history :
            if log['result'] == Record.Status.SINK :
                sink_list.append({'location' : log['guess'], 'sink' : record['sink']})
        if ship_id == None : return sink_list
        if type(ship_id) == int and ship_id in [1, 2, 3, 4, 5] :
            for sink in sink_list :
                if sink['sink'] == ship_id :
                    return dict(sink['location'])
            else : return {}
        else :
            if not type(ship_id) == int     : raise ValueError('ship_id should be int type. Current ship_id has %s type' % str(type(ship_id)))
            elif ship_id not in [1,2,3,4,5] : raise ValueError('ship_id should be in range of [1, 2, 3, 4, 5]. Current ship_id is %d' % ship_id)
    # API ENDS

    def update_board(self, board ):
        self.board = board

    def update_history(self, last_result ):
        self.history.append(last_result)

    def update_result(self, board, last_result):
        self.update_board(board)
        self.update_history(last_result)
