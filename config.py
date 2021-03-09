### GENERATED AT: 2021-03-09 20:14:16

class Config(object):
	DEBUG = False
	TESTING = False
	
	JWT_SECRET_KEY = 'zdlzcfhjoulrwvgbplts'
	SQLALCHEMY_DATABASE_URI = 'sqlite:////home/user/Documents/dict_api/data.db'
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	PROPAGATE_EXCEPTIONS = True
	JWT_BLACKLIST_ENABLED = True
	JWT_BLACKLIST_TOKEN_CHECKS = ['access','refresh']
	
class ProductionConfig(Config):
	pass

class DevelopmentConfig(Config):
	DEBUG = True
	
class TestingConfig(Config):
	TESTING = True
