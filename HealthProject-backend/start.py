#!manage/exec-in-virtualenv.sh
# -*- coding: utf-8 -*-
# $File: start.py
# $Author: He Zhang <mattzhang9[at]gmail[dot]com>

from hp import get_app
import api

app = get_app()

@app.route('/')
def hello():
    return 'hello'

def main():
    app.run(app.config['HOST'], app.config['PORT'], debug = True)


if __name__ == '__main__':
    main()
