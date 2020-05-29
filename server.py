
# Start with a basic flask app webpage.
from flask_socketio import SocketIO, emit
from flask import Flask, render_template, url_for, copy_current_request_context
from random import random
from time import sleep
from threading import Thread, Event
import json
import urllib3

__author__ = 'slynn'

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['DEBUG'] = True

#turn the flask app into a socketio app
socketio = SocketIO(app, async_mode=None, logger=True, engineio_logger=True)

#random number Generator Thread
thread = Thread()
thread_stop_event = Event()

def getBTC():
    while not thread_stop_event.isSet():
        http = urllib3.PoolManager()
        response = http.request('GET',"https://api.tidex.com/api/3/ticker/eth_btc")
        values = json.loads(response.data)
        socketio.emit('newnumber', {'bid': str(values['eth_btc']['buy']),'ask': str(values['eth_btc']['sell']),'vol': str(values['eth_btc']['sell'])}, namespace='/test')
        socketio.sleep(1)

@app.route('/')
def index():
    #only by sending this page first will the client be connected to the socketio instance
    return render_template('index.html')

@socketio.on('connect', namespace='/test')
def test_connect():
    # need visibility of the global thread object
    global thread
    print('Client connected')

    #Start the random number generator thread only if the thread has not been started before.
    if not thread.isAlive():
        thread = socketio.start_background_task(getBTC)

@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected')


if __name__ == '__main__':
    socketio.run(app)