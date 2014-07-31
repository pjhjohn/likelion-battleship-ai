# -*- coding : utf-8 -*-
from flask import Flask, request, session, g, redirect, url_for, render_template, abort
#from Crypto.PublicKey import RSA
#from base64 import b64decode
import pymysql
from time import time
import os.path
from os import mkdir
from glob import glob
import datetime
from bs4 import BeautifulSoup as BS
import json


app = Flask(__name__)
app.config.from_pyfile('ai.cfg')

def get_db():
    if not hasattr(g,'db'):
        g.db = pymysql.connect(host='54.193.111.125', port=3306, user='likelion', passwd='likelion', db='battleship')
        cur = g.db.cursor()
        cur.execute('SET NAMES utf8')
    return g.db

# def get_rsa_key():
#   if not hasattr(g, 'RSAKey'):
#       g.RSAKey = RSA.generate(1024)
#   return g.RSAKey


def is_login():
    return 'userid' in session and 'userlevel' in session

def is_admin():
    return is_login() and int(session['userlevel']) > 1

@app.route('/')
def index():
    if 'userid' not in session:
        return redirect(url_for('login'))
    return render_template('index.html')




################# admin ##################
@app.route('/admin')
def admin():
    if not is_login():
        return redirect(url_for('login'))
    if not is_admin():
        return redirect(url_for('index'))


    query = "SELECT * FROM users "+("WHERE schoolId=(SELECT schoolId FROM users WHERE ID = '"+session['userid']+"')" if int(session['userlevel']) < 3 else '')
    db = get_db()
    cur = db.cursor(pymysql.cursors.DictCursor)
    cur.execute(query)
    res = cur.fetchall()
    return render_template('admin.html', current = request.path[1:],users = res)


################## code management ###############
@app.route('/code')
def code():
    if 'userid' not in session:
        return redirect(url_for('login'))


    filelist = glob('codes/'+str(session['userid'])+'/*.py')
    filelist.reverse()
    files=[]
    for file in filelist:
        f = open(file)
        files.append({
            'time':datetime.datetime.fromtimestamp(int(file.split('/')[2].split('.')[0])).strftime('%Y-%m-%d %H:%M:%S'),
            'code':f.read()
            })
        f.close
    return render_template('code.html', current = request.path[1:],files=files, filecount = len(files))


@app.route('/submit_code', methods = ["POST"])
def submit_code():
    if not is_login():
        return '1'

    code = request.form['new']
    dirpath = 'codes/'+str(session['userid'])
    if not os.path.isdir(dirpath):
        mkdir(dirpath)

    fileName = str(int(time()))
            
    f = open(dirpath+"/"+fileName+".py", 'w')
    f.write(code.encode('utf8'))
    f.close()

    query = "INSERT INTO codes (userId,fileName) VALUES ('"+str(session['userid'])+"','"+fileName+"')"
    db = get_db()
    cur = db.cursor()
    cur.execute(query)
    db.commit()

    # code test here

    if request.referrer and request.referrer.split('/')[-1] == 'test':
        return '0'
    return redirect(url_for('code'))


################## code test ############
@app.route('/test')
def test():
    return render_template('test.html', current = request.path[1:])


@app.route('/run_test')
def run_test():

    return '0'


################## ship placement ###############
@app.route('/ship')
def ship():
    if not is_login():
        return redirect(url_for('login'))

    query = "SELECT * FROM shipPlacement WHERE userId = '"+str(session['userid'])+"' ORDER BY uploadedTime DESC"
    db = get_db()
    cur = db.cursor(pymysql.cursors.DictCursor)
    cur.execute(query)
    res = cur.fetchall()

    


    for i in range(len(res)):
        positions = json.loads(res[i]['placement'])
        
        activePositions = []
        for position in positions:
            startRow = int(position['location']['y'])
            
            startCol = int(position['location']['x'])
            for l in range(int(position['size'])):
                if position['direction'] == 'x':
                    activePositions.append((startRow,startCol+l))
                else :
                    activePositions.append((startRow+l,startCol))

        bs = BS('<table class="ship-placement"></table>')
        for j in range(10):
            row = BS('<tr data-row="'+str(j)+'"></tr>')
            for k in range(10):
                row.tr.append(BS('<td data-col="'+str(k)+'" '+('class="placed"' if (j,k) in activePositions else '')+'></td>'))
            bs.table.append(row)

        res[i]['placement'] = str(bs)

        
        



    return render_template('ship.html', current = request.path[1:],placementList = res, placementCount = len(res))

@app.route('/submit_placement',methods = ['POST'])
def submit_placement():
    if not is_login():
        return '1'

    placement = request.form['placement']
    query = "INSERT INTO shipPlacement (userId,placement) VALUES ('"+str(session['userid'])+"','"+placement+"')"
    db = get_db()
    cur = db.cursor()
    cur.execute(query)
    db.commit()
    return '0'



#################### auth ######################
@app.route('/join', methods = ['POST'])
def join():
    salt = app.config['SALT']
    email = request.form['email']
    password = request.form['password']
    query = "SELECT ID FROM users WHERE email='"+email+"'"
    db = get_db()
    cur = db.cursor()
    cur.execute(query)
    if cur.rowcount:
        # duplicated email
        return '1'
    else:
        # insert to db
        query = "INSERT INTO users (email, password) VALUES ('"+email+"',password('"+password+salt+"'))"
        cur.execute(query)
        db.commit()
        return '0'

@app.route('/login')
def login():
    if is_login():
        return redirect(url_for('index'))

    query = "SELECT * FROM schoolList"
    db = get_db()
    cur = db.cursor(pymysql.cursors.DictCursor)
    cur.execute(query)
    res = cur.fetchall()



    return render_template('login.html',schoolList = res)

@app.route('/login_submit', methods=['POST'])
def login_submit():
    email = request.form['email']
    password = request.form['password']+app.config['SALT']
    query = "SELECT * FROM users WHERE email = '"+email+"' AND password = password('"+password+"')"
    db = get_db()
    cur = db.cursor(pymysql.cursors.DictCursor)
    cur.execute(query)
    if cur.rowcount == 1:
        res = cur.fetchone()
        session['userid'] = res['ID']
        session['userlevel'] = res['userLevel']
        return '0'
    else:
        #fail
        return '1'

@app.route('/logout')
def logout():
    session.pop('userid',None)
    session.pop('userlevel',None)
    return redirect(url_for('login'))

# @app.route('/publickey')
# def request_public_key():
#   if request.referrer and request.referrer.split('/')[-1] == 'login':
#       return get_rsa_key().publickey().exportKey()
#   else: abort(404)



if __name__ == '__main__':

    app.debug = True
    app.run(host = '0.0.0.0', port = 8000)
