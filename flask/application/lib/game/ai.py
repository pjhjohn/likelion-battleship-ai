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
    last_result = result.get_last_result()

    if "result" in last_result:
        x = last_result["guess"]["x"] + 1
        y = last_result["guess"]["y"]
    else:
        x = 0
        y = 0

    if x > 9:
        x = 0
        y = y + 1

#-- to here --

    return x,y

