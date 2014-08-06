import random
from record import Record

def guess(record):
    board = record.board
    last = record.get_latest()
    empty_points = []
    for i in range(10) :
        for j in range(10) :
            if not board[i][j] :
                empty_points.append((i,j))
    x, y = random.sample(empty_points, 1)[0]
    return x, y