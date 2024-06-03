import sqlite3
import logging
logger = logging.getLogger("Accounts_Formatter")

class AccountsDatabase:
    def __init__(self, db_name='accounts_formatter.db'):
        self.conn = sqlite3.connect(db_name)
        logger.info("Database created/connected")
        self.cursor = self.conn.cursor()
        self.create_table("customer")
        self.create_table("supplier")

    def create_table(self, table: str):
        self.cursor.execute(
            f"CREATE TABLE IF NOT EXISTS {table} (reference INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT NOT "
            "NULL)")
        logger.info("Table created: %s", table)
        self.conn.commit()

    def add_customer(self, ref, name):
        self.cursor.execute('''INSERT INTO customer VALUES (?, ?)''', (ref, name))
        logger.info("Customer added: %s", name)
        self.conn.commit()

    def get_customer(self, ref):
        self.cursor.execute('''SELECT name FROM customer WHERE reference = ?''', (ref,))
        logger.info("Customer accessed: %d", ref)
        return self.cursor.fetchone()

    def add_supplier(self, ref, name):
        self.cursor.execute('''INSERT INTO supplier VALUES (?, ?)''', (ref, name))
        logger.info("Supplier added: %s", name)
        self.conn.commit()

    def get_supplier(self, ref):
        self.cursor.execute('''SELECT name FROM supplier WHERE reference = ?''', (ref,))
        logger.info("Supplier accessed: %d", ref)
        return self.cursor.fetchone()

    def delete_customer(self, ref):
        self.cursor.execute('''DELETE FROM customer WHERE reference = ?''', (ref,))
        logger.info("Customer deleted: %d", ref)
        self.conn.commit()

    def delete_supplier(self, ref):
        self.cursor.execute('''DELETE FROM supplier WHERE reference = ?''', (ref,))
        logger.info("Supplier deleted: %d", ref)
        self.conn.commit()

    def delete_table(self, table):
        assert isinstance(table, str)
        if not table.isidentifier():
            logger.error("Invalid table name %s", table)
            raise ValueError("Invalid table name")
        self.cursor.execute(f'DELETE FROM {table}')
        logger.info("Table deleted: %s", table)
        self.conn.commit()

    def get_table(self, table):
        self.cursor.execute(f'SELECT * FROM {table}')
        return self.cursor.fetchall()

    def close_db(self):
        self.conn.close()

# db = AccountsDatabase()
