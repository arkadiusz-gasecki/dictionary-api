from flask_restful import Resource, reqparse
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_raw_jwt
from blacklist import BLACKLIST

from hashlib import sha256

from models.user import UserModel

class UserLogin(Resource):
	parser = reqparse.RequestParser()
	parser.add_argument('username',
				type=str,
				required=True,
				help="This field cannot be blank"
			)
	parser.add_argument('password',
				type=str,
				required=True,
				help="This field cannot be blank"
			)

	@classmethod
	def post(cls):
		data = cls.parser.parse_args()
		
		user = UserModel.find_by_username(data['username'])
		
		if user and safe_str_cmp(user.password,sha256(data['password'].encode()).hexdigest()):
			access_token = create_access_token(identity=user.role, fresh=True)
			refresh_token = create_refresh_token(user.id)
			return {
				'access_token': access_token,
				'refresh_token': refresh_token,
				'role': user.role
			}, 200
		
		return { 'message': 'Invalid credentials'}, 401
		

class UserLogout(Resource):
	@jwt_required
	def post(self):
		jti = get_raw_jwt()['jti']
		BLACKLIST.add(jti)
		return {'message': 'Succesfully logged out'}, 200
