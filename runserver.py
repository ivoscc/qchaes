# -*- coding:utf-8 -*-

# Insert Project Root Dir to path
import sys
import imp
from os.path import join

try:
    imp.find_module('settings')  # Assumed to be in the same directory
except ImportError:
    sys.stderr.write("Error: Can't find the file 'settings.py' in the directory")
    sys.exit(1)

import settings
sys.path.insert(0, settings.ROOT_DIR)  # Insert Root dir into Path

from flask import Flask
#from qchapp.views import *
import qchapp.views
import settings

app = Flask(__name__)
app.secret_key = settings.SECRET_KEY
app.debug = True
if app.debug:
    #Logging
    import logging
    file_handler = logging.FileHandler('logs/qchapp.log')
    file_handler.setLevel(logging.WARNING)
    app.logger.addHandler(file_handler)

if __name__ == '__main__':
    qchapp.app.run()
