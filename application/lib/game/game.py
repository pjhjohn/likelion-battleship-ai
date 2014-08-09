import operator
from record import Record
from board import Board
from ship import Ship
from log import Log
from application.lib.timeout import TimeoutError
from application.const import *

class Player1LostWithError(Exception): pass
class Player2LostWithError(Exception): pass
class MakersError(Exception) : pass
def with_errormsg(func) :
    def with_args(*args, **kwargs) :
        try :
            return {'errorcode' : 0, 'result' : func(*args, **kwargs)}
        except Exception as e :
            name = e.__class__.__name__
            if name in ErrorCode : code = ErrorCode[name]
            else                 : code = len(ErrorCode)
            return {'errorcode' : code , 'result' : e.message }
    return with_args
# With decorator above, game.play returns { 'errorcode' : errorcode, 'result' : return-value OR e.message }

def build_fleet(ships):
    # Sorted by size in increment order
    ships.sort(key=operator.itemgetter("size"))

    # Length Check
    if not len(ships) == 5 : raise ValueError("# of ships are below 5. You got %d" % len(ships))

    # Size Check
    size_check = [2, 3, 3, 4, 5]
    for ship in ships :
        try : size_check.remove(ship['size'])
        except : raise ValueError("Exceed in size %d battleship" % ship['size'])

    # Build Fleet
    fleet = []
    ids = [1, 2, 3, 4, 5]
    for index in range(len(ships)) :
        ship = ships[index]
        ship_id = ids[index]
        fleet.append(Ship(ship['size'], dict(ship['location']), ship['direction'], ship_id))
    return fleet

@with_errormsg
def play(fleet1, fleet2, player_module1, player_module2):
    # INIT Player 1 & 2
    fleet1.sort(key = operator.itemgetter('size'))
    fleet2.sort(key = operator.itemgetter('size'))
    board1 = Board(build_fleet(fleet2))
    board2 = Board(build_fleet(fleet1))
    record1 = Record(board1.convert())
    record2 = Record(board2.convert())
    # INIT Others
    log = Log({'player1':fleet1, 'player2':fleet2})
    turn1, turn2 = 0, 0
    # Game Loop
    while board1.remaining > 0 and board2.remaining > 0 :
        hit1, hit2 = 1, 1
        # Player1 Turn
        while hit1 > 0 :
            turn1 += 1
            print 'Turn %d for player 1' % turn1
            guess1 = {}
            try                   : 
                guess1['x'], guess1['y'] = player_module1.guess(record1)
                guess1['x'], guess1['y'] = int(guess1['x']), int(guess1['y'])
            except Exception as e : raise Player1LostWithError(log)
            last_record = board1.hit(1, guess1)
            log.history.append(last_record)
            record1.update_board(board1.convert())
            print last_record
            board1.show()
            record1.history.append({'guess':last_record['guess'], 'result':last_record['result'], 'sink':last_record['sink']})
            hit1 = last_record['result']
            if hit1 == 3:
                break
            print

        if hit1 == 3 :
            print "Player 1 Won!"
            break
        elif hit1 in [-2, -1] :
            print "Player 1 Lost! (Player1 hit ", ["invalid location)", "the same location twice)"][hit1 + 2]
            break

        # Player2 Turn
        while hit2 > 0 :
            turn2 += 1
            print 'Turn %d for player 2' % turn2
            guess2 = {}
            try                   : guess2['x'], guess2['y'] = player_module2.guess(record2)
            except Exception as e : raise Player2LostWithError(log)
            last_record = board2.hit(2, guess2)
            log.history.append(last_record)
            record2.update_board(board2.convert())
            print last_record
            board2.show()
            record2.history.append({'guess':last_record['guess'], 'result':last_record['result'], 'sink':last_record['sink']})
            hit2 = last_record['result']
            if hit2 == 3:
                break
            print

        if hit2 == 3 :
            print "Player 2 Won!"
            break
        elif hit2 in [-2, -1] :
            print "Player 2 Lost! (Player2 hit ", ["invalid location)", "the same location twice)"][hit2 + 2]
            break

    return log