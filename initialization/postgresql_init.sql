--create database tmp;
--use tmp;
--create user root PASSWORD 'root';
--grant all privileges on database tmp to root;
--grant all privileges on all tables in schema public to root;
--grant all privileges on all sequences in schema public to root;

create table tables (
 id SERIAL PRIMARY KEY,
 name VARCHAR(100) NOT NULL,
 description VARCHAR(1000)
);


create table columns (
 id SERIAL PRIMARY KEY,
 column_name VARCHAR(100) NOT NULL,
 column_type VARCHAR(100) NOT NULL,
 column_length INT,
 column_precision INT,
 column_nullable BOOL,
 table_id INT,
 FOREIGN KEY (table_id) REFERENCES tables(id)
);

create table users (
	id SERIAL PRIMARY KEY,
	username VARCHAR(100) NOT NULL,
	password VARCHAR(100) NOT NULL,
	role     VARCHAR(100)
);

INSERT INTO users (username, password, role) VALUES('root','4813494d137e1631bba301d5acab6e7bb7aa74ce1185d456565ef51d737677b2','admin');


-- test example

create table test_table (
 id SERIAL PRIMARY KEY,
 col2 SMALLINT,
 col3 INTEGER NOT NULL,
 col4 INTEGER,
 col5 DECIMAL(18,5),
 col6 FLOAT,
 col7 DATE,
 col8 TIMESTAMP(0),
 col9 VARCHAR(50),
 col10 CHAR(50),
 status VARCHAR(100) NOT NULL
 );

INSERT INTO test_table (col2,col3,col4,col5,col6,col7,col8,col9,col10,Status)
VALUES(1,1000,-100,15.2,20.345,current_date,current_timestamp(0),'vartext','text','INSERTED');

--grant all privileges on all tables in schema public to root;
--grant all privileges on all sequences in schema public to root;

