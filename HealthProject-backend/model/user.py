#!/usr/bin/python
# -*- coding: utf-8 -*-
# $File: user.py
# $Date: Sat Jul 04 15:54:20 2015 +0800
# $Author: He Zhang <mattzhang9[at]gmail[at]com>


from util import *
from hp import *

from flask import Flask, abort, request, jsonify, g
from flask.ext.httpauth import HTTPBasicAuth
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import JSONWebSignatureSerializer as Serializer
import werkzeug

app = get_app()
db = get_db()
auth = HTTPBasicAuth()

Sex = enum('male', 'female')


class User(db.Document):

    email = db.StringField(required=True)
    password_hash = db.StringField(required=True)
    data = db.DictField()

    meta = {
        'indexes': [
            'email',
        ],
        'ordering': ['email']
    }

    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)

    def as_json(self, verbose=0):
        data = dict(
            email=self.email,
        )
        return {u'user': data}

    def encrypted_password(self, password):
        return pwd_context.encrypt(password)

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)
        
    def generate_auth_token(self):
        s = Serializer(app.config['SECRET_KEY'])
        return s.dumps(self.email)

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        print 'token:' + token
        try:
            data = s.loads(token)
        except:
            return None
        print 'data:{}'.format(data)
        user = User.get_one(email=data)
        return user

    # For test
    @classmethod
    def delete_user(cls, email):
        udummy = User.get_one(email=email)
        udummy.delete()


# To pass the authentification, you should use Basic Auth to provide phone and
# password or token. When using token, the password can be any value.
# Basic Auth can be implemented by `curl -u`, for more information, read
# http://stackoverflow.com/questions/20737031/curlss-option-u

@auth.verify_password
def verify(email_or_token, password):
    # first try to authenticate by token
    print 'Here!'
    print "token: {}".format(email_or_token)
    user = User.verify_auth_token(email_or_token)
    if not user:
        # try to authenticate with username/password
        user = User.get_one(email=email_or_token)
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True


@auth.error_handler
def authErrorHandler():
    print u'AUTH ERROR in'
    print request.url
    raise werkzeug.exceptions.Unauthorized
