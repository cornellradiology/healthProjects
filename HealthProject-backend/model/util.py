#!/usr/bin/python
# -*- coding: utf-8 -*-
# $File: util.py
# $Date: 2015-10-06 10:34
# $Author: Matt Zhang <mattzhang9[at]gmail[dot]com>

from hp import get_db
from hpconfig import *
from hputil import *
from functools import wraps

db = get_db()


@classmethod
def _get_one(cls, *args, **kwargs):
    try:
        # print args, kwargs
        objs = cls.objects(*args, **kwargs)
        # print objs
        if len(objs) == 0:
            return None
        if len(objs) > 1:
            raise RuntimeError((
                "{}.get_one failed: more than one object with" +
                "  query:\n" +
                "    {}\n" +
                "    {}\n").format(cls.__name__, args, kwargs))
        return objs[0]
    except mongoengine.errors.ValidationError:
        return None
    except RuntimeError:
        return None


setattr(db.Document, 'get_one', _get_one)
