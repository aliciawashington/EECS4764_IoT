import os
from flask import Flask, render_template, request
from flask_socketio import SocketIO
from random import random
from threading import Lock
from datetime import datetime
from time import sleep
import db


"""
Background Thread
"""
thread = None
thread_lock = Lock()

app = Flask(__name__)
#app.config['SECRET_KEY'] = 'thatscrazy'
#import pdb; pdb.set_trace()
app.config.from_mapping(
    SECRET_KEY='thatscrazy',
    DATABASE=os.path.join(app.instance_path, 'app.sqlite3')
)
socketio = SocketIO(app, cors_allowed_origins='*')

# ensure the instance folder exists
try:
    os.makedirs(app.instance_path)
except OSError:
    pass

db.init_app(app)

"""
Get current date time
"""
def get_current_datetime():
    now = datetime.now()
    return now.strftime("%m/%d/%Y %H:%M:%S")


"""
Generate random sequence of dummy sensor values and send it to our clients
"""
def background_thread():
    print("Generating random sensor values")
    while True:
        dummy_sensor_value = round(random() * 100, 3)
        socketio.emit('updateSensorData', {'value': dummy_sensor_value, "date": get_current_datetime()})
        socketio.sleep(1)
        print("Inserting Data into database")
        db.insert_data(dummy_sensor_value)
        sleep(1)
        db.get_data()
        print("Reading Data from database")



"""
Serve root index file
"""
@app.route('/')
def index():
    return render_template('index.html')

#"""Serve the database updates"""
#@app.route('/update', methods=['GET'])

"""
Decorator for connect
"""
@socketio.on('connect')
def connect():
    global thread
    print('Client connected')

    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(background_thread)

"""
Decorator for disconnect
"""
@socketio.on('disconnect')
def disconnect():
    print('Client disconnected',  request.sid)

if __name__ == '__main__':
    socketio.run(app, port=4999, host='0.0.0.0', debug=True)