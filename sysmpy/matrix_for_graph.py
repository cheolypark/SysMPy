import numpy as np
from sysmpy.entity import *
from operator import add


class MatrixForGraph():
    def __init__(self, m=None):
        self.m = m
        self.entity = None

    def sum_upper_diagonal(self, m=None):
        if m is None:
            m = self.m
        ret_matrix = np.zeros(m.shape)
        for x in range(m.shape[0]):
            for y in range(m.shape[1]):
                if x > y:
                    ret_matrix[y, x] = m[y, x] + m[x, y]
        return ret_matrix

    def sum_lower_diagonal(self, m=None):
        if m is None:
            m = self.m
        ret_matrix = np.zeros(m.shape)
        for x in range(m.shape[0]):
            for y in range(m.shape[1]):
                if x < y:
                    ret_matrix[y, x] = m[y, x] + m[x, y]
        return ret_matrix

    def sum_column(self, m=None):
        if m is None:
            m = self.m
        return m.sum(axis=0)

    def sum_row(self, m=None):
        if m is None:
            m = self.m
        return m.sum(axis=1)

    def one_matrix(self, m=None):
        if m is None:
            m = self.m
        ret_matrix = np.zeros(m.shape)
        for x in range(m.shape[0]):
            for y in range(m.shape[1]):
                if m[y, x] > 0:
                    ret_matrix[y, x] = 1
        return ret_matrix

    def check_critical_elements(self):
        # print(self.m)
        sum_com = self.sum_column(self.m)
        sum_row = self.sum_row(self.m)
        res_list = list(map(add, sum_com, sum_row))
        res_dict = {i: v for i, v in enumerate(res_list)}
        res_dict = {k: v for k, v in sorted(res_dict.items(), reverse=True, key=lambda item: item[1])}

        critical_elements = []

        for index, v in res_dict.items():
            entity = self.entity[index]
            critical_elements.append(entity)

        return critical_elements

    def check_feedback(self):
        one_matrix = self.one_matrix()
        ret_matrix = self.sum_upper_diagonal(one_matrix)
        sum_com = self.sum_column(ret_matrix)
        sum_row = self.sum_row(ret_matrix)
        # print(ret_matrix)
        feedback_elements = []
        index = 0
        for sc in sum_com:
            if sc >= 2:
                entity = self.entity[index]
                feedback_elements.append(entity)
            index += 1

        index = 0
        for sc in sum_row:
            if sc == 2:
                entity = self.entity[index]
                feedback_elements.append(entity)
            index += 1
        return feedback_elements

    def to_matrix(self, entity):
        """
        Thia makes an action graph to a matrix
        e.g.,)
          +----+                  [[0. 1. 0. 0.]
          |    v                   [1. 0. 0. 0.]
        [A1]->[A2]->[A3]->[A4] =>  [0. 0. 0. 0.]
          ^    |                   [0. 0. 0. 0.]]
          -----+
        :param entity: a process containing actions
        :return: a matrix for the graph
        """
        self.entity, _ = entity.search(class_search=[Action])
        size = len(self.entity)
        ret_matrix = np.zeros((size, size))

        for sa in self.entity:
            x_index = self.entity.index(sa)
            if 'sends' in sa.relation:
                sending_items = [x.end for x in sa.relation['sends']]
                for si in sending_items:
                    receivers = [x.start for x in si.inv_relation['received by']]
                    for re in receivers:
                        y_index = self.entity.index(re)
                        ret_matrix[x_index][y_index] += 1

        # print(ret_matrix)
        self.m = ret_matrix
        return ret_matrix

# Test ###############################################################
# mn = MatrixForGraph(np.matrix([[1, 2, 3], [3, 4, 5], [6, 7, 8]]))
# print(mn.sum_column())

