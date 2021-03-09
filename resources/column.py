from flask_restful import Resource
from flask_jwt_extended import jwt_required
from models.table import TableModel
from models.column import ColumnModel

class ColumnList(Resource):

	@classmethod
	def get_columns(cls, name):
		table = TableModel.find_by_name(name)
		if table is None:
			return {"message": "Table {} not defined".format(name) }, 400
		columns = ColumnModel.get_columns_by_table_id(table.id)
			
		return {
		    'tablename': table.name
		  , 'columns': [ column.json() for column in columns ] 
		}, 200
	
	@jwt_required
	def get(self, name):
		return ColumnList.get_columns(name)

