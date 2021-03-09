from flask_jwt_extended import get_jwt_claims
from resources.content.common.parser import dict_parser

###################### insert item ##############################
def insert_prepare(cls,data,key):
	if cls.find_by_logical_key(data[key]):
		return 400, {'message': "Item with id '{}' already exists".format(data[key])} #bad request 
	else:
		data['status'] = 'INSERTED'
		item = cls(**data)
		return (200, item)
	
def upsert_execute(status, item, msg):
	if status != 200:
		return item, status
	else:
		try:
			item.save_to_db()
		except Exception as e:
			return {"message": msg, "error": str(e)}, 500 #internal server error
		return item.json(), 201


###################### update item ##############################

def update_prepare(cls, _id, data, key):
	item = cls.find_by_id(_id)
	if item:
		if item.status == 'DELETED':
			return 400, {'message': "Item with id '{}' is DELETED and cannot be modified".format(_id)}

		del data[key]
		data['status'] = 'MODIFIED'
		item.update(**data)
	else:
		data['status'] = 'INSERTED'
		item = cls(**data)
	return 200, item


###################### delete item ##############################

def delete_prepare(cls, _id):
	item = cls.find_by_id(_id)
		
	if item is None:
		return 400, {'message': "Item with id '{}' does not exist".format(_id)}
	elif item.status == 'DELETED':
		return 400, {'message': "Item with id '{}' is already deleted".format(_id)}
	else:
		item.status = 'MARKED FOR DELETION'
		return 200, item
		
###################### approve item ##############################		
def approve_prepare(cls, _id):
	claims = get_jwt_claims()
	if not claims['is_admin']:
		return 401, {'message': 'Admin rights required for approval'} #unauthorized
		
	item = cls.find_by_id(_id)
	if item is None:
		return 400, {'message': "Item with id '{}' does not exist".format(_id)} #bad request
	elif item.status in ('APPROVED', 'DELETED'):
		return 201, {'message': "Item with id '{}' already approved".format(_id)}
	elif item.status in ('INSERTED', 'MODIFIED'):
		item.status = 'APPROVED'
		return 200, item
	elif item.status in ('MARKED FOR DELETION'):
		item.status = 'DELETED'
		return 200, item
	else:
		return 500, {"mesage": "Item with id '{}' has unexpected status value '{}'".format(_id, item.status)} #internal server error

		
###################################################################
##################   bulk methods   ###############################
###################################################################

def bulk_insert(items, base_resource, model_class):
	inserted = list()
	rejected = list()
	return_code = 201

	try:
		for item in items:
			new_item_data = dict_parser(base_resource.columns, item)
			if new_item_data:
				item_logical_key_value = new_item_data.get(base_resource.logical_key,None)
				(status, item) = insert_prepare(model_class, new_item_data, base_resource.logical_key)
				(new_item, new_status) = upsert_execute(status, item, "An error occured inserting the item")
				if new_status == 201:
					inserted.append({item_logical_key_value: "INSERTED"})
				else:
					rejected.append({item_logical_key_value: new_item.get("message", "REJECTED")})
			else:
				rejected.append({ item.get(base_resource.logical_key, None): item })
	except:
		return_code = 500

	return { 'inserted': inserted, 'rejected': rejected }, 500
	

def bulk_update(items, base_resource, model_class):
	updated = list()
	rejected = list()
	return_code = 201
	
	try:	
		for item in items:
			new_item_data = dict_parser(base_resource.columns, item)
			if new_item_data:
				item_logical_key_value = new_item_data.get(base_resource.logical_key,None)
				old_item = model_class.find_by_logical_key(item_logical_key_value)
				item_id = 0 if old_item is None else old_item.id
				
				(status, item) = update_prepare(model_class, item_id, new_item_data, base_resource.logical_key)
				(new_item, new_status) = upsert_execute(status, item, "An error occured updating the item")
				
				if new_status == 201:
					updated.append({item_logical_key_value : "UPDATED"})
				else:
					rejected.append({item_logical_key_value : new_item.get("message", "REJECTED")})
			else:
				rejected.append({item_logical_key_value : new_item_data })
	except:
		return_code = 500

	return { 'updated': updated, 'rejected': rejected }, return_code
	
def bulk_delete(items, model_class):
	deleted = list()
	rejected = list()
	return_code = 201
	
	try:
	
		for item_id in items:
			(status, item) = delete_prepare(model_class, item_id)
			(new_item, new_status) = upsert_execute(status, item, "An error occured marking item as deleted")
			
			if new_status == 201:
				deleted.append({item_id: "DELETED"})
			else:
				rejected.append({item_id: new_item.get("message", "REJECTED")})
	except:
		return_code = 500
		
	return { 'deleted': deleted, 'rejected': rejected }, return_code
	

def bulk_approve(items, model_class):
	approved = list()
	rejected = list()
	return_code = 201
	
	try:	
		for item_id in items:
			(status, item) = approve_prepare(model_class, item_id)
			(new_item, new_status) = upsert_execute(status, item, "An error occured approving item")

			if new_status == 201:
				approved.append({item_id: item.get("message", "APPROVED")})
			else:
				rejected.append({item_id: new_item.get("message", "REJECTED")})
	except:
		return_code = 500
		
	return { 'approved': approved, 'rejected': rejected }, return_code
