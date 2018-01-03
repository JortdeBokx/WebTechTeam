from flask import Flask, render_template, request, send_from_directory

from forms import registerForm, loginForm

app = Flask(__name__, static_url_path='/static')


#############################################
#				App routes					#
#############################################

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