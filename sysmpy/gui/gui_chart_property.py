from sysmpy.entity import *
from sysmpy.relationship import *
from sysmpy.gui.gui_mxgraph import GuiMXGraph


class GuiChartProperty():
    def __init__(self):
        pass

    def get_chart_info(self, proc_en, width, height):
        new_proc = proc_en.make_network()

        # get list of properties which are updated by the simulation
        new_proc.properties, _ = new_proc.search(class_search=[Property])

        if new_proc.properties is not None:
            property_list = [f"'{x.name}':0" for x in new_proc.properties]
            prop_str = '{' + ", ".join(property_list) + '}'
            return prop_str

        return ''
