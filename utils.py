import sqlite3

db_path = "./my_db"

def fetch_all(table_name):
    add_table()
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    rows = cursor.execute(f'SELECT * FROM {table_name}')
    rows = rows.fetchall()
    connection.commit()
    return rows
    

def add_table():
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS inventory (
id INTEGER NOT NULL,
name TEXT NOT NULL,
type TEXT NOT NULL
);""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS user_info (
name TEXT NOT NULL,
id INT NOT NULL
);""")
    rows = cursor.execute(f'SELECT * FROM user_info;')
    rows = rows.fetchall()
    if len(rows) != 0:
        connection.commit()
    else:
        cursor.execute("""INSERT INTO user_info (name, id) VALUES ('skin', 0);""")
        cursor.execute("""INSERT INTO user_info (name, id) VALUES ('scooter', 0);""")
        cursor.execute("""INSERT INTO user_info (name, id) VALUES ('clean', 0);""")
        connection.commit()

def update_item(table_name, new_item):
    """
    new_item
        - id
        - name
    """
    add_table()
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor(f"UPDATE {table_name} SET id = ? WHERE name = ?", (new_item['id'], new_item['name']))
    connection.commit()


def add_item(table_name, new_item):
    add_table()
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    column_names = list(new_item.keys())
    values = tuple(list(new_item.values))
    columns="("
    for name in column_names:
        columns+=f"{name},"
        columns+=' '
    columns =columns.strip()
    columns+=')'
    cursor.execute(f"INSERT OR IGNORE INTO {table_name} {columns} VALUES (?, ?, ?)", values)
    connection.commit()
    
