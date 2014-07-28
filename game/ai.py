import random
import result

def guess(x,y):
    guess = {'x':None,'y':None}
    guess['x'] = x
    guess['y'] = y
    return guess

def guess_helper(result):
    """
    result : result of last guess. 0 = guess again, 1 = hit, -1 = missed
    board : current status of all tiles. 
    """
    x = random.randint(0,9)
    y = random.randint(0,9)

    # print x
    # print y 

    # user AI here
    board = result.board

    while board[y][x] < 0:
        x = random.randint(0,9)
        y = random.randint(0,9)
    #---------------

    return guess(x,y)
