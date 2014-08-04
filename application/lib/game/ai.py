import random
import result
import const as constant 


def guess(result):

    """
    @result : result class that contains all game log
    return : guess location coordinate as tuple (x,y)
    """

#-- user needs to write from here --

    board = result.board
    last_result = result.get_last_log()

    emptyPoints = []
    for i in range(10):
        for j in range(10):
            if not board[i][j]:
                emptyPoints.append((i,j))

    x,y = random.sample(emptyPoints,1)[0]


#-- to here --

    return x,y

