# -*- coding:utf-8 -*-

from flask import Flask
#from qchapp.views import *
import qchapp
import settings

app = Flask(__name__)
app.secret_key = settings.SECRET_KEY
app.debug = True

if __name__ == '__main__':
    qchapp.app.run()
