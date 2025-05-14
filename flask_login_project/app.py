# from flask import Flask, render_template, request, redirect, url_for, session, flash
# import sqlite3
# from werkzeug.security import generate_password_hash, check_password_hash

# app = Flask(__name__)
# app.secret_key = "your_secret_key"  # Needed for session management
# DATABASE = "instance/users.db"

# # Function to connect to the database
# def get_db_connection():
#     conn = sqlite3.connect(DATABASE)
#     conn.row_factory = sqlite3.Row
#     return conn

# # Route to initialize the database
# @app.route('/init-db')
# def init_db():
#     conn = get_db_connection()
#     cursor = conn.cursor()
#     cursor.execute("""
#     CREATE TABLE IF NOT EXISTS users (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         username TEXT UNIQUE NOT NULL,
#         password TEXT NOT NULL
#     )
#     """)
#     conn.commit()
#     conn.close()
#     return "Database initialized!"

# @app.route('/')
# def home():
#     if "username" in session:
#         return render_template("home.html", username=session["username"])
#     return redirect(url_for("login"))

# @app.route('/login', methods=["GET", "POST"])
# def login():
#     if request.method == "POST":
#         username = request.form["username"]
#         password = request.form["password"]

#         conn = get_db_connection()
#         user = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
#         conn.close()

#         if user and check_password_hash(user["password"], password):
#             session["username"] = username
#             flash("Login successful!", "success")
#             return redirect(url_for("home"))
#         else:
#             flash("Invalid credentials!", "danger")

#     return render_template("login.html")

# @app.route('/register', methods=["GET", "POST"])
# def register():
#     if request.method == "POST":
#         username = request.form["username"]
#         password = request.form["password"]

#         hashed_password = generate_password_hash(password)

#         try:
#             conn = get_db_connection()
#             conn.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
#             conn.commit()
#             conn.close()
#             flash("Registration successful! Please log in.", "success")
#             return redirect(url_for("login"))
#         except sqlite3.IntegrityError:
#             flash("Username already exists!", "danger")

#     return render_template("register.html")

# @app.route('/logout')
# def logout():
#     session.pop("username", None)
#     flash("Logged out successfully!", "info")
#     return redirect(url_for("login"))

# if __name__ == '__main__':
#     app.run(debug=True)



# Store this code in 'app.py' file
import flask
from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re


app = Flask(__name__)


app.secret_key = 'your secret key'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'your password'
app.config['MYSQL_DB'] = 'geeklogin'

mysql = MySQL(app)

@app.route('/')
@app.route('/login', methods =['GET', 'POST'])
def login():
	msg = ''
	if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
		username = request.form['username']
		password = request.form['password']
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM accounts WHERE username = % s AND password = % s', (username, password, ))
		account = cursor.fetchone()
		if account:
			session['loggedin'] = True
			session['id'] = account['id']
			session['username'] = account['username']
			msg = 'Logged in successfully !'
			return render_template('index.html', msg = msg)
		else:
			msg = 'Incorrect username / password !'
	return render_template('login.html', msg = msg)

@app.route('/logout')
def logout():
	session.pop('loggedin', None)
	session.pop('id', None)
	session.pop('username', None)
	return redirect(url_for('login'))

@app.route('/register', methods =['GET', 'POST'])
def register():
	msg = ''
	if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form :
		username = request.form['username']
		password = request.form['password']
		email = request.form['email']
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM accounts WHERE username = % s', (username, ))
		account = cursor.fetchone()
		if account:
			msg = 'Account already exists !'
		elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
			msg = 'Invalid email address !'
		elif not re.match(r'[A-Za-z0-9]+', username):
			msg = 'Username must contain only characters and numbers !'
		elif not username or not password or not email:
			msg = 'Please fill out the form !'
		else:
			cursor.execute('INSERT INTO accounts VALUES (NULL, % s, % s, % s)', (username, password, email, ))
			mysql.connection.commit()
			msg = 'You have successfully registered !'
	elif request.method == 'POST':
		msg = 'Please fill out the form !'
	return render_template('register.html', msg = msg)
