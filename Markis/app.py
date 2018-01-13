#############################################
#				Imports 					#
#############################################

import datetime
import os
from urllib.parse import urlparse, urljoin

from flask import Flask, render_template, request, send_from_directory, redirect, url_for, flash, abort, send_file, \
	json, make_response, current_app, session
from flask_login import LoginManager, login_user, logout_user, current_user, login_required, UserMixin
from flask_principal import Principal, Permission, RoleNeed, identity_changed, Identity, AnonymousIdentity, \
	identity_loaded, UserNeed
from passlib.hash import sha256_crypt
from sqlalchemy import create_engine
from sqlalchemy.sql import text
from werkzeug.utils import secure_filename

from forms import registerForm, loginForm, uploadFileForm, profileForm

app = Flask(__name__, static_url_path='/static')

ALLOWED_EXTENSIONS = ['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif']
REQUIRED_SUBJECT_SUBFOLDERS = ['exams', 'homework', 'literature', 'misc', 'summaries']
ICONS = {'music_note': 'm4a,mp3,oga,ogg,webma,wav', 'archive': '7z,zip,rar,gz,tar', 'photo': 'ico,jpe,jpeg,jpg,png,svg,webp', 'gif':'gif', 'picture_as_pdf': 'pdf', 'insert_drive_file': 'txt', 'local_movies': '3g2,3gp,3gp2,3gpp,mov,qt,mp4,m4v,ogv,webm', 'code': 'atom,plist,bat,bash,c,cmd,coffee,css,hml,js,json,java,less,markdown,md,php,pl,py,rb,rss,sass,scpt,swift,scss,sh,xml,yml',  'web': 'htm,html,mhtm,mhtml,xhtm,xhtml'}
SUBJECTS_PATH = "/subject"
PATHS_IGNORE_BREADCRUMB = {'subject': SUBJECTS_PATH}
INITIAL_YEAR= 2010
#############################################
#				Databse Setup				#
#############################################

engine = create_engine('mysql://markis:dlSvw7noOQbiExlU@cs-students.nl:3306/markis', pool_pre_ping=True)
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
app.config['FILE_BASE_DIR'] = os.path.join(app.root_path, "storage")
app.secret_key = 'kjdnkjfn89dbndh7cg76chb7hjhsbGHmmDDEaQc4By9VH5667HkmFxdxAjhb5Eub' # This is just something random, used for sessions


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
login_manager.login_message = "You need to be logged in to view this page!"

principals = Principal(app)
admin_permission = Permission(RoleNeed('admin'))

#############################################
#				App routes					#
#############################################


@app.route('/')
def home():
	if not current_user.is_active:
		return redirect(url_for('login'))
	conn = engine.connect()
	subjects = conn.execute(text("SELECT subject_id, subject_name, faculty_name FROM subjects LEFT JOIN faculties ON faculty_id = SUBSTR(subject_id, 1) ORDER BY subject_id ASC")).fetchall()
	faculties = conn.execute(text("SELECT * FROM faculties")).fetchall()
	conn.close()
	return render_template('home.html', subjects=subjects, faculties=faculties)

@app.route('/admin/')
@admin_permission.require(http_exception=403)
@login_required
def do_admin_index():
	data = []
	conn = engine.connect()
	s = text("SHOW TABLES")
	rv = conn.execute(s).fetchall()
	
	for table in rv:
		s = text("SELECT * FROM " + table[0])
		rv2 = conn.execute(s).fetchall()
		data.append(table[0])
		data.append(rv2)
	conn.close()
	print("D= " + str(data))
	return render_template('admin.html', tables=rv, data=data)

#@app.route('/uploadfile', methods=["GET", "POST"])
#def uploadFile():
#	if request.method == "POST":
#		file = request.files['file']
#		if file.filename == '':
#			flash('No file selected')
#			return make_response('No file selected', 400)
#		if file and allowed_file(file.filename):
#			filename = secure_filename(file.filename)
#			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#
#			return redirect(url_for('uploaded_file',
#												filename=filename))
#		else:
#			return make_response('File not allowed', 400)
#	else:
#		return make_response('Only POST messages allowed', 400)


@app.route(SUBJECTS_PATH,)
@login_required
def subjectGoHome():
	return redirect("/", code=302)

@app.route(SUBJECTS_PATH +'/<subjectid>/',)
@login_required
def subject(subjectid):
	subjectDataSet = getSubjectData(subjectid.upper())
	if subjectDataSet == None:
		return render_template('404.html', reason="nosubject"), 404
	else:
		foldersToShow = getSubjectFolders(subjectid)
		return render_template('subject.html', subjectDataSet = subjectDataSet, folders = foldersToShow)


@app.route('/form/getuploadform', methods=["GET", "POST"])
@login_required
def uploadFileGetForm():
	form = uploadFileForm(request.form)
	conn = engine.connect()
	subjects = conn.execute(text(
		"SELECT subject_id, subject_name, faculty_name FROM subjects LEFT JOIN faculties ON faculty_id = SUBSTR(subject_id, 1) ORDER BY subject_id ASC")).fetchall()
	conn.close()
	form.subject.choices = [('course', 'Course')]
	yearToShow = getYearsAvailable()
	form.opt1.choices = yearToShow
	form.opt1.default = yearToShow[-1][0]
	for g in subjects:
		form.subject.choices.append((g.subject_id, g.subject_id + ' - ' + g.subject_name))
	form.process()

	if request.method == "GET":
		return render_template('uploadForm.html', form=form)
	elif request.method == "POST":
		print(form.subject.data)
		if form.validate():
			uploaderid = current_user.get_id()
			subjectid = form.subject.data
			category = form.filetype.data
			opt1 = form.opt1.data
			opt2 = form.opt2.data
			print(opt1)
			print(opt2)
			file = request.files["file"]
			filename = secure_filename(file.filename)
			if file.filename == '':
				flash('No file selected')
	else:
		return abort(405)



@app.route(SUBJECTS_PATH + '/<subjectid>/<path:subfolder>',)
@login_required
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
			filesToShow = getFilesToShow(Path, subfolder, subjectid.upper(), current_user.get_id())
			res =  render_template('files.html', folders=foldersToShow, files=filesToShow, subjectDataSet = getSubjectData(subjectid.upper()))
		elif os.path.isfile(Path):
			res = send_file(Path)
		else:
			res = render_template('404.html', reason="nopath"), 404
	return res

@app.route('/setfavorite', methods=["POST"])
def setFavorite():
	if request.method == "POST":
		if current_user.is_authenticated and current_user.is_active:
			if request.method == 'POST':
				userid = current_user.get_id()
				fileid = int(request.json['fileid'])
				if fileid is not None or type(fileid) is not int:
					if FileExistsByID(fileid):
						conn = engine.connect()
						s = text("SELECT COUNT(*) FROM user_file_favorite WHERE user_ID=:u AND file_ID=:f")
						rv = conn.execute(s, u=userid, f=fileid).fetchone()
						exists = dict(rv.items())['COUNT(*)']
						if exists:
							s = text("DELETE FROM user_file_favorite WHERE user_ID=:u AND file_ID=:f")
						else:
							s = text("INSERT INTO user_file_favorite (user_ID, file_ID) VALUES (:u, :f)")
						rv = conn.execute(s, u=userid, f=fileid)
						conn.close()
						return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}
					else:
						return make_response('File does not exist', 400)
				else:
					return make_response('Invalid FileID', 400)
		else:
			return abort(403)

@app.route('/removefavorite', methods=["POST"])
def removeFavorite():
	if current_user.is_authenticated and current_user.is_active:
		if request.method == 'POST':
			userid = current_user.get_id()
			fileid = int(request.json['fileid'])
			if fileid is not None and type(fileid) is int:
				if FileExistsByID(fileid):
					conn = engine.connect()
					s = text("DELETE FROM user_file_favorite WHERE user_ID = :u and file_ID = :f")
					rv = conn.execute(s, u=userid, f=fileid)
					conn.close()
					return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}
				else:
					return make_response('File does not exist', 400)
			else:
				return make_response('Invalid FileID', 400)
	else:
		return abort(403)




@app.route('/removefile', methods=["POST"])
def removeFile():
	if current_user.is_authenticated and current_user.is_active and current_user.hasRole('admin'):
		if request.method == 'POST':
			fileid = int(request.json['fileid'])
			if fileid is not None and type(fileid) is int:
				if FileExistsByID(fileid):
					conn = engine.connect()
					s = text("DELETE FROM files WHERE file_ID = :f")
					rv = conn.execute(s, f=fileid)
					conn.close()
					removeFileFromDisk(fileid)
					return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}
				else:
					return make_response('File does not exist', 400)
			else:
				return make_response('Invalid FileID', 400)
	else:
		return abort(403)


@app.route('/profile', methods=["GET", "POST"])
@login_required
def profile():
	uid = current_user.get_id()
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
		rv = conn.execute(s, f=first_name, l = last_name, u=username, e=email, p=password, i=uid)
		conn.close()
		return redirect(url_for('profile'), code=302)
	else:
		conn = engine.connect()
		s = text("SELECT * FROM users WHERE id=:i")
		rv = conn.execute(s, i=uid).fetchall()
		conn.close()
		data = rv[0]
		form = profileForm(firstname=data['first_name'], lastname=data['last_name'], email=data['email'], username=data['username'])
		return render_template('profile.html', form=form)




@app.route('/favorites')
@login_required
def favorites():
	userid = current_user.get_id()
	favorites = getFavoriteFiles(userid)
	return render_template('favorites.html', favorites=favorites)

@app.route("/logout")
def logout():
	logout_user()

	# Remove session keys set by Flask-Principal
	for key in ('identity.name', 'identity.auth_type'):
		session.pop(key, None)

	# Tell Flask-Principal the user is anonymous
	identity_changed.send(current_app._get_current_object(),
						  identity=AnonymousIdentity())
	flash("You are now successfully logged out", 'success')
	return redirect("/login", code=302)



@app.route('/register', methods=['GET', 'POST'])
def register():
	form = registerForm(request.form, engine)
	if request.method == 'POST' and form.validate():
		conn = engine.connect()
		username = form.username.data
		first_name = form.firstname.data
		last_name = form.lastname.data
		email = form.email.data
		password = sha256_crypt.encrypt(str(form.password.data))
		p = text("SELECT id FROM users WHERE email = :e")
		mailcheck = conn.execute(p, e=email).fetchone()
		if mailcheck:
			form.email.errors.append('An account with that email already exists')

		s = text("INSERT INTO users (first_name, last_name, username, password, email) VALUES (:f, :l, :u, :p, :e)")
		rv = conn.execute(s, f=first_name, l = last_name, u=username, p=password, e=email)
		conn.close()

		flash("You are now successfully registered", 'success')
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
		rv = conn.execute(s, u= str(form.username.data) ).fetchone()
		conn.close()
		if rv:
			if sha256_crypt.verify(str(form.password.data), str(rv['password'])):
				user = User(rv['id'])
				user.authenticate(rv['id'])
				login_user(user, remember=form.keepLoggedIn.data)
				identity_changed.send(current_app._get_current_object(),
									  identity=Identity(user.user_id))
			else:
				return render_template('login.html', error='Password incorrect', form=form)
		else:
			return render_template('login.html', error='Username not found', form=form)

		next = request.args.get('next')
		if not is_safe_url(next):
			return abort(400)

		return redirect(next or url_for('home'))
	else:
		return render_template('login.html', form=form)





@app.route('/votefile', methods=['POST'])
def voteFile():
	if current_user.is_authenticated and current_user.is_active:
		if request.method == 'POST':
			userid = current_user.get_id()
			fileid = request.json['fileid']
			newVote = request.json['vote']
			if type(userid) == int and  type(fileid) == int and  type(newVote) == int :
				if FileExistsByID(fileid):
					currentVote = getFileVote(userid, fileid)
					if currentVote == 0:
						if newVote != 0:
							InsertNewVote(userid, fileid, newVote)
							return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}
						else:
							return make_response('Vote is same as current vote', 400)
					elif currentVote == -1:
						if newVote == 1:
							UpdateVote(userid, fileid, currentVote, newVote)
							return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}
						elif newVote == 0:
							RemoveVote(userid, fileid)
							return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}
						else:
							return make_response('Vote is same as current vote', 400)
					elif currentVote == 1:
						if newVote == -1:
							UpdateVote(userid, fileid, currentVote, newVote)
							return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}
						elif newVote == 0:
							RemoveVote(userid, fileid)
							return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}
						else:
							return make_response('Vote is same as current vote', 400)
					else:
						return make_response('Current vote cannot be found', 500)
			else:
				return make_response('Data types incorrect', 400)
		else:
			return make_response('Only POST requests accepted', 400)
	else:
		return abort(403)

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

@identity_loaded.connect_via(app)
def on_identity_loaded(sender, identity):
	# Set the identity user object
	identity.user = current_user

	# Add the UserNeed to the identity
	if hasattr(current_user, 'user_id'):
		identity.provides.add(UserNeed(current_user.get_id()))
		if current_user.isAdmin == 1 :
			identity.provides.add(RoleNeed('admin'))


def FileExistsByID(fileid):
	conn = engine.connect()
	s = text(
		"SELECT * FROM files WHERE file_ID=:u")
	rv = conn.execute(s, u=fileid).fetchone()
	conn.close()
	return rv != []

def getFileVote(userid, fileid):
	conn = engine.connect()
	s = text(
		"SELECT IFNULL(vote, 0) AS vote FROM user_file_vote WHERE file_ID=:f and user_ID = :u")
	rv = conn.execute(s, u=userid, f=fileid).fetchone()
	conn.close()
	if not rv:
		return 0
	else:
		return dict(rv.items())['vote']


def InsertNewVote(userid, fileid, newVote):
	conn = engine.connect()
	s = text("INSERT INTO user_file_vote (user_ID, file_ID, vote) VALUES (:u, :f, 1)")
	rv = conn.execute(s, u=userid, f=fileid, v=newVote)
	conn.close()
	return rv

def UpdateVote(userid, fileid, currentVote, newVote):
	conn = engine.connect()
	s = text("UPDATE user_file_vote SET vote = :v WHERE user_ID = :u and file_ID = :f and vote = :c")
	rv = conn.execute(s, u=userid, f=fileid, v=newVote, c = currentVote)
	conn.close()
	return rv

def RemoveVote(userid, fileid):
	conn = engine.connect()
	s = text("DELETE FROM user_file_vote WHERE user_ID = :u and file_ID = :f")
	rv = conn.execute(s, u=userid, f=fileid)
	conn.close()
	return rv

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

def getYearsAvailable():
	initialPeriod = str(INITIAL_YEAR) + " - " + str(INITIAL_YEAR + 1) + " (and earlier)"
	years = [(INITIAL_YEAR, initialPeriod)]
	now = datetime.datetime.now()
	currentYear = now.year
	if now.month < 8:
		currentYear -= 1  # if between jan and august, make sure currentYear is first year of year period
	for year in range(INITIAL_YEAR + 1, currentYear + 1):
		yearPeriod = str(year) + " - " + str(year + 1)
		years.append((year, yearPeriod))
	return years

def removeFileFromDisk(fileid):
	conn = engine.connect()
	s = text(
		"SELECT path, name, subject_code FROM files WHERE file_ID = :i")
	rv = conn.execute(s, i=fileid).fetchone()
	conn.close()
	folderpath = rv['path']
	filename = rv['name']
	subjectid = rv['subject_code']
	if FileExistsInFolderStrucure(subjectid, folderpath, filename):
		FilePath = os.path.join(app.config['FILE_BASE_DIR'], subjectid, folderpath, filename)
		os.remove(FilePath)
		FolderPath = os.path.join(app.config['FILE_BASE_DIR'], subjectid, folderpath)
		try:
			os.removedirs(FolderPath)
			makeSubjectFolder(subjectid)
		except:
			pass

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


def FileExistsInDB(relativePath, subject, filename):
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

def getUserVote(fileid, userid):
	# returns 1 or -1 for user vote on file, 0 if not voted
	conn = engine.connect()
	s = text("SELECT IFNULL(vote,0) as vote FROM user_file_vote WHERE user_ID = :u and file_ID = :f")
	rv = conn.execute(s, u=userid, f=fileid).fetchone()
	if not rv:
		return 0
	else:
		return dict(rv.items())['vote']

def getUserFavorite(fileid, userid):
	conn = engine.connect()
	s = text("SELECT * FROM user_file_favorite WHERE user_ID = :u and file_ID = :f")
	rv = conn.execute(s, u=userid, f=fileid).fetchone()
	if rv:
		return 1
	else:
		return 0


def getFilesToShow(FolderPath, relativePath, subject, userid):
	files = []
	for file in os.listdir(FolderPath):
		newPath = os.path.join(FolderPath, file)
		if not os.path.isdir(newPath):
			fileID = FileExistsInDB(relativePath, subject, file)
			if fileID:
				conn = engine.connect()
				s = text(
					"SELECT files.file_id, files.name, DATE(files.upload_date) AS upload_date, IFNULL(SUM(vote), 0) AS votes, users.username AS uploader, files.path as path FROM files INNER JOIN user_file_vote ON files.file_ID = user_file_vote.file_ID INNER JOIN users ON files.uploader_ID = users.id WHERE files.file_ID = :p;")
				rv = conn.execute(s, p=fileID).fetchone()
				d = dict(rv.items())
				fileSize = round(os.path.getsize(newPath)/1000, 1)
				filesizestr = str(fileSize) + " kB" if fileSize <= 1000 else str(round(os.path.getsize(newPath)/1000000, 1)) + "MB"
				d['size'] = filesizestr
				d['downloadpath'] = SUBJECTS_PATH + "/" + subject + "/" + d['path'] + "/" + d['name']
				d['user_vote'] = getUserVote(d['file_id'], userid)
				d['user_favorite'] = getUserFavorite(d['file_id'], userid)
				files.append(d)
	return files


def FileExistsInFolderStrucure(subjectid, folderpath, filename):
	PathToCheck = os.path.join(app.config['FILE_BASE_DIR'], subjectid, folderpath, filename)
	return os.path.isfile(PathToCheck)

def getFavoriteFiles(userid):
	conn = engine.connect()
	s = text(
		"SELECT files.file_id, files.name, DATE(files.upload_date) AS upload_date, files.path as path, files.subject_code as subject_code FROM user_file_favorite AS fav RIGHT JOIN files ON fav.file_ID = files.file_ID WHERE user_id=:i")
	rv = conn.execute(s, i=userid).fetchall()
	favFilesThatExist = []
	for file in rv:
		d = dict(file.items())
		if FileExistsInFolderStrucure(d['subject_code'], d['path'], d['name']):
			newPath = os.path.join(app.config['FILE_BASE_DIR'], d['subject_code'], d['path'], d['name'])
			fileSize = round(os.path.getsize(newPath) / 1000, 1)
			filesizestr = str(fileSize) + " kB" if fileSize <= 1000 else str(
				round(os.path.getsize(newPath) / 1000000, 1)) + "MB"
			d['size'] = filesizestr
			d['downloadpath'] = SUBJECTS_PATH + "/" + d['subject_code'] + "/" + d['path'] + "/" + d['name']
			favFilesThatExist.append(d)
	conn.close()
	return favFilesThatExist


#############################################
#               Data Objects 	        	#
#############################################

class User(UserMixin):

	def __init__(self, uid, active=True):
		conn = engine.connect()
		#self.is_authenticated = False
		#self.is_active = False
		#self.is_anonymous = True
		self.user_id = uid
		rv = conn.execute(text('SELECT * FROM users WHERE id= :u'), u = uid).fetchone()
		self.first_name = rv['first_name']
		self.last_name = rv['last_name']
		self.username= rv['username']
		self.email = rv['email']
		self.password = rv['password']
		self.isAdmin = rv['is_admin']
		self.active = active
		conn.close()

	def get_id(self):
		return self.user_id

	def get_admin(self):
		return self.isAdmin

	def is_active(self):
		# Here you should write whatever the code is
		# that checks the database if your user is active
		return self.active

	def is_anonymous(self):
		return False

	def is_authenticated(self):
		return True

	def authenticate(self, uid):
		self.is_authenticated = True
		self.is_active = True
		self.is_anonymous = False
		self.user_id = uid

	def returnUsername(self):
		return self.username

#############################################
#   Fasten your seatbelts, here we go! 		#
#############################################

if __name__ == '__main__':
	app.run(debug=True)
