import random
import result
import const as constant 

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

def guess(result):
    """
    return  
    """
    # user AI here
    # def check_last_four(result):
    #     if result.get_history(1)["result"] == 1:

    #     elif result.get_history(1)["result"] == 0:
    #         if result.get_history(2)["result"] == 1:

    #         elif result.get_history(2)["result"] == 0:
    #             if result.get_history(3)["result"] == 1:

    #             elif result.get_history(3)["result"] == 0:
    #                 if result.get_history(4)["result"] == 1:

    x = 0
    y = 0

    board = result.board
    last_result = result.get_last_result()

    if "result" in last_result:
        x = last_result["guess"]["x"]
        y = last_result["guess"]["y"]

    if ("result" in last_result) and (last_result["result"] == constant.RESULT_HIT) and (x < 9) and board[y][x+1] > 0:
        x = last_result["guess"]["x"] + 1
        y = last_result["guess"]["y"]
    elif ("result" in result.get_history(2)) and (result.get_history(2)["result"] == constant.RESULT_HIT) and (x < 9) and board[y][x-1] > 0:
        x = result.get_history(2)["guess"]["x"] - 1
        y = result.get_history(2)["guess"]["y"]
    else:
        while board[y][x] < 0:
            x = random.randint(0,9)
            y = random.randint(0,9)
    #----------------

    return (x,y)
