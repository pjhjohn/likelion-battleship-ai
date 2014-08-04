from flask import redirect, url_for, session, render_template, request
from application import app
import time


@app.route('/bugreport', methods = ['POST'])
def bugreport():
    title = request.form['title'].encode('utf8')
    body = request.form['body'].encode('utf8')
    f = open('bugreport/'+str(int(time.time()))+".txt",'w')
    f.write(title)
    f.write('\n\n')
    f.write(body)
    f.close()
    return '0'
