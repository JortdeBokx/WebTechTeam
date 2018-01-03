from wtforms import Form, StringField, TextAreaField, PasswordField, BooleanField, validators

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
	keepLoggedIn = BooleanField("")