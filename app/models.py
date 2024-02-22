from datetime import datetime, timezone
from typing import Optional
import sqlalchemy.orm as so
import sqlalchemy as sa
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.ext.declarative import declarative_base
from app import login
from config import Config
from app import app

from app import Base

class User(Base):
    __tablename__ = 'Users'
    id = sa.Column(sa.Integer, primary_key=True, unique=True, autoincrement=True)
    username = sa.Column(sa.String(64), index=True, unique=True)
    email = sa.Column(sa.String(120), index=True, unique=True)
    role = sa.Column(sa.Integer, default=0)
    password_hash = sa.Column(sa.String(256))

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login.user_loader
def load_user(id):
    return User.get(user_id)