#!/usr/bin/python
# -*- coding: utf-8 -*-
# $File: user.py
# $Date: 2015-10-06 10:31
# $Author: Matt Zhang <mattzhang9[at]gmail[dot]com>

from util import *
from model import *
from flask import request, request, jsonify, g
from hp import get_app

from flask_httpauth import HTTPBasicAuth
app = get_app()
#auth = HTTPBasicAuth()

# For test
@app.route('/test/delete/<string:email>')
def delete_user(email):
    User.delete_user(email)
    return jsonify(success=1)


@app.route('/senddata', methods=['POST'])
@auth.login_required
def send_data():
    print request.headers
    req = request.json
    g.user.data = req
    g.user.save()
    return jsonify(success=1)


@app.route('/user/register', methods=['POST'])
def register():
    req = request.json
    email = req.get('email')
    pwd = req.get('pwd')
    exists = User.objects(email=email)
    if len(exists):
        return jsonify(error=u'RepeatRegisteration')
    user = User(email=email)
    user.hash_password(pwd)
    user.save()
    return jsonify(token=user.generate_auth_token())


@app.route('/user/login', methods=['POST'])
def login():
    req = request.json
    email = req.get('email')
    pwd = req.get('pwd')
    r = verify(email, pwd)
    if r == False:
        return jsonify(success=0)
    else:
        token = g.user.generate_auth_token()
        return jsonify(token=token)

