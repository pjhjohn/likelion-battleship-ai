from board import Board
from battleship import Battleship
from importlib import import_module
from result import Result
from log import Log

a1 = Battleship(2, 'x', {'x':1,'y':1}, 1)
b1 = Battleship(3, 'x', {'x':1,'y':2}, 2)
c1 = Battleship(3, 'x', {'x':1,'y':3}, 3)
d1 = Battleship(4, 'x', {'x':1,'y':4}, 4)
e1 = Battleship(5, 'x', {'x':1,'y':5}, 5)

a2 = Battleship(2, 'x', {'x':1,'y':1}, 1)
b2 = Battleship(3, 'x', {'x':1,'y':2}, 2)
c2 = Battleship(3, 'x', {'x':1,'y':3}, 3)
d2 = Battleship(4, 'x', {'x':1,'y':4}, 4)
e2 = Battleship(5, 'x', {'x':1,'y':5}, 5)

battleships1 = [a1,b1,c1,d1,e1]
battleships2 = [a2,b2,c2,d2,e2]

player1 = {"ai":"ai","battleships":battleships1}
player2 = {"ai":"ai","battleships":battleships2}

def print_board(board):
    for row in board:
        for col in row:
            print col, " ",
        print "\n"

def main( player1, player2 ):

    log = Log()

    ai1 = import_module(player1['ai']) 
    ai2 = import_module(player2['ai'])

    gb1 = Board(player2['battleships'])
    gb2 = Board(player1['battleships'])

    results1 = Result(gb1.board)
    results2 = Result(gb2.board)

    turn = 0

    turn1 = 0
    turn2 = 0

    while( gb1.remaining > 0 and gb2.remaining > 0 ):
        hit1 = 1
        hit2 = 1

        while hit1 > 0 and gb1.remaining != 0:
            turn1 += 1
            print "Turn %d" %turn1
            last_result = gb1.hit(1, ai1.guess_helper(results1))
            log.history.append(last_result)
            results1.board = gb1.board
            print last_result
            print_board(gb1.board)
            results1.history.append({"guess":last_result["guess"],"result":last_result["result"],"sink":last_result["sink"]})
            hit1 = last_result["result"]
            print ""

        if gb1.remaining == 0:
            "Player1 won!"
            break

        while hit2 > 0 and gb2.remaining != 0:
            turn2 += 1
            print "Turn %d" %turn2
            last_result = gb2.hit(2, ai2.guess_helper(results2))
            log.history.append(last_result)
            results2.board = gb2.board
            print last_result
            print_board(gb2.board)
            results2.history.append({"guess":last_result["guess"],"result":last_result["result"],"sink":last_result["sink"]})
            hit2 = last_result["result"]
            print ""

        if gb2.remaining == 0:
            "Player2 won!"
            break

    print_board(gb1.board)
    print results1.history
    print ""
    print_board(gb2.board)
    print results2.history
    
main(player1, player2)