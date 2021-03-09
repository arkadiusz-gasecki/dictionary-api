create database tmp;

use tmp;

create table tables (
 id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
 name VARCHAR(100) NOT NULL,
 description VARCHAR(1000)
);


create table columns (
 id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
 column_name VARCHAR(100) NOT NULL,
 column_type VARCHAR(100) NOT NULL,
 column_length INT,
 column_precision INT,
 column_nullable BOOL,
 table_id INT UNSIGNED,
 FOREIGN KEY (table_id) REFERENCES tables(id)
);

create table users (
	id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
	username VARCHAR(100) NOT NULL,
	password VARCHAR(100) NOT NULL,
	role     VARCHAR(100)
);

INSERT INTO users VALUES(1,'root','4813494d137e1631bba301d5acab6e7bb7aa74ce1185d456565ef51d737677b2','admin');


-- test example

create table test_table (
 id INT AUTO_INCREMENT PRIMARY KEY,
 col2 SMALLINT,
 col3 INTEGER UNSIGNED NOT NULL,
 col4 INTEGER,
 col5 DECIMAL(18,5),
 col6 FLOAT,
 col7 DATETIME,
 col8 DATE,
 col9 TIMESTAMP,
 col10 VARCHAR(50),
 col11 CHAR(50),
 Status VARCHAR(100) NOT NULL
 );

INSERT INTO test_table VALUES(1,1,1000,-100,15.2,20.345,sysdate(),curdate(),timestamp(curdate()),'vartext','text','INSERTED');

