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
    code_type_enemy = request.form[Key.TEST_ENEMY_TYPE]
    code_for_test   = request.form[Key.TEST_CODE].encode('utf-8')
    code_header     = code_manager.get_header_code()
    tmp_file_name   = os.tempnam('%stest' % Path.TEMP) + '.py'
    with open(tmp_file_name, 'w') as tmp :
        tmp.write(code_header)
        tmp.write(code_for_test)

    try :
        test_module = import_from_file(tmp_file_name)
    except :
        os.remove(tmp_file_name)
        raise

    if code_type_enemy == 'custom' :
        tmp_file_name_2 = os.tempnam('%stest2' % Path.TEMP) + '.py'
        enemy_code = request.form[Key.ENEMY_CODE].encode('utf-8')
        with open(tmp_file_name_2, 'w') as tmp :
            tmp.write(code_header)
            tmp.write(enemy_code)
        enemy_module = import_from_file(tmp_file_name_2)
        os.remove(tmp_file_name_2)
    elif code_type_enemy == 'test' :
        enemy_module = import_from_file(tmp_file_name)
    else :
        enemy_module = dummy_ai

    os.remove(tmp_file_name)
    return test_battle(test_module, enemy_module)

def test_battle(test_module, enemy_module) :
    fleet = fleet_manager.get_latest_fleet(session[Key.USER_ID])
    if not fleet :
        return '1'
    else :
        # TODO
        try :
            result = game.play(fleet, fleet, test_module, enemy_module).get_log()
        except :
            return '1'