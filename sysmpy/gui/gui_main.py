from sysmpy.entity import *
import asyncio

from IPython.core.display import HTML
from IPython.display import IFrame
from IPython.display import HTML
from sysmpy.gui.gui_mxgraph_action_diagram import GuiMXGraphActionDiagram
from sysmpy.gui.gui_mxgraph_block_diagram import GuiMXGraphBlockDiagram
from sysmpy.gui.gui_mxgraph_hierarchy_diagram import GuiMXGraphHierarchyDiagram
import urllib


def show(p, width=960, height=750, diagram='AD', remote=True, type=Action):

    if diagram == 'AD':
        graph = GuiMXGraphActionDiagram().get_mxgraph(p)
    elif diagram == 'BD':
        graph = GuiMXGraphBlockDiagram().get_mxgraph(p)
    elif diagram == 'HD':
        graph = GuiMXGraphHierarchyDiagram().get_mxgraph(p, type)

    # print(graph)

    if remote is True:
        src = "http://www.sysmpy.org/view/?g=" + graph
    else:
        src = "http://127.0.0.1:8000/view/?g=" + graph

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