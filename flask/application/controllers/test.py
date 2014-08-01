from flask import render_template, request, session
from application import app
from application.constants import *
from application.models.code_management import *
from application.models import ship_management
import os
from application.lib.game import ai
from application.lib.game import game

@app.route('/test')
def test():
    return render_template('test.html', current = request.path[1:])


@app.route('/run_test', methods = ['POST'])
def run_test():
    enemyCodeType = request.form[KEY_TEST_ENEMY_TYPE]
    testCode = request.form[KEY_TEST_CODE].encode('utf8')

    headerCode = get_header_code()

    tempFileName = os.tempnam(TEMP_DIR,'test')+".py"

    tempFile = open(tempFileName, 'w')
    tempFile.write(headerCode)
    tempFile.write(testCode)
    tempFile.close()

    try:
        testModule = import_from_file(tempFileName)
    except:
        os.remove(tempFileName)
        raise
    




    if enemyCodeType == 'custom':
        tempFileName2 = os.tempnam(TEMP_DIR,'test2')+".py"
        enemyCode = request.form[KEY_ENEMY_CODE].encode('utf8')
        tempFile = open(tempFileName2, 'w')
        tempFile.write(headerCode)
        tempFile.write(enemyCode)
        tempFile.close()

        enemyModule = import_from_file(tempFileName2)
        os.remove(tempFileName2)
    elif enemyCodeType == 'test':
        enemyModule = import_from_file(tempFileName)
    else:
        enemyModule = ai

    os.remove(tempFileName)

    return test_battle(testModule, enemyModule)

def test_battle(testModule, enemyModule):
    placement = ship_management.get_last_placement(session[KEY_USER_ID])
    return game.game(placement, placement, testModule, enemyModule).get_log()