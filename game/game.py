import operator
from board import Board
from battleship import Battleship
from importlib import import_module
from result import Result
from log import Log
import const as constant

constant.STATUS_MISSED  = -2
constant.STATUS_HIT     = -1
constant.STATUS_EMPTY   = 0

constant.RESULT_INVALID = -2
constant.RESULT_TWICE   = -1
constant.RESULT_MISSED  = 0
constant.RESULT_HIT     = 1
constant.RESULT_SINK    = 2
constant.RESULT_WIN     = 3

battleships1 = [{"location":{"x":1,"y":1},"size":2,"direction":"x"},{"location":{"x":4,"y":2},"size":4,"direction":"y"},{"location":{"x":7,"y":3},"size":3,"direction":"x"},{"location":{"x":2,"y":4},"size":3,"direction":"y"},{"location":{"x":5,"y":7},"size":5,"direction":"x"}]
battleships2 = [{"location":{"x":1,"y":1},"size":2,"direction":"x"},{"location":{"x":1,"y":4},"size":4,"direction":"x"},{"location":{"x":1,"y":3},"size":3,"direction":"x"},{"location":{"x":1,"y":2},"size":3,"direction":"x"},{"location":{"x":5,"y":9},"size":5,"direction":"x"}]

ai1 = "ai"
ai2 = "ai_test"

def make_fleet(battleships):
    battleships.sort(key=operator.itemgetter("size"))
    
    fleet = []
    size = [2,3,3,4,5]
    size3_id = [2,3]

    for bs in battleships:
        if bs["size"] == 3:
            try:
                size.remove(3)
            except:
                raise ValueError("There are more than two size 3 battleships.")
            fleet.append(Battleship(bs["size"],bs["direction"],dict(bs["location"]), size3_id.pop(0)))

        elif bs["size"] == 2:
            try:
                size.remove(2)
            except:
                raise ValueError("There are more than one size 2 battleship.")
            fleet.append(Battleship(bs["size"],bs["direction"],dict(bs["location"]), 1))

        else:
            try:
                size.remove(bs["size"])
            except:
                raise ValueError("There are more than one size %d battleship." %bs["size"])
            fleet.append(Battleship(bs["size"],bs["direction"],dict(bs["location"]), bs["size"]))
    return fleet

def print_board(board):
    for row in board:
        for col in row:
            if col >= 0:
                print " ",col,
            else:
                print "",col,
        print "\n"

def convert_board(board):

    board_copy = []

    for x in range(10):  
        board_copy.append( [0] * 10 )

    for row in range(10):
        for col in range(10):
            board_copy[row][col] = board[row][col] 

    for row in range(10):
        for col in range(10):
            if board_copy[row][col] > 0:
                board_copy[row][col] = 0

    return board_copy

def game( battleships1, battleships2, ai1, ai2 ):
    """
    battleships1 : Player1's list of battleship from front-end
    battleships2 : Player2's list of battleship from front-end
    ai1 : Player1's ai file name (+path)
    ai2 : Player2's ai file name (+path)
    """

    battleships1.sort(key=operator.itemgetter("size"))
    battleships2.sort(key=operator.itemgetter("size"))

    log = Log({"player1":battleships1, "player2":battleships2})

    ai1 = import_module(ai1)
    ai2 = import_module(ai2)

    gb1 = Board(make_fleet(battleships2))
    gb2 = Board(make_fleet(battleships1))

    results1 = Result(convert_board(gb1.board))
    results2 = Result(convert_board(gb2.board))

    turn = 0

    turn1 = 0
    turn2 = 0

    while( gb1.remaining > 0 and gb2.remaining > 0 ):

        hit1 = 1
        hit2 = 1

        while hit1 > 0:
            turn1 += 1
            print "Turn %d" %turn1
            guess1 = {}
            guess1['x'], guess1['y'] = ai1.guess(results1)
            # guess1_tuple = ai1.guess(results2)
            # guess1["x"] = guess1_tuple[0]
            # guess1["y"] = guess1_tuple[1]
            last_result = gb1.hit(1, guess1)
            log.history.append(last_result)
            results1.update_board(convert_board(gb1.board)) 
            print last_result
            print_board(gb1.board)
            results1.history.append({"guess":last_result["guess"],"result":last_result["result"],"sink":last_result["sink"]})
            hit1 = last_result["result"]
            if hit1 == 3:
                break
            print ""

        if hit1 == 3:
            print "Player1 Won!"
            break
        elif hit1 == -1:
            print "Player1 Lost! (Player1 hit the same location twice)"
            break
        elif hit1 == -2:
            print "Player1 Lost! (Player1 hit invalid location)"
            break

        while hit2 > 0:
            turn2 += 1
            print "Turn %d" %turn2
            guess2 = {}
            guess2['x'], guess2['y'] = ai2.guess(results2)
            # guess2_tuple = ai2.guess(results2)
            # guess2["x"] = guess2_tuple(0)
            # guess2["y"] = guess2_tuple(1)
            last_result = gb2.hit(2, guess2)
            log.history.append(last_result)
            results2.update_board(convert_board(gb2.board))
            print last_result
            print_board(gb2.board)
            results2.history.append({"guess":last_result["guess"],"result":last_result["result"],"sink":last_result["sink"]})
            hit2 = last_result["result"]
            if hit2 == 3:
                break
            print ""

        if hit2 == 3:
            print "Player2 Won!"
            break
        elif hit2 == -1:
            print "Player2 Lost! (Player2 hit the same location twice)"
            break
        elif hit2 == -2:
            print "Player2 Lost! (Player2 hit invalid location)" 
            break

    print_board(gb1.board)
    print results1.history
    print ""
    print_board(gb2.board)
    print results2.history
    print log.history

    return log.get_log()
    
print game(battleships1, battleships2, ai1, ai2)
print game(battleships1, battleships2, ai1, ai2)