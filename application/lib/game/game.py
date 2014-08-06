import operator
from record import Record
from board import Board
from ship import Ship
from log import Log

def build_fleet(ships):
    # Sorted by size in increment order
    ships.sort(key=operator.itemgetter("size"))
    # Length Check
    if not len(ships) == 5 :
        raise ValueError("# of ships are below 5. You got %d" % len(ships))
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

def play(fleet1, fleet2, player_module1, player_module2):
    """
    battleships1 : Player1's list of battleship from front-end
    battleships2 : Player2's list of battleship from front-end
    ai1 : Player1's ai file name (+path)
    ai2 : Player2's ai file name (+path)
    """
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
        while hit1 > 0 :
            turn1 += 1
            print 'Turn %d for player 1' % turn1
            guess1 = {}
            guess1['x'], guess1['y'] = player_module1.guess(record1)
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
            print "Player 1 Lost! (Player1 hit ", ["invalid location)","the same location twice)"][hit1+2]
            break

        while hit2 > 0 :
            turn2 += 1
            print 'Turn %d for player 2' % turn2
            guess2 = {}
            guess2['x'], guess2['y'] = player_module2.guess(record2)
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
            print "Player 2 Lost! (Player2 hit ", ["invalid location)","the same location twice)"][hit2+2]
            break

    return log

# Test Code
if __name__ == '__main__' :
    ships1 = [{"location":{"x":1,"y":1},"size":2,"direction":"x"},{"location":{"x":4,"y":2},"size":4,"direction":"y"},{"location":{"x":7,"y":3},"size":3,"direction":"x"},{"location":{"x":2,"y":4},"size":3,"direction":"y"},{"location":{"x":5,"y":7},"size":5,"direction":"x"}]
    ships2 = [{"location":{"x":1,"y":1},"size":2,"direction":"x"},{"location":{"x":1,"y":4},"size":4,"direction":"x"},{"location":{"x":1,"y":3},"size":3,"direction":"x"},{"location":{"x":1,"y":2},"size":3,"direction":"x"},{"location":{"x":5,"y":9},"size":5,"direction":"x"}]

    ai1, ai2 = "ai_1", "ai_2"
    print play(ships1, ships2, ai1, ai2)
    print play(ships2, ships1, ai2, ai1)