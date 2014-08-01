import random
from application.lib.game import result
from application.lib.game import const as constant 


def guess_helper(location, result):

    board = result.board
    x = location[0]
    y = location[1]

    guess = {'x':None,'y':None}

    if x == None or y == None:
        while board[y][x] < 0:
            x = random.randint(0,9)
            y = random.randint(0,9)

    guess['x'] = x
    guess['y'] = y

    return guess

#-- user needs to write from here --

ㄹㅁㄴ
