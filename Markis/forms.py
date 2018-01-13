from sqlalchemy import text
from wtforms import Form, StringField, PasswordField, BooleanField, SelectField, validators, ValidationError

class registerForm(Form):

	def validate_email(self, field):  # here is where the magic is
		if self.mailIsDuplicate(field.data):  # check if in database
			raise ValidationError("There already exists an account with that email")

	firstname = StringField("First Name", [validators.Length(min=1, max=50)], render_kw={"placeholder": "First Name"})
	lastname = StringField("Last Name", [validators.Length(min=1, max=50)], render_kw={"placeholder": "Last Name"})
	email = StringField("E-mail", [validators.Email(message="Please enter a valid email address"), validate_email], render_kw={"placeholder": "Email"})
	username = StringField("Username", [validators.Length(min=3, max=35)], render_kw={"placeholder": "Username"})
	password = PasswordField("Password", [validators.Length(min=8, max=64)], render_kw={"placeholder": "Password"})
	password2 = PasswordField("Confirm Password", [
		validators.Length(min=8, max=64),
		validators.EqualTo('password', message="Both passwords need to match!")
	], render_kw={"placeholder": "Password Confirmation"})

	def mailIsDuplicate(self, email):
		conn = engine.connect()
		p = text("SELECT id FROM users WHERE email = :e")
		mailcheck = conn.execute(p, e=email).fetchone()
		conn.close()
		return True if mailcheck else False


class loginForm(Form):
	username = StringField("Username", [validators.Length(min=3, max=35)], render_kw={"placeholder": "Username"})
	password = PasswordField("Password", [validators.Length(min=8, max=64)], render_kw={"placeholder": "Password"})
	keepLoggedIn = BooleanField("")



class uploadFileForm(Form):
	subject = SelectField('Subject')
	filetype = SelectField('File Type', choices=[('category', 'Category'), ('exams', 'Exams'), ('hw', 'Homework'), ('lit', 'Literature'), ('misc','Miscellanious'), ('sum','Summaries')])
	opt1 = SelectField('Released/Made')
	opt2 = SelectField('Upload Type', choices=[('type', 'Type'), ('ans', 'Answers'), ('ques', 'Questions')])


class profileForm(Form):
	firstname = StringField("First Name", [validators.Length(min=1, max=20)], render_kw={"placeholder": "First Name"})
	lastname = StringField("Last Name", [validators.Length(min=1, max=20)], render_kw={"placeholder": "Last Name"})
	email = StringField("E-mail", [validators.Email(message="Please enter a valid email address")], render_kw={"placeholder": "Email"})
	username = StringField("Username", [validators.Length(min=3, max=35)], render_kw={"placeholder": "Username"})
	password = PasswordField("Password", [], render_kw={"placeholder": "Password"})

from app import engine



