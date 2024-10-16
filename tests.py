import unittest

import sqlalchemy
from sqlalchemy import Table, select, func

from connection import old_db_connection, new_db_connection


class MigrationTestSuite(unittest.TestCase):
	@classmethod
	def setUpClass(cls):
		cls.mysql = sqlalchemy.create_engine(old_db_connection())
		cls.psql = sqlalchemy.create_engine(new_db_connection())
		cls.mysql_metadata = sqlalchemy.MetaData()
		cls.mysql_metadata.reflect(bind=cls.mysql)
		cls.mysql_tables = cls.mysql_metadata.tables.keys()
		cls.psql_metadata = sqlalchemy.MetaData()
		cls.psql_metadata.reflect(bind=cls.psql)
		cls.psql_tables = cls.psql_metadata.tables.keys()

		sqlalchemy.MetaData().reflect(bind=cls.psql)

	@classmethod
	def tearDownClass(cls):
		cls.mysql.dispose()
		cls.psql.dispose()

	def test_table_count(self):
		self.assertEqual(
			len(self.mysql_tables), len(self.psql_tables),
			f'Number of tables do not match. \n'
			f'Previous number of tables: {len(self.mysql_tables)}. Current number of tables: {len(self.psql_tables)} '
		)

	def test_table_migration(self):
		missing_tables = set(self.mysql_tables) - set(self.psql_tables)
		extra_tables = set(self.psql_tables) - set(self.mysql_tables)
		self.assertEqual(
			0, len(missing_tables),
			f'These tables were not found in the new database: {missing_tables}'
		)
		self.assertEqual(
			0, len(extra_tables),
			f'These tables were not found in the old database: {extra_tables}'
		)

	def test_column_migration(self):
		for table in self.mysql_tables:
			if table not in self.psql_tables:
				self.fail(f'Table {table} was not found in the new database')

			old_columns = set(self.mysql_metadata.tables[table].columns.keys())
			new_columns = set(self.psql_metadata.tables[table].columns.keys())

			missing_columns = old_columns - new_columns
			extra_missing_columns = new_columns - old_columns
			self.assertEqual(
				0, len(missing_columns),
				f'Columns were not found in the new database: {missing_columns}'
			)
			self.assertEqual(
				0, len(extra_missing_columns),
				f'Columns were not found in the old database: {extra_missing_columns}'
			)

	def test_row_count(self):
		for table in self.mysql_tables:
			if table not in self.psql_tables:
				self.fail(f'Table {table} was not found in the new database')

			old_table = Table(table, self.mysql_metadata, autoload_with=self.mysql)
			new_table = Table(table, self.psql_metadata, autoload_with=self.psql)

			conn = self.mysql.connect()
			old_table_row_count = conn.execute(select([func.count()]).select_from(old_table)).scalar()
			new_table_row_count = conn.execute(select([func.count()]).select_from(new_table)).scalar()
			self.assertEqual(
				old_table_row_count, new_table_row_count,
				f'Row count do not match in table: {old_table.name}.\n'
				f'Previous table row count: {old_table_row_count}.\n'
				f'Current table row count: {new_table_row_count}.'
			)

	def test_primary_key_constraints(self):
		for table in self.mysql_tables:
			if table not in self.psql_tables:
				self.fail(f'Table {table} was not found in the new database')

			old_table = Table(table, self.psql_metadata, autoload_with=self.mysql)
			new_table = Table(table, self.psql_metadata, autoload_with=self.psql)

			old_pk = old_table.primary_key
			new_pk = new_table.primary_key

			self.assertEqual(old_pk, new_pk, f'Primary key does not match in table: {old_table.name}.\n')

	def test_foreign_key_constraints(self):
		old_foreign_keys = []
		new_foreign_keys = []
		for table in self.mysql_tables:
			if table not in self.psql_tables:
				self.fail(f'Table {table} was not found in the new database')

			old_table = Table(table, self.psql_metadata, autoload_with=self.mysql)
			new_table = Table(table, self.psql_metadata, autoload_with=self.psql)

			old_foreign_keys = [o_fk for o_fk in old_table.foreign_keys]
			new_foreign_keys = [n_fk for n_fk in new_table.foreign_keys]
			self.assertEqual(
				len(old_foreign_keys), len(new_foreign_keys),
				f'Foreign keys length Mismatch: {len(old_foreign_keys)} vs {len(new_foreign_keys)}.\n'
			)

		for old_fk, new_fk in zip(old_foreign_keys, new_foreign_keys):
			self.assertEqual(
				old_fk, new_fk,
				f'Foreign keys do not match in table: {old_fk.name}.\n'
			)

	def test_table_indexes(self):
		for table in self.mysql_tables:
			if table not in self.psql_tables:
				self.fail(f'Table {table} was not found in the new database')

			old_table = Table(table, self.psql_metadata, autoload_with=self.mysql)
			new_table = Table(table, self.psql_metadata, autoload_with=self.psql)

			self.assertEqual(
				old_table.indexes, new_table.indexes,
				f'Indexes do not match in table: {old_table.name}.\n'
				f'Previous Indexes: {old_table.indexes}.\n'
				f'Current Indexes: {new_table.indexes}.'
			)

	def test_null_constraint(self):
		for table in self.mysql_tables:
			if table not in self.psql_tables:
				self.fail(f'Table {table} was not found in the new database')

			old_table = Table(table, self.psql_metadata, autoload_with=self.mysql)
			new_table = Table(table, self.psql_metadata, autoload_with=self.psql)

			for column in old_table.columns.keys():
				old_nullable = old_table.columns[column.name].nullable
				new_nullable = new_table.columns[column.name].nullable
				self.assertEqual(
					old_nullable, new_nullable,
					f"Nullability mismatch in table '{table}' for column '{column.name}'"
				)
