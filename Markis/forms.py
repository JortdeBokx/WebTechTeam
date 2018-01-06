from wtforms import Form, StringField, PasswordField, BooleanField, validators

class registerForm(Form):
	firstname = StringField("First Name", [validators.Length(min=1, max=20)], render_kw={"placeholder": "First Name"})
	lastname = StringField("Last Name", [validators.Length(min=1, max=20)], render_kw={"placeholder": "Last Name"})
	email = StringField("E-mail", [validators.Email(message="Please enter a valid email address")], render_kw={"placeholder": "Email"})
	username = StringField("Username", [validators.Length(min=3, max=35)], render_kw={"placeholder": "Username"})
	password = PasswordField("Password", [validators.Length(min=8, max=64)], render_kw={"placeholder": "Password"})
	password2 = PasswordField("Confirm Password", [
		validators.Length(min=8, max=64),
		validators.EqualTo('password', message="Both passwords need to match!")
	], render_kw={"placeholder": "Password Confirmation"})
class loginForm(Form):
	username = StringField("Username", [validators.Length(min=3, max=35)], render_kw={"placeholder": "Username"})
	password = PasswordField("Password", [validators.Length(min=8, max=64)], render_kw={"placeholder": "Password"})
	keepLoggedIn = BooleanField("")
