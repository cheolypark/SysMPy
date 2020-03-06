from entity import *
import asyncio

from IPython.core.display import HTML
from IPython.display import IFrame
from IPython.display import HTML
import requests
import urllib

def show(p, width=960, height=750):

    src = "http://localhost:8080/?g=" + p.get_mxgraph()
    # parsed_html = urllib.parse.quote(view_html, safe="~@#$&()*!+=:;,.?/\'")
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
#     IFrame("http://localhost:8080/?g=" + p.get_mxgraph(), width=1000, height=700)