import json

from core.entity.file_system.File import File
from core.entity.file_system.Folder import Folder


def recursive_print(object):
    if isinstance(object, File):
        print(object.name)
    else:
        print(object.name)
        for x in object.heirs:
            recursive_print(x)


def recursive_descend(file_dict, name, parent):
    parent_ = Folder(name, parent)
    heirs_list = []
    for heir_name in file_dict[name].keys():
        if file_dict[name][heir_name] == 'file':
            heirs_list.append(File(heir_name, print, parent_))
        else:
            heirs_list.append(recursive_descend(file_dict[name], heir_name, parent_))
    parent_.heirs = heirs_list
    return parent_


def dump_json():
    f = open("resources/file_tree.json")
    data = json.load(f)
    c_folder = recursive_descend(data, "C:/", None)
    return c_folder
