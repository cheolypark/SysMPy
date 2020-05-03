from sysmpy.entity import *
from sysmpy.relationship import *
from sysmpy.gui.gui_mxgraph import GuiMXGraph


class GuiMXGraphBlockDiagram(GuiMXGraph):
    def __init__(self):
        super().__init__()

    ########################################################################
    # Graphic Methods
    #
    def init_graphic_variables(self, entity):
        entity.margin_x = 0
        entity.margin_y = 0
        entity.node_width = 150
        entity.node_height = 100

        entity.boundary_width = 0
        entity.boundary_height = 0
        entity.boundary_x = 0
        entity.boundary_y = 0
        entity.width_half = (entity.node_width + entity.margin_x * 2) / 2
        entity.height_half = (entity.node_height + entity.margin_y * 2) / 2
        entity.width = entity.node_width + entity.margin_x * 2
        entity.height = entity.node_height + entity.margin_y * 2
        entity.center_x = 0
        entity.center_y = 0
        entity.root_x = 0

    def make_node(self, en, x=None, y=None):
        # var v1 = graph.insertVertex(parent, null, 'Hello,', 20, 20, 80, 30) \\n
        if x is None:
            x = en.center_x
        if y is None:
            y = en.center_y

        node_width = en.node_width
        node_height = en.node_height
        label = en.name
        id = en.get_id()
        name = en.get_name_with_parent()

        if isinstance(en, Process):
            pass
        if isinstance(en, Process_END):
            label = ''
        elif isinstance(en, And) or isinstance(en, And_END):
            label = 'A'
        elif isinstance(en, Or) or isinstance(en, Or_END) or isinstance(en, Condition_END):
            label = 'OR'
        elif isinstance(en, XOr) or isinstance(en, XOr_END):
            label = 'XO'
        elif isinstance(en, Loop) or isinstance(en, Loop_END):
            label = 'L'

        # compensate the node position after resizing
        x += (en.node_width - node_width) / 2
        y += (en.node_height - node_height) / 2

        node = ''
        if id not in self.mx_nodes:
            self.mx_nodes.append(id)
            # var c3 = graph.insertVertex(parent, null,'Process 1', 150,30,100,200,'Process;');
            # var c31 = graph.insertVertex(c3,null,'', 0,0,100,50,'ProcessImage;image=images/img3.png;');
            # var c33 = graph.insertVertex(c3,null,'Action 1', 0,0,50,20,'ActionBoundary');
            # var c36 = graph.insertVertex(c3,null,':', 0,0,100,30,'Property');
            # var c37 = graph.insertVertex(c36,null,'Temp', 0,0,50,30,'Property');
            # var c38 = graph.insertVertex(c36,null,'2', 50,0,50,30,'Property');
            node = f"var {id} = graph.insertVertex(parent, '{name}', '{label}', {x}, {y}, {node_width}, {node_height}, '{type(en).__name__}') /n "

        return node, node_height

    def make_image(self, parent):
        node_width = parent.node_width
        node_height = parent.node_height - 30
        id_parent = parent.get_id()
        name = parent.name

        style_image = 'ProcessImage'
        if isinstance(parent, Item):
            style_image = 'ItemImage'

        # We use '/8/' to substitute for ';', because the tornado has a problem with ';', when the GET request is used.
        # var c31 = graph.insertVertex(c3,null,'', 0,0,100,50,'ProcessImage;image=images/img3.png;');
        # node = f"graph.insertVertex({id_parent}, null, '', 0, 0, {node_width}, {node_height}, '{style_image}//image=images/{name}.png') /n "
        img_url = f'http://127.0.0.1:9191/images/{name}.png'
        node = f"graph.insertVertex({id_parent}, null, '', 0, 0, {node_width}, {node_height}, '{style_image}/8/image={img_url}') /n "

        #
        return node

    def make_action(self, parent, en):
        id = parent.get_id()
        label = en.name
        node_width = parent.node_width
        node_height = 20

        # var c33 = graph.insertVertex(c3,null,'Action 1', 0,0,50,20,'actionBoundary');
        node = f"graph.insertVertex({id}, null, '{label}', 0, 0, {node_width}, {node_height}, 'ActionBoundary') /n "

        return node, node_height

    def make_property(self, parent, en):
        node_width = parent.node_width
        node_height = 20
        label = en.get_name(5)
        id_parent = parent.get_id()
        name = en.get_name_with_parent()
        id = en.get_id()
        id_p = id + '_p'
        id_k = id + '_k'
        id_v = id + '_v'
        # var c36 = graph.insertVertex(c3,null,':', 0,0,100,30,'property');
        # var c37 = graph.insertVertex(c36,null,'Temp', 0,0,50,30,'property');
        # var c38 = graph.insertVertex(c36,null,'2', 50,0,50,30,'property');

        node = ''
        node += f"var {id_p} = graph.insertVertex({id_parent}, null, '', 0, 0, {node_width}, {node_height}, 'Property') /n "
        node += f"var {id_k} = graph.insertVertex({id_p}, null, '{label}', 0, 0, {node_width/2}, {node_height}, 'Property') /n "
        node += f"var {id_v} = graph.insertVertex({id_p}, '{name}', 'null', {node_width/2}, 0, {node_width/2}, {node_height}, 'Property') /n "

        return node, node_height

    def make_edge(self, s, e, point=None, edge_style=None):
        # var e1 = graph.insertEdge(parent, null, '', v1, v2)\\n
        s_name = self.safe_name(s.get_numbered_name())
        e_name = self.safe_name(e.get_numbered_name())
        # edge = f"var {s}_{e} = graph.insertEdge(parent, null, '', {s}, {e}, 'verticalAlign=top') /n "
        # edge += f'{s}_{e}.geometry.points = [new mxPoint({s}.geometry.x + 10, 10)]/n'

        if edge_style is None:
            if s.is_root is True or e.is_root is True:
                edge_style = 'Arrow_Edge_Process'
            elif isinstance(s, Item):
                edge_style = 'Arrow_Edge_Item'
            elif isinstance(e, Item):
                edge_style = 'Edge_Item'
            elif isinstance(s, Resource):
                edge_style = 'Arrow_Edge_Resource'
            elif isinstance(e, Resource):
                edge_style = 'Edge_Resource'
            elif isinstance(s, Loop_END) and isinstance(e, Loop):
                edge_style = 'Arrow_Edge_Loop'
            else:
                edge_style = None

        if edge_style is not None:
            edge = f"var {s_name}_{e_name} = graph.insertEdge(parent, null, '', {s_name}, {e_name}, '{edge_style}' ) /n "
        else:
            edge = f"var {s_name}_{e_name} = graph.insertEdge(parent, null, '', {s_name}, {e_name} ) /n "

        if point is not None:
            edge += f'{s_name}_{e_name}.geometry.points = [new mxPoint({point}, 50)] /n '
        # e = graph.insertEdge(lane2a, null, 'No', step444, end3, 'verticalAlign=top');
        # e.geometry.points = [new mxPoint(step444.geometry.x + step444.geometry.width / 2,
        #                                  end3.geometry.y + end3.geometry.height / 2)];

        # 'shape=link;labelBackgroundColor=#FFFFFF;'

        # print(edge)
        return edge

    def get_mxgraph_string(self, proc_en, view_width=600, hide_no_action_process=False):
        # 1. Find Process
        list_processes, _ = proc_en.search(class_search=[Process])

        # Remove the root process according to a request.
        # list_processes.remove(proc_en)

        # Initialize graphic parameters
        str = ''
        view_x, view_y = 20, 20
        x, y = view_x, view_y
        width_gap, height_gap = 30, 20

        # max_height stands for the maximum height among processes
        # total_height stands for the current height of this process
        max_height, total_height = 0, 0

        # For each process, make an MXGraph script
        for proc in list_processes:

            # Search actions of this process
            list_actions, _ = proc.search(class_search=[Action], depth=1)

            # If the view state is hide_no_action_process, then skip this process
            if hide_no_action_process is True:
                if len(list_actions) == 0:
                    continue

            # Generate graphical variables (e.g., height) for this process
            self.init_graphic_variables(proc)

            # Make an MXGraph script for this process
            s, h = self.make_node(proc, x, y)
            str += s
            total_height += h

            # Make an MXGraph script for the image of this process
            str += self.make_image(proc)

            # For each action, make an MXGraph script
            for action in list_actions:
                # Make an MXGraph script for this action
                s, h = self.make_action(proc, action)
                str += s
                total_height += h

            # Search properties of this process
            list_properties, _ = proc.search(class_search=[Property], depth=1)

            # For each property, make an MXGraph script
            for property in list_properties:
                # Make an MXGraph script for this property
                s, h = self.make_property(proc, property)
                str += s
                total_height += h

            # By comparing max_height and total_height, find the maximum height
            max_height = max(max_height, total_height)

            # Reset total_height
            total_height = 0

            # Search items which this process outputs
            list_items = proc.search_entity_by_relation(relation_class=[Sends], entity_class=[Item], depth=2)

            # For each item, make an MXGraph script
            for item in list_items:
                if item.name == '슬라브2':
                    print('')
                # Generate graphical variables (e.g., height) for this process
                self.init_graphic_variables(item)

                # Check whether this entity size is over the view size
                if view_width > (x + item.node_width + width_gap):
                    x += item.node_width + width_gap
                else:
                    x = view_x
                    y += max_height + view_y + width_gap
                    max_height = 0

                # Make an MXGraph script for this item
                s, h = self.make_node(item, x, y)
                str += s
                total_height += h

                # Make an MXGraph script for the image of this item
                str += self.make_image(item)

                # Search properties of this item
                list_properties, _ = item.search(class_search=[Property], depth=1)

                # For each property, make an MXGraph script
                for property in list_properties:
                    s, h = self.make_property(item, property)
                    str += s
                    total_height += h

                max_height = max(max_height, total_height)
                total_height = 0

            # Check whether this entity size is over the view size
            if view_width > (x + proc.node_width + width_gap):
                x += proc.node_width + width_gap
            else:
                x = view_x
                y += max_height + view_y + width_gap
                max_height = 0

        return str


    def get_mxgraph(self, proc_en, width, height, kwarg=None):
        """
        :param proc_en:
        :param width:
        :param height:
        :param kwarg:
        if Hide_No_Action_Process=True, the process without actions will be ignored for display
        :return:
        """
        # Copy a new process entity using the original process entity
        new_en = deepcopy(proc_en)

        # Add the numbers for each process and action entity
        new_en.numbering('A')

        # Set this with a root process flag
        new_en.is_root = True
        new_en.end.is_root = True

        # Check whether the process without actions is shown or not
        hide_no_action_process = False

        if kwarg is not None and 'Hide_No_Action_Process' in kwarg:
            hide_no_action_process = kwarg['Hide_No_Action_Process']

        # Adjust the view boundary
        boundary_width = 100
        width -= boundary_width

        # Generate the block diagram
        str = self.get_mxgraph_string(new_en, view_width=width, hide_no_action_process=hide_no_action_process)

        return str