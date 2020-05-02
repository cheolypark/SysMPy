from threading import Thread, Event
from flask import Flask, render_template, request
import html
from flask_socketio import SocketIO, emit
import ast
from threading import Lock
import threading
import time

"""
    We use a thread for the flask web server with the SocketIO.
    A cell in a Jupyterlab or notebook doesn't allow to be blocked by a web server's listening.
    So, a thread is used to make the web server and it can listen the client message without blocking the cell.
    
    Message Flows of this Flask Socket Thread
    
    
    
     +----------------+     Connect     +-----------------+   
     |                |---------------->|                 |
     |  Web Client 1  |      Index      |     Flask       |
     |    (SysMPy)    |<----------------|     Socket      |        
     |   (Action D')  |     Update S    |     Thread      |
     |                |---------------->|(Web Distributor)|
     +----------------+                 +-----------------+
              ^                                  | Update C
              |                                  |
              -----------------------------------+
              |                                  |
              v                                  v
     +----------------+                 +----------------+
     |                |                 |                |
     |                |                 |                |
     |  Web Client 2  |                 |  Web Client 3  |
     |   (Block D')   |                 |    (Chart D')  |
     |                |                 |                |
     +----------------+                 +----------------+
 
"""

thread_lock = Lock()


class FlaskSocketThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.updated_events = []

    def message_broadcast(self):
        print("Start the message broadcast")
        while not self.thread_stop_event.isSet():
            self.socketio.sleep(0.5)
            while len(self.updated_events) > 0:
                thread_lock.acquire()
                # print(self.updated_events)
                evt = self.updated_events.pop(0)
                thread_lock.release()
                # print(f'Update this[{evt}]')

                self.socketio.emit('sim_updated', {'data': evt}, namespace='/socket')
                self.socketio.sleep(0.5)

    def run(self):
        print('Start the flask server')
        # 1. Create a Flask server
        self.app = Flask(__name__, static_url_path='', static_folder='')
        # self.app.config['SECRET_KEY'] = 'secret!'
        self.app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50 Mb limit
        self.app.config['MAX_COOKIE_SIZE'] = 50 * 1024 * 1024  # 50 Mb limit


        # 2. Create a Flask socketio
        self.socketio = SocketIO(self.app)

        # 3. Create a thread for the message broadcast
        self.message_thread = Thread()
        self.thread_stop_event = Event()


        #==========================================================================================#
        #                                   Main address
        #==========================================================================================#
        @self.app.route('/', methods=['GET'])
        def index():
            if request.method == 'GET':
                return render_template('<html><body> Select a view type (e.g., ?v=\'AD\') </body> </html>')

            return '<html><body> Hello! </body> </html>'

        # ==========================================================================================#
        #                                   Action Diagram
        # ==========================================================================================#
        @self.app.route('/ad', methods=['GET'])
        def ad():
            print('Show AD')
            if request.method == 'GET':
                """
                Take an updated data from the url parameters
                e.g., ) ?g=var A_process = graph.insertVertex(parent, \'A process\', \'\', 15.0, 42.0, 30, 30, \'Process\')'
                """

                ad_model = request.args.get('g')
                print(ad_model)
                if ad_model is None:
                    ad_model = 'var A_process = graph.insertVertex(parent, \'A process\', \'\', 105.0, 142.0, 30, 30, \'Process\')'

                ad_model = ad_model.replace("/n", "\n")
                ad_model = html.unescape(ad_model)
                return render_template('mx_ad_view.html', ad_model=ad_model)

            return '<html><body> Hello! </body> </html>'

        # ==========================================================================================#
        #                                   Block Diagram
        # ==========================================================================================#
        @self.app.route('/bd', methods=['GET'])
        def bd():
            if request.method == 'GET':
                """
                Take an updated data from the url parameters
                e.g., ) ?g=var A_process = graph.insertVertex(parent, \'A process\', \'\', 15.0, 42.0, 30, 30, \'Process\')'
                """

                print('Show BD')
                bd_model = request.args.get('g')
                print(bd_model)
                if bd_model is None:
                    bd_model = 'var A_process = graph.insertVertex(parent, \'A process\', \'\', 105.0, 142.0, 30, 30, \'Process\')'

                bd_model = bd_model.replace("/n", "\n")
                bd_model = html.unescape(bd_model)
                return render_template('mx_bd_view.html', bd_model=bd_model)

            return '<html><body> Hello! </body> </html>'

        # ==========================================================================================#
        #                              Hierarchy Diagram
        # ==========================================================================================#
        @self.app.route('/hd', methods=['GET'])
        def hd():
            if request.method == 'GET':
                """
                Take an updated data from the url parameters
                e.g., ) ?g=var A_process = graph.insertVertex(parent, \'A process\', \'\', 15.0, 42.0, 30, 30, \'Process\')'
                """

                print('Show HD')
                hd_model = request.args.get('g')
                print(hd_model)
                if hd_model is None:
                    bd_model = 'var A_process = graph.insertVertex(parent, \'A process\', \'\', 105.0, 142.0, 30, 30, \'Process\')'

                hd_model = hd_model.replace("/n", "\n")
                hd_model = html.unescape(hd_model)
                return render_template('mx_hd_view.html', hd_model=hd_model)

            return '<html><body> Hello! </body> </html>'

        # ==========================================================================================#
        #                              Property Chart viewer address
        # ==========================================================================================#
        @self.app.route('/pc', methods=['GET'])
        def pc():
            """
                When the chart_view is initialized, multiple charts are created.
                e.g.,)
                <div class="grid-container">
                  <div class="grid-item">
                      <div id="linechart" name="size" style="width: 400; height: 300"></div>
                  </div>
                  <div class="grid-item">
                        <div id="linechart2" name="speed" style="width: 400; height: 300"></div>
                  </div>
                </div>
            """
            ids = ''
            chart_html = ''

            if request.method == 'GET':
                properties = request.args.get('g')
                properties = ast.literal_eval(properties)
                print(properties)
                ids += 'var ids = ['
                chart_html += '<div class="grid-container">'
                for k, v in properties.items():
                    chart_html += '<div class="grid-item">'
                    chart_html += f'<div id="{k}" name="{k}" style="width: 400; height: 300"></div>'
                    chart_html += '</div>'
                    ids += f'"{k}", '
                chart_html += '</div>'
                ids += ']'
            else:
                chart_html += '''<div class="grid-container">
                                      <div class="grid-item">
                                          <div id="linechart" name="size" style="width: 400; height: 300"></div>
                                      </div>
                                    </div>
                                   '''

            return render_template('chart_line_multi_vars.html', ids=ids, chart_html=chart_html)
        # ==========================================================================================#
        #                                Simulation Update address
        # ==========================================================================================#
        @self.app.route('/sim_udpated', methods=['GET', 'POST'])
        def mx_changed():
            print('Simulation data was updated')

            if request.method == 'POST':
                print(request)

            if request.method == 'GET':
                data = request.args.get('g')
                thread_lock.acquire()
                print(f'new data was received {data}')
                self.updated_events.append(data)
                thread_lock.release()

                return f' updated => {data} '

            print(self.updated_events)

            return '<html><body> updated events! </body> </html>'

        # ==========================================================================================#
        #                               Socketio connect address
        # ==========================================================================================#
        @self.socketio.on('connect', namespace='/socket')
        def test_connect():
            # need visibility of the global thread object
            global message_thread

            current_socket_id = request.sid

            print(f'A client ({current_socket_id}) was connected')

            # Start the random number generator thread only if the thread has not been started before.
            # if not thread.is_alive():
            message_thread = self.socketio.start_background_task(self.message_broadcast)

        # ==========================================================================================#
        #                              Socketio disconnect address
        # ==========================================================================================#
        @self.socketio.on('disconnect', namespace='/socket')
        def test_disconnect():

            current_socket_id = request.sid

            print(f'A client ({current_socket_id}) was disconnected')



        # Execute Socketio
        self.srv = self.socketio.run(self.app, host='127.0.0.1', port=9191)

    def shutdown(self):
        self.srv.shutdown()


def start_server():
    flask_thread = FlaskSocketThread()
    flask_thread.start()
    time.sleep(.9)

# start_server()