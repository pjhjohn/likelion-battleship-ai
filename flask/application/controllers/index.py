from flask import render_template, redirect, url_for, session
from application.lib.auth import *
from application import app
from application.constants import *


@app.route('/')
def index():
    if not is_login():
        return redirect(url_for('login'))
    return render_template('index.html')
