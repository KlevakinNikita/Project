from sqlalchemy import create_engine, MetaData, Table, Integer, String, \
    Column, DateTime, ForeignKey, Numeric
from sqlalchemy.ext.declarative import declarative_base
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

Base = declarative_base()
engine = create_engine('sqlite:///user.db')

class Users(db.Model):
    __tablename__ = 'Users'
    id = db.Column(Integer, primary_key=True)
    username = db.Column(String(64), nullable=False)
    email = db.Column(String(120), nullable=False)
    password_hash = db.Column(String(256), nullable=False)

Base.metadata.create_all(engine)