from flask import render_template, request, session
from application import app
from application.const import *
from application.lib.auth import *
from application.lib.game import dummy_ai, game
from application.models import code_manager, fleet_manager
import os

@app.route('/test')
def test() :
    return render_template('test.html', current = request.path[1:])

@app.route('/run_test', methods = ['POST'])
def run_test() :
    header      = code_manager.get_header_code()
    my_code     = request.form[Key.TEST_CODE].encode('utf-8')

    # Write Temp File
    my_filename = os.tempnam('%stest' % Path.TEMP) + '.py'
    with open(my_filename, 'wb') as f : f.write(header + my_code)

    print 'MYCODE\n' + header + my_code + '\nMYEND'
    # Try Import
    try :
        my_module = code_manager.import_from_path(my_filename)
    except :
        os.remove(my_filename)
        raise

    # Determine Enemy Code
    enemy_type  = request.form[Key.ENEMY_TYPE]
    if enemy_type == 'custom' :
        enemy_code     = request.form[Key.ENEMY_CODE].encode('utf-8')
        enemy_filename = os.tempnam('%stest2' % Path.TEMP) + '.py'
        with open(enemy_filename, 'wb') as f : f.write(header + enemy_code)
        print 'ENEMYCODE\n' + header + my_code + '\nENEMYEND'
        enemy_module = code_manager.import_from_path(enemy_filename)
        os.remove(enemy_filename)
    elif enemy_type == 'test' : enemy_module = code_manager.import_from_path(my_filename)
    else :                      enemy_module = dummy_ai

    os.remove(my_filename)
    return test_battle(my_module, enemy_module)

def test_battle(my_module, enemy_module) :
    fleet = fleet_manager.get_latest_fleet(session[Key.USER_ID])
    if not fleet : return '1'   # No Fleet
    else :
        try :    result = game.play(fleet, fleet, my_module, enemy_module).get_log()
        except : return '2'     # Timeout
