import os, time, imp, uuid, battleship_db, fleet_manager
from application.const import *
from application.lib.game import dummy_ai, game

def add_code(user_id, code) :
    base = '%s/%d' % (Path.Upload.DIR, user_id)
    if not os.path.isdir(base) :
        os.mkdir(base)

    code_encoded = code.encode('utf-8')
    file_name = str(int(time.time()))

    code_headerf = open(Path.CODE_HEADER_FILE_NAME)
    code_header = code_headerf.read()
    code_headerf.close()

    file_for_user = open('%s/%s.py'%(base, file_name), 'w')
    file_for_user.write(code_encoded)
    file_for_user.close()

    file_for_competition = open('%s/%s.py'%(base, Path.Upload.PREFIX + file_name), 'w')
    file_for_competition.write(code_header + code_encoded)
    file_for_competition.close()

    error = False
    # Import AI Module
    try :
        test_ai_module = import_from_file('%s/%s.py'%(base, Path.Upload.PREFIX + file_name))
    except : 
        error = True
    # Test
    fleet_placement = fleet_manager.get_latest_fleet(user_id)
    enemy_ai_module = dummy_ai
    if not error :
        try :
            game.play(ship_placement, ship_placement, test_ai_module, enemy_ai_module)
        except :
            error = True
    # If Test Succeed
    query = "INSERT INTO codes (user_id, file_name, has_error) VALUES " + "('%d', '%s', '%d')" % (user_id, file_name, [0, 1][error])
    return battleship_db.insert(query)

def get_codes(user_id) :
    query = "SELECT * FROM codes WHERE user_id = '" + '%d'%user_id + "' ORDER BY uploaded_time DESC"
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
    query = "SELECT file_name FROM codes WHERE user_id = '" + '%d'%user_id + "' AND has_error = '0' ORDER BY uploaded_time DESC LIMIT 1"
    cursor = battleship_db.select(query)
    if len(cursor) > 0 :    # return None if not
        return ['', Path.Upload.PREFIX][with_header] + cursor[0][Col.FILE_NAME]

def get_latest_code_module(user_id) :
    try : 
        file_name = get_latest_code_file_name(user_id, True)
        return import_from_path(get_code_path(user_id) + file_name + '.py')
    except :
        return None

def import_from_path(file_path) :
    return imp.load_source(str(uuid.uuid4()), file_path)

def get_header_code() :
    with open(Path.CODE_HEADER_FILE_NAME) as header :
        return header.read()