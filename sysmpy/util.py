import re


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

# print(is_path_same('Projects.AD_Folder\\AD1', 'E:\\SW-SysMPy\\SysMPy\\examples\\Projects\\AD_Folder\\AD1'))
