from flask import redirect, url_for, json, request, render_template
from application import app
from application.models.ship_management import *
from application.lib.auth import *
from bs4 import BeautifulSoup as BS
from application.constants import *


@app.route('/ship')
def ship():
    if not is_login():
        return redirect(url_for('login'))

    res = get_placements(session[KEY_USER_ID])

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

    add_placement(session[KEY_USER_ID],request.form['placement'])
    return '0'
