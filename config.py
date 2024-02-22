import os
import time

basedir = os.path.abspath(os.path.dirname(__file__))
basedir_log = os.path.join(basedir, 'logging')
logfile = "log_" + str(time.time()).replace('.', '') + ".log"

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'user.db')
    LOG_PATH = os.path.join(basedir_log, logfile)