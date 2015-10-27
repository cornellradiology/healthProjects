#!/usr/bin/python
# -*- coding: utf-8 -*-
# $File: hpconfig.py
# $Date: 2015-10-06 10:32
# $Author: Matt Zhang <mattzhang9[at]gmail[dot]com>


class _DefaultConfig(object):
    HOST = '0.0.0.0'
    PORT = 54321

    OPTIONS = {'debug': True}

    MONGODB_SETTINGS = {
        'DB': 'hp',
        'HOST': 'localhost',
        'PORT': 27017,
    }

app_config = _DefaultConfig()
