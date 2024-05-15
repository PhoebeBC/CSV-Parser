import sqlite3


def add_customer(ref, name):
    conn = sqlite3.connect('accounts_formatter.db')
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO customer VALUES (?, ?)''', (ref, name))
    conn.commit()
    conn.close()

def get_customer(ref):
    conn = sqlite3.connect('accounts_formatter.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT name FROM customer WHERE reference = ?''', (ref,))
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else None

def add_supplier(ref, name):
    conn = sqlite3.connect('accounts_formatter.db')
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO supplier VALUES (?, ?)''', (ref, name))
    conn.commit()
    conn.close()

def get_supplier(ref):
    conn = sqlite3.connect('accounts_formatter.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT name FROM supplier WHERE reference = ?''', (ref,))
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else None

def delete_customer(ref):
    conn = sqlite3.connect('accounts_formatter.db')
    cursor = conn.cursor()
    cursor.execute('''DELETE FROM customer WHERE reference = ?''', (ref,))
    conn.commit()
    conn.close()

def delete_supplier(ref):
    conn = sqlite3.connect('accounts_formatter.db')
    cursor = conn.cursor()
    cursor.execute('''DELETE FROM supplier WHERE reference = ?''', (ref,))
    conn.commit()
    conn.close()

def delete_table(table):
    conn = sqlite3.connect('accounts_formatter.db')
    cursor = conn.cursor()
    assert isinstance(table, object)
    cursor.execute(f'DELETE FROM {table}')
    conn.commit()
    conn.close()


def get_table(table):
    conn = sqlite3.connect('accounts_formatter.db')
    cursor = conn.cursor()
    assert isinstance(table, object)
    cursor.execute(f'SELECT * FROM {table}')
    rows = cursor.fetchall()
    print("Column Headers:", [description[0] for description in cursor.description])
    # Print each row of the table
    for row in rows:
        print(row)
    conn.close()


#delete_table("customer")
#delete_table("supplier")

