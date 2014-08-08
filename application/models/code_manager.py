import os, time, imp, uuid, battleship_db, fleet_manager
from application.const import *
from application.lib import static_analyzer as analyzer
from application.lib.game import dummy_ai, game

def add_code(user_id, code) :
    base_dir = '%s/%d' % (Path.Upload.DIR, user_id)
    if not os.path.isdir(base_dir) : os.mkdir(base_dir)
    code_encoded = code.encode('utf-8')
    file_name = str(int(time.time()))

    # Load Header
    header_file = open(Path.CODE_HEADER_FILE_NAME, 'rb')
    header = header_file.read()
    header_file.close()

    # Code for user
    file_user = open('%s/%s.py'%(base_dir, file_name), 'wb')
    file_user.write(code_encoded)
    file_user.close()

    # Code for competition
    analyzed_code, error_msg = code_encoded, ''
    analyzer_result = analyzer.static_analysis(code_encoded)   
    analyzed_code, error_code = analyzer_result['code'], analyzer_result['errorcode']
    file_competition = open('%s/%s.py'%(base_dir, Path.Upload.PREFIX + file_name), 'wb')
    file_competition.write(header + analyzed_code)
    file_competition.close()

    # Import AI Module
    if not error_code :
        try    : test_ai_module = import_from_path('%s/%s.py'%(base_dir, Path.Upload.PREFIX + file_name))
        except : error_code = ErrorCode.CompileError

    # Test
    fleet_deployment = fleet_manager.get_latest_fleet(user_id)
    enemy_ai_module = dummy_ai
    if not error_code :
        playresult = game.play(fleet_deployment, fleet_deployment, test_ai_module, enemy_ai_module)
        error_code = playresult['errorcode']
        if error_code : error_msg  = playresult['result']

    # INSERT Code
    query = "INSERT INTO ai_code (user_id, file_name, errorcode, description) VALUES " + "('%d', '%s', '%d', '%s')" % (user_id, file_name, error_code, error_msg)
    return battleship_db.insert(query)

def get_codes(user_id) :
    query = "SELECT * FROM ai_code WHERE user_id = '%d' ORDER BY uploaded_time DESC" % user_id
    cursor = battleship_db.select(query)
    codes = []
    for row in cursor :
        code = open('%s/%d/%s.py'%(Path.Upload.DIR, user_id, row[Col.FILE_NAME])).read()
        row[Key.CODE] = code
        codes.append(row)
    return codes

def get_code_path(user_id) :
    return '%s/%d/' % (Path.Upload.DIR, user_id)

def get_latest_code_file_name(user_id, with_header = False) :
    query = "SELECT file_name FROM ai_code WHERE user_id = '%d' AND errorcode = '0' ORDER BY uploaded_time DESC LIMIT 1" % user_id
    cursor = battleship_db.select(query)
    if len(cursor) > 0 : return ['', Path.Upload.PREFIX][with_header] + cursor[0][Col.FILE_NAME] # return None if not

def get_latest_code_module(user_id) :
    try : 
        file_name = get_latest_code_file_name(user_id, True)
        return import_from_path(get_code_path(user_id) + file_name + '.py')
    except : return None

def import_from_path(file_path) :
    return imp.load_source(str(uuid.uuid4()), file_path)

def get_header_code() :
    with open(Path.CODE_HEADER_FILE_NAME) as header : return header.read()