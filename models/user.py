from db import db

class UserModel(db.Model):
	__tablename__ = 'users'
	
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(100))
	password = db.Column(db.String(1000))
	role     = db.Column(db.String(100))
	
	def __init__(self, username, password, role):
		self.username = username
		self.password = password
		self.role = role

	@classmethod
	def find_by_username(cls, username):
		return cls.query.filter_by(username=username).first()
		
