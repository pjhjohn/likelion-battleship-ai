from flask import render_template, request
from application import app


@app.route('/test')
def test():
    return render_template('test.html', current = request.path[1:])


@app.route('/run_test')
def run_test():

    return '0'