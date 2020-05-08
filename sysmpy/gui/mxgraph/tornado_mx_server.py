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
from script_sample import *

from sysmpy import *


# /ad_sample/ Handler
class ActionDiagramSampleHandler(RequestHandler):
    def get(self):
        p = getActionScript() # call sample Acton diagram Unified Script
        gad = GuiMXGraphActionDiagram()
        my_graph = gad.get_mxgraph( p )
        my_graph = my_graph.replace("/n", "\n")
        self.write(ad_script.mxGraph_start_nice_label + ad_script.mxGraph_styles + my_graph + ad_script.mxGraph_end)
        self.render('simple_mx_web.html')


# /DM/ Handler
class DiagramModifyHandler(RequestHandler):
    def get(self):
        evt = self.get_arguments("evt")
        evt = str(evt[0])
        evt = evt.replace("/n", "\n").strip()
        evtData = self.get_arguments("data")
        evtData = str(evtData[0])
        evtData = evtData.replace("/n", "\n").strip()

        if evt == "addItem" :
            print("addItem: ", evtData )
        elif evt == "deleteItem" :
            print("deleteItem: ", evtData)
        else :
            print("undefine event(evt)")


        #rootEntity = entity_db.get_by_type( Process )[0]
        #rootEntity = entity_db.get("Root Process")

        #targetData = entity_db.get( "신규액션1" )
        targetData = edb.get( "Action2" )

        edb.remove_entity( targetData )

        gad = GuiMXGraphActionDiagram()

        #my_graph = gad.get_mxgraph( rootEntity )
        my_graph = my_graph.replace("/n", "\n")
        self.write(ad_script.mxGraph_start_nice_label + ad_script.mxGraph_styles + my_graph + ad_script.mxGraph_end)
        #self.write( my_graph )
        self.render('simple_mx_web.html')


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
        define("port", default=9191, help="run on the given port", type=int)

    def run(self):
        tornado.options.parse_command_line()
        application = Application([ (r'/src/js/(.*)', StaticFileHandler, {'path': './src/js'}),
                                    (r'/src/css/(.*)', StaticFileHandler, {'path': './src/css'}),
                                    (r'/src/images/(.*)', StaticFileHandler, {'path': './src/images'}),
                                    (r"/ad_sample/", ActionDiagramSampleHandler),
                                    (r"/DM/", DiagramModifyHandler),
                                    (r"/AD/", ActionDiagramHandler),
                                    (r"/BD/", BlockDiagramHandler),
                                    (r"/HD/", HierarchyDiagramHandler)
                                    ] )

        http_server = tornado.httpserver.HTTPServer(application, max_header_size=1024 ** 3)
        http_server.listen(options.port)
        tornado.ioloop.IOLoop.current().start()

TornadoMXServer().run()