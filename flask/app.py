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


app = Flask(__name__)
app.config.from_pyfile('ai.cfg')

def get_db():
	if not hasattr(g,'db'):
		g.db = pymysql.connect(host='54.193.111.125', port=3306, user='likelion', passwd='likelion', db='battleship')
		cur = g.db.cursor()
		cur.execute('SET NAMES utf8')
	return g.db

# def get_rsa_key():
# 	if not hasattr(g, 'RSAKey'):
# 		g.RSAKey = RSA.generate(1024)
# 	return g.RSAKey


@app.route('/')
def index():
	if 'userid' not in session:
		return redirect(url_for('login'))
	return render_template('index.html')


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
	if 'userid' not in session:
		return '1'

	code = request.form['new']
	dirpath = 'codes/'+str(session['userid'])
	if not os.path.isdir(dirpath):
		mkdir(dirpath)

	f = open(dirpath+"/"+str(int(time()))+".py", 'w')
	f.write(code.encode('utf8'))
	f.close()

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
	if 'userid' in session:
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
# 	if request.referrer and request.referrer.split('/')[-1] == 'login':
# 		return get_rsa_key().publickey().exportKey()
# 	else: abort(404)



if __name__ == '__main__':

	app.debug = True
	app.run(host = '0.0.0.0', port = 8000)
	