from flask import Flask, render_template, send_from_directory

app = Flask(__name__, static_url_path='/static')

@app.route('/')
def home():
	return render_template('home.html')

@app.route('/about')
def about():
	return render_template('about.html')

@app.route('/register')
def register():
	return render_template('register.html')

@app.route('/login')
def login():
	return render_template('login.html')

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