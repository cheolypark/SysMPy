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

from entity import *
from code_gui.gui_mxgraph_action_diagram import *

import core

#sys.path.insert(0, os.path.abspath('..\..\core'))
#sys.path.insert(0, os.path.abspath('..\..\code_gui'))

# p를 다루자
class aaa(RequestHandler):
    def get(self):
        my_graph = self.get_arguments("evt")
        my_graph = str(my_graph[0])
        my_graph = my_graph.replace("/n", "\n")
        entt = Entity.get( "Root Process" )
        self.write( my_graph )

        aaa = entt.get("신규액션" )
        print( id( aaa ) )


# /ad_sample/ 핸들러
class ActionDiagramSampleHandler(RequestHandler):
    def get(self):
        p = Process("Root Process")
        p1, p2 = p.Condition("한글 컨디션 입니다. 이것은 테스트 ", "P1", "P2")
        p_act1 = p1.Action("Action1")
        p3, p4 = p1.Condition("Condition 2", "P3", "P4")
        p2_act1 = p2.Action("신규액션")
        p_act1 = p3.Action("Action2")
        p_act2 = p4.Action("Action3")
        p.Action("Action4")
        p.Action("Action5")
        gad = GuiMXGraphActionDiagram()
        my_graph = gad.get_mxgraph( p )
        my_graph = my_graph.replace("/n", "\n")
        self.write(ad_script.mxGraph_start_nice_label + ad_script.mxGraph_styles + my_graph + ad_script.mxGraph_end)
        self.render('simple_mx_web.html')


class DiagramModifyHandler(RequestHandler):
    def get(self):
        my_graph = self.get_arguments("g")
        my_graph = str(my_graph[0])
        my_graph = my_graph.replace("/n", "\n")

        self.write(ad_script.mxGraph_start_nice_label + ad_script.mxGraph_styles + my_graph + ad_script.mxGraph_end)
        index = 'simple_mx_web.html'
        self.render(index)


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
                                    (r"/HD/", HierarchyDiagramHandler),
                                    (r"/ad_sample/", ActionDiagramSampleHandler),
                                    (r"/dmh/", DiagramModifyHandler),
                                    (r"/aaa/", aaa)
                                    ] )

        http_server = tornado.httpserver.HTTPServer(application, max_header_size=1024 ** 3)
        http_server.listen(options.port)
        tornado.ioloop.IOLoop.current().start()

TornadoMXServer().run()