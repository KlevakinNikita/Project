import os
import sqlite3
import logging
import time
from pathlib import Path

db_name = 'user.db'
BASE_DIR = Path(__file__).resolve().parent.parent.parent
TEMPLATES_DIR = BASE_DIR.joinpath('tmp')

logging.basicConfig(level=logging.INFO, filename="log_" + str(time.time()).replace('.', '') + ".log",filemode="w")
connection = sqlite3.connect(db_name)
cursor = connection.cursor()
cursor.execute('''
            CREATE TABLE IF NOT EXISTS USERS (
            id INTEGER NOT NULL PRIMARY KEY,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            email TEXT NOT NULL
                   )''')
logging.info(f"База данных создана")
connection.commit()