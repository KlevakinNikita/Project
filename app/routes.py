from flask import render_template, request
from flask_login import current_user
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from app import app
from app.forms import LoginForm
from app import User
from flask import g
import re
import logging

@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():
    # current_user = g.
    return render_template('index.html', title='Home Page')

@app.route('/register', methods=['GET', 'POST'])
def register():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password1' in request.form and 'email' in request.form:
        # Create variables for easy access
        user = User(username=request.form['username'], email=request.form['email'])
        user.set_password(request.form['password1'])

        # Check if account exists using MySQL
        engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
        DBSession = sessionmaker(bind=engine)
        session = DBSession()
        account = session.query(User).all()
        flag = False
        for value in account:
            if value.username == user.username:
                flag = True

        # If account exists show error and validation checks
        if flag == True:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', user.email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', user.username):
            msg = 'Username must contain only characters and numbers!'
        elif not user.username or not user.email:
            msg = 'Please fill out the form!'
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            session.add(user)
            session.commit()
            msg = 'You have successfully registered!'
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('register.html', msg=msg)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User(username=request.form['username'])
        logging.info(f"Вход в базу данных" + user.username)
        if user is None or not user.check_password_hash(request.form['password']):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)