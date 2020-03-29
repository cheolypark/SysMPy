from sysmpy.entity import *
from sysmpy.matrix_for_graph import MatrixForGraph


class InterfaceAnalyzer:
    def __init__(self, entity):
        self.entity = entity
        self.matrix = MatrixForGraph()
        self.matrix.to_matrix(entity)

    def get_critical_elements(self, entity):
        # 1. Find critical elements
        critical_elements = self.matrix.check_critical_elements()
        print(f'critical_elements {critical_elements}')
        return critical_elements

    def get_sphere_of_influence(self, entity):
        # 2. Find the sphere of influence of critical elements
        entity_results, relation_results = entity.search(class_search=[Action])

        sphere_of_influence = {}

        for sa in entity_results:
            sphere_of_influence[sa] = set()
            if 'sends' in sa.relation:
                sending_items = [x.end for x in sa.relation['sends']]
                for si in sending_items:
                    receivers = [x.start for x in si.inv_relation['received by']]

                    for re in receivers:
                        sphere_of_influence[sa].add(re)

            if 'receives' in sa.relation:
                receiving_items = [x.end for x in sa.relation['receives']]
                for si in receiving_items:
                    senders = [x.start for x in si.inv_relation['sent from']]

                    for sender in senders:
                        sphere_of_influence[sa].add(sender)

        print(f'sphere_of_influence {sphere_of_influence}')
        return sphere_of_influence

    def get_feedback_elements(self, entity):
        # 3. Find the feedback loops
        feedback_elements = self.matrix.check_feedback()
        print(f'feedback_elements {feedback_elements}')
        return feedback_elements

    def get_recursive_elements(self, entity):
        # 4. Find the recursive elements
        recursive_elements = []
        entity_results, relation_results = entity.search(class_search=[Action])

        for e in entity_results:
            sending_items, receiving_items = [], []
            if 'sends' in e.relation:
                sending_items = [x.end for x in e.relation['sends']]
            if 'receives' in e.relation:
                receiving_items = [x.end for x in e.relation['receives']]

            sum = sending_items + receiving_items
            if len(sum) != 0:
                found = [s for s in sending_items for r in receiving_items if s is r]
                recursive_elements += found

        print(f'recursive_elements {recursive_elements}')

        return recursive_elements

    def get_absence_items(self, entity):
        # 5. Find the absence of items
        absence_items = []
        entity_results, relation_results = entity.search(class_search=[Action])

        for e in entity_results:
            sending_items, receiving_items = [], []
            if 'sends' in e.relation:
                sending_items = [x.end for x in e.relation['sends']]
            if 'receives' in e.relation:
                receiving_items = [x.end for x in e.relation['receives']]
            sum = sending_items + receiving_items
            if len(sum) == 0:
                absence_items.append(e)

        print(f'absence_items {absence_items}')

        return absence_items

    def get_unused_items(self, entity):
        # 6. Find the unused items
        unused_items = []
        list_item = Entity.get_by_type(Item)
        list_resource = Entity.get_by_type(Resource)
        list_item = list_item + list_resource
        for item in list_item:
            senders, receivers = [], []
            if 'sent from' in item.inv_relation:
                senders = [x.start for x in item.inv_relation['sent from']]
            if 'received by' in item.inv_relation:
                receivers = [x.start for x in item.inv_relation['received by']]
            sum = senders+receivers
            if len(sum) == 0:
                unused_items.append(item)

        print(f'unused_items {unused_items}')
        return unused_items
