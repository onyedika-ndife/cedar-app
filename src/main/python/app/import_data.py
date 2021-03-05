import os
import csv
from datetime import datetime, timedelta

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from app import home_dir, functions


class IMPORT(QDialog):
    def __init__(self, params):
        super().__init__()
        self.params = params

        self.setStyleSheet(
            open(self.params["ctx"].get_resource("css/style.css")).read()
        )
        self.setFixedSize(320, 150)
        self.setWindowTitle(f"Import Data - Cedar")
        self.setWindowFlags(Qt.WindowStaysOnTopHint)

        self._view()

    def _view(self):
        initial_layout = QVBoxLayout()
        upload_btn = QPushButton(
            QIcon(self.params["ctx"].get_resource("icon/upload.png")),
            "Import Data via CSV",
        )
        upload_btn.setIconSize(QSize(50, 50))

        download_btn = QPushButton(
            QIcon(self.params["ctx"].get_resource("icon/download.png")),
            "View CSV Sample",
        )

        initial_layout.addWidget(upload_btn)
        initial_layout.addWidget(download_btn)

        upload_btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        upload_btn.clicked.connect(self._handle_upload_btn)

        download_btn.clicked.connect(self._handle_download_btn)

        self.setLayout(initial_layout)

    def _handle_upload_btn(self):
        data_dir = os.sep.join([home_dir, "Documents"])
        frame = QFileDialog.getOpenFileName(
            self, "Select CSV", data_dir, "CSV Files (*.csv)"
        )
        self.import_database(file_path=frame[0])

    def _handle_download_btn(self):
        data_dir = os.sep.join([home_dir, "Documents"])

        frame = QFileDialog.getSaveFileName(
            self, "Save File", "cedar-sample.csv", "CSV Files (*.csv)"
        )

        with open(frame[0], mode="w") as csv_file:
            field_names = [
                "NAME",
                "ACCOUNT NUMBER",
                "SHARES",
                "DATE (SHARES)",
                "SAVINGS CREDIT",
                "DATE (SAVINGS CREDIT)",
                "SAVINGS DEBIT",
                "DATE (SAVINGS DEBIT)",
                "LOAN",
                "DATE (LOAN)",
                "CLEARED PAYMENT (LOAN)",
                "OUTSTANDING PAYMENT (LOAN)",
            ]

            writer = csv.DictWriter(csv_file, fieldnames=field_names)
            writer.writeheader()
            self.hide()

    def import_database(self, file_path):
        user_list = []
        user_deposit_list = []
        db = self.params["db"].conn.cursor()
        msg = QMessageBox()
        msg.setStyleSheet(open(self.params["ctx"].get_resource("css/style.css")).read())
        msg.setWindowFlags(Qt.WindowStaysOnTopHint)
        with open(file_path) as csv_file:
            csv_reader = csv.DictReader(csv_file)
            row_count = 0

            try:
                for row in csv_reader:
                    user_id, status, last_deposit_id, dep_amt, deposit_date = (
                        None,
                        None,
                        None,
                        None,
                        None,
                    )
                    name = row["NAME"].split(" ")
                    status = (
                        "inactive"
                        if name[-1] == "***" or name[-1].lower() == "xxx"
                        else "active"
                    )
                    name = [item.capitalize() for item in name]
                    name = " ".join(
                        name[:-1]
                        if name[-1] == "***" or name[-1].lower() == "xxx"
                        else name
                    )

                    db.execute("""SELECT id FROM users WHERE name=?;""", (name,))
                    current_user = db.fetchone()

                    user_does_exist = True if not current_user is None else False
                    create_date = (
                        datetime.strptime(row["DATE (SHARES)"], "%d/%m/%Y").strftime(
                            "%Y-%m-%d %H:%M:%S"
                        )
                        if not row["DATE (SHARES)"] == ""
                        else datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    )

                    db.execute(
                        """SELECT loan_duration FROM settings WHERE account_type=?;""",
                        ("member",),
                    )
                    loan_dura = db.fetchone()[0]

                    dur = loan_dura.split(" ")
                    time = dur[1].lower().replace("(s)", "")

                    if time == "year":
                        time = 52.143 * int(dur[0])
                    elif time == "month":
                        time = 4.345 * int(dur[0])

                    if not user_does_exist:
                        db.execute(
                            """INSERT INTO users (
                                account_number,
                                shares,
                                name,
                                account_type,
                                status,
                                date_created) VALUES (?,?,?,?,?,?);""",
                            (
                                row["ACCOUNT NUMBER"],
                                row["SHARES"].replace(",", ""),
                                name,
                                "member",
                                status,
                                create_date,
                            ),
                        )
                        db.execute(
                            """
                            SELECT id FROM users ORDER BY id DESC LIMIT 1;
                            """
                        )
                        user_id = db.fetchone()[0]
                        db.execute(
                            """INSERT INTO next_of_kin (
                                user_id) VALUES (?);""",
                            (user_id,),
                        )
                        db.execute(
                            """INSERT INTO company (
                                user_id) VALUES (?);""",
                            (user_id,),
                        )

                        db.execute(
                            """INSERT INTO savings(date_updated, user_id) VALUES (?,?);""",
                            (
                                create_date,
                                user_id,
                            ),
                        )

                        # -------------------------------------
                        # -------------------------------------
                        deposit_date = (
                            datetime.strptime(
                                row["DATE (SAVINGS CREDIT)"], "%d/%m/%Y"
                            ).strftime("%Y-%m-%d")
                            if not row["DATE (SAVINGS CREDIT)"] == ""
                            else datetime.now().strftime("%Y-%m-%d")
                        )
                        savings_date = (
                            datetime.strptime(deposit_date, "%Y-%m-%d").strftime(
                                "%Y-%m-%d %H:%M:%S"
                            )
                            if not deposit_date == ""
                            else create_date
                        )
                        dep_amt = row["SAVINGS CREDIT"]

                        if not dep_amt == "":
                            dep_amt = dep_amt.replace(",", "")

                            db.execute(
                                """SELECT balance,total FROM savings WHERE user_id=?""",
                                (user_id,),
                            )

                            savings = db.fetchone()
                            bal = float(savings[0]) + float(dep_amt)
                            total = float(savings[1]) + float(dep_amt)
                            db.execute(
                                """UPDATE savings SET
                                        balance=?,
                                        total=?,
                                        date_updated=? WHERE user_id=?""",
                                (
                                    bal,
                                    total,
                                    savings_date,
                                    user_id,
                                ),
                            )
                            db.execute(
                                f"""INSERT INTO deposits (
                                    amount,
                                    date,
                                    user_id) VALUES (?,?,?);""",
                                (
                                    float(dep_amt),
                                    deposit_date,
                                    user_id,
                                ),
                            )

                            db.execute(
                                f"""SELECT id FROM deposits WHERE user_id=? ORDER BY id DESC LIMIT 1;""",
                                (user_id,),
                            )
                            last_deposit_id = db.fetchone()[0]

                        # -------------------------------------
                        # -------------------------------------
                        withdraw_date = (
                            datetime.strptime(
                                row["DATE (SAVINGS DEBIT)"], "%d/%m/%Y"
                            ).strftime("%Y-%m-%d")
                            if not row["DATE (SAVINGS DEBIT)"] == ""
                            else datetime.now().strftime("%Y-%m-%d")
                        )
                        savings_date = (
                            datetime.strptime(withdraw_date, "%Y-%m-%d").strftime(
                                "%Y-%m-%d %H:%M:%S"
                            )
                            if not withdraw_date == ""
                            else create_date
                        )

                        amt = row["SAVINGS DEBIT"]

                        if not amt == "":
                            amt = amt.replace(",", "")
                            db.execute(
                                """SELECT balance,total FROM savings WHERE user_id=?""",
                                (user_id,),
                            )
                            savings = db.fetchone()
                            bal = float(savings[0]) - float(amt)
                            total = float(savings[1]) - float(amt)
                            db.execute(
                                """UPDATE savings SET
                                    balance=?,
                                    total=?,
                                    date_updated=? WHERE user_id=?;""",
                                (
                                    bal,
                                    total,
                                    savings_date,
                                    user_id,
                                ),
                            )
                            db.execute(
                                """INSERT INTO withdrawals (
                                    amount,
                                    withdrawn_from,
                                    date,
                                    user_id) VALUES (?,?,?,?)""",
                                (
                                    float(amt),
                                    "balance",
                                    withdraw_date,
                                    user_id,
                                ),
                            )
                        # -------------------------------------
                        # -------------------------------------
                        loan_date = (
                            datetime.strptime(row["DATE (LOAN)"], "%d/%m/%Y").strftime(
                                "%Y-%m-%d"
                            )
                            if not row["DATE (LOAN)"] == ""
                            else datetime.now().strftime("%Y-%m-%d")
                        )
                        td_date = datetime.strptime(loan_date, "%Y-%m-%d")

                        loan_amt = row["LOAN"]

                        if not loan_amt == "":
                            loan_amt = loan_amt.replace(",", "")
                            due_date = td_date + timedelta(weeks=time)
                            loan_status = (
                                "cleared"
                                if row["OUTSTANDING PAYMENT (LOAN)"] == ""
                                else "not cleared"
                            )
                            db.execute(
                                """INSERT INTO loans (
                                    amount,
                                    guarantor_one,
                                    guarantor_two,
                                    cleared_amount,
                                    current_liability,
                                    status,
                                    loan_period,
                                    loan_due_date,
                                    date_issued,
                                    user_id) VALUES (?,?,?,?,?,?,?,?,?,?)""",
                                (
                                    float(loan_amt),
                                    "nil",
                                    "nil",
                                    round(
                                        float(
                                            row["CLEARED PAYMENT (LOAN)"].replace(
                                                ",", ""
                                            )
                                            if not row["CLEARED PAYMENT (LOAN)"] == ""
                                            else 0.0
                                        ),
                                        2,
                                    ),
                                    round(
                                        float(
                                            row["OUTSTANDING PAYMENT (LOAN)"].replace(
                                                ",", ""
                                            )
                                            if not row["OUTSTANDING PAYMENT (LOAN)"]
                                            == ""
                                            else 0.0
                                        ),
                                        2,
                                    ),
                                    loan_status,
                                    loan_dura,
                                    due_date.date(),
                                    loan_date,
                                    user_id,
                                ),
                            )
                    else:
                        user_id = current_user[0]
                        db.execute(
                            """INSERT INTO savings(date_updated, user_id) VALUES (?,?);""",
                            (
                                create_date,
                                user_id,
                            ),
                        )

                        # -------------------------------------
                        # -------------------------------------
                        deposit_date = (
                            datetime.strptime(
                                row["DATE (SAVINGS CREDIT)"], "%d/%m/%Y"
                            ).strftime("%Y-%m-%d")
                            if not row["DATE (SAVINGS CREDIT)"] == ""
                            else datetime.now().strftime("%Y-%m-%d")
                        )
                        savings_date = (
                            datetime.strptime(deposit_date, "%Y-%m-%d").strftime(
                                "%Y-%m-%d %H:%M:%S"
                            )
                            if not deposit_date == ""
                            else create_date
                        )
                        dep_amt = row["SAVINGS CREDIT"]

                        if not dep_amt == "":
                            dep_amt = dep_amt.replace(",", "")
                            db.execute(
                                """SELECT balance,total FROM savings WHERE user_id=?""",
                                (user_id,),
                            )

                            savings = db.fetchone()

                            bal = float(savings[0]) + float(dep_amt)
                            total = float(savings[1]) + float(dep_amt)

                            db.execute(
                                """UPDATE savings SET
                                        balance=?,
                                        total=?,
                                        date_updated=? WHERE user_id=?""",
                                (
                                    bal,
                                    total,
                                    savings_date,
                                    user_id,
                                ),
                            )
                            db.execute(
                                f"""INSERT INTO deposits (
                                    amount,
                                    date,
                                    user_id) VALUES (?,?,?);""",
                                (
                                    float(dep_amt),
                                    deposit_date,
                                    user_id,
                                ),
                            )

                            db.execute(
                                f"""SELECT id FROM deposits WHERE user_id=? ORDER BY id DESC LIMIT 1;""",
                                (user_id,),
                            )
                            last_deposit_id = db.fetchone()[0]

                        # -------------------------------------
                        # -------------------------------------

                        withdraw_date = (
                            datetime.strptime(
                                row["DATE (SAVINGS DEBIT)"], "%d/%m/%Y"
                            ).strftime("%Y-%m-%d")
                            if not row["DATE (SAVINGS DEBIT)"] == ""
                            else datetime.now().strftime("%Y-%m-%d")
                        )
                        savings_date = (
                            datetime.strptime(withdraw_date, "%Y-%m-%d").strftime(
                                "%Y-%m-%d %H:%M:%S"
                            )
                            if not withdraw_date == ""
                            else create_date
                        )

                        amt = row["SAVINGS DEBIT"]

                        if not amt == "":
                            amt = amt.replace(",", "")
                            db.execute(
                                """SELECT balance,total FROM savings WHERE user_id=?""",
                                (user_id,),
                            )

                            savings = db.fetchone()

                            bal = float(savings[0]) - float(amt)
                            total = float(savings[1]) - float(amt)

                            db.execute(
                                """UPDATE savings SET
                                    balance=?,
                                    total=?,
                                    date_updated=? WHERE user_id=?;""",
                                (
                                    bal,
                                    total,
                                    savings_date,
                                    user_id,
                                ),
                            )
                            db.execute(
                                """INSERT INTO withdrawals (
                                    amount,
                                    withdrawn_from,
                                    date,
                                    user_id) VALUES (?,?,?,?)""",
                                (
                                    float(amt),
                                    "balance",
                                    withdraw_date,
                                    user_id,
                                ),
                            )

                        # -------------------------------------
                        # -------------------------------------

                        loan_date = (
                            datetime.strptime(row["DATE (LOAN)"], "%d/%m/%Y").strftime(
                                "%Y-%m-%d"
                            )
                            if not row["DATE (LOAN)"] == ""
                            else datetime.now().strftime("%Y-%m-%d")
                        )
                        td_date = datetime.strptime(loan_date, "%Y-%m-%d")

                        loan_amt = row["LOAN"]

                        if not loan_amt == "":
                            loan_amt = loan_amt.replace(",", "")
                            due_date = td_date + timedelta(weeks=time)
                            loan_status = (
                                "cleared"
                                if row["OUTSTANDING PAYMENT (LOAN)"] == ""
                                else "not cleared"
                            )
                            db.execute(
                                """INSERT INTO loans (
                                    amount,
                                    guarantor_one,
                                    guarantor_two,
                                    cleared_amount,
                                    current_liability,
                                    status,
                                    loan_period,
                                    loan_due_date,
                                    date_issued,
                                    user_id) VALUES (?,?,?,?,?,?,?,?,?,?)""",
                                (
                                    float(loan_amt),
                                    "nil",
                                    "nil",
                                    round(
                                        float(
                                            row["CLEARED PAYMENT (LOAN)"].replace(
                                                ",", ""
                                            )
                                            if not row["CLEARED PAYMENT (LOAN)"] == ""
                                            else 0.0
                                        ),
                                        2,
                                    ),
                                    round(
                                        float(
                                            row["OUTSTANDING PAYMENT (LOAN)"].replace(
                                                ",", ""
                                            )
                                            if not row["OUTSTANDING PAYMENT (LOAN)"]
                                            == ""
                                            else 0.0
                                        ),
                                        2,
                                    ),
                                    loan_status,
                                    loan_dura,
                                    due_date.date(),
                                    loan_date,
                                    user_id,
                                ),
                            )

                    self.params["db"].conn.commit()

                    if not dep_amt == "" and not last_deposit_id is None:
                        functions.check_sched_deposit(
                            self.params,
                            user_id,
                            status,
                            "member",
                            last_deposit_id,
                            float(dep_amt),
                            deposit_date,
                        )
                    row_count += 1

                msg.setWindowTitle("Import Completed")
                msg.setIconPixmap(
                    QPixmap(self.params["ctx"].get_resource("icon/success.png"))
                )
                msg.setText("Account import completed")
                msg.setDefaultButton(QMessageBox.Ok)
                msg.buttonClicked.connect(lambda: self.hide())
            except Exception as e:
                msg.setWindowTitle("ERROR")
                msg.setIconPixmap(
                    QPixmap(self.params["ctx"].get_resource("icon/error.png"))
                )
                msg.setText(f"Error:\n{e}")
                msg.setDefaultButton(QMessageBox.Ok)
            msg.exec_()
            msg.show()
