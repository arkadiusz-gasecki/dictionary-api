from os import path
import gzip
import shutil
from datetime import datetime

from string import Template

def generate_resource_file(table, no_backup):

	############## create backup of existing resource file ##################
	if no_backup != 'Y':
		try:
			if path.isfile('../resources/content/'+table+'.py'):
				with open('../resources/content/'+table+'.py', 'rb') as f_in:
					with gzip.open('../resources/content/'+table+'_'+datetime.now().strftime('%Y%m%d%H%M%S')+'.py.gz', 'wb') as f_out:
						shutil.copyfileobj(f_in, f_out)
		except Exception as e:
			print("Backup of resource file {} failed. Generation interrupted.".format(table+'.py'))
			print(e)
			return None

	############## define dictionary for template replacement ##################			
	d = dict()
	general_name = ''.join(w.capitalize() for w in table.split('_'))
	d['GENERATION_TIMESTAMP'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	d['MODEL_FILE'] = table
	d['MODEL_NAME'] = general_name+'Model'
	d['ITEM_NAME']  = general_name+'Item'
	d['ITEM_LIST_NAME'] = general_name+'ItemList'

	############## create file based on template ##################
	with open('templates/resource_template.py', 'r') as f:
		src = Template(f.read())
		result = src.substitute(d)
		tgt = open('../resources/content/'+table+'.py','w')
		tgt.write(result)
		tgt.close()

