### GENERATED AT: 2021-02-27 14:16:44

from db import db

class CosTypeModel(db.Model):
	__tablename__ = 'cos_type'

	id = db.Column(db.Integer, primary_key=True)
	Cos_Type_Id = db.Column(db.Integer)
	Cos_Type = db.Column(db.String(100))
	Cos_Segment = db.Column(db.String(100))
	Cos_Category = db.Column(db.String(100))
	Product_Group_Sac = db.Column(db.String(100))
	Status = db.Column(db.String(100))

	def __init__(self, Cos_Type_Id, Cos_Type, Cos_Segment, Cos_Category, Product_Group_Sac, Status):
		self.Cos_Type_Id = Cos_Type_Id
		self.Cos_Type = Cos_Type
		self.Cos_Segment = Cos_Segment
		self.Cos_Category = Cos_Category
		self.Product_Group_Sac = Product_Group_Sac
		self.Status = Status

	def update(self, Cos_Type, Cos_Segment, Cos_Category, Product_Group_Sac, Status):
		self.Cos_Type = Cos_Type
		self.Cos_Segment = Cos_Segment
		self.Cos_Category = Cos_Category
		self.Product_Group_Sac = Product_Group_Sac
		self.Status = Status

	def json(self):
		return {
			'Cos_Type_Id' : self.Cos_Type_Id
			, 'Cos_Type' : self.Cos_Type
			, 'Cos_Segment' : self.Cos_Segment
			, 'Cos_Category' : self.Cos_Category
			, 'Product_Group_Sac' : self.Product_Group_Sac
			, 'Status' : self.Status
		}

	def json_with_id(self):
		return {
			self.id : self.json()
		}

	@classmethod
	def arguments(self):
		return {
			'logical_key': 'Cos_Type_Id',
			'column_list': [
				{
					'name': 'Cos_Type_Id',
					'type': ' int',
					'required': True
				},
				{
					'name': 'Cos_Type',
					'type': 'str',
					'required': True
				},
				{
					'name': 'Cos_Segment',
					'type': 'str',
					'required': False
				},
				{
					'name': 'Cos_Category',
					'type': 'str',
					'required': False
				},
				{
					'name': 'Product_Group_Sac',
					'type': 'str',
					'required': False
				},
			]
		}

	@classmethod
	def find_by_id(cls,_id):
		return cls.query.filter_by(id=_id).first()

	@classmethod
	def find_by_logical_key(cls,_id):
		return cls.query.filter_by(Cos_Type_Id=_id).first()

	def save_to_db(self):
		db.session.add(self)
		db.session.commit()

	def delete_from_db(self):
		db.session.delete(self)
		db.session.commit()

