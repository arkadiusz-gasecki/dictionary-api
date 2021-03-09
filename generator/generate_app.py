from os import path
import gzip
import shutil
from datetime import datetime

from string import Template, ascii_lowercase
import random

def generate_app_file(tables, conn_string, no_backup):

	############## create backup of existing app file ##################
	if no_backup != 'Y':
		try:
			if path.isfile('../app.py'):
				with open('../app.py', 'rb') as f_in:
					with gzip.open('../app_'+datetime.now().strftime('%Y%m%d%H%M%S')+'.py.gz', 'wb') as f_out:
						shutil.copyfileobj(f_in, f_out)
		except Exception as e:
			print("Backup of app file app.py failed. Generation interrupted.")
			print(e)
			return None

	############## define dictionary for template replacement ##################			
	d = dict()
	
	d['GENERATION_TIMESTAMP'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	d['CONNECTION_STRING'] = conn_string
	d['SECRET_KEY'] = ''.join(random.choice(ascii_lowercase) for i in range(20))
	
	resources_import = list()
	api_calls = list()
	
	for table in tables:
		general_name = ''.join(w.capitalize() for w in table.split('_'))
		resources_import.append("from resources.content.{} import {}Item, {}ItemList".format(table, general_name, general_name))
		api_calls.append("api.add_resource({}ItemList, '/table/{}/items')".format(general_name, table))
		api_calls.append("api.add_resource({}Item, '/table/{}/item/<int:_id>')".format(general_name, table))
		
	d['RESOURCES_IMPORT'] = "\n".join(resources_import)
	d['API_CALLS']        = "\n".join(api_calls)

	############## create file based on template ##################
	with open('templates/app_template.py', 'r') as f:
		src = Template(f.read())
		result = src.substitute(d)
		tgt = open('../app.py','w')
		tgt.write(result)
		tgt.close()
		
	with open('templates/config_template.py', 'r') as f:
		src = Template(f.read())
		result = src.substitute(d)
		tgt = open('../config.py','w')
		tgt.write(result)
		tgt.close()

