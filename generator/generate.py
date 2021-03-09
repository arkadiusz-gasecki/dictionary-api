import sys


############## check files and folders ######################
from pre_check_generate import check_structure
err = check_structure()
if err > 0:
	print("Error while checking structure... generation broken")
	sys.exit()

############## parse arguments for script ######################
import argparse
parser = argparse.ArgumentParser(
		prog="generate.py",
		formatter_class=argparse.ArgumentDefaultsHelpFormatter	
		)
parser.add_argument("--overwrite", type=str, choices=['Y','N'], default='N', help='Set to Y if you want to overwite existing configuration and files')
parser.add_argument("--no-backup", type=str, choices=['Y','N'], default='N', help='Set to Y if you do not need to backup current version of files')
parser.add_argument("--tables"   , type=str,                    default=None, help="Overwrite configuration by providing list of tables, comma separated")
parser.add_argument("--in-app"   , type=str, choices=['ALL','LISTED_ONLY'], default='LISTED_ONLY', help="Set to ALL if you want to include all configured tables to be provided in app.py file")
args = parser.parse_args()

############## parse configuration ######################
from parse_configuration import prepare_configuration, data_type_transform
(conn_string, list_of_tables) = prepare_configuration()
if conn_string is None:
	print("Connection string could not be prepared")
	sys.exit()
if args.tables != None:
	list_of_tables = args.tables.split(',')
if len(list_of_tables) == 0:
	print("No tables defined for generator - check configuration file! ... exiting program")
	sys.exit()

src_to_flask, src_to_reqparse = data_type_transform()
if src_to_flask == None or src_to_reqparse == None:
	print("Missing conversion type section in configuration file... exiting program")
	sys.exit()

############## verify database connection ######################
from sqlalchemy import create_engine
engine = create_engine(conn_string)
try:
	engine.connect()
	print("Test connection successful")
except Exception as e:
	print(e)
	sys.exit()


############## define imports needed ######################
from sqlalchemy import MetaData, Table, Column, Integer, String, Boolean, func, select, ForeignKey
from sqlalchemy.engine import reflection


############## define metadata tables ######################
############## these have to be created beforehand #########
meta = MetaData()

table_tables = Table(
	'tables', meta,
	Column('id', Integer, primary_key=True),
	Column('name', String),
	Column('description', String),
)

table_columns = Table(
	'columns', meta,
	Column('id', Integer, primary_key=True),
	Column('column_name', String),
	Column('column_type', String),
	Column('column_length', Integer),
	Column('column_precision', Integer),
	Column('column_nullable', Boolean),
	Column('table_id', Integer, ForeignKey("table.id")),
)

############## define metadata inspector ######################
insp = reflection.Inspector.from_engine(engine)
available_tables = insp.get_table_names()


############## connect to database ######################
conn = engine.connect()

############## check if tables exist in database ######################
non_existing_tables = [ table for table in list_of_tables if table not in available_tables ]
if len(non_existing_tables):
	print("Following tables do not exist in database, therefore cannot be defined: {}".format(",".join(non_existing_tables)))
	print("Update entry 'Table_To_Parse' in list of tables in configuration file.")
	sys.exit()

############## check if tables are already defined in metadata ######################		
if args.overwrite != 'Y':
	s = select([table_tables.c.name, table_tables.c.description]).where(func.lower(table_tables.c.name).in_(list_of_tables))
	result = conn.execute(s).fetchall()
	if len(result):
		print("Following tables are already defined in metadata: {}".format(",".join([r[0] for r in result])))
		print("If you want to overwrite configuration, execute script with option --overwrite=Y")
		sys.exit()

############## populate information in metadata tables ######################
from generate_metadata import populate_metadata
from generate_resource import generate_resource_file
from generate_model import generate_model_file
from generate_app import generate_app_file	

for table in list_of_tables:
	try:
		columns = insp.get_columns(table)
		populate_metadata(conn, table, columns, table_tables, table_columns)
	except Exception as e:
		print("Error when populating metadata information for table: {}".format(table))
		print(e)
		sys.exit()
	
	############## generate resource file ###################
	try:
		generate_resource_file(table, args.no_backup)
		print("Resource file for table {} generated successfully.".format(table))
	except Exception as e:
		print("Error when generating resource file for table: {}".format(table))
		print(e)
		sys.exit()
	
	
		
	############## generate model file ######################
	
	try:
		generate_model_file(table, columns, args.no_backup, src_to_flask, src_to_reqparse)
		print("Model file for table {} generated successfully.".format(table))
	except Exception as e:
		print("Error when generating model file for table: {}".format(table))
		print(e)
		sys.exit()

############## finally generate api file ######################

if args.in_app == 'ALL':
	s = select([table_tables.c.name])
else:
	s = select([table_tables.c.name]).where(func.lower(table_tables.c.name).in_(list_of_tables))
result = conn.execute(s).fetchall()
all_tables = [r[0] for r in result]
try:
	generate_app_file(all_tables, conn_string, args.no_backup)
	print("Files app.py and config.py generated successfully.")
except Exception as e:
	print("Error when generating app.py and config.py files")
	print(e)
	sys.exit()		

	
	
