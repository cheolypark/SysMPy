from werkzeug.serving import make_server
import threading
from flask import Flask, render_template, request
import html


class ServerThread(threading.Thread):
    def __init__(self, app):
        threading.Thread.__init__(self)
        self.srv = make_server('127.0.0.1', 9191, app)
        self.ctx = app.app_context()
        self.ctx.push()

    def run(self):
        # print('starting server-')
        self.srv.serve_forever()

    def shutdown(self):
        self.srv.shutdown()


def start_server():
    global server
    app = Flask(__name__, static_url_path='', static_folder='')

    server = ServerThread(app)
    server.start()
    # print('server started')

    @app.route('/')
    def flask_app():
        # mx_model = "var A_process = graph.insertVertex(parent, 'A process', '', 105.0, 42.0, 30, 30, 'Process') /n var A_1_a = graph.insertVertex(parent, 'A.1 a', 'a', 80.0, 84.0, 80, 30, 'Action') /n var A_process_A_1_a = graph.insertEdge(parent, null, '', A_process, A_1_a, 'Arrow_Edge_Process' ) /n var A_process_END = graph.insertVertex(parent, 'A process_END', '', 105.0, 126.0, 30, 30, 'Process_END') /n var A_1_a_A_process_END = graph.insertEdge(parent, null, '', A_1_a, A_process_END, 'Arrow_Edge_Process' ) /n"
        # mx_model = 'var A_process = graph.insertVertex(parent, \'A process\', \'\', 105.0, 42.0, 30, 30, \'Process\')'

        mx_model = request.args.get('g')
        if mx_model is None:
            mx_model = 'var A_process = graph.insertVertex(parent, \'A process\', \'\', 105.0, 42.0, 30, 30, \'Process\')'

        mx_model = mx_model.replace("/n", "\n")
        mx_model = html.unescape(mx_model)

        # return '<html><body> hi </body> </html>'
        return render_template('view.html', mx_model=mx_model)


def stop_server():
    global server
    server.shutdown()