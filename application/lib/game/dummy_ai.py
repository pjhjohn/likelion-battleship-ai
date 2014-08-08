# -*- coding:utf-8 -*-
from application.lib.game.record import Record
from application.lib.game.board import Board
from application.lib.timeout import timeout_sec

# ============= USER AI PROGRAM CODE =============
from random import sample

@timeout_sec(3)
def guess(record) :
    global THREAD_ACTIVE
    board = record.board
    last = record.get_latest()
    empty_points = []
    for i in range(10) :
        for j in range(10) :
            if not board[i][j] : 
                empty_points.append((i, j))
    return sample(empty_points, 1)[0]