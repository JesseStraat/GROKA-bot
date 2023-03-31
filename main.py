import json
from datetime import datetime

import mariadb

config = json.load(open("config.json"))


class Server:
    """
    This class is meant to access the database.
    """

    def __init__(self, config_path):
        config_json = json.load(open(config_path))
        self.host = config_json["host"]
        self.database = config_json["database"]
        self.user = config_json["user"]
        self.password = config_json["password"]
        self.port = config_json["port"]
        self.connection = None
        self.cursor = None
        self.connect()
        self.getCursor()

    def connect(self):
        self.connection = mariadb.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database,
            port=self.port
        )

    def getCursor(self):
        self.cursor = self.connection.cursor()

    def closeCursor(self):
        self.cursor.close()
        self.getCursor()

    def execute(self, query):
        try:
            self.cursor.execute(query)
        except mariadb.Error as e:
            print(f"Error: {e}\nQuery: {query}")
            raise e

    def commit(self):
        self.connection.commit()

    def close(self):
        self.connection.close()


default_server = Server("config.json")


class Table:
    """
    This class is meant to access a table in the database.
    """

    def __init__(self, name, server_object=None):
        self.name = name
        self.server = server_object
        if self.server is None:
            self.server = default_server

    def retrieve(self, value, column):
        self.server.execute(
            f"SELECT * FROM {self.name} WHERE {column} = '{value}';")
        values = self.server.cursor.fetchall()
        self.server.closeCursor()
        return values

    def query(self, query):
        self.server.execute(query)
        values = self.server.cursor.fetchall()
        self.server.closeCursor()
        return values

    def find(self, value, column, return_column):
        self.server.execute(
            f"SELECT {return_column} FROM {self.name} WHERE {column} = '{value}';")
        values = self.server.cursor.fetchall()
        self.server.closeCursor()
        return values

    def values(self):
        self.server.execute(f"SELECT * FROM {self.name};")
        values = self.server.cursor.fetchall()
        self.server.closeCursor()
        return values

    def like(self, value, column):
        self.server.execute(
            f"SELECT * FROM {self.name} WHERE {column} LIKE '%{value}%';")
        values = self.server.cursor.fetchall()
        self.server.closeCursor()
        return values

    def soundsLike(self, value, column):
        self.server.execute(
            f"SELECT * FROM {self.name} WHERE STRCMP({column},'{value}');")
        values = self.server.cursor.fetchall()
        self.server.closeCursor()
        return values

    def execute(self, query):
        self.server.execute(query)

    def commit(self):
        self.server.commit()

    def find_all(self, column):
        self.server.execute(
            f"SELECT {column} FROM {self.name};")
        values = self.server.cursor.fetchall()
        self.server.closeCursor()
        return [i[0] for i in values]




