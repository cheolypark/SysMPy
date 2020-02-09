from entity import *


class InterfaceAnalyzer:
    def __init__(self):
        pass

    def run(self, entity):
        entity_results, relation_results = entity.search(class_search=[Action])

        for e in entity_results:
            print(e)

        # 1. Find critical elements

        # 2. Find the sphere of influence of critical elements

        # 3. Find the tightly bound groups

        # 4. Find the feedback loops

        # 5. Find the recursive elements

        # 6. Find the absence of items

        # 7. Find the unused items

