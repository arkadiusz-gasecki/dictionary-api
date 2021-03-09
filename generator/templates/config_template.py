### GENERATED AT: $GENERATION_TIMESTAMP

class Config(object):
	DEBUG = False
	TESTING = False
	
	JWT_SECRET_KEY = '$SECRET_KEY'
	SQLALCHEMY_DATABASE_URI = '$CONNECTION_STRING'
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
