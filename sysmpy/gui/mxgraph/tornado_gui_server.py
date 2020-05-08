import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.web import StaticFileHandler
from tornado.web import Application, RequestHandler
from sysmpy.gui.mxgraph.script_sample import *
from tornado.options import define, options
import socket
import tornado.escape
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.websocket
import os.path
import uuid
import ast

from sysmpy.gui.gui_config import gui_server_address

#=================================================================================================#
#                                           Main Handler                                          #
#=================================================================================================#
class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('gui_index.html')

#=================================================================================================#
#                                     Property Chart Handler                                      #
#=================================================================================================#
class PropertyChartHandler(tornado.web.RequestHandler):
    def get(self):
        """
            # http://127.0.0.1:9191/pc/?g={'x':0, 'y':0}
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

        properties = self.get_arguments("g")[0]
        properties = ast.literal_eval(properties)

        # print(properties)
        ids += 'var ids = ['
        chart_html += '<div class="grid-container">'
        for k, v in properties.items():
            chart_html += '<div class="grid-item">'
            chart_html += f'<div id="{k}" name="{k}" style="width: 200; height: 150"></div>'
            chart_html += '</div>'
            ids += f'"{k}", '
        chart_html += '</div>'
        ids += ']'

        self.render("chart_line_multi_vars.html", ids=ids, chart_html=chart_html)


#=================================================================================================#
#                                     Property Table Handler                                      #
#=================================================================================================#
class PropertyTableHandler(tornado.web.RequestHandler):
    def get(self):
        """
            # http://127.0.0.1:9191/pt/?g={'x':0, 'y':'0', 'z':'true'}
            e.g.,)
            columns =
            "data.addColumn('string', 'Name');
            data.addColumn('number', 'Salary');
            data.addColumn('boolean', 'Full Time Employee');"
        """
        columns = ''

        properties = self.get_arguments("g")[0]
        properties = ast.literal_eval(properties)

        # print(properties)
        for k, v in properties.items():
            if isinstance(v, str):
                if v == 'true':
                    type_val = 'boolean'
                else:
                    type_val = 'string'
            else:
                type_val = 'number'

            columns += f'data.addColumn("{type_val}", "{k}");  '

        self.render('table_multi_vars.html', columns=columns)


#=================================================================================================#
#                                  Simulation Update Handler                                      #
#=================================================================================================#
class SimUpdateHandler(tornado.web.RequestHandler):
    def get(self):
        """
            # http://127.0.0.1:9191/sim_updated?g={'x':0, 'y':0}
        """
        # print('Simulation data was updated')

        data = self.get_arguments("g")[0]
        GuiSocketHandler.updated_events.append(data)
        GuiSocketHandler.send_to_clients()

#=================================================================================================#
#                                     Action Diagram Handler                                      #
#=================================================================================================#
class ActionDiagramHandler(RequestHandler):
    def get(self):
        my_graph = self.get_arguments("g")
        if len(my_graph) == 0:
            my_graph = """var A_process = graph.insertVertex(parent, 'A process', '', 105.0, 42.0, 30, 30, 'Process') """
        else:
            my_graph = str(my_graph[0])
            my_graph = my_graph.replace("/n", "\n")
            my_graph = my_graph.replace("/", ";")

        mxClient_js = f"<script type='text/javascript' src='http://{gui_server_address}:9191/src/js/mxClient.js'></script>"

        self.render("mx_ad_view.html", ad_model=my_graph, mxClient_js=mxClient_js)

#=================================================================================================#
#                                      Block Diagram Handler                                      #
#=================================================================================================#
class BlockDiagramHandler(RequestHandler):
    def get(self):
        # print('BlockDiagramHandler')
        my_graph = self.get_arguments("g")
        if len(my_graph) == 0:
            my_graph = """var c3 = graph.insertVertex(parent, 'idc3','Process 1', 150,30,100,200,'Process;');
                          var c31 = graph.insertVertex(c3,null,'', 0,0,100,50,'ProcessImage;image=images/img3.png;');"""
        else:
            my_graph = str(my_graph[0])
            my_graph = my_graph.replace("/n", "\n")
            my_graph = my_graph.replace("/8/", ";")
            # print(my_graph)

        mxClient_js = f"<script type='text/javascript' src='http://{gui_server_address}:9191/src/js/mxClient.js'></script>"

        self.render("mx_bd_view.html",  bd_model=my_graph, mxClient_js=mxClient_js)

#=================================================================================================#
#                                  Hierarchy Diagram Handler                                      #
#=================================================================================================#
class HierarchyDiagramHandler(RequestHandler):
    def get(self):
        my_graph = self.get_arguments("g")
        if len(my_graph) == 0:
            my_graph = """var A_process = graph.insertVertex(parent, 'A process', '', 105.0, 42.0, 30, 30, 'Process') """
        else:
            my_graph = str(my_graph[0])
            my_graph = my_graph.replace("/n", "\n")
            my_graph = my_graph.replace("/", ";")

        mxClient_js = f"<script type='text/javascript' src='http://{gui_server_address}:9191/src/js/mxClient.js'></script>"

        self.render("mx_hd_view.html", hd_model=my_graph, mxClient_js=mxClient_js)

#=================================================================================================#
#                                      Gui Socket Handler                                         #
#=================================================================================================#
class GuiSocketHandler(tornado.websocket.WebSocketHandler):
    waiters = set()
    updated_events = []

    def get_compression_options(self):
        return {}

    def open(self):
        GuiSocketHandler.waiters.add(self)

    def on_close(self):
        GuiSocketHandler.waiters.remove(self)

    @classmethod
    def send_to_clients(cls):
        while len(cls.updated_events) > 0:
            evt = cls.updated_events.pop(0)
            for waiter in cls.waiters:
                time.sleep(0.5)
                try:
                    waiter.write_message(evt)
                except:
                    print("Update error!")

    def on_message(self, message):
        parsed = tornado.escape.json_decode(message)
        chat = {"id": str(uuid.uuid4()), "body": parsed["body"]}
        chat["html"] = tornado.escape.to_basestring(
            self.render_string("message.html", message=chat)
        )

        # ChatSocketHandler.update_cache(chat)
        GuiSocketHandler.send_to_clients()

#=================================================================================================#
#                                     Tornado  Application                                        #
#=================================================================================================#
class Application(tornado.web.Application):
    def __init__(self, images_path=None):
        define("port", default=9191, help="run on the given port", type=int)

        if images_path is None:
            images_path = '/examples/Jupyter_notebook_examples/CyberFactory/images'

        handlers = [(r"/", MainHandler),
                    (r'/src/js/(.*)', StaticFileHandler, {'path': './src/js'}),
                    (r'/src/css/(.*)', StaticFileHandler, {'path': './src/css'}),
                    (r'/src/images/(.*)', StaticFileHandler, {'path': './src/images'}),
                    (r'/images/(.*)', StaticFileHandler, {'path': images_path}),
                    (r"/pt/", PropertyTableHandler),
                    (r"/pc/", PropertyChartHandler),
                    (r"/ad/", ActionDiagramHandler),
                    (r"/bd/", BlockDiagramHandler),
                    (r"/hd/", HierarchyDiagramHandler),
                    (r"/sim_updated", SimUpdateHandler),
                    (r"/guisocket", GuiSocketHandler)]

        settings = dict(
            cookie_secret="__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            xsrf_cookies=True,
        )
        super(Application, self).__init__(handlers, **settings)

def TornadoGuiServer(images_path=None):
    app = Application(images_path)
    http_server = tornado.httpserver.HTTPServer(app, max_header_size=1024 ** 3)

    try:
        http_server.listen(options.port)
    except socket.error as e:
        print(e)

    current = tornado.ioloop.IOLoop.current()
    if current.asyncio_loop.is_running() is False:
        print('Tornado Server runs!')
        current.start()
    else:
        print('We use the existing tornado server!')


def RunServer():
    notebook_path = os.path.abspath('')+'/images'
    # print(notebook_path)
    TornadoGuiServer(images_path=notebook_path)

# if __name__ == "__main__":
#     TornadoGuiServer(images_path=None)
