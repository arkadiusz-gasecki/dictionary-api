from sqlalchemy import select, func

def populate_metadata(conn, table, columns, table_tables, table_columns):

	# prepare statements for metadata tables table
	sel_stmt = select([table_tables.c.id]).where(func.lower(table_tables.c.name) == table.lower())
	del_stmt = table_tables.delete().where(func.lower(table_tables.c.name) == table.lower())
	ins_stmt = table_tables.insert().values(name=table, description="")
	
	# fetch id of the table that has to be deleted
	result = conn.execute(sel_stmt).fetchone()
	if result is not None:
		old_table_id = result[0]
	
		# remove entries from metadata columns table
		del_col_stmt = table_columns.delete().where(table_columns.c.table_id == old_table_id)
		conn.execute(del_col_stmt)
	
	# re-insert information to metadata tables table	
	conn.execute(del_stmt)
	result = conn.execute(ins_stmt)
	table_id = result.inserted_primary_key[0] if result.lastrowid == 0 else result.lastrowid
	
	# prepare entries to be populated to metadata columns table
	entries = list()

	for column in columns:
		entry = {}
		entry['table_id'] = table_id
		for key,v in column.items():
			if key == "name":
				entry['column_name'] = v
			elif key == "type":
				elems = str(v).split("(")
				entry["column_type"] = elems[0]
				entry['column_length'] = None
				entry['column_precision'] = None
				if len(elems) > 1 and 'TIMESTAMP' not in elems[0]:
					i_elems = elems[1].strip(')').split(",")
					entry['column_length'] = i_elems[0] if i_elems[0].isnumeric() else None
					if len(i_elems) > 1:
						entry['column_precision'] = i_elems[1] if i_elems[1].isnumeric() else None
			elif key == 'nullable':
				entry['column_nullable'] = v	
		entries.append(entry)
	
	# save entries to metadata columns table	
	conn.execute(table_columns.insert(), entries)
	
	return columns
