import sqlite3
import os
from datetime import datetime
import csv


class DataBase:
    def __init__(self):
        super().__init__()

        basedir = os.path.dirname("./db.sqlite3")
        if not os.path.exists(basedir):
            file = open("./db.sqlite3", "w+")

        self.conn = sqlite3.connect("./db.sqlite3")

        self.setUp()

    def setUp(self):
        db = self.conn.cursor()
        db.execute(
            """CREATE TABLE IF NOT EXISTS settings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                account_type TEXT NOT NULL,
                interest_rate INT NOT NULL,
                loan_rate INT NOT NULL,
                loan_duration TEXT NOT NULL,
                date_added DATE NOT NULL,
                date_updated DATE NOT NULL);"""
        )

        db.execute(
            """CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT NOT NULL,
                middle_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                dob DATE NOT NULL,
                phonenumber TEXT NOT NULL,
                email TEXT, 
                address TEXT,
                account_type TEXT NOT NULL,
                status TEXT DEFAULT "active" NOT NULL,
                date_created TIMESTAMP NOT NULL);"""
        )
        db.execute(
            """CREATE TABLE IF NOT EXISTS next_of_kin (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT,
                middle_name TEXT,
                last_name TEXT,
                phonenumber TEXT,
                address TEXT,
                relationship TEXT,
                user_id INTEGER NOT NULL,
                FOREIGN KEY (user_id)
                REFERENCES users (id)
                    ON UPDATE CASCADE
                    ON DELETE CASCADE
                );
            """
        )
        db.execute(
            """CREATE TABLE IF NOT EXISTS company (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                telephone TEXT,
                address TEXT,
                user_id INTEGER NOT NULL,
                FOREIGN KEY (user_id)
                REFERENCES users (id)
                    ON UPDATE CASCADE
                    ON DELETE CASCADE
                );
            """
        )
        db.execute(
            """
            CREATE TABLE IF NOT EXISTS savings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                balance REAL DEFAULT 0,
                interest_earned REAL DEFAULT 0,
                total REAL DEFAULT 0,
                date_updated TIMESTAMP NOT NULL,
                user_id INTEGER NOT NULL,
                FOREIGN KEY (user_id)
                REFERENCES users (id)
                    ON UPDATE CASCADE
                    ON DELETE CASCADE
            );"""
        )
        db.execute(
            """CREATE TABLE IF NOT EXISTS loans (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                amount REAL NOT NULL,
                guarantor_one TEXT NOT NULL,
                guarantor_two TEXT NOT NULL,
                cleared_amount REAL DEFAULT 0,
                current_liability REAL NOT NULL DEFAULT 0,
                status TEXT DEFAULT "not cleared" NOT NULL,
                loan_period TEXT NOT NULL,
                loan_due_date DATE NOT NULL,
                date_issued TIMESTAMP NOT NULL,
                user_id INTEGER NOT NULL,
                FOREIGN KEY (user_id)
                REFERENCES users (id)
                    ON UPDATE CASCADE
                    ON DELETE CASCADE
                );
            """
        )
        db.execute(
            """CREATE TABLE IF NOT EXISTS withdrawals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                amount REAL NOT NULL,
                date TIMESTAMP NOT NULL,
                user_id INTEGER NOT NULL,
                FOREIGN KEY (user_id)
                REFERENCES users (id)
                    ON UPDATE CASCADE
                    ON DELETE CASCADE
                );
            """
        )
        db.execute(
            """CREATE TABLE IF NOT EXISTS deposits (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                amount REAL NOT NULL,
                date TIMESTAMP NOT NULL,
                user_id INTEGER NOT NULL,
                FOREIGN KEY (user_id)
                REFERENCES users (id)
                    ON UPDATE CASCADE
                    ON DELETE CASCADE
                )
                """
        )

        db.execute(
            """CREATE TABLE IF NOT EXISTS deposit_interest (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                amount REAL NOT NULL,
                interest REAL DEFAULT 0 NOT NULL,
                date_added TIMESTAMP NOT NULL,
                date_interest_start TIMESTAMP,
                date_last_interest TIMESTAMP,
                deposit_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                FOREIGN KEY (deposit_id)
                REFERENCES deposits (id)
                    ON UPDATE CASCADE
                    ON DELETE CASCADE,
                FOREIGN KEY (user_id)
                REFERENCES users (id)
                    ON UPDATE CASCADE
                    ON DELETE CASCADE
            )
            """
        )

        # a_file = open("./app/csv/user.csv")
        # rows = csv.reader(a_file)
        # db.executemany(
        #     "INSERT INTO users VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", rows
        # )

        # a_file = open("./app/csv/com_db.csv")
        # rows = csv.reader(a_file)
        # db.executemany("INSERT INTO company VALUES (?, ?, ?, ?, ?)", rows)

        # a_file = open("./app/csv/nok.csv")
        # rows = csv.reader(a_file)
        # db.executemany("INSERT INTO next_of_kin VALUES (?, ?, ?, ?,?, ?, ?,?)", rows)

        # a_file = open("./app/csv/dep.csv")
        # rows = csv.reader(a_file)
        # db.executemany("INSERT INTO deposits VALUES (?, ?, ?, ?)", rows)

        # a_file = open("./app/csv/loan.csv")
        # rows = csv.reader(a_file)
        # db.executemany("INSERT INTO loans VALUES (?, ?, ?, ?, ?, ?,?,?,?,?,?)", rows)

        # a_file = open("./app/csv/wall.csv")
        # rows = csv.reader(a_file)
        # db.executemany("INSERT INTO savings VALUES (?, ?, ?, ?,?,?)", rows)

        # a_file = open("./app/csv/dep_int.csv")
        # rows = csv.reader(a_file)
        # db.executemany("INSERT INTO deposit_interest VALUES (?, ?, ?, ?, ?,?,?,?)", rows)

        # db.execute(
        #     "INSERT INTO withdrawals VALUES (1, 5000.0, '2020-11-17 15:53:52',1)"
        # )
        # db.execute(
        #     "INSERT INTO withdrawals VALUES (2, 2000.0, '2020-11-17 20:53:52', 2)"
        # )

        # self.conn.commit()
