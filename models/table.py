from db import db

class TableModel(db.Model):
	__tablename__ = 'tables'
	
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100))
	description = db.Column(db.String(1000))
	
	def __init__(self, name):
		self.name = name
		self.description = description
		
	def json(self):
		return {'id': self.id, 'name': self.name, 'description': self.description}
	
	@classmethod
	def find_by_name(cls,name):
		return cls.query.filter_by(name=name).first()
