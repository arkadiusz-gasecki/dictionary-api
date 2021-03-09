from flask_restful import reqparse

type_converter = {
	'str': str,
	'int': int,
	'float': float,
	'dict': dict
}

def make_parser(columns):
	parser = reqparse.RequestParser()
	
	for column in columns:
		if column['name'].lower() != "status":
			parser.add_argument(column['name'], 
				type=type_converter.get(column['type'], str), 
				required=column['required'], 
				help="This field cannot be left blank" if column['required'] else ''
			)
	return parser
	
		

bulk_post_put_parser = reqparse.RequestParser()
bulk_post_put_parser.add_argument('tablename',
			type=str,
			required=True,
			help="This field cannot be left blank"
		)
bulk_post_put_parser.add_argument('items',
			type=dict,
			required=True,
			location='json',
			action='append',
			help="This field cannot be left blank"
		)

bulk_delete_patch_parser = reqparse.RequestParser()
bulk_delete_patch_parser.add_argument('tablename',
			type=str,
			required=True,
			help="This field cannot be left blank"
		)
bulk_delete_patch_parser.add_argument('items',
			type=list,
			required=True,
			location='json',
			help="This field cannot be left blank"
		)


def dict_parser(keys, dct):
	new_item_data = { k: v for k,v in dct.items() if k in keys }
	return new_item_data
