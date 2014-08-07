from flask import redirect, url_for, request, render_template
from application import app
from application.const import *
from application.lib.auth import *
from application.models import fleet_manager
from bs4 import BeautifulSoup
import json

@app.route('/fleet')
def fleet() :
    if not is_login() :
        return redirect(url_for('login'))
    fleets = fleet_manager.get_fleets(session[Key.USER_ID])
    for i in range(len(fleets)) :
        positions = json.loads(fleets[i]['deployment'])
        active_positions = []
        for position in positions :
            start_row = int(position['location']['y'])
            start_col = int(position['location']['x'])
            for j in range(int(position['size'])) :
                if position['direction'] == 'x' :
                    active_positions.append((start_row, start_col + j))
                else :
                    active_positions.append((start_row + j, start_col))

        soup = BeautifulSoup('<table class="fleet-deployment"></table>', 'html.parser')
        for x in range(10) :
            row = BeautifulSoup('<tr data-row="%d"></tr>' % x, 'html.parser')
            for y in range(10) :
                row.tr.append(BeautifulSoup('<td data-col="%d" %s></td>' % (y, ['','class="deployed"'][(y,x) in active_positions]), 'html.parser'))
            soup.table.append(row)
        fleets[i]['deployment'] = str(soup)

    return render_template('fleet.html', current = request.path[1:], fleet_list = fleets, fleet_count = len(fleets))

@app.route('/submit_fleet', methods = ['POST'])
def submit_fleet() :
    if not is_login() or not request.method == 'POST':
        return '1'
    fleet_manager.add_fleet(session[Key.USER_ID], request.form['deployment'])
    return '0'