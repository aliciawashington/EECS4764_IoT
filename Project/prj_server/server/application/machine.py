import os

from datetime import datetime
from flask import g, Blueprint, render_template, url_for, request, redirect
from application.db import get_db
from application.uconfig import API_KEY, MAC_ADDRESS, MACHINE_NAME

bp = Blueprint("machine", __name__, url_prefix='/machine')

@bp.route("/")
def index():
    db = get_db()
    # Do a db.execute to grab data
    return render_template("machine/index.html")

@bp.route("/add_data/API_key=<api_key>/mac=<mac>/field=<int:field>/data=<data>", methods=("GET", "POST"))
def add_data(api_key, mac, field, data):
    db = get_db()

    if  request.method == 'POST':
        if (api_key==API_KEY and mac==MAC_ADDRESS):
            
            db.execute(
            "INSERT INTO machine_stats(api_key, mac_address, machine_name, field, data_point) VALUES (:api_key, :mac_address, :machine_name, :field, :data_point)",
            {
                'api_key': api_key,
                'mac_address': mac,
                'machine_name': MACHINE_NAME,
                'field': field,
                'data_point': data
            }
        )
            db.commit()

            return redirect(url_for("machine.index"))
            
        else:
            return render_template('403.html')
        
@bp.route("/update")       
def update():
    db = get_db()
    now  = datetime.now()
    datetimeString = now.strftime("%m/%d/%Y %H:%M:%S")
    last_data_pt = db.execute(
        "SELECT machine_name, field, data_point, created, MAX(rowid) FROM machine_stats"
        ).fetchone()

    templateData = {
            "data": last_data_pt["data_point"],
            "time_stamp": datetimeString
        }

    return render_template("machine/update.html", **templateData)
