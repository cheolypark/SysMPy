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


define("port", default=8080, help="run on the given port", type=int)

mxGraph_start = '''
                <!-- Example code -->
                   <script type="text/javascript">
                      // Program starts here. Creates a sample graph in the
                      // DOM node with the specified ID. This function is invoked
                      // from the onLoad event handler of the document (see below).
                      function main(container)
                      {
                         // Checks if the browser is supported
                         if (!mxClient.isBrowserSupported())
                         {
                            mxUtils.error('Browser is not supported!', 200, false);
                         }
                         else
                         {
                            // Creates the graph inside the given container
                            var graph = new mxGraph(container);
                 
                            // Enables rubberband selection
                            new mxRubberband(graph);
                            
                            // Set styles  
                            var style = graph.getStylesheet().getDefaultVertexStyle();
                            style[mxConstants.STYLE_FONTSIZE] = 11;
                            style[mxConstants.STYLE_FONTCOLOR] = 'RoyalBlue';
                            style[mxConstants.STYLE_STROKECOLOR] = 'RoyalBlue'; 
                            style[mxConstants.STYLE_FILLCOLOR] = 'white';   
                            style[mxConstants.STYLE_ROUNDED] = true;   
                            
                            // style = graph.getStylesheet().getDefaultEdgeStyle();
                            // style[mxConstants.STYLE_EDGE] = mxEdgeStyle.ElbowConnector;
                            // style[mxConstants.STYLE_STROKECOLOR] = '#b9c8f4';
                            // style[mxConstants.STYLE_ROUNDED] = true; 
                            
                            style = graph.getStylesheet().getDefaultEdgeStyle();
                            style[mxConstants.STYLE_EDGE] = mxEdgeStyle.ElbowConnector;
                            style[mxConstants.STYLE_ENDARROW] = mxConstants.ARROW_BLOCK;
                            style[mxConstants.STYLE_ROUNDED] = false;
                            style[mxConstants.STYLE_FONTCOLOR] = 'black';
                            style[mxConstants.STYLE_STROKECOLOR] = '#b9c8f4'; 
                              
                            var style = new Object();  
                            style[mxConstants.STYLE_SHAPE] = mxConstants.SHAPE_ELLIPSE;
                            style[mxConstants.STYLE_PERIMETER] = mxPerimeter.EllipsePerimeter;
                            style[mxConstants.STYLE_FONTCOLOR] = 'RoyalBlue';
                            style[mxConstants.STYLE_FILLCOLOR] = 'white'; 
                            style[mxConstants.STYLE_STROKECOLOR] = 'RoyalBlue'; 
                            style[mxConstants.STYLE_ALIGN] = mxConstants.ALIGN_CENTER;
                            style[mxConstants.STYLE_VERTICAL_ALIGN] = mxConstants.ALIGN_MIDDLE;
                            style[mxConstants.STYLE_FONTSIZE] = 11; 
                            graph.getStylesheet().putCellStyle('circlestyle', style);
                            
                            var style = new Object();  
                            style[mxConstants.STYLE_SHAPE] = 'box'; 
                            style[mxConstants.STYLE_FONTCOLOR] = 'RoyalBlue';
                            style[mxConstants.STYLE_FILLCOLOR] = 'white'; 
                            style[mxConstants.STYLE_STROKECOLOR] = 'RoyalBlue'; 
                            style[mxConstants.STYLE_ALIGN] = mxConstants.ALIGN_CENTER;
                            style[mxConstants.STYLE_VERTICAL_ALIGN] = mxConstants.ALIGN_MIDDLE;
                            style[mxConstants.STYLE_FONTSIZE] = 11; 
                            graph.getStylesheet().putCellStyle('boxstyle', style);
                             
                            var style = new Object(); 
                            style[mxConstants.STYLE_SHAPE] = mxConstants.SHAPE_RHOMBUS;
                            style[mxConstants.STYLE_PERIMETER] = mxPerimeter.RhombusPerimeter;   
                            style[mxConstants.STYLE_OPACITY] = 50;   
                            style[mxConstants.STYLE_FONTCOLOR] = 'RoyalBlue';
                            style[mxConstants.STYLE_FILLCOLOR] = 'white'; 
                            style[mxConstants.STYLE_STROKECOLOR] = 'RoyalBlue'; 
                            style[mxConstants.STYLE_ALIGN] = mxConstants.ALIGN_CENTER;
                            style[mxConstants.STYLE_VERTICAL_ALIGN] = mxConstants.ALIGN_MIDDLE;
                            style[mxConstants.STYLE_FONTSIZE] = 11;                      
                            graph.getStylesheet().putCellStyle('itemstyle', style);
                
                            // Gets the default parent for inserting new cells. This
                            // is normally the first child of the root (ie. layer 0).
                            var parent = graph.getDefaultParent();
                
                            // Adds cells to the model in a single step
                            graph.getModel().beginUpdate();
                            try
                            { 
                '''

mxGraph_end = '''  
                        }
                        finally
                        {
                           // Updates the display
                           graph.getModel().endUpdate();
                        }
                     }
                  };
               </script> 
            '''

mxGraph_graph = ''' 
                    var v1 = graph.insertVertex(parent, null, 'Hello,', 20, 20, 80, 30) \n
                    var v2 = graph.insertVertex(parent, null, 'World!', 200, 150, 80, 30)\n
                    var e1 = graph.insertEdge(parent, null, '', v1, v2)\n
                 '''


class MainHandler(RequestHandler):
    def get(self):
        # my_graph = mxGraph_graph
        my_graph = self.get_arguments("g")
        my_graph = str(my_graph[0])
        my_graph = my_graph.replace("/n", "\n")
        print(my_graph)

        self.write(mxGraph_start + my_graph + mxGraph_end)
        index = 'simpl_mx_test.html'
        self.render(index)


def main():
    tornado.options.parse_command_line()
    application = Application([ (r'/src/js/(.*)', StaticFileHandler, {'path': './src/js'}),
                                (r'/src/css/(.*)', StaticFileHandler, {'path': './src/css'}),
                                (r'/src/images/(.*)', StaticFileHandler, {'path': './src/images'}),
                                (r"/", MainHandler)
                                ])

    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()
