import re
import sys, inspect
import numpy as np


def is_path_same(path_base, path_target):
    """
    Return True or False if two paths are relatively same.

    :param path_base: e.g., ) Projects2.AD_Folder.AD1'
    :param path_target: e.g., ) 'E:\\SW-SysMPy\\SysMPy\\examples\\Projects\\AD_Folder\\AD1'
    :return:
    """

    base = reversed(re.split(r'\.|\\', path_base))
    target = reversed(re.split(r'\.|\\', path_target))

    for b in base:
        t = next(target)
        if b != t:
            return False

    return True


def or_selector(elements):
    cur_index = 0
    cur_element = None
    el_list = or_selector_tree(elements, cur_index, cur_element)

    del el_list[-1]

    for el in el_list:
        del el[-1]

    return el_list


def or_selector_tree(elements, cur_index, cur_element):
    if len(elements) == cur_index:
        return_list = []
        el_list = []
        return_list.append(el_list)
        el_list.append(cur_element)
        return return_list

    el_list1 = or_selector_tree(elements, cur_index + 1, elements[cur_index])
    el_list2 = or_selector_tree(elements, cur_index + 1, None)

    cur = cur_element

    return_list = []
    for el in el_list1:
        el.append(cur)
        return_list.append(el)
    for el in el_list2:
        el.append(cur)
        return_list.append(el)

    return return_list


is_print_out = False
def print_out(*str):
    if is_print_out is True:
        str = '   '.join(str)
        print(str)

# import entity
# def print_class_hierachy():
#     hierachy = {}
#     for name, obj in inspect.getmembers(entity):
#         if inspect.isclass(obj):
#             base = obj.__bases__[0].__name__
#             name = obj.__name__
#             if base not in hierachy:
#                 hierachy[base] = []
#
#             hierachy[base].append(name)
#             print(name, 'is a', base)
#
#     print(hierachy)

# print_class_hierachy()
# Function: or_selector
# elements = ['1', '2', '3']
# or_selector(elements)

# Function: is_path_same
# print(is_path_same('Projects.AD_Folder\\AD1', 'E:\\SW-SysMPy\\SysMPy\\examples\\Projects\\AD_Folder\\AD1'))


class Normal():
    def __init__(self, mean, sigma):
        """
        :param mean: Mean
        :param sigma: Standard Deviation
        """
        self.mean = mean
        self.sigma = sigma

    def get_random_value(self):
        return np.random.normal(self.mean, self.sigma, 1)[0]