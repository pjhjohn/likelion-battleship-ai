from flask import render_template, request, session
from application import app
from application.const import *
from application.lib import static_analyzer as analyzer
from application.lib.auth import *
from application.lib.game import dummy_ai, game
from application.models import code_manager, fleet_manager
import json, os

@app.route('/test')
def test() :
    return render_template('test.html', current = request.path[1:])

@app.route('/run_test', methods = ['POST'])
def run_test() :
    header      = code_manager.get_header_code()
    my_code     = request.form[Key.TEST_CODE].encode('utf-8')
    my_saresult = analyzer.static_analysis(my_code)
    my_code, my_error = my_saresult['code'], my_saresult['errorcode']
    my_filename = os.tempnam('%stest' % Path.TEMP) + '.py'
    with open(my_filename, 'wb') as f : f.write(header + my_code)
    if my_error : return json.dumps({ 
        'my_error' : my_error,
        'my_error_msg' : ErrorMsg.CodeSubmit[my_error]
    })
    try    : my_module = code_manager.import_from_path(my_filename)
    except : 
        os.remove(my_filename)
        return json.dumps({
            'my_error' : ErrorCode.CompileError,
            'my_error_msg' : ErrorMsg.CodeSubmit[ErrorCode.CompileError]
        })
    # MY CODE AT LEAST RUNNABLE

    enemy_type  = request.form[Key.ENEMY_TYPE]
    if enemy_type == 'custom' :
        enemy_code     = request.form[Key.ENEMY_CODE].encode('utf-8')
        enemy_saresult = analyzer.static_analysis(enemy_code)
        enemy_code, enemy_error = enemy_saresult['code'], enemy_saresult['errorcode']
        enemy_filename = os.tempnam('%stest2' % Path.TEMP) + '.py'
        with open(enemy_filename, 'wb') as f : f.write(header + enemy_code)
        if enemy_error : return json.dumps({
            'my_error' : my_error,
            'enemy_error' : enemy_error,
            'enemy_error_msg' : ErrorMsg.CodeSubmit[enemy_error]
        })
        try : enemy_module = code_manager.import_from_path(enemy_filename)
        except :
            os.remove(enemy_filename)
            return json.dumps({
                'my_error' : my_error,
                'enemy_error' : ErrorCode.CompileError,
                'enemy_error_msg' : ErrorMsg.CodeSubmit[ErrorCode.CompileError]
            })
        os.remove(enemy_filename)
    elif enemy_type == 'test' : enemy_module = code_manager.import_from_path(my_filename)
    else :                      enemy_module = dummy_ai
    os.remove(my_filename)
    # ENEMY CODE AT LEAST RUNNABLE

    try : fleet = fleet_manager.get_latest_fleet(session[Key.USER_ID])
    except ValueError as e : 
        return json.dumps({
            'my_error'      : 0,
            'enemy_error'   : 0,
            'game_error'    : 100,
            'game_error_msg': e.message,
            'game_log'      : None
        })
    # AT LEAST, WE GOT OUR OWN FLEET

    playresult = game.play(fleet, fleet, my_module, enemy_module)
    if not playresult['errorcode'] :
        return json.dumps({
            'my_error'      : 0,
            'enemy_error'   : 0,
            'game_error'    : 0,
            'game_error_msg': playresult['errormsg'], #ErrorMsg.CodeSubmit[playresult['errorcode']],
            'game_log'      : playresult['result'].get_log(False)
        })
    else :
        return json.dumps({
            'my_error'      : 0,
            'enemy_error'   : 0,
            'game_error'    : playresult['errorcode'],
            'game_error_msg': playresult['errormsg'], #ErrorMsg.CodeSubmit[playresult['errorcode']],
            'game_log'      : playresult['result'].get_log(False)
        })