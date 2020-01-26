import sqlite3


class Database:
    def __init__(self, database_path):
        self.database = database_path

        self.conn = sqlite3.connect(self.database)
        self.conn.row_factory = self.dict_factory

    def raw_query(self, query):
        c = self.conn.cursor()
        c.execute(query)

        return c.fetchall()

    def get_rows(self, table, key, value):
        c = self.conn.cursor()

        # The usual ? security trick doesn't work here.
        query_params = (value,)
        query = "SELECT * FROM %s WHERE %s=?" % (table, key)

        c.execute(query, query_params)

        return c.fetchall()

    @staticmethod
    def dict_factory(cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

    def __del__(self):
        self.conn.close()
