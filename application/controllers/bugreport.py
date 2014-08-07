from flask import request
from application import app
import time

@app.route('/bugreport', methods = ['POST'])
def bugreport() :
	title = request.form['title'].encode('utf-8')
	body = request.form['body'].encode('utf-8')
	with open('bugreport/%d.txt' % int(time.time()), 'w') as report :
		report.write(title + '\n\n' + body)
	return '0'