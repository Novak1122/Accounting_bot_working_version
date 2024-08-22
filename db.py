import logging
import sqlite3


class botdb:
    # Initialization of the connection with the database
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS  records (id INTEGER PRIMARY KEY, user_id INTEGER, operation BOOLEAN, value DECIMAL, date DATETIME)"
        )
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS  users (id INTEGER PRIMARY KEY, user_id INTEGER, join_date DATETIME)"
        )

    # check whether the user is in the database
    def user_exist(self, user_id):
        result = self.cursor.execute(
            "SELECT id FROM users WHERE user_id = ?", (user_id,)
        )
        return bool(len(result.fetchall()))

    # get the user id in the database by his user_id in the telegram
    def get_user_id(self, user_id):
        result = self.cursor.execute(
            "SELECT * FROM users WHERE user_id = ?", (user_id,)
        )
        return result.fetchone()[0]

    # add the user to the database
    def add_user(self, user_id):
        self.cursor.execute("INSERT INTO 'users' ('user_id') VALUES (?)", (user_id,))
        return self.conn.commit()

    # create an expense/profit record
    def add_record(self, user_id, operation, value):
        self.cursor.execute(
            "INSERT INTO 'records' ('user_id', 'operation', 'value', 'date' ) VALUES (?, ?, ?, datetime('now'))",
            (user_id, operation == "+", value,))

        return self.conn.commit()

    # receive the history of operations for a certain period of time
    def get_records(self, user_id, within="*"):
        if within == "day":
            result = self.cursor.execute(
                "SELECT * FROM records WHERE user_id = ? AND date BETWEEN datetime('now', 'start of day') AND datetime('now', 'localtime') ORDER BY date",
                (user_id,)
            )

        elif within == "week":
            result = self.cursor.execute(
                "SELECT * FROM records WHERE user_id = ? AND date BETWEEN datetime('now', '- 6 days', 'start of day') AND datetime('now', 'localtime') ORDER BY date",
                (user_id,)
            )

        elif within == "month":
            result = self.cursor.execute(
                "SELECT * FROM records WHERE user_id = ? AND date BETWEEN datetime('now', 'start of month') AND datetime('now', 'localtime') ORDER BY date",
                (user_id,)
            )

        else:
            result = self.cursor.execute(
                "SELECT * FROM records WHERE user_id = ? ORDER BY date",
                (user_id,),
            )

        return result.fetchall()

    def get_users(self):
        result = self.cursor.execute("SELECT * FROM 'users'")
        return result.fetchall()

    # Closing the connection with the database
    def close(self):
        self.conn.close()
