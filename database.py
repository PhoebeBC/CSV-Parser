import sqlite3
from psycopg import sql


class AccountsDatabase:
    def __init__(self, db_name='accounts_formatter'):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self, table):
        assert isinstance(table, str)
        if not table.isidentifier():
            raise ValueError("Invalid table name")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS {table} (key INTEGER PRIMARY KEY AUTOINCREMENT,value TEXT NOT "
                            "NULL)")
        self.conn.commit()

    def add_customer(self, ref, name):
        self.cursor.execute('''INSERT INTO customer VALUES (?, ?)''', (ref, name))
        self.conn.commit()

    def get_customer(self, ref):
        self.cursor.execute('''SELECT name FROM customer WHERE reference = ?''', (ref,))
        return self.cursor.fetchone()

    def add_supplier(self, ref, name):
        self.cursor.execute('''INSERT INTO supplier VALUES (?, ?)''', (ref, name))
        self.conn.commit()

    def get_supplier(self, ref):
        self.cursor.execute('''SELECT name FROM supplier WHERE reference = ?''', (ref,))
        return self.cursor.fetchone()

    def delete_customer(self, ref):
        self.cursor.execute('''DELETE FROM customer WHERE reference = ?''', (ref,))
        self.conn.commit()

    def delete_supplier(self, ref):
        self.cursor.execute('''DELETE FROM supplier WHERE reference = ?''', (ref,))
        self.conn.commit()

    def delete_table(self, table):
        assert isinstance(table, str)
        if not table.isidentifier():
            raise ValueError("Invalid table name")
        self.cursor.execute(f'DELETE FROM {table}')
        self.conn.commit()

    def get_table(self, table):
        assert isinstance(table, object)
        self.cursor.execute(f'SELECT * FROM {table}')
        return self.cursor.fetchall()

    def close_db(self):
        self.conn.close()

db = AccountsDatabase()

