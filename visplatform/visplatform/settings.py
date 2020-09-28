import os
import sys
from visplatform import app

SECRET_KEY = os.getenv('SECRET_KEY', 'secret string')
#本地数据库
MONGODB_SETTINGS ={
    'db': 'vis',
    'host': 'localhost',
    'port': 27017
}
#远程数据库
""" MONGODB_SETTINGS ={
    'db': 'vis',
    'host': '103.219.39.150',
    'port': 20055
} """
CSRF_ENABLED = True
COURSE_UPLOAD_FOLDER = 'visplatform/data'
PROJECT_UPLOAD_FOLDER = 'visplatform/js/test4project'
VISUALIZATION_FOLDER  = 'visplatform/data/visualization'
