from flask import Flask
app = Flask(__name__)
app.secret_key = ""
app.debug = True

from qchapp.views import *

if __name__ == '__main__':
    app.run()

