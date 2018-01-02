<<<<<<< HEAD
from flask import Flask, render_template, flash, redirect, url_for, session, logging, request
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, BooleanField, validators
from passlib.hash import sha256_crypt
=======
from flask import Flask, render_template, send_from_directory
>>>>>>> d68d85e3f1f0e5713264b054e267b6f1f8224da9

app = Flask(__name__, static_url_path='/static')

@app.route('/')
def home():
	return render_template('home.html')

@app.route('/about')
def about():
	return render_template('about.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
	form = registerForm(request.form)
	if request.method == 'POST' and form.validate():
		return "Done"
	else:
		return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
	form = loginForm(request.form)
	if request.method == 'POST' and form.validate():
		return "Logged in"
	else:
		return render_template('login.html', form=form)

class registerForm(Form):
	firstname = StringField("First Name", [validators.Length(min=1, max=20)])
	lastname = StringField("Last Name", [validators.Length(min=1, max=20)])
	email = StringField("E-mail", [validators.Email(message="Please enter a valid email address")])
	username = StringField("Username", [validators.Length(min=3, max=35)])
	password = PasswordField("Password", [validators.Length(min=8, max=64)])
	password2 = PasswordField("Confirm Password", [
		validators.Length(min=8, max=64),
		validators.EqualTo('password', message="Both passwords need to match!")
	])

class loginForm(Form):
	username = StringField("Username", [validators.Length(min=3, max=35)])
	password = PasswordField("Password", [validators.Length(min=8, max=64)])
	keepLoggedIn = BooleanField("Keep logged in?")

#############################################
#			Paths to static Files			#
#############################################

@app.route('/css/<path:filename>')
def css(filename):
	return send_from_directory('css',
                               filename)
@app.route('/js/<path:filename>')
def javascript(filename):
	return send_from_directory('js',
                               filename)


if __name__ == '__main__':
	app.run(debug=True)