from sqlalchemy import create_engine, MetaData, Table, Integer, String, \
    Column, DateTime, ForeignKey, Numeric
from flask import Flask
from config import Config
from flask_login import LoginManager
from sqlalchemy.ext.declarative import declarative_base
from flask_wtf.csrf import CSRFProtect
import logging
import time

csrf = CSRFProtect()
app = Flask(__name__)
app.config.from_object(Config)
login = LoginManager(app)
login.login_view = 'login'

csrf.init_app(app)
logging.basicConfig(level=logging.INFO, filename=Config.LOG_PATH,filemode="w")
Base = declarative_base()

from app.models import User

engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)

Base.metadata.create_all(engine)
logging.info(f"База данных создана")

from app import routes