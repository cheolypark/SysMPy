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

mxGraph_start_basic = '''
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
                                // var graph = new mxGraph(container);
                     
                                // Enables rubberband selection
                                // new mxRubberband(graph);
                     '''

mxGraph_start_nice_label = '''
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
                             
                             
                             ////////////////////////////////////////////////////////////////////////////                            
                             // Create a window which contains this graph
                             // var wnd = new mxWindow('AD', container, 10, 10, 800, 1000, true, true);
                             // wnd.setMaximizable(true);
                             // wnd.setResizable(true);
                             // wnd.setVisible(true); 
                             // wnd.setScrollable(true);
                             
                             
                            ////////////////////////////////////////////////////////////////////////////                            
                            // Creates the graph inside the given container
                            var graph = new mxGraph(container);
                            graph.setTooltips(true);
                            graph.htmlLabels = true;
                            graph.vertexLabelsMovable = true;
                            new mxRubberband(graph);
                            new mxKeyHandler(graph);
                            
                               
                            ////////////////////////////////////////////////////////////////////////////                            
                            // Do not allow removing labels from parents
                            graph.graphHandler.removeCellsFromParent = false;
                            
                            // Autosize labels on insert where autosize=1
                            graph.autoSizeCellsOnAdd = true;
                            
                            // Allows moving of relative cells
                            graph.isCellLocked = function(cell)
                            {
                                return this.isCellsLocked();
                            };
                            
                            graph.isCellResizable = function(cell)
                            {
                                var geo = this.model.getGeometry(cell);
                                
                                return geo == null || !geo.relative;
                            };
                            
                            // Truncates the label to the size of the vertex
                            graph.getLabel = function(cell)
                            {
                                var label = (this.labelsVisible) ? this.convertValueToString(cell) : '';
                                var geometry = this.model.getGeometry(cell);
                                
                                if (!this.model.isCollapsed(cell) && geometry != null && (geometry.offset == null ||
                                    (geometry.offset.x == 0 && geometry.offset.y == 0)) && this.model.isVertex(cell) &&
                                    geometry.width >= 2)
                                {
                                    var style = this.getCellStyle(cell);
                                    var fontSize = style[mxConstants.STYLE_FONTSIZE] || mxConstants.DEFAULT_FONTSIZE;
                                    var max = geometry.width / (fontSize * 0.625);
                                    
                                    if (max < label.length)
                                    {
                                        return label.substring(0, max) + '...';
                                    }
                                }
                                
                                return label;
                            };
                            
                            // Enables wrapping for vertex labels
                            graph.isWrapping = function(cell)
                            {
                                return this.model.isCollapsed(cell);
                            };
                            
                            // Enables clipping of vertex labels if no offset is defined
                            graph.isLabelClipped = function(cell)
                            {
                                var geometry = this.model.getGeometry(cell);
                                
                                return geometry != null && !geometry.relative && (geometry.offset == null ||
                                    (geometry.offset.x == 0 && geometry.offset.y == 0));
                            };
                            
                            // Gets the default parent for inserting new cells. This
                            // is normally the first child of the root (ie. layer 0).
                            var parent = graph.getDefaultParent();
                     '''

mxGraph_styles = '''                            
                            // Set styles  
                            var style = graph.getStylesheet().getDefaultVertexStyle();
                            style[mxConstants.STYLE_FONTSIZE] = 11;
                            style[mxConstants.STYLE_FONTCOLOR] = 'RoyalBlue';
                            style[mxConstants.STYLE_STROKECOLOR] = 'RoyalBlue'; 
                            style[mxConstants.STYLE_FILLCOLOR] = '#C2DFFF';   
                            //style[mxConstants.STYLE_ROUNDED] = true;   
                              
                            style = graph.getStylesheet().getDefaultEdgeStyle();
                            //style[mxConstants.STYLE_EDGE] = mxEdgeStyle.ElbowConnector;
                            //style[mxConstants.STYLE_ENDARROW] = mxConstants.ARROW_BLOCK;
                            //style[mxConstants.STYLE_ROUNDED] = false;
                            style[mxConstants.STYLE_FONTCOLOR] = 'black';
                            style[mxConstants.STYLE_STROKECOLOR] = '#b9c8f4'; 
                            delete graph.getStylesheet().getDefaultEdgeStyle()['endArrow'];
                            
                            // Custom styles
                            // 1. Custom Edge
                            var style = new Object();
                            style[mxConstants.STYLE_ENDARROW] = mxConstants.ARROW_BLOCK;
                            style[mxConstants.STYLE_STROKECOLOR] = '#b9c8f4';  
                            graph.getStylesheet().putCellStyle('Arrow_Edge_Process', style);
                            
                            var style = new Object();
                            style[mxConstants.STYLE_ENDARROW] = mxConstants.ARROW_BLOCK;
                            style[mxConstants.STYLE_STROKECOLOR] = '#6AFB92';   
                            graph.getStylesheet().putCellStyle('Arrow_Edge_Item', style);
                            
                            var style = new Object(); 
                            style[mxConstants.STYLE_STROKECOLOR] = '#6AFB92';   
                            graph.getStylesheet().putCellStyle('Edge_Item', style);
                            
                            var style = new Object();
                            style[mxConstants.STYLE_ENDARROW] = mxConstants.ARROW_BLOCK;
                            style[mxConstants.STYLE_EDGE] = mxEdgeStyle.ElbowConnector;
                            style[mxConstants.STYLE_ROUNDED] = true;
                            style[mxConstants.STYLE_STROKECOLOR] = '#b9c8f4';  
                            graph.getStylesheet().putCellStyle('Arrow_Edge_Loop', style);
                            
                            // 2. Custom Node
                            var style = new Object();
                            style[mxConstants.STYLE_SHAPE] = mxConstants.SHAPE_HEXAGON;
                            style[mxConstants.STYLE_FONTSIZE] = 11;
                            style[mxConstants.STYLE_FONTCOLOR] = 'RoyalBlue';
                            style[mxConstants.STYLE_STROKECOLOR] = 'RoyalBlue'; 
                            style[mxConstants.STYLE_FILLCOLOR] = 'white';
                            graph.getStylesheet().putCellStyle('Loop', style);
                            graph.getStylesheet().putCellStyle('Loop_END', style);
                             
			                var style = new Object();
                            style[mxConstants.STYLE_SHAPE] = mxConstants.SHAPE_ELLIPSE;
                            style[mxConstants.STYLE_FONTSIZE] = 11;
                            style[mxConstants.STYLE_FONTCOLOR] = 'RoyalBlue';
                            style[mxConstants.STYLE_STROKECOLOR] = 'RoyalBlue'; 
                            style[mxConstants.STYLE_FILLCOLOR] = 'white';
                            graph.getStylesheet().putCellStyle('And', style);
                            graph.getStylesheet().putCellStyle('And_END', style);
                            graph.getStylesheet().putCellStyle('Condition', style);
                            graph.getStylesheet().putCellStyle('Condition_END', style);
            
                            var style = new Object();
                            style[mxConstants.STYLE_SHAPE] = mxConstants.SHAPE_RHOMBUS;
                            style[mxConstants.STYLE_FONTSIZE] = 11;
                            style[mxConstants.STYLE_FONTCOLOR] = 'RoyalBlue';
                            style[mxConstants.STYLE_STROKECOLOR] = 'RoyalBlue'; 
                            style[mxConstants.STYLE_FILLCOLOR] = 'white';
                            graph.getStylesheet().putCellStyle('Or', style);
                            graph.getStylesheet().putCellStyle('Or_END', style);
                            
                            var style = new Object();
                            style[mxConstants.STYLE_SHAPE] = mxConstants.SHAPE_ELLIPSE;
                            style[mxConstants.STYLE_FONTSIZE] = 11;
                            style[mxConstants.STYLE_FONTCOLOR] = 'RoyalBlue';
                            style[mxConstants.STYLE_STROKECOLOR] = 'RoyalBlue'; 
                            style[mxConstants.STYLE_FILLCOLOR] = 'white';
                            graph.getStylesheet().putCellStyle('Process', style);
                            
                            var style = new Object();
                            style[mxConstants.STYLE_SHAPE] = mxConstants.SHAPE_DOUBLE_ELLIPSE;
                            style[mxConstants.STYLE_FONTSIZE] = 11;
                            style[mxConstants.STYLE_FONTCOLOR] = 'RoyalBlue';
                            style[mxConstants.STYLE_STROKECOLOR] = 'RoyalBlue'; 
                            style[mxConstants.STYLE_FILLCOLOR] = 'white';
                            graph.getStylesheet().putCellStyle('Process_END', style);
                               
                            var style = new Object();  
                            style[mxConstants.STYLE_SHAPE] = 'box'; 
                            style[mxConstants.STYLE_FONTCOLOR] = 'RoyalBlue';
                            style[mxConstants.STYLE_FILLCOLOR] = '#C2DFFF'; 
                            style[mxConstants.STYLE_STROKECOLOR] = 'RoyalBlue'; 
                            style[mxConstants.STYLE_ALIGN] = mxConstants.ALIGN_CENTER;
                            style[mxConstants.STYLE_VERTICAL_ALIGN] = mxConstants.ALIGN_MIDDLE;
                            style[mxConstants.STYLE_FONTSIZE] = 11; 
                            graph.getStylesheet().putCellStyle('Action', style);
                             
                            var style = new Object(); 
                            style[mxConstants.STYLE_SHAPE] = mxConstants.SHAPE_RECTANGLE;
                            //style[mxConstants.STYLE_PERIMETER] = mxPerimeter.RhombusPerimeter;   
                            //style[mxConstants.STYLE_OPACITY] = 50;   
                            style[mxConstants.STYLE_FONTCOLOR] = '#3EA055';
                            style[mxConstants.STYLE_FILLCOLOR] = '#C3FDB8'; 
                            style[mxConstants.STYLE_STROKECOLOR] = '#6AFB92';
                            style[mxConstants.STYLE_ROUNDED] = true; 
                            style[mxConstants.STYLE_FONTSIZE] = 11;                
                            graph.getStylesheet().putCellStyle('Item', style);
                
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
                        
                        // Fit the graph size to the html div size
                        graph.fit();
                        graph.view.rendering = true;
                        graph.refresh();           
                          
                         
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

        self.write(mxGraph_start_nice_label + mxGraph_styles + my_graph + mxGraph_end)
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
