from db import db

class ColumnModel(db.Model):
	__tablename__ = 'columns'
	
	id = db.Column(db.Integer, primary_key=True)
	column_name = db.Column(db.String(100))
	column_type = db.Column(db.String(100))
	column_length = db.Column(db.Integer)
	column_precision = db.Column(db.Integer)
	column_nullable = db.Column(db.Boolean)
	table_id = db.Column(db.Integer,db.ForeignKey('tables.id'))
	table = db.relationship('TableModel')
	
	def __init__(self, column_name, column_type, column_length, column_precision, column_nullable):
		self.column_name = column_name
		self.column_type = column_type
		self.column_length = column_length
		self.column_precision = column_precision
		self.column_nullable = column_nullable

	def json(self):
		return {
		    'column_id'          : self.id
			, 'column_name'      : self.column_name
			, 'column_type'      : self.column_type
			, 'column_length'    : self.column_length
			, 'column_precision' : self.column_precision
			, 'column_nullable'  : self.column_nullable
		}
	
	
	@classmethod
	def get_columns_by_table_id(cls,_id):
		return cls.query.filter_by(table_id=_id).all()

