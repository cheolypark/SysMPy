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

from sysmpy.gui.mxgraph.script_sample import root_process


# /ad_sample/ Handler
class ActionDiagramSampleHandler(RequestHandler):
    def get(self):
        p = root_process # call sample Acton diagram Unified Script
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

        print(root_process)

        # 저장된 root_process 를 이용하고 Action Type을 이용하여 object 추출
        entity_results, _ = root_process.search(words_search=[Action])
        print(entity_results)

        # 저장된 root_process 를 이용하고 entity name을 이용하여 object 추출
        entity_results, _ = root_process.search(words_search=["Root Process"])
        print(entity_results)

        # 저장된 root_process 를 이용하고 entity name을 이용하여 object 추출
        entity_results, _ = root_process.search(words_search=["신규액션1"])
        print(entity_results)

        # edb (entity_db)를 이용하여 object 추출 (Path 명기 필수)
        targetData = edb.get("Action2", path=root_process.module)
        print(targetData)

        edb.remove_entity(targetData)

        my_graph = GuiMXGraphActionDiagram().get_mxgraph( root_process )
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