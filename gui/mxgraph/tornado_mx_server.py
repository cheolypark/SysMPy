import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.web import StaticFileHandler
from tornado.web import Application, RequestHandler

from tornado.options import define, options

import ad_script
import bd_script
import hd_script


class ActionDiagramHandler(RequestHandler):
    def get(self):
        # my_graph = mxGraph_graph
        my_graph = self.get_arguments("g")
        my_graph = str(my_graph[0])
        my_graph = my_graph.replace("/n", "\n")

        self.write(ad_script.mxGraph_start_nice_label + ad_script.mxGraph_styles + my_graph + ad_script.mxGraph_end)
        index = 'simple_mx_web.html'
        self.render(index)


class BlockDiagramHandler(RequestHandler):
    def get(self):
        # my_graph = mxGraph_graph
        my_graph = self.get_arguments("g")
        my_graph = str(my_graph[0])
        my_graph = my_graph.replace("/n", "\n")

        self.write(bd_script.mxGraph_start_nice_label + bd_script.mxGraph_styles + my_graph + bd_script.mxGraph_end)
        index = 'simple_mx_web.html'
        self.render(index)


class HierarchyDiagramHandler(RequestHandler):
    def get(self):
        # my_graph = mxGraph_graph
        my_graph = self.get_arguments("g")
        my_graph = str(my_graph[0])
        my_graph = my_graph.replace("/n", "\n")

        self.write(hd_script.mxGraph_start_nice_label + hd_script.mxGraph_styles + my_graph + hd_script.mxGraph_end)
        index = 'simple_mx_web.html'
        self.render(index)


class TornadoMXServer():
    def __init__(self):
        define("port", default=8080, help="run on the given port", type=int)

    def run(self):
        tornado.options.parse_command_line()
        application = Application([ (r'/src/js/(.*)', StaticFileHandler, {'path': './src/js'}),
                                    (r'/src/css/(.*)', StaticFileHandler, {'path': './src/css'}),
                                    (r'/src/images/(.*)', StaticFileHandler, {'path': './src/images'}),
                                    (r"/AD/", ActionDiagramHandler),
                                    (r"/BD/", BlockDiagramHandler),
                                    (r"/HD/", HierarchyDiagramHandler)
                                    ] )

        http_server = tornado.httpserver.HTTPServer(application, max_header_size=1024 ** 3)
        http_server.listen(options.port)
        tornado.ioloop.IOLoop.current().start()

TornadoMXServer().run()