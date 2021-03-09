### GENERATED AT: 2021-03-09 20:14:16

from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager
from db import db

from resources.user import UserLogin, UserLogout
from resources.table import TableList
from resources.column import ColumnList
#from resources.content.<table_name> import TableNameItem, TableNameItemList
from resources.content.test_table import TestTableItem, TestTableItemList

app = Flask(__name__)
app.config.from_object("config.DevelopmentConfig")
api = Api(app)


from blacklist import BLACKLIST

@app.before_first_request
def create_tables():
	db.create_all()
	
jwt = JWTManager(app)

@jwt.user_claims_loader
def add_claims_to_jwt(identity):
	if identity == 'admin':
		return {'is_admin': True}
	return{'is_admin': False}

@jwt.expired_token_loader
def expired_token_callback():
	return jsonify({
		'description': 'The token has expired',
		'error': 'token_expired'
	}), 401

@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
	return decrypted_token['jti'] in BLACKLIST
	
@jwt.revoked_token_loader
def revoked_token_callback():
	return jsonify({
		'description': 'The token has been revoked',
		'error': 'token_revoked'
	}), 401

api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout, '/logout')

api.add_resource(TableList, '/tables')
api.add_resource(ColumnList, '/table/<string:name>/columns')

### dedicated for each dictionary
#api.add_resource(TableNameItemList, '/table/table_name/items')
#api.add_resource(TableNameItem, '/table/table_name/item/<int:_id>')
api.add_resource(TestTableItemList, '/table/test_table/items')
api.add_resource(TestTableItem, '/table/test_table/item/<int:_id>')


if __name__ == '__main__':
	db.init_app(app)
	app.run(port=5000, debug=app.config['DEBUG'])
	
