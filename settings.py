# -*- coding:utf-8 -*-

# Project Dirs
from os.path import dirname, join, realpath
ROOT_DIR = realpath(join(dirname(__file__)))
TEMPLATE_DIR = realpath(join(dirname(__file__), 'templates'))
DATA_DIR = realpath(join(dirname(__file__), 'data'))
STATIC_DIR = realpath(join(dirname(__file__), 'static'))

# Development Secret Key
SECRET_KEY = 'liw!a4!0^&-zzfd6ivm2m##$s*ld76d1($)k#jtnneievp2$vb'

# Pagination
PAGE_SIZE = 5

# DB Configuration

DB_NAME = 'qchapp'
DB_HOST = 'localhost'
DB_PORT = 27017
DB_USER = ''
DB_PASSWORD = ''

# Override Default Settings
try:
    from local_settings import *
except:
    pass
