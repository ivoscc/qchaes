# -*- coding:utf-8 -*-

# Development Secret Key
SECRET_KEY = 'liw!a4!0^&-zzfd6ivm2m##$s*ld76d1($)k#jtnneievp2$vb'

# Pagination
PAGE_SIZE = 5

# DB Configuration

DB_NAME = 'qchapp'
DB_HOST = ''
DB_PORT = 27857
DB_USER = ''
DB_PASSWORD = ''

# Override Default Settings
try:
    from local_settings import *
except:
    pass
