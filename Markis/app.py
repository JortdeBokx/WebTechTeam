#############################################
#				Imports 					#
#############################################

import os
from urllib.parse import urlparse, urljoin

from flask import Flask, render_template, request, send_from_directory, redirect, url_for, flash, abort, send_file
from flask_login import LoginManager, login_user, logout_user
from passlib.hash import sha256_crypt
from sqlalchemy import create_engine
from sqlalchemy.sql import text
from werkzeug.utils import secure_filename

from forms import registerForm, loginForm, uploadFileForm, profileForm

app = Flask(__name__, static_url_path='/static')

UPLOAD_FOLDER = "C:/Users/s164376/Documents/WebTechTeam/Markis/uploads" #Put your upload folder here, used by drag&drop upload
ALLOWED_EXTENSIONS = ['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif']
REQUIRED_SUBJECT_SUBFOLDERS = ['exams', 'homework', 'literature', 'misc', 'summaries']
ICONS = {'music_note': 'm4a,mp3,oga,ogg,webma,wav', 'archive': '7z,zip,rar,gz,tar', 'photo': 'ico,jpe,jpeg,jpg,png,svg,webp', 'gif':'gif', 'picture_as_pdf': 'pdf', 'insert_drive_file': 'txt', 'local_movies': '3g2,3gp,3gp2,3gpp,mov,qt,mp4,m4v,ogv,webm', 'code': 'atom,plist,bat,bash,c,cmd,coffee,css,hml,js,json,java,less,markdown,md,php,pl,py,rb,rss,sass,scpt,swift,scss,sh,xml,yml',  'web': 'htm,html,mhtm,mhtml,xhtm,xhtml'}
SUBJECTS_PATH = "/subject"
PATHS_IGNORE_BREADCRUMB = {'subject': SUBJECTS_PATH}

#############################################
#				Databse Setup				#
#############################################

engine = create_engine('mysql://markis:dlSvw7noOQbiExlU@cs-students.nl:3306/markis', pool_pre_ping=True)
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['FILE_BASE_DIR'] = os.path.join(app.root_path, "storage")
app.secret_key = 'kjdnkjfn89dbndh7cg76chb7hjhsbGHmmDDEaQc4By9VH5667HkmFxdxAjhb5Eub' # This is just something random, used for sessions


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
login_manager.login_message = "You need to be logged in to view this page!"

#############################################
#				App routes					#
#############################################

@app.route('/')
def home():
	conn = engine.connect()
	subjects = conn.execute(text("SELECT subject_id, subject_name, faculty_name FROM subjects LEFT JOIN faculties ON faculty_id = SUBSTR(subject_id, 1) ORDER BY subject_id ASC")).fetchall()
	faculties = conn.execute(text("SELECT * FROM faculties")).fetchall()
	conn.close()
	return render_template('home.html', subjects=subjects, faculties=faculties)

@app.route('/uploadfile', methods=["GET", "POST"])
def uploadFile():
	if request.method == "POST":
		if 'file' not in request.files:
			flash('No selected items')
			return "No selected items"
		file = request.files['file']
		if file.filename == '':
			flash('No file selected')
			return "No file selected"
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			return redirect(url_for('uploaded_file',
												filename=filename))
		else:
			return "File not allowed"
	else:
		return "Only POST Methods allowed"

@app.route(SUBJECTS_PATH,)
def subjectGoHome():
	return redirect("/", code=302)

@app.route(SUBJECTS_PATH +'/<subjectid>/',)
#@login_required
def subject(subjectid):
	subjectDataSet = getSubjectData(subjectid.upper())
	if subjectDataSet == None:
		return render_template('404.html', reason="nosubject"), 404
	else:
		foldersToShow = getSubjectFolders(subjectid)
		return render_template('subject.html', subjectDataSet = subjectDataSet, folders = foldersToShow)


@app.route('/form/getUploadForm', methods=["GET", "POST"])
def uploadFileGetForm():
	form = uploadFileForm(request.form)
	conn = engine.connect()
	subjects = conn.execute(text("SELECT subject_id, subject_name, faculty_name FROM subjects LEFT JOIN faculties ON faculty_id = SUBSTR(subject_id, 1) ORDER BY subject_id ASC")).fetchall()
	conn.close()
	form.subject.choices = [(g.subject_id, g.subject_id + ' - ' + g.subject_name) for g in subjects]
	return render_template('uploadForm.html', form=form)


@app.route(SUBJECTS_PATH + '/<subjectid>/<path:subfolder>',)
#@login_required
def subjectfiles(subjectid, subfolder):
	subjectDataSet = getSubjectData(subjectid)
	if subjectDataSet == None:
		res =  render_template('404.html', reason="nosubject"), 404
	Path = os.path.join(app.config['FILE_BASE_DIR'], subjectid, subfolder)
	if not os.path.exists(Path):
		if not checksubjectPath(subjectid):
			res = render_template('404.html', reason="nopath"), 404
	else:
		if os.path.isdir(Path):
			foldersToShow = getFoldersToShow(Path)
			filesToShow = getFilesToShow(Path, subfolder, subjectid.upper())
			res =  render_template('files.html', folders=foldersToShow, files=filesToShow, subjectDataSet = getSubjectData(subjectid.upper()))
		elif os.path.isfile(Path):
			res = send_file(Path)
		else:
			res = render_template('404.html', reason="nopath"), 404
	return res



@app.route('/profile', methods=["GET", "POST"])
#@login_required
def profile():
	form = profileForm(request.form)
	if request.method == "POST" and form.validate():
		conn = engine.connect()
		username = form.username.data
		first_name = form.firstname.data
		last_name = form.lastname.data
		email = form.email.data
		password = sha256_crypt.hash(form.password.data)
		if form.password.data == '':
			s = text("UPDATE users SET first_name=:f, last_name=:l, username=:u, email=:e WHERE id=:i")
		else:
			s = text("UPDATE users SET first_name=:f, last_name=:l, username=:u, password=:p, email=:e WHERE id=:i")
		rv = conn.execute(s, f=first_name, l = last_name, u=username, e=email, p=password, i=4)
		conn.close()
		return redirect(url_for('profile'), code=302)	
	else:
		conn = engine.connect()
		s = text("SELECT * FROM users WHERE id=:i")
		rv = conn.execute(s, i=4).fetchall()
		conn.close()
		data = rv[0]
		form = profileForm(firstname=data['first_name'], lastname=data['last_name'], email=data['email'], username=data['username'])
		return render_template('profile.html', form=form)

@app.route('/favorites')
#@login_required
def favorites():
	return render_template('favorites.html')

@app.route("/logout")
def logout():
	logout_user()
	return redirect("/login", code=302)

@app.route('/register', methods=['GET', 'POST'])
def register():
	form = registerForm(request.form)
	if request.method == 'POST' and form.validate():
		conn = engine.connect()

		username = form.username.data
		first_name = form.firstname.data
		last_name = form.lastname.data
		email = form.email.data
		password = sha256_crypt.hash(form.password.data)
		s = text("INSERT INTO users (first_name, last_name, username, password, email) VALUES (:f, :l, :u, :p, :e)")
		rv = conn.execute(s, f=first_name, l = last_name, u=username, p=password, e=email)
		conn.close()
		if str(rv):
			return redirect(url_for('login'))
	else:
		return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
	form = loginForm(request.form)
	if request.method == 'POST' and form.validate():

		# Get the password Hash from  the DB where username
		conn = engine.connect()
		s = text("SELECT id, password FROM users WHERE username=:u")
		rv = conn.execute(s, u= str(form.username.data) ).fetchall()
		conn.close()
		#return str(rv[0]['password'])
		if sha256_crypt.verify(form.password.data, str(rv[0]['password'])):
			user = User(rv[0]['id'])
			user.authenticate(form.username.data)
			login_user(user)
		else:
			return "Wrong password"

		flash('Logged in successfully.')

		next = request.args.get('next')
		if not is_safe_url(next):
			return abort(400)

		return redirect(next or url_for('home'))
	else:
		return render_template('login.html', form=form)

#############################################
#			Template Filters				#
#############################################

@app.template_filter('file_icon')
def icon_fmt(filename):
	i = 'insert_drive_file'
	for icon, exts in ICONS.items():
		if filename.split('.')[-1] in exts:
			i = icon
	return i

@app.template_filter('breadcrumb')
def getBreadcrumbPath(url):
	r = {'home': '/'}
	currpath = ''
	urlList = url.split('/')
	urlList = list(filter(('').__ne__, urlList))
	for section in urlList:
		currpath = currpath + '/' + section
		r[section] =  currpath
	for pathnames in PATHS_IGNORE_BREADCRUMB:
		r.pop(pathnames)
	return r

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

@app.route('/img/<path:filename>')
def image(filename):
	return send_from_directory('img',
							   filename)
@app.route('/favicon.ico')
def favicon():
	return send_from_directory('img',
							   'favicon.ico')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
		return send_from_directory(app.config['UPLOAD_FOLDER'],
								filename)

#############################################
#			     Error Pages    			#
#############################################

@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'), 404

@app.errorhandler(403)
def page_not_found(e):
	return render_template('403.html'), 403

@app.errorhandler(418)
def page_not_found(e):
	return render_template('418.html'), 418

@app.errorhandler(500)
def page_not_found(e):
	return render_template('500.html'), 500

#############################################
#			   Helper Functions 			#
#############################################

@login_manager.user_loader
def load_user(userid):
	return User(userid)

def is_safe_url(target):
	ref_url = urlparse(request.host_url)
	test_url = urlparse(urljoin(request.host_url, target))
	return test_url.scheme in ('http', 'https') and \
		   ref_url.netloc == test_url.netloc

def allowed_file(filename):
		return '.' in filename and \
		filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def getSubjectData(subjectid):
	facultyid = int(subjectid[0])
	conn = engine.connect()
	s = text("SELECT subject_id, subject_name, faculty_name FROM subjects, faculties WHERE subject_id=:u and faculty_id = :i")
	rv = conn.execute(s, u=subjectid, i=facultyid).fetchone()
	conn.close()
	return rv


def makeSubjectFolder(subjectid):
	# return true if a new folder was made, false if not
	created = False
	FolderPath = os.path.join(app.config['FILE_BASE_DIR'], subjectid)
	os.makedirs(FolderPath)
	for requiredFolder in REQUIRED_SUBJECT_SUBFOLDERS:
		if requiredFolder not in os.listdir(FolderPath):
			newPath = os.path.join(FolderPath, requiredFolder)
			os.makedirs(newPath)
			created = True
	return created


def checksubjectPath(subjectid):
	#return true if a new folder was made, false if not
	created = False
	FolderPath = os.path.join(app.config['FILE_BASE_DIR'], subjectid)
	if not os.path.exists(FolderPath):
		created = makeSubjectFolder(subjectid)
	for requiredFolder in REQUIRED_SUBJECT_SUBFOLDERS:
		if requiredFolder not in os.listdir(FolderPath):
			newPath = os.path.join(FolderPath, requiredFolder)
			created = True
			os.makedirs(newPath)

	return created


def getSubjectFolders(subjectID):
	checksubjectPath(subjectID)
	foldersToShow = []
	PathToSubjects = os.path.join(app.config['FILE_BASE_DIR'], subjectID)
	for subFolder in os.listdir(PathToSubjects):
		SubFolderPath = os.path.join(PathToSubjects, subFolder)
		if os.path.isdir(SubFolderPath):
			info = {}
			info['name'] = subFolder
			info['hasContent'] = os.listdir(SubFolderPath) != []
			foldersToShow.append(info)
	return foldersToShow

def getFoldersToShow(FolderPath):
	foldersToShow = []
	for folder in os.listdir(FolderPath):
		newPath = os.path.join(FolderPath, folder)
		if os.path.isdir(newPath):
			info={}
			info['name'] = folder
			info['hasContent'] = os.listdir(newPath) != []
			foldersToShow.append(info)
	return foldersToShow


def FileExists(relativePath, subject, filename):
	#returns file id, otherwise empty set []
	conn = engine.connect()
	pattern = "%" +relativePath+ "%"
	s = text(
		"SELECT file_ID FROM files WHERE path LIKE :p and subject_code = :s and name = :n")
	rv = conn.execute(s, p=pattern, s=subject, n=filename).fetchone()
	conn.close()
	if not rv:
		return []
	else:
		return rv[0]


def getFilesToShow(FolderPath, relativePath, subject):
	files = []
	for file in os.listdir(FolderPath):
		newPath = os.path.join(FolderPath, file)
		if not os.path.isdir(newPath):
			fileID = FileExists(relativePath, subject, file)
			if fileID:
				conn = engine.connect()
				s = text("SELECT files.file_id, files.name, DATE(files.upload_date) AS upload_date, SUM(vote)  AS votes, users.username AS uploader, files.path as path FROM files INNER JOIN user_file_vote ON files.file_ID = user_file_vote.file_ID INNER JOIN users ON files.uploader_ID = users.id WHERE files.file_ID = :p;")
				rv = conn.execute(s, p=fileID).fetchone()
				d = dict(rv.items())
				d['size'] = str( round(os.path.getsize(newPath)/1000, 1)) + " kB"
				d['path'] = SUBJECTS_PATH + "/" + subject + "/" + d['path'] + "/" + d['name']
				files.append(d)
	return files

#############################################
#               Data Objects 	        	#
#############################################

class User:

	def __init__(self, uid):
		self.is_authenticated = False
		self.is_active = False
		self.is_anonymous = True
		self.username = None
		self.user_id = uid

	def __repr__(self):
		return "%d/%s" % (self.user_id, self.username)

	def get_id(self):
		conn = engine.connect()
		s = text("SELECT id FROM users WHERE username=:u")
		rv = conn.execute(s, u=self.username).fetchall()
		conn.close()
		return str(rv[0]['id'])

	def authenticate(self, username):
		self.is_authenticated = True
		self.is_active = True
		self.is_anonymous = False
		self.username = username

	def setUsername(self, username):
		self.username = username

	def get(user_id):
		return self

	def returnUsername(self):
		return self.username

#############################################
#   Fasten your seatbelts, here we go! 		#
#############################################

if __name__ == '__main__':
	app.run(debug=True)
