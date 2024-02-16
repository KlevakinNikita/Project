from flask import render_template, request
from flask_login import current_user
from app import app
import sqlalchemy as sa
from app import app, db
from app.forms import LoginForm
from app.models import User
import sqlite3

@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():
        #connection = sqlite3.connect(db)
        #cursor = connection.cursor()
        #data = cursor.execute('SELECT * FROM USERS').fetchall()
        #print(data)
        #connection.commit()
    return render_template('index.html')

@app.route('/register')
def register():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM form WHERE username = %s', (username,))
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            cursor.execute('INSERT INTO accounts VALUES (NULL, %s, %s, %s)', (username, password, email,))
            mysql.connection.commit()
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
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        user = db.session.scalar(sa.select(User).where(User.username == form.username.data))
        print(user)
    if form.validate_on_submit():
        print('work')
        flash('Login requested for user {}, remember_me={}'.format(form.username.data, form.remember_me.data))
        print('ОК')
        return redirect('/index')
    return render_template('login.html', title='Sign In', form=form)