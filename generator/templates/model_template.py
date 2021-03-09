### GENERATED AT: $GENERATION_TIMESTAMP

from db import db

class $MODEL_NAME(db.Model):
	__tablename__ = '$TABLE_NAME'

	$CLASS_COLUMNS

	def __init__(self, $INIT_ARGS):
		$INIT_COLUMNS

	def update(self, $UPDATE_ARGS):
		$UPDATE_COLUMNS

	def json(self):
		return {
			$JSON_COLUMNS
		}

	def json_with_id(self):
		return {
			self.id : self.json()
		}

	@classmethod
	def arguments(self):
		return {
			'logical_key': '$LOGICAL_KEY',
			'column_list': [
				$ARGUMENTS_COLUMNS
			]
		}

	@classmethod
	def find_by_id(cls,_id):
		return cls.query.filter_by(id=_id).first()

	@classmethod
	def find_by_logical_key(cls,_id):
		return cls.query.filter_by($LOGICAL_KEY=_id).first()

	def save_to_db(self):
		db.session.add(self)
		db.session.commit()

	def delete_from_db(self):
		db.session.delete(self)
		db.session.commit()

