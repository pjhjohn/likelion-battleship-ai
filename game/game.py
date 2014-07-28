from board import Board
from battleship import Battleship
from importlib import import_module
from result import Result
from log import Log

a = Battleship(2, 'x', {'x':1,'y':1}, 1)
b = Battleship(3, 'x', {'x':1,'y':2}, 2)
c = Battleship(3, 'x', {'x':1,'y':3}, 3)
d = Battleship(4, 'x', {'x':1,'y':4}, 4)
e = Battleship(5, 'x', {'x':1,'y':5}, 5)

battleships = [a,b,c,d,e]

player1 = {"ai":"ai","battleships":battleships}
player2 = {"ai":"ai","battleships":battleships}

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

    while( gb1.remaining > 0 and gb2.remaining > 0 ):
        hit1 = 1
        hit2 = 1

        while hit1 > 0 and gb1.remaining != 0:
            last_result = gb1.hit(1, ai1.guess_helper(results1))
            log.history.append(last_result)
            results1.board = gb1.board
            print last_result
            print_board(gb1.board)
            results1.history.append(last_result[1:])
            hit1 = last_result[2] 

        if gb1.remaining == 0:
            "Player1 won!"
            break

        # while hit2 > 0 and gb2.remaining != 0:
        #     last_result = gb2.hit(2, ai2.guess_helper(results2))
        #     log.history.append(last_result)
        #     results2.board = gb2.board
        #     print last_result
        #     print_board(gb2.board)
        #     results2.history.append(last_result[1:])
        #     hit2 = last_result[2]

        # if gb2.remaining == 0:
        #     "Player2 won!"
        #     break

    print_board(gb1.board)
    print ""
    print_board(gb2.board)
    
main(player1, player2)