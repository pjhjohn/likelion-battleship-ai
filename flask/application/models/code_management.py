from database import *
from application.constants import *
from os import mkdir, remove
import imp
import uuid
from application.lib.game import ai, game
from ship_management import *

def add_code(userId, code):
    dirpath = UPLOAD_DIR+'/'+str(userId)
    if not os.path.isdir(dirpath):
        mkdir(dirpath)

    encodedCode = code.encode('utf8')

    fileName = str(int(time()))

    codeHeaderFile = open(CODE_HEADER_FILE_NAME)
    codeHeader = codeHeaderFile.read()
    codeHeaderFile.close()

            
    f = open(dirpath+"/"+fileName+".py", 'w')
    f.write(code.encode('utf8'))
    f.close()

    f = open(dirpath+"/"+UPLOAD_PREFIX+fileName+".py",'w')
    f.write(codeHeader + encodedCode)
    f.close()


    error = False
    # code test
    try:
        testModule = import_from_file(dirpath+"/"+UPLOAD_PREFIX+fileName+".py")
    except: error = True

    shipPlacement = get_last_placement(userId)
    enemyModule = ai

    if not error:
        try:
            game.game(shipPlacement, shipPlacement, testModule, enemyModule)
        except:
            error = True

    return insert_query(query = "INSERT INTO codes (userId,fileName, hasError) VALUES ('"+str(userId)+"','"+fileName+"', '"+('1' if error else '0')+"')")

def get_codes(userId):
    query = "SELECT * FROM codes WHERE userId = '"+str(userId)+"' ORDER BY uploadedTime DESC"

    res = select_query(query)

    codes = []
    for row in res:
        code = open(UPLOAD_DIR+'/'+str(userId)+'/'+row[COL_FILE_NAME]+'.py').read()
        row[KEY_CODE] = code
        codes.append(row)

    return codes

def get_code_path(userId):
    return UPLOAD_DIR+'/'+str(userId)+'/'
    

def get_latest_code_file_name(userId, withHeader = False):
    query = "SELECT fileName FROM codes WHERE userId = '"+str(userId)+"' AND hasError = '0' ORDER BY uploadedTime DESC LIMIT 1"
    res = select_query(query)
    if len(res) == 0 :
        return None
    else:
        return (UPLOAD_PREFIX if withHeader else '') + res[0][COL_FILE_NAME]

# return latest code file as module
def get_latest_code(userId):
    
    fileName = get_latest_code_file_name(userId, True)
    
    return import_from_file(get_code_path(userId)+fileName+".py")

    #userai = imp.load_source(str(uuid.uuid4()),get_code_path(userId)+fileName+".py")
    

    #return userai

def import_from_file(filePath):
    return imp.load_source(str(uuid.uuid4()), filePath)

def get_header_code():
    with open(CODE_HEADER_FILE_NAME) as headerFile:
        return headerFile.read()

