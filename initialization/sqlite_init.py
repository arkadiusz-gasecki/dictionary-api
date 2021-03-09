import sqlite3

connection = sqlite3.connect('data.db')

cursor = connection.cursor()

create_table = ' \
create table tables ( \
 id INTEGER PRIMARY KEY, \
 name VARCHAR(100) NOT NULL, \
 description VARCHAR(100) \
);'

cursor.execute(create_table)


create_table = ' \
create table columns ( \
 id INTEGER PRIMARY KEY, \
 column_name VARCHAR(100) NOT NULL, \
 column_type VARCHAR(100) NOT NULL, \
 column_length INT, \
 column_precision INT, \
 column_nullable BOOL, \
 table_id INT, \
 FOREIGN KEY (table_id) REFERENCES tables(id) \
);'

cursor.execute(create_table)

create_table = ' \
create table users ( \
	id INT PRIMARY KEY, \
	username VARCHAR(100) NOT NULL, \
	password VARCHAR(100) NOT NULL, \
	role     VARCHAR(100) \
);'

cursor.execute(create_table)


user = (1,'root','4813494d137e1631bba301d5acab6e7bb7aa74ce1185d456565ef51d737677b2', 'admin')
insert_query = "INSERT INTO users VALUES(?,?,?,?)"
cursor.execute(insert_query, user)



connection.commit()

create_table = ' \
create table test_table ( \
 id INTEGER PRIMARY KEY, \
 col2 SMALLINT, \
 col3 INTEGER NOT NULL, \
 col4 INTEGER, \
 col5 DECIMAL(18,5), \
 col6 FLOAT, \
 col10 VARCHAR(50), \
 col11 CHAR(50), \
 status VARCHAR(100) NOT NULL \
 );'
 
cursor.execute(create_table)

entry = (1,1,1000,-100,15.2,20.345,'vartext','text','INSERTED');

insert_query = "INSERT INTO test_table VALUES(?,?,?,?,?,?,?,?,?)"

cursor.execute(insert_query, entry)



connection.commit()

connection.close()

