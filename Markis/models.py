from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy, Model
from sqlalchemy import func, Column, String, Integer, ForeignKey, DATETIME, CHAR, Boolean

from app import db #pylint: 


class Subject(Model):
	__tablename__ = 'subjects'
	subject_id = Column(String(45), unique=True, nullable=False, primary_key=True)
	subject_name = Column(String(200), unique=True, nullable=False)
	faculty_id = Column(Integer, ForeignKey('faculties.faculty_id'), unique=False, nullable=False)

	def __repr__(self):
		return '<Subject %r>' % self.subject_id


class File(Model):
	__tablename__ = 'files'
	file_id = Column(Integer, unique=True, nullable=False, primary_key=True)
	file_hash = Column(CHAR(40), unique=True, nullable=False)  # SHA-1 is always 40 chars long
	name = Column(String(200), unique=False, nullable=False)
	display_path = Column(String(200), unique=False, nullable=False)
	subject_id = Column(String(45), unique=False, nullable=False)
	type = Column(String(127), unique=False, nullable=False)  # 127 is the max length according to RFC 4288
	upload_date = Column(DATETIME, server_default=func.now(), nullable=False)
	uploader_username = Column(String(100), nullable=False)


class Faculty(Model):
	__tablename__ = 'faculties'
	faculty_id = Column(Integer, unique=True, nullable=False, primary_key=True)
	faculty_name = Column(String(100), unique=True, nullable=False)

	def __repr__(self):
		return '<Faculty %r>' % self.faculty_name


class Vote(Model):
	__tablename__ = 'user_file_vote'
	user_username = Column(String(100), unique=False, nullable=False, primary_key=True)
	file_id = Column(Integer, ForeignKey('files.file_id'), unique=False, nullable=False, primary_key=True)
	vote = Column(Integer, unique=False, nullable=False)


class Favorite(Model):
	__tablename__ = 'user_file_favorite'
	user_username = Column(String(100), unique=False, nullable=False, primary_key=True)
	file_id = Column(Integer, ForeignKey('files.file_id'), unique=False, nullable=False, primary_key=True)


class User(Model):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(100), unique=True)
    first_name = Column(String(100))
    last_name = Column(String(100))
    displayname = Column(String(100))
    email = Column(String(100))
    isAdmin = Column(Boolean)
    active = Column(Boolean)
    _authenticated = False

    def get_id(self):
    	return self.username

    def get_admin(self):
	    return self.isAdmin

    def is_active(self):
	    return self.active

    def is_anonymous(self):
	    return False

    def is_authenticated(self):
	    return self._authenticated

    def authenticate(self, username, password):
	    self.username = username
	    authenticated = True
	    self._authenticated = (authenticated is not None)
	    return self._authenticated

    def return_username(self):
	    return self.username