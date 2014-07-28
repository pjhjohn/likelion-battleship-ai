import random
import result
import const as constant

constant.status_missed = -2
constant.status_hit = -1
constant.status_empty = 0

constant.result_invalid = -2
constant.result_alredy = -1
constant.result_missed = 0
constant.result_hit = 1
constant.result_sink = 2
constant.result_win = 3

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

    # user AI here
    board = result.board
    last_result = result.get_last_result()

    print "get_last_result(): ", result.get_last_result()
    print "get_history(3): ", result.get_history(3)
    print "get_board(): ", result.get_board()
    print "get_coordinate(3,3): ", result.get_coordinate(3,3)
    print "get_remaining_ships(): ", result.get_remaining_ships()
    print "get_sank_locations_and_ships_info(): ", result.get_sank_locations_and_ships_info()
    print "get_sank_location_by_ship_id(2): ", result.get_sank_location_by_ship_id(2)

    if "result" in last_result and last_result["result"] == constant.result_hit and last_result["guess"]["x"] < 9:
        x = last_result["guess"]["x"] + 1
        y = last_result["guess"]["y"]
    else:
        while board[y][x] < 0:
            x = random.randint(0,9)
            y = random.randint(0,9)
    #----------------

    return guess(x,y)
