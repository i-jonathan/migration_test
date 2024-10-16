from testcontainers.mysql import MySqlContainer
from testcontainers.postgres import PostgresContainer

old_container = MySqlContainer()
old_container.start()
new_container = PostgresContainer(username='postgres', password='postgres', dbname='postgres')
new_container.start()


def old_db_connection() -> str:
	return old_container.get_connection_url()


def new_db_connection() -> str:
	return new_container.get_connection_url()
