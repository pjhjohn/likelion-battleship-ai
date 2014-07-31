from database import *
from application.constants import *
from os import mkdir
import imp

def add_code(userId, code):
    dirpath = UPLOAD_DIR+'/'+str(userId)
    if not os.path.isdir(dirpath):
        mkdir(dirpath)

    fileName = str(int(time()))
            
    f = open(dirpath+"/"+fileName+".py", 'w')
    f.write(code.encode('utf8'))
    f.close()

    return insert_query(query = "INSERT INTO codes (userId,fileName) VALUES ('"+str(userId)+"','"+fileName+"')")

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
    

def get_latest_code_file_name(userId):
    query = "SELECT fileName FROM codes WHERE userId = '"+str(userId)+"' AND hasError = '0' ORDER BY uploadedTime DESC LIMIT 1"
    res = select_query(query)
    if len(res) == 0 :
        return None
    else:
        return res[0][COL_FILE_NAME]

# return latest code file as module
# latest code has only 'guess' function
def get_latest_code(userId):
    # add path
    filePath = os.path.join(os.path.dirname(__file__), get_code_path(userId))


    # get file name
    fileName = get_latest_code_file_name(userId)

    userai = imp.load_source('userai',filePath+fileName+".py")

    
    return userai

