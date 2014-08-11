import operator, traceback, sys
from record import Record
from board import Board
from ship import Ship
from log import Log
from application.lib.timeout import TimeoutError
from application.const import *
from cStringIO import StringIO

class Player1LostWithError(Exception): pass
class Player2LostWithError(Exception): pass
class MakersError(Exception) : pass
# return : {'result' : game_log, 'errorcode' : error_code, 'errormsg' : error_type }
def handle_exception(func) :
    def func_args(*args, **kwargs) :
        # Override Standard-IO
        old_stdout = sys.stdout
        sys.stdout = custom_stdout = StringIO()
        try : 
            log = func(*args, **kwargs)
            # Stop overriding
            sys.stdout = old_stdout
            return { 'result' : log, 'errorcode' : 0, 'errormsg' : '', 'description' : custom_stdout.getvalue() }
        except Exception as e : 
            # Exception-triggered values
            name = e.__class__.__name__
            if 'description' in e.message : trace = e.message['traceback']
            else                          : trace = traceback.format_exc()
            
            if name in ErrorCode : errorcode = ErrorCode[name]
            else                 : errorcode = len(ErrorCode)
            # Stop overriding
            sys.stdout = old_stdout
            console_log = custom_stdout.getvalue()
            
            return {    
                'result'      : e.message['log'] ,
                'errorcode'   : errorcode ,
                'errormsg'    : '%s[%s] : %s' % (name, e.message['type'], e.message['description']),
                'description' : '%s\nError %s' % (console_log, trace)
            }
    return func_args
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

@handle_exception
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
            guess1 = {}
            try                   : guess1['x'], guess1['y'] = player_module1.guess(record1)
            except Exception as e : raise Player1LostWithError({'log' : log, 'type' : e.__class__.__name__, 'description' : e.message['msg'], 'traceback' : e.message['traceback']})
            last_record = board1.hit(1, guess1)
            log.history.append(last_record)
            record1.update_board(board1.convert())
            record1.history.append({'guess':last_record['guess'], 'result':last_record['result'], 'sink':last_record['sink']})
            hit1 = last_record['result']
            if hit1 == 3: break

        if hit1 == 3 :
            print "Player 1 Won!"
            break
        elif hit1 in [-2, -1] :
            print "Player 1 Lost! (Player1 hit ", ["invalid location)", "the same location twice)"][hit1 + 2]
            break

        # Player2 Turn
        while hit2 > 0 :
            turn2 += 1
            guess2 = {}
            try                   : guess2['x'], guess2['y'] = player_module2.guess(record2)
            except Exception as e : raise Player2LostWithError({'log' : log, 'type' : e.__class__.__name__, 'description' : e.message['msg'], 'traceback' : e.message['traceback']})
            last_record = board2.hit(2, guess2)
            log.history.append(last_record)
            record2.update_board(board2.convert())
            record2.history.append({'guess':last_record['guess'], 'result':last_record['result'], 'sink':last_record['sink']})
            hit2 = last_record['result']
            if hit2 == 3 : break

        if hit2 == 3 :
            print "Player 2 Won!"
            break
        elif hit2 in [-2, -1] :
            print "Player 2 Lost! (Player2 hit ", ["invalid location)", "the same location twice)"][hit2 + 2]
            break

    return log
