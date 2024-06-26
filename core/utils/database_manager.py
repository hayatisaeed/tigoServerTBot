import sqlite3
from datetime import datetime


def user_exists(user_id: int) -> bool:
    """
    Checks if the user exists in UserData, table profiles
    :param user_id: user_id of corresponding user
    :return: bool, True if user exists, False otherwise
    """

    conn = sqlite3.connect(f"data/UserData.db")
    cursor = conn.cursor()
    cursor.execute("\n"
                   "        CREATE TABLE IF NOT EXISTS profiles (\n"
                   "            id INTEGER PRIMARY KEY,\n"
                   "            user_id INTEGER,\n"
                   "            username TEXT,\n"
                   "            phone TEXT,\n"
                   "            ref INTEGER,\n"
                   "            credit REAL,\n"
                   "            verified BOOLEAN\n"
                   "        )")
    conn.commit()
    cursor.execute(f"SELECT * FROM profiles WHERE user_id={user_id}")
    row = cursor.fetchone()
    conn.close()

    if row:
        return True
    else:
        return False


def create_user(user_id: int, username: str, phone: str, credit=0.0, ref=0, verified=False):
    """
    Creates a new user in the UserData, in table profiles. if table does not exist, it will be created.
    :param user_id: user_id of new user
    :param username: username of new user. ("none": does not exist)
    :param phone: (0: does not exist)
    :param credit: by default its 0
    :param ref: user_id of ref (0: does not exist)
    :param verified: False if user is not verified, True otherwise
    :return: void
    """
    conn = sqlite3.connect(f"data/UserData.db")
    cursor = conn.cursor()
    cursor.execute("\n"
    "        CREATE TABLE IF NOT EXISTS profiles (\n"
    "            id INTEGER PRIMARY KEY,\n"
    "            user_id INTEGER,\n"
    "            username TEXT,\n"
    "            phone TEXT,\n"
    "            ref INTEGER,\n"
    "            credit REAL,\n"
    "            verified BOOLEAN\n"
    "        )")
    cursor.execute("INSERT INTO profiles (user_id, username, phone, credit, ref, verified) VALUES (?, ?, ?, ?, ?, ?)",
                   (user_id, username, phone, credit, ref, verified))
    conn.commit()
    cursor.close()
    conn.close()


def edit_user(user_id: int, parameter: str, value):
    """
    Edits a user in the UserData, in table profiles
    :param user_id: user_id of corresponding user
    :param parameter: the parameter to be edited
    :param value: value of the parameter
    :return: void
    """
    conn = sqlite3.connect('data/UserData.db')
    cursor = conn.cursor()

    query = f"UPDATE profiles SET {parameter} = ? WHERE user_id = ?"
    cursor.execute(query, (value, user_id))
    conn.commit()
    cursor.close()


def get_user_data(user_id: int) -> dict:
    """
    Gets user data of a specific user.
    :param user_id: user_id of corresponding user
    :return: a dictionary, containing user data
    """
    conn = sqlite3.connect('data/UserData.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM profiles WHERE user_id=?", (user_id,))
    user_data = cursor.fetchone()

    # If user_data is not None, convert it to dictionary format
    if user_data:
        columns = [column[0] for column in cursor.description]
        user_dict = dict(zip(columns, user_data))
    else:
        user_dict = {}  # Return an empty dictionary if user not found

    # Close the connection
    conn.close()

    return user_dict


def get_all_user_ids() -> list:
    """
    Get all user ids
    :return: a list of user ids
    """
    conn = sqlite3.connect('data/UserData.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM profiles")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    result = []
    for user_data in data:
        result.append(user_data[1])
    return result


def new_transaction(user_id: int, amount: float, transaction_type: str, payment_hash: str, date: datetime.date,
                    status: str, currency="Rials"):
    """
    Creates a new transaction in Transactions, table main. if table does not exist, creates it.
    :param user_id: user_id of corresponding user
    :param amount: amount of transaction
    :param transaction_type: could be "internal" or "gateway"
    :param payment_hash: unique payment hash of the transaction (of length 32)
    :param date: date of transaction
    :param status: could be "OK" or "FAILED"
    :param currency: could be "Rials" or anything else.
    :return: void
    """


def user_is_blocked(user_id: int) -> bool:
    """
    Checks if user is in blocked list
    :param user_id: user_id of corresponding user
    :return: bool, True if user is in blocked list, False otherwise
    """

    conn = sqlite3.connect('data/UserData.db')
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS blocked_users( id INTEGER PRIMARY KEY, user_id INTEGER)")
    conn.commit()
    cursor.execute("SELECT * FROM blocked_users WHERE user_id=?", (user_id,))
    data = cursor.fetchall()
    cursor.close()
    conn.close()

    if len(data) > 0:
        return True
    else:
        return False


def block_unblock_user(user_id: int):
    """
    Saves a user in blocked table or removes it.
    :param user_id: user_id of corresponding user
    :return: void
    """
    conn = sqlite3.connect('data/UserData.db')
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS blocked_users( id INTEGER PRIMARY KEY, user_id INTEGER)")
    conn.commit()
    cursor.execute("SELECT * FROM blocked_users WHERE user_id=?", (user_id,))
    data = cursor.fetchall()

    if len(data) > 0:
        cursor.execute("DELETE FROM blocked_users WHERE user_id=?", (user_id,))
        conn.commit()
    else:
        cursor.execute("INSERT INTO blocked_users (user_id) VALUES (?)", (user_id,))
        conn.commit()

    cursor.close()
    conn.close()

