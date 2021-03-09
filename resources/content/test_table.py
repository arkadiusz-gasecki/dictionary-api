### GENERATED AT: 2021-03-09 20:14:16

from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_claims
from models.content.test_table import TestTableModel

import resources.content.common.crud as crud
import resources.content.common.parser as mk_parser
from resources.content.common.parser import bulk_post_put_parser, bulk_delete_patch_parser, dict_parser


class TestTableItem(Resource):

	model_class = TestTableModel
	tablename = model_class.__tablename__
	args = model_class.arguments()

	logical_key = args['logical_key']
	columns = [ col['name'] for col in args['column_list'] ]
	
	# general methods
	@classmethod
	def insert_item(cls, data):
		(status, item) = crud.insert_prepare(cls.model_class, data, cls.logical_key)
		return crud.upsert_execute(status, item, "An error occured inserting the item")	

	@classmethod
	def upsert_item(cls,_id, data):
		(status, item) = crud.update_prepare(cls.model_class, _id, data, cls.logical_key)
		return crud.upsert_execute(status, item, "An error occured updating the item")

	@classmethod
	def delete_item(cls,_id):
		(status, item) = crud.delete_prepare(cls.model_class, _id)
		return crud.upsert_execute(status, item, "An error occured marking item as deleted")
	
	@classmethod
	def approve_item(cls,_id):
		(status, item) = crud.approve_prepare(cls.model_class, _id)
		return 	crud.upsert_execute(status, item, "An error occured approving item")

	# REST API methods
	@jwt_required
	def get(self, _id):

		m = self.model_class.find_by_id(_id)
		if m is None:
			return {"message": "Item with id: {} not found".format(_id)}, 400
		return {
			"tablename": self.tablename
			, _id: m.json()
		}, 200
	
	@jwt_required
	def post(self, _id):
		parser = mk_parser.make_parser(self.args['column_list'])	
		data = parser.parse_args()
		return self.insert_item(data)
	
	@jwt_required
	def put(self, _id):
		parser = mk_parser.make_parser(self.args['column_list'])
		data = parser.parse_args()
		return self.upsert_item(_id, data)
	
	@jwt_required
	def delete(self, _id):
		return self.delete_item(_id)
		
	@jwt_required	
	def patch(self, _id):
		return self.approve_item(_id)
				

class TestTableItemList(Resource):

	base_resource = TestTableItem
	model_class = TestTableModel
	
	@jwt_required
	def get(self):

		return {
			"tablename": self.base_resource.tablename
			, "items": [ m.json_with_id() for m in self.model_class.query.all() ]
		}
		
	@jwt_required	
	def post(self):
		data = bulk_post_put_parser.parse_args()
		return crud.bulk_insert(data['items'], self.base_resource, self.model_class)
		
	@jwt_required
	def put(self):
		data = bulk_post_put_parser.parse_args()
		return crud.bulk_update(data['items'], self.base_resource, self.model_class)
		
	@jwt_required		
	def delete(self):
		data = bulk_delete_patch_parser.parse_args()
		return crud.bulk_delete(data['items'], self.model_class)

	
	@jwt_required
	def patch(self):
		data = bulk_delete_patch_parser.parse_args()
		return crud.bulk_approve(data['items'], self.model_class)
			

