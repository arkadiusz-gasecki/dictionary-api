import configparser

def prepare_configuration():
	config = configparser.ConfigParser()
	config.read('config.ini')
	
	if 'DATABASE' not in config:
		print("DATABASE section missing in config.ini")
		return (None, None)
	
	elems = [key for key in ['engine', 'user', 'password', 'url', 'port', 'schema'] if key not in config['DATABASE']]
	if len(elems) > 0:
		print("Missing parameters: {} in DATABASE section".format(",".join(elems)))
		return (None, None)
		
	if 'TABLE' not in config:
		print("TABLE section missing in config.ini")
		return (None, None)
	
	if 'Table_To_Parse' not in config['TABLE']:
		print("Missing parameter Table_To_Parse in TABLE section")
		return (None, None)
	
	if config['DATABASE']['engine'] == 'sqlite':
		
		conn_string = config['DATABASE']['engine'] + \
				":/" + '/'.join([config['DATABASE']['user'] , config['DATABASE']['password'] , config['DATABASE']['url']]) + \
				('' if config['DATABASE']['port'] == "" else ':'+config['DATABASE']['port'] ) + \
				('' if config['DATABASE']['schema'] == "" else '/'+config['DATABASE']['schema'] )
	else:
		conn_string = config['DATABASE']['engine'] + \
				"://" + ':'.join([config['DATABASE']['user'] , config['DATABASE']['password']]) +'@'+ config['DATABASE']['url'] + \
				('' if config['DATABASE']['port'] == "" else ':'+config['DATABASE']['port'] ) + \
				('' if config['DATABASE']['schema'] == "" else '/'+config['DATABASE']['schema'] )
	
	list_of_tables = [] if config['TABLE']['Table_To_Parse'] == "" else [ x.strip() for x in config['TABLE']['Table_To_Parse'].split(",") ]
				
	return (conn_string, list_of_tables)


def data_type_transform():
	config = configparser.ConfigParser()
	config.read('config.ini')
	
	key = config['DATABASE']['engine'].upper() + " " + "TYPES"
	
	if key not in config:
		return(None, None)		
	else:	
		source_to_flask = dict()
		source_to_reqparse = dict()
		for k,v in config[key].items():
			source_to_flask[k.upper()] = v.split(',')[0]
			source_to_reqparse[k.upper()] = v.split(',')[1]
	
		return (source_to_flask, source_to_reqparse)
	

