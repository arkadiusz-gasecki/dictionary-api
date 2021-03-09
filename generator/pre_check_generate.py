import os

def check_structure():
	######## check if file is in generator folder
	if os.getcwd().split('/')[-1] == 'generator':
		print("File present in generator subdirectory...OK")
	else:
		print("Subdirectory generator not found.. ERROR");
		return 1

	######## check if other generator files are present in directory

	expected_files = { "generate.py": "Main"
						, "config.ini": "Configuration"
						, "parse_configuration.py": "Configuration parser"
						, "generate_metadata.py": "Metadata generator"
						, "generate_model.py": "Model file generator" 
					}
	for k,v in expected_files.items():
		if k in os.listdir():
			print("{} file {} present...OK".format(v,k))
		else:
			print("{} file {} missing...ERROR".format(v,k))
			return 2
	
	######## check if template directory exists
	with os.scandir() as entries:
		if 'templates' in [ entry.name for entry in entries ]:
			print("Templates directory exists...OK")
		else:
			print("Templates direcory missing...ERROR")
			return 3
		
	######## check if template files exist
	for elem in ['resource_template.py']:
		if elem in os.listdir('templates'):
			print("{} template file present...OK".format(elem))
		else:
			print("{} template file missing...ERROR".format(elem))
			return 4	
					
	######## check if app.py file exists in upper

	if "app.py" in os.listdir('..'):
		print("File app.py found...OK")
	else:
		print("File app.py missing...ERROR")
		return 5

	with os.scandir('..') as entries:
		subdirectories = [ entry.name for entry in entries ]
	
	######## check if models and resources paths are defined	
	expected_dirs = [ "models", "resources"	]
	for d in expected_dirs:
		if d in subdirectories:
			print("Subpath {} found...OK".format(d))
			with os.scandir('../'+d) as m:
				if 'content' in [ entry.name for entry in m ]:
					print("Subpath content found in {}...OK".format(d))
				else:
					print("Missing subpath content in {}...ERROR".format(d))
					return 6
		else:
			print("Subpath {} missing...ERROR".format(d))
			return 7

	return 0	

