import operator
from board import Board
from battleship import Battleship
from importlib import import_module
from result import Result
from log import Log

# battleships1 = [{"location":{"x":1,"y":1},"size":2,"direction":"x"},{"location":{"x":4,"y":2},"size":4,"direction":"y"},{"location":{"x":7,"y":3},"size":3,"direction":"x"},{"location":{"x":2,"y":4},"size":3,"direction":"y"},{"location":{"x":5,"y":7},"size":5,"direction":"x"}]
# battleships2 = [{"location":{"x":1,"y":1},"size":2,"direction":"x"},{"location":{"x":4,"y":2},"size":4,"direction":"y"},{"location":{"x":7,"y":3},"size":3,"direction":"x"},{"location":{"x":2,"y":4},"size":3,"direction":"y"},{"location":{"x":5,"y":7},"size":5,"direction":"x"}]

# ai1 = "ai"
# ai2 = "ai"

def make_fleet(battleships):
    battleships.sort(key=operator.itemgetter("size"))
    
    fleet = []
    size3_id = [2,3]
    for bs in battleships:
        if bs["size"] == 3:
            fleet.append(Battleship(bs["size"],bs["direction"],bs["location"], size3_id.pop(0)))
        elif bs["size"] == 2:
            fleet.append(Battleship(bs["size"],bs["direction"],bs["location"], 1))
        else:
            fleet.append(Battleship(bs["size"],bs["direction"],bs["location"], bs["size"]))
    return fleet

def print_board(board):
    for row in board:
        for col in row:
            print col, " ",
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

def main( battleships1, battleships2, ai1, ai2 ):

    log = Log()

    ai1 = import_module(ai1)
    ai2 = import_module(ai2)

    gb1 = Board(make_fleet(battleships1))
    gb2 = Board(make_fleet(battleships2))

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
            last_result = gb1.hit(1, ai1.guess_helper(results1))
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

        while hit2 > 0:
            turn2 += 1
            print "Turn %d" %turn2
            last_result = gb2.hit(2, ai2.guess_helper(results2))
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

    print_board(gb1.board)
    print results1.history
    print ""
    print_board(gb2.board)
    print results2.history
    print log.history

    return log.get_log()
    
# main(battleships1, battleships2, ai1, ai2)