### GENERATED AT: 2021-03-09 20:14:16

from db import db

class TestTableModel(db.Model):
	__tablename__ = 'test_table'

	id = db.Column(db.Integer, primary_key=True)
	col2 = db.Column(db.SmallInteger)
	col3 = db.Column(db.Integer)
	col4 = db.Column(db.Integer)
	col5 = db.Column(db.Numeric(18, 5, asdecimal=False))
	col6 = db.Column(db.Float)
	col10 = db.Column(db.String(50))
	col11 = db.Column(db.String(50))
	status = db.Column(db.String(100))

	def __init__(self, col2, col3, col4, col5, col6, col10, col11, status):
		self.col2 = col2
		self.col3 = col3
		self.col4 = col4
		self.col5 = col5
		self.col6 = col6
		self.col10 = col10
		self.col11 = col11
		self.status = status

	def update(self, col3, col4, col5, col6, col10, col11, status):
		self.col3 = col3
		self.col4 = col4
		self.col5 = col5
		self.col6 = col6
		self.col10 = col10
		self.col11 = col11
		self.status = status

	def json(self):
		return {
			'col2' : self.col2
			, 'col3' : self.col3
			, 'col4' : self.col4
			, 'col5' : self.col5
			, 'col6' : self.col6
			, 'col10' : self.col10
			, 'col11' : self.col11
			, 'status' : self.status
		}

	def json_with_id(self):
		return {
			self.id : self.json()
		}

	@classmethod
	def arguments(self):
		return {
			'logical_key': 'col2',
			'column_list': [
				{
					'name': 'col2',
					'type': ' int',
					'required': False
				},
				{
					'name': 'col3',
					'type': ' int',
					'required': True
				},
				{
					'name': 'col4',
					'type': ' int',
					'required': False
				},
				{
					'name': 'col5',
					'type': 'str',
					'required': False
				},
				{
					'name': 'col6',
					'type': ' float',
					'required': False
				},
				{
					'name': 'col10',
					'type': 'str',
					'required': False
				},
				{
					'name': 'col11',
					'type': 'str',
					'required': False
				},
				{
					'name': 'status',
					'type': 'str',
					'required': True
				},
			]
		}

	@classmethod
	def find_by_id(cls,_id):
		return cls.query.filter_by(id=_id).first()

	@classmethod
	def find_by_logical_key(cls,_id):
		return cls.query.filter_by(col2=_id).first()

	def save_to_db(self):
		db.session.add(self)
		db.session.commit()

	def delete_from_db(self):
		db.session.delete(self)
		db.session.commit()

