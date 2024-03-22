import sqlite3


def read_from_db(db_name, table_name):
    conn = sqlite3.connect(f"data/{db_name}.db")
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()
    conn.close()
    return rows


def write_to_db(db_name, table_name, *args):
    conn = sqlite3.connect(f"data/{db_name}.db")  # Assuming the database has a .db extension
    cursor = conn.cursor()

    # Create the table if it doesn't exist
    cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({','.join(args)})")

    # Assuming args are column names, construct the placeholders for insertion
    placeholders = ','.join(['?' for _ in args])

    # Insert data into the table
    cursor.execute(f"INSERT INTO {table_name} VALUES ({placeholders})", args)

    # Commit the transaction and close the connection
    conn.commit()
    conn.close()
