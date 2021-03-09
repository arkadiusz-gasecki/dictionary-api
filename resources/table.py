from flask_restful import Resource
from flask_jwt_extended import jwt_required

from models.table import TableModel

class TableList(Resource):

	@jwt_required
	def get(self):			
		return {'tables': [ table.json() for table in TableModel.query.all() ]}, 200

