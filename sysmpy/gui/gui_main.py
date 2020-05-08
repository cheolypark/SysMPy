from IPython.display import HTML
from sysmpy.gui.gui_mxgraph_action_diagram import GuiMXGraphActionDiagram
from sysmpy.gui.gui_mxgraph_block_diagram import GuiMXGraphBlockDiagram
from sysmpy.gui.gui_mxgraph_hierarchy_diagram import GuiMXGraphHierarchyDiagram
from sysmpy.gui.gui_property_line_chart import GuiPropertyLineChart
from sysmpy.gui.gui_property_table import GuiPropertyTable
from sysmpy.config import gui_server_address


# This removes all warning messages in the Jupyter notebook.
# Since the flask web server generates warning messages, we use this.
import logging

logging.disable()


def show(p, width=960, height=750, diagram='AD', **kwarg):
    diagram = diagram.lower()
    # print(diagram)

    if diagram == 'ad': # Action Diagram
        graph = GuiMXGraphActionDiagram().get_mxgraph(p)
    elif diagram == 'bd': # Block Diagram
        graph = GuiMXGraphBlockDiagram().get_mxgraph(p, width, height, kwarg)
    elif diagram == 'hd': # Hierarchy Diagram
        graph = GuiMXGraphHierarchyDiagram().get_mxgraph(p, width, height, kwarg)
    elif diagram == 'pc': # Property Line Chart View
        graph = GuiPropertyLineChart().get_chart_info(p, width, height)
    elif diagram == 'pt':  # Property Table View
        graph = GuiPropertyTable().get_chart_info(p, width, height)

    # print(graph)

    src = f"http://{gui_server_address}:9191/{diagram}/?g={graph}"

    # parsed_html = urllib.parse.quote(src, safe="~@#$&()*!+=:;,.?/\'")
    # print(src)

    iframe = f"""
           <iframe
               width="{width}"
               height="{height}"
               src="{src}"
               frameborder="0"
               allowfullscreen
           ></iframe>
           """

    display(HTML(iframe))
#
# def show(p):
#     IFrame("http://localhost:8080/?g=" + p.get_mx_action_diagram(), width=1000, height=700)

# Example
# http://www.sysmpy.org/view/?g=var v1 = graph.insertVertex(parent, null, 'Hello,', 20, 20, 80, 30) /n var v2 = graph.insertVertex(parent, null, 'World!', 200, 150, 80, 30)/n var e1 = graph.insertEdge(parent, null, '', v1, v2)/n