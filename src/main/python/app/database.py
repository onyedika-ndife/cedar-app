import os
import shutil
import sqlite3

from app import data_dir, data_dir_2, db_file, home_dir


class DataBase:
    def __init__(self):
        super().__init__()

        if not os.path.exists(data_dir):
            os.mkdir(os.sep.join([home_dir, "Cedar"]))
            os.mkdir(data_dir)
            os.mkdir(data_dir_2)

        if not os.path.exists(db_file):
            _file = open(db_file, "w+")

        self.conn = sqlite3.connect(db_file)

        self.setUp()

        shutil.copy(db_file, data_dir_2)

    def setUp(self):
        db = self.conn.cursor()
        db.execute(
            """CREATE TABLE IF NOT EXISTS settings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                account_type TEXT NOT NULL,
                interest_rate INT NOT NULL,
                loan_rate INT NOT NULL,
                loan_duration TEXT NOT NULL,
                interest_start TEXT NOT NULL,
                date_added DATE NOT NULL,
                date_updated DATE NOT NULL);"""
        )

        db.execute(
            """CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                account_number TEXT NOT NULL,
                shares REAL DEFAULT 0 NOT NULL,
                name TEXT NOT NULL,
                phonenumber TEXT,
                email TEXT, 
                address TEXT,
                account_type TEXT NOT NULL,
                status TEXT DEFAULT "active" NOT NULL,
                profile_picture TEXT,
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
                date_issued DATE NOT NULL,
                run_time INT DEFAULT 0 NOT NULL,
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
                withdrawn_from TEXT NOT NULL,
                date DATE NOT NULL,
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
                date DATE NOT NULL,
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
                date_added DATE NOT NULL,
                date_interest_start DATE,
                date_last_interest DATE,
                run_time INT DEFAULT 0 NOT NULL,
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

        db.execute(
            """CREATE TABLE IF NOT EXISTS deleted (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                deleted_amount REAL NOT NULL,
                deleted_date DATE NOT NULL,
                date DATE NOT NULL,
                user_id INTEGER NOT NULL,
                FOREIGN KEY (user_id)
                REFERENCES users (id)
                    ON UPDATE CASCADE
                    ON DELETE CASCADE
            )
            """
        )
