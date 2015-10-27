#!/usr/bin/python
# -*- coding: utf-8 -*-
# $File: hputil.py
# $Date: 2015-10-06 10:32
# $Author: Matt Zhang <mattzhang9[at]gmail[dot]com>
"""common utility functions"""

from importlib import import_module
from pkgutil import walk_packages
from functools import wraps

import os
import re
import cgi
import new
import copy
import random
import datetime

def get_all_methods(dirname, pkg_name):
    ret = dict()
    for _, module_name, _ in walk_packages([dirname], pkg_name + '.'):
        mod = import_module(module_name)
        for key, val in mod.__dict__.iteritems():
            ret[key] = val
    return ret


def import_all_modules(file_path, pkg_name, import_to_globals=None):
    """import all modules recursively in a package
    :param file_path: just pass __file__
    :param pkg_name: just pass __name__
    :param import_to_globals: a dict of globals()
    """
    for _, module_name, _ in walk_packages(
            [os.path.dirname(file_path)], pkg_name + '.'):
        mod = import_module(module_name)
        if import_to_globals:
            for key, val in mod.__dict__.iteritems():
                # print("{}.{}".format(module_name,key))
                import_to_globals[key] = val


def enum(*sequential, **named):
    """defined a `enum' class similar to that in c++"""

    # string -> int
    enums = dict(zip(sequential, range(len(sequential))), **named)
    # all stored as unicode
    enums = dict(map(lambda x: (unicode(x[0]), x[1]), enums.iteritems()))

    reverse = dict((value, key) for key, value in enums.iteritems())
    cls_dict = copy.deepcopy(enums)
    cls_dict['enums'] = copy.deepcopy(enums)
    cls_dict['reverse_mapping'] = reverse
    cls_dict['values'] = enums.values()
    cls_dict['value_to_names'] = dict((b, a) for a, b in enums.iteritems())

    def __getitem__(self, key):  # number -> number
        return self.values[key]

    def get_name_by_value(self, value):
        return self.value_to_names[value]

    def get_value_by_name(self, key):
        return self.enums[key]

    cls_dict['__getitem__'] = __getitem__
    cls_dict['get_value_by_name'] = get_value_by_name
    cls_dict['get_name_by_value'] = get_name_by_value
    cls = type('Enum', (), cls_dict)

    return cls()



