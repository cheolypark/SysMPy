from threading import Thread, Event
from flask import Flask, render_template, request
import html
from flask_socketio import SocketIO, emit

import threading
import time

"""
    We use a thread for the flask web server with the SocketIO.
    A cell in a Jupyterlab or notebook doesn't allow to be blocked by a web server's listening.
    So, a thread is used to make the web server and it can listen the client message without blocking the cell.
    
    Message Flows of this Flask Socket Thread
    
    
    
     +----------------+      Connect    +----------------+   
     |                |---------------->|                |
     |                |     Index       |     Flask      |
     |  Web Client 1  |<----------------|     Socket     |        
     |  (Action D')   |    Update S     |     Thread     |
     |                |---------------->|                |
     +----------------+                 +----------------+
              ^                                  | Update C
              |                                  |
              -----------------------------------+
              |                                  |
              v                                  |
     +----------------+                 +----------------+
     |                |                 |                |
     |                |                 |                |
     |  Web Client 2  |                 |  Web Client 3  |
     |   (Block D')   |                 |    (Chart D')  |
     |                |                 |                |
     +----------------+                 +----------------+
 
"""


class FlaskSocketThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.updated_sim = None

    def message_broadcast(self):
        print("Start the message broadcast")
        while not self.thread_stop_event.isSet():
            self.socketio.sleep(5)
            if self.updated_sim is not None:
                print(f'Update this[{self.updated_sim}]')
                self.socketio.emit('sim_updated', {'data': self.updated_sim}, namespace='/socket')
                self.updated_sim = None

    def run(self):
        print('Start the flask server')
        # 1. Create a Flask server
        self.app = Flask(__name__, static_url_path='', static_folder='')
        self.app.config['SECRET_KEY'] = 'secret!'

        # 2. Create a Flask socketio
        self.socketio = SocketIO(self.app)

        # 3. Create a thread for the message broadcast
        self.message_thread = Thread()
        self.thread_stop_event = Event()

        @self.app.route('/', methods=['GET'])
        def index():
            if request.method == 'GET':
                """
                Take an updated data from the url parameters
                e.g., ) ?v=AD&g=var A_process = graph.insertVertex(parent, \'A process\', \'\', 15.0, 42.0, 30, 30, \'Process\')'
                """
                view = request.args.get('v').lower()
                print(view)
                if 'ad' in view: # Action diagram
                    print('Show AD')
                    ad_model = request.args.get('g')
                    print(ad_model)
                    if ad_model is None:
                        ad_model = 'var A_process = graph.insertVertex(parent, \'A process\', \'\', 105.0, 142.0, 30, 30, \'Process\')'

                    ad_model = ad_model.replace("/n", "\n")
                    ad_model = html.unescape(ad_model)
                    return render_template('mx_ad_view.html', ad_model=ad_model)
                elif 'bd' in view: # Block diagram
                    print('Show BD')
                    bd_model = request.args.get('g')
                    print(bd_model)
                    if bd_model is None:
                        bd_model = 'var A_process = graph.insertVertex(parent, \'A process\', \'\', 105.0, 142.0, 30, 30, \'Process\')'

                    bd_model = bd_model.replace("/n", "\n")
                    bd_model = html.unescape(bd_model)
                    return render_template('mx_bd_view.html', bd_model=bd_model)
                elif 'hd' in view: # Hierarchy diagram
                    pass
                elif 'pc' in view: # Property Chart
                    pass
                else:
                    return render_template('<html><body> Select a view type (e.g., ?v=\'AD\') </body> </html>')

            return '<html><body> Hello! </body> </html>'

        @self.app.route('/sim_udpated', methods=['GET', 'POST'])
        def mx_changed():
            print('Simulation data was updated')

            # global updated_model
            self.updated_sim

            if request.method == 'POST':
                print(request)

            if request.method == 'GET':
                self.updated_sim = request.args.get('g')

            print(self.updated_sim)

            return self.updated_sim

        @self.socketio.on('connect', namespace='/socket')
        def test_connect():
            # need visibility of the global thread object
            global message_thread
            print('A client was connected')

            # Start the random number generator thread only if the thread has not been started before.
            # if not thread.is_alive():
            message_thread = self.socketio.start_background_task(self.message_broadcast)

        @self.socketio.on('disconnect', namespace='/socket')
        def test_disconnect():
            print('A client was disconnected')

        self.srv = self.socketio.run(self.app, host='127.0.0.1', port=9191)

    def shutdown(self):
        self.srv.shutdown()


def start_server():
    mythread = FlaskSocketThread()
    mythread.start()
    time.sleep(.9)

start_server()