# dictionary-api
-----------------------------------------------------------------
Author:
Arkadiusz Gasecki, PhD

-----------------------------------------------------------------
Aim:
Reason to write this API was just to learn about the topic itself - like REST API 101 with Python and Flask.


-----------------------------------------------------------------
Business need:
Idea for API came from need of having an application, where business users could manage dictionary tables by themselves.
API handles backend part of application, satisfying simple lifecycle and approval process.

-----------------------------------------------------------------
Architecture assumption:
There is a web based application with database underneath. Database contains dictionary tables, being managed by users through web interface.
Data from the tables is extracted using ETL processes to target datawarehouse. Only records with particular statuses are extracted.

-----------------------------------------------------------------
Requirements:
Given in file requirements.txt
API is written in Python and Flask
Currently API supports following databases: sqlite (for test purposes), mysql, postgresql

In order to function properly, database associated with API has to have three tables:
- "tables"
- "columns"
- "users"
Scripts to initialize these tables are provided in folder initialization.
Each script provides DDL queries to create 3 tables mentioned and DML query to create a single user of type admin with login "root" and password "root".
Moreover, script provides query to create single test table and populate it with one entry, with all supported data types.

-----------------------------------------------------------------
Users and authentication:
Password is kept in database as hash using SHA256.
Assumption is that final users of this API will adjust authentication to use e.g. AD, if needed. However, API does not support it natively.
Table "users" should be used a whitelist where logins of users allowed to use application are provided, together with their roles.
API does not provides mechanism to manage table users through API calls.

-----------------------------------------------------------------
Roles:
API support two kinds of roles: user and admin. Role "admin" has to be given explicitly.
User is allowed to provide, modify and remove entries in dictionaries.
Admin is additionally allowed to approve changes provided by users.

-----------------------------------------------------------------
Lifecycle of record:
Each records can be in one of the following statues:
- INSERTED
- MODIFIED
- APPROVED
- MARKED FOR DELETION
- DELETED


Lifecycle of records is as follows
INSERTED -> APPROVED -> MODIFIED -> APPROVED -> MARKED FOR DELETION -> DELETED

Approval of records of type INSERTED and MODIFIED changes their status to APPROVED.
Approval of records of type MARKED FOR DELETION changes theis status to DELETED.

Currently there is no option to restore records that are DELETED. These ones should be finally removed from table manually.
Assumption is that only records with status APPROVED are extracted and loaded to target data warehouse.
Also, records of type DELETED should be detected and removed from target data warehouse.
If record is in status MARKED FOR DELETION, it can be updated so it will change its status to MODIFIED.
There is no option to reject change and come back to state before modification.

-----------------------------------------------------------------
Dictionaries:
Each table, which is intended to be managed with help of this API, should satify following requirements
- first column has to be named "id", be of type INTEGER and set up as AUTOINCREMENT PRIMARY KEY - this column is intended not to be visible for business users
- secord column has to represent logical/business key. This means that values in this column have to be unique across table. API supports only one-column business key
- last column has to be named "status" of type VARCHAR, minimum 20 characters. This column will keep statues of records
- column names have to be lower case
API does not support SCD2, which means that assumption is that dictionaries present only current state of data

-----------------------------------------------------------------
EXAMPLE:
We have dictionary where business user manages price of the products
Table will contain following columns:
- id INTEGER AUTO_INCREMENT PRIMARY KEY
- product_id INTEGER NOT NULL
- product_name VARCHAR(100)
- product_price FLOAT
- status VARCHAR(20) NOT NULL


Table will contain only one entry per product_id.
User provides values for three columns:
- product_id: 100
- product_name: phone
- product_price 500.00

Entry in table will look as follows:
id product_id product_name product_price status
-- ---------- ------------ ------------- ------
1  100        phone        500.00        INSERTED


This entry should not be considered by ETL process.

Once admin approves it, entry will look as follows:
id product_id product_name product_price status
-- ---------- ------------ ------------- ------
1  100        phone        500.00        APPROVED

This entry should be selected by ETL process and loaded to target table in data warehouse.

Now, user is eligible to change following columns:
- product_name
- product_price
Column product_id is business key, which means it cannot be changed. New value in this columns corresponds to new, totally independent entry.

After update, entry will look as follows (e.g.):
id product_id product_name product_price status
-- ---------- ------------ ------------- ------
1  100        yourphone    650.00        MODIFIED

This entry should not be selected by ETL process, and in target table values still should be as: phone, 500.00
Only after approval, record should be selected and updated in target table.

Finally, when user decides to remove record, it will look as follows
id product_id product_name product_price status
-- ---------- ------------ ------------- ------
1  100        yourphone    650.00        MARKED FOR DELETION

This entry should not be selected by ETL process, therefore still be visible in target table.
After being approved, entry will look as follows:
id product_id product_name product_price status
-- ---------- ------------ ------------- ------
1  100        yourphone    650.00        DELETED

This entry should be selected by ETL process and corresponding record in target table should be removed.




---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------- TECHNICAL DOCUMENTATION ---------------------------------------------------------------------------------------------------------
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

blacklist.py - definition of set that supports operation of log out
db.py - definition of database connection
app.py - main file for API - this file is generated by generator tool

----------------------------------------------------------------- GENERATOR ---------------------------------------------------------------------------------------------------------
Folder generator contains set of scripts that generate proper code for model, resource and app files.

config.ini
----------
In section [DATABASE] connection to database has to be defined. Only particular engines are supported.
In section [TABLE] variable Table_To_Parse expects lists of tables, comma separated, for which API codes need to be generated. For each table, one file in model/content folder and one file in resource/content folder are created.

Next sections determine types that are supported for each database engine.
For each datatype, translation is provided to corresponding type in SQLAlchemy and corresponding type to be used in reqparse.
Reqparse supports only four datatypes:
- str
- int
- float
- bool
Flask SQLAlchemy supports following types:
- SmallInteger
- Integer
- Numeric
- Float
- DateTime
- String
- Boolean
These types are case sensitive!


pre_check_generate.py
---------------------
This script provides function to scan the structure of files and folders and to verify that all are in place.
This is executed at the beginning of generation process

parse_configuration.py
----------------------
This script provides function that reads file config.ini

generate_metadata.py
----------------------
This script provides function that populates metadata info about parsed tables into metadata tables: tables and columns

generate_resource.py
---------------------
This script provides function that generates resource file, for each parsed table, based on template file resource_template.py located in templates folder

generate_model.py
---------------------
This script provides function that generates model file, for each parsed table, based on template file model_template.py located in templates folder

generate_app.py
---------------------
This script provides function that generates app file, based on template file app_template.py located in templates folder

---------------------
generate.py
---------------------
This is main file that generates all the files for API. Generation is done based on entries in config.ini file
Following arguments are supported with this script:
- overwrite - if table is already defined in metadata, it cannot be generated once again. To overrule it, this argument has to be set to Y
- no-backup - by default, if files are overwritten, old versions are renamed and gzipped for backup purpose. If you do not want this, set this option to Y
- tables - if you want to override argument table_to_parse from config.ini file, you can do it by determining list of tables with this argument
- in-app - for each generated table, proper entries have to be added in app.py file. File is always fully regenerated, and by default only these entries are populated in app.py file, which are explicitly generated. But if you want that all tables are mentioned, you have to set it to ALL.
Example: if you generate code for newly added table, you will only define this new table as table_to_parse. But app.py file should have entries also for all tables, so previously defined as well. In such case, parameter has to be set up to ALL.

Generator uses table name as indicator for naming convention. Files for model and resource are named same way as table. Classes are renamed, underline characters are removed and each word, separated by underline character is capitalized.
Example: name of table is test_table
Both model file and resource file are named: test_table.py
Class in model file is called TestTableModel
Classes in resource file are called: TestTableItem and TestTableItemList

templates
-------------------
This folder contains templates for app.py and proper model and resource type. These are the files you should adjust, if you need changes in codes.




----------------------------------------------------------------- API CALLS ---------------------------------------------------------------------------------------------------------

POST /login
-----------
Header:
	Content-Type: application-json
Body:
	{
      "username" : "<login>"
    , "password" : "<password>"
	}

example body:	
	{
      "username" : "root"
    , "password" : "root"
	}
Response:
	{
    "access_token": <jwt_token>,
    "refresh_token": <refresh_token>,
    "role": ["user"|"admin"]
	}, 200
Alternative responses:
	{
	  'message': 'Invalid credentials'
	}, 401
	
example response:
	{
    "access_token": 	"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE2MTQ1MTY4NDMsIm5iZiI6MTYxNDUxNjg0MywianRpIjoiMjc2MjIwM2ItODlmNi00ZTA0LThmZTktMmQwOGVkMDhmNjVhIiwiZXhwIjoxNjE0NTE3NzQzLCJpZGVudGl0eSI6ImFkbWluIiwiZnJlc2giOnRydWUsInR5cGUiOiJhY2Nlc3MiLCJ1c2VyX2NsYWltcyI6eyJpc19hZG1pbiI6dHJ1ZX19.xgyk38PDgv5Yp6Aufaqxl-	C_nTUIqKhoxxlsBPnnwfk",
    "refresh_token": 	"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE2MTQ1MTY4NDMsIm5iZiI6MTYxNDUxNjg0MywianRpIjoiOGJkZjVmOWEtZTFhYi00ODIzLTgyYTMtZjEwMGQ2ZmE4YTM2IiwiZXhwIjoxNjE3MTA4ODQzLCJpZGVudGl0eSI6MSwidHlwZSI6InJlZnJlc2gifQ.T6iIflI1M3bVNfJzP6mi4IClrSLq4dAMxHu1XigMaSA",
	"role": "admin"
	}



POST /logout
-----------
Header:
	Authorization: Bearer <jwt_token>
Body:
	none

Response:
	{
      "message": "Succesfully logged out"
	}, 200
	
	
GET /tables
-------------------------------------------
returns list of all configured dictionaries
returns empty list if no dictionaries are defined
-------------------------------------------
Header:
	Authorization: Bearer <jwt_token>
Body:
	none
	
Response:
{
	"tables": [ 
		{
		  "id": <table id>
		  "name": "<table name>"
		  "description": "<table description>"
		}
	 ]
}, 200

example response:
{
    "tables": [
        {
            "id": 1,
            "name": "test_table",
            "description": ""
        }
    ]
}


GET /table/<table_name>/columns
-------------------------------------------
returns list of all columns of given dictionary
-------------------------------------------
Header:
	Authorization: Bearer <jwt_token>
Body:
	none

Response:
{
	"tablename": "<name of table>"
  , "columns": [
  		{
  		   "column_id" : <column_id>
  	  	 , "column_name": "<column_name>",
         ,  "column_type": "<column_type>",
         ,  "column_length": <column_length>,
         ,  "column_precision": <column_precision>,
         ,  "column_nullable": true/false
        },
  		...
  	]
}, 200

Alternative response:
{
    "message": "Table <table_name> not defined"
}, 400

example call:
GET /table/test_table/columns

example response:
{
    "tablename": "test_table",
    "columns": [
        {
            "column_id": 1,
            "column_name": "id",
            "column_type": "INTEGER",
            "column_length": null,
            "column_precision": null,
            "column_nullable": false
        },
        {
            "column_id": 2,
            "column_name": "col2",
            "column_type": "SMALLINT",
            "column_length": null,
            "column_precision": null,
            "column_nullable": true
        },
        {
            "column_id": 3,
            "column_name": "col3",
            "column_type": "INTEGER UNSIGNED",
            "column_length": null,
            "column_precision": null,
            "column_nullable": false
        },
        {
            "column_id": 4,
            "column_name": "col4",
            "column_type": "INTEGER",
            "column_length": null,
            "column_precision": null,
            "column_nullable": true
        },
        {
            "column_id": 5,
            "column_name": "col5",
            "column_type": "DECIMAL",
            "column_length": 18,
            "column_precision": 5,
            "column_nullable": true
        },
        {
            "column_id": 6,
            "column_name": "col6",
            "column_type": "FLOAT",
            "column_length": null,
            "column_precision": null,
            "column_nullable": true
        },
        {
            "column_id": 7,
            "column_name": "col7",
            "column_type": "DATETIME",
            "column_length": null,
            "column_precision": null,
            "column_nullable": true
        },
        {
            "column_id": 8,
            "column_name": "col8",
            "column_type": "DATE",
            "column_length": null,
            "column_precision": null,
            "column_nullable": true
        },
        {
            "column_id": 9,
            "column_name": "col9",
            "column_type": "TIMESTAMP",
            "column_length": null,
            "column_precision": null,
            "column_nullable": true
        },
        {
            "column_id": 10,
            "column_name": "col10",
            "column_type": "VARCHAR",
            "column_length": 50,
            "column_precision": null,
            "column_nullable": true
        },
        {
            "column_id": 11,
            "column_name": "col11",
            "column_type": "CHAR",
            "column_length": 50,
            "column_precision": null,
            "column_nullable": true
        },
        {
            "column_id": 12,
            "column_name": "Status",
            "column_type": "VARCHAR",
            "column_length": 100,
            "column_precision": null,
            "column_nullable": false
        }
    ]
}


GET /table/<table_name>/items
-------------------------------------------
returns list of all items from given dictionary
-------------------------------------------
Header:
	Authorization: Bearer <jwt_token>
Body:
	none

Response:
{
	"tablename": "<name of table>"
  , "items": [
  		{
  	  		"<item_id>":
  	  			{
  	  	  			"<column name>": "<column value">
  	  	  			, ...
  				}
  	 		 , ...
  		}
  	]
}, 200

example call:
GET /table/test_table/items

example response:
{
    "tablename": "test_table",
    "items": [
        {
            "1": {
                "col2": 1,
                "col3": 1000,
                "col4": -100,
                "col5": 15.2,
                "col6": 20.345,
                "col7": "2021-02-28 13:53:45",
                "col8": "2021-02-28",
                "col9": "2021-02-28 00:00:00",
                "col10": "vartext",
                "col11": "text",
                "Status": "INSERTED"
            }
        }
    ]
}



GET /table/<table_name>/item/<id>
-------------------------------------------
returns item with given id from given dictionary
-------------------------------------------
Header:
	Authorization: Bearer <jwt_token>
Body:
	none

Response:
{
	"tablename": "<name of table>"
  , "<item_id>":
  	  	{
  	  	  "<column name>": "<column value">
  	  	  , ...
  	  	}
}, 200

Alternative responses:
{
    "message": "Item with id: <id> not found"
}, 400

example call:
GET /table/test_table/item/1

example response:
{
    "tablename": "test_table",
    "1": {
        "col2": 1,
        "col3": 1000,
        "col4": -100,
        "col5": 15.2,
        "col6": 20.345,
        "col7": "2021-02-28 13:53:45",
        "col8": "2021-02-28",
        "col9": "2021-02-28 00:00:00",
        "col10": "vartext",
        "col11": "text",
        "Status": "INSERTED"
    }
}

example call for non-existing item:
GET /table/test_table/item/3

response:
{
    "message": "Item with id: 3 not found"
}


POST /table/<table_name>/item/0
-------------------------------------------
 loads new item into given dictionary
-------------------------------------------
Header:
	Authorization: Bearer <jwt_token>
	Content-Type: application-json
Body:
{
   <column_name_1>: <column_value_1>,
   <column_name_2>: <column_value_2>,
      ...
}

Response:
{
   <column_name_1>: <column_value_1>,
   <column_name_2>: <column_value_2>,
      ...
   "Status": "INSERTED"
}, 201

Alternative responses:
{
    "message": "Item with id <column_value_1> already exists"
}, 400

{
	"mesage": "An error occured inserting the item"
  , "error": <database error>
}, 500
 

example call:
POST /table/test_table/item/0

example body:
{
        "col2": 2,
        "col3": 1000,
        "col4": -100,
        "col5": 15.2,
        "col6": 20.345,
        "col7": "2021-02-27 15:21:07",
        "col8": "2021-02-27",
        "col9": "2021-02-27 00:00:00",
        "col10": "vartext",
        "col11": "text"
}

example response:
{
    "col2": 2,
    "col3": 1000,
    "col4": -100,
    "col5": 15.2,
    "col6": 20.345,
    "col7": "2021-02-27 15:21:07",
    "col8": "2021-02-27",
    "col9": "2021-02-27 00:00:00",
    "col10": "vartext",
    "col11": "text",
    "Status": "INSERTED"
}

example response if entry with given business key already exists (applies also for records in status DELETED):
{
    "message": "Item with id '2' already exists"
}
 
 
PUT /table/<table_name>/item/<item_id>
-------------------------------------------
 updates item with <item_id> in given dictionary
-------------------------------------------
Header:
	Authorization: Bearer <jwt_token>
	Content-Type: application-json
Body:
{
   <column_name_2>: <column_value_3>,
   <column_name_3>: <column_value_3>,
      ...
}
(column with value for business key is not required)

Response:
{
   <column_name_1>: <column_value_1>,
   <column_name_2>: <column_value_2>,
   <column_name_3>: <column_value_3>,
      ...
   "Status": "MODIFIED"
}, 201

Alternative responses:
{
    "message": "Item with id <item_id> is DELETED and cannot be modified"
}, 400

{
	"mesage": "An error occured updating the item"
  , "error": <database error>
}, 500

example call:
PUT /table/test_table/item/1

example body:
{
        "col3": 1000,
        "col4": -100,
        "col5": 15.2,
        "col6": 20.345,
        "col7": "2021-02-27 15:21:07",
        "col8": "2021-02-27",
        "col9": "2021-02-27 00:00:00",
        "col10": "vartext",
        "col11": "text"
}

example response:
{
    "col2": 1,
    "col3": 1000,
    "col4": -100,
    "col5": 15.2,
    "col6": 20.345,
    "col7": "2021-02-27 15:21:07",
    "col8": "2021-02-27",
    "col9": "2021-02-27 00:00:00",
    "col10": "vartext",
    "col11": "text",
    "Status": "MODIFIED"
}



DELETE /table/<name>/item/<item_id>
-------------------------------------------
set status of item with <item_id> in given dictionary to MARKED FOR DELETION
-------------------------------------------
Header:
	Authorization: Bearer <jwt_token>
Body:
    none
Response:
{
   <column_name_1>: <column_value_1>,
   <column_name_2>: <column_value_2>,
   <column_name_3>: <column_value_3>,
      ...
   "Status": "MARKED FOR DELETION"
}, 200

Alternative responses:
{
    "message": "Item with id <item_id> does not exist"
}, 400

{
    "message": "Item with id <item_id> is already deleted"
}, 400

{
	"mesage": "An error occured marking item as deleted"
  , "error": <database error>
}, 500

example call:
DELETE /table/test_table/item/1

example response:
{
    "col2": 1,
    "col3": 1000,
    "col4": -100,
    "col5": 15.2,
    "col6": 20.345,
    "col7": "2021-02-27 15:21:07",
    "col8": "2021-02-27",
    "col9": "2021-02-27 00:00:00",
    "col10": "vartext",
    "col11": "text",
    "Status": "MARKED FOR DELETION"
}


PATCH /table/<name>/item/<item_id>
-------------------------------------------
"approves" - changes status of item with <item_id> in given dictionary
if status was INSERTED or MODIFIED - it will be changed to APPROVED
if status was MARKED FOR DELETION - it will be changed to DELETED
admin role is required to make this call successfully
-------------------------------------------
Header:
	Authorization: Bearer <jwt_token>
Body:
    none
Response:
{
   <column_name_1>: <column_value_1>,
   <column_name_2>: <column_value_2>,
   <column_name_3>: <column_value_3>,
      ...
   "Status": ["APPROVED"|"DELETED"]
}, 200

Alternative responses:
{
    "message": "Item with id <item_id> already approved"
}, 201

{
	"message": "Admin rights required for approval"
}, 401

{
    "message": "Item with id <item_id> does not exist"
}, 400

{
	"mesage": "Item with id <item_id>  has unexpected status value <status_value>"
}, 500

{
	"mesage": "An error occured approving item"
  , "error": <database error>
}, 500



example call:
PATCH /table/test_table/item/1

example response:
{
    "col2": 1,
    "col3": 1000,
    "col4": -100,
    "col5": 15.2,
    "col6": 20.345,
    "col7": "2021-02-27 15:21:07",
    "col8": "2021-02-27",
    "col9": "2021-02-27 00:00:00",
    "col10": "vartext",
    "col11": "text",
    "Status": "APPROVED"
}
or
{
    "col2": 1,
    "col3": 1000,
    "col4": -100,
    "col5": 15.2,
    "col6": 20.345,
    "col7": "2021-02-27 15:21:07",
    "col8": "2021-02-27",
    "col9": "2021-02-27 00:00:00",
    "col10": "vartext",
    "col11": "text",
    "Status": "DELETED"
}


