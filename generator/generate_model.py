from os import path
import gzip
import shutil
from datetime import datetime

from string import Template


def generate_model_file(table, columns, no_backup, src_to_flask, src_to_reqparse):

	############## create backup of existing model file ##################
	if no_backup != 'Y':
		try:
			if path.isfile('../models/content/'+table+'.py'):
				with open('../models/content/'+table+'.py', 'rb') as f_in:
					with gzip.open('../models/content/'+table+'_'+datetime.now().strftime('%Y%m%d%H%M%S')+'.py.gz', 'wb') as f_out:
						shutil.copyfileobj(f_in, f_out)
		except Exception as e:
			print("Backup of model file {} failed. Generation interrupted.".format(table+'.py'))
			print(e)
			return None

	############## define dictionary for template replacement ##################			
	d = dict()
	general_name = ''.join(w.capitalize() for w in table.split('_'))
	
	############## base names ##################
	d['MODEL_NAME'] = general_name+"Model"
	d['TABLE_NAME'] = table
	d['GENERATION_TIMESTAMP'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	
	############## define arguments of class ##################
	class_columns = list()
	for column in columns:
		col_type = str(column['type']).upper()
		for k,v in src_to_flask.items():
			col_type = col_type.replace(k,v)
			entry = "\t" + column['name']+' = '+"db.Column(db."+col_type+(", primary_key=True" if column['name'] == 'id' else '')+")"
			if 'Numeric' in col_type:
				entry = entry.replace("))",", asdecimal=False))")
		class_columns.append(entry)
	
	d['CLASS_COLUMNS'] = "\n".join(class_columns).lstrip()
		
		
	############## define arguments of init function ##################
	d['INIT_ARGS'] = ", ".join([column['name'] for column in columns if column['name'].lower() != "id"])
	
	init_columns = list()
	for column in columns:
		if column['name'].lower() != 'id':
			init_columns.append("\t\t"+"self."+column['name'] +" = " + column['name'] )
	
	d['INIT_COLUMNS'] = "\n".join(init_columns).lstrip()

	
	############## define update function ##################
	d['UPDATE_ARGS'] = ", ".join([column['name'] for i, column in enumerate(columns) if i > 1])

	update_columns = list()
	for i, column in enumerate(columns):
		#skip first two columns
		if i > 1:
			update_columns.append("\t\t" + "self."+column['name'] +" = " + column['name'] )

	d['UPDATE_COLUMNS'] = "\n".join(update_columns).lstrip()
	
	############## define function that will return object as json ##################
	
	json_columns = list()
	for i, column in enumerate(columns):
		if i > 0:
			to_str = True if any(tp in str(column['type']) for tp in ['DATE','TIME']) else False
			json_columns.append("\t\t\t"+(", " if i > 1 else '')+"'"+column['name']+"' : "+("str(" if to_str else "")+"self."+column['name']+(")" if to_str else ""))
	
	d['JSON_COLUMNS'] = "\n".join(json_columns).lstrip()

	############## define function that will return columns expected with data delivery ##################
	
	logical_key = ""
	arguments_columns = list()
	for i, column in enumerate(columns):
		#skip first column and Status column
		if i > 0 and column['name'] != "Status":
			if i == 1:
				logical_key = column['name']
			
			elem = ""
			elem += ("\t\t\t\t"+"{"+"\n")
			elem += ("\t\t\t\t\t"+"'name': '"+column['name']+"',\n")
			elem += ("\t\t\t\t\t"+"'type': '"+src_to_reqparse.get(str(column['type']), 'str')+"',\n")
			elem += ("\t\t\t\t\t"+"'required': "+str(not column['nullable'])+"\n")
			elem += ("\t\t\t\t"+"}"+",")
			
			arguments_columns.append(elem)

	d['LOGICAL_KEY'] = logical_key
	d['ARGUMENTS_COLUMNS'] = "\n".join(arguments_columns).lstrip()
	
	############## create file based on template ##################
	with open('templates/model_template.py', 'r') as f:
		src = Template(f.read())
		result = src.substitute(d)
		tgt = open('../models/content/'+table+'.py','w')
		tgt.write(result)
		tgt.close()
