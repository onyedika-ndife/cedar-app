import sqlite3
from datetime import datetime, timedelta

from apscheduler.triggers.interval import IntervalTrigger
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from app import db_file


class DEPOSIT_FORM(QDialog):
    def __init__(self, params):
        super().__init__()
        self.params = params
        self.db = self.params["db"].conn.cursor()

        self.accounts = self._get_data_db()

        self.setStyleSheet(
            open(self.params["ctx"].get_resource("css/style.css")).read()
        )
        self.setFixedSize(320, 150)
        self.setWindowTitle(f"Deposit Form - Cedar")
        self.setWindowFlags(Qt.WindowStaysOnTopHint)

        self._view()

    def _view(self):
        initial_layout = QGridLayout()

        self.combo_box = QComboBox()
        self.combo_box.setEditable(True)
        if len(self.accounts) > 0:
            self.combo_box.addItems(self.accounts)
            combo_comp = QCompleter(self.accounts)
            self.combo_box.setCompleter(combo_comp)
            combo_comp.setCompletionMode(QCompleter.PopupCompletion)
            combo_comp.setCaseSensitivity(Qt.CaseInsensitive)
            combo_comp.setFilterMode(Qt.MatchContains)
        else:
            self.combo_box.addItems(["No Account Registered"])

        self.combo_box.setCurrentIndex(-1)
        self.combo_box.lineEdit().setPlaceholderText("--Select Account--")
        initial_layout.addWidget(self.combo_box, 0, 0, 1, 0)
        amt_lbl = QLabel("Amount:")
        self.amt_int = QLineEdit()
        self.amt_int.setValidator(QRegExpValidator(QRegExp("^[0-9]{1,},*")))
        self.amt_int.setClearButtonEnabled(True)
        self.amt_int.textChanged.connect(self._calc)
        initial_layout.addWidget(amt_lbl, 1, 0)
        initial_layout.addWidget(self.amt_int, 1, 1)
        amt_lbl.setObjectName("DW")

        date_lbl = QLabel("Date:")
        self.date_select = QDateEdit(calendarPopup=True)
        self.date_select.setDate(QDate.currentDate())
        #  QLabel(str(datetime.today().date().strftime("%B %d, %Y")))
        initial_layout.addWidget(date_lbl, 2, 0)
        initial_layout.addWidget(self.date_select, 2, 1)
        date_lbl.setObjectName("DW")

        btn_layout = QHBoxLayout()
        btn_layout.setContentsMargins(0, 0, 0, 0)

        save_btn = QPushButton("Deposit")
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(lambda: self.hide())

        cancel_btn.setFixedHeight(40)
        save_btn.setFixedHeight(40)

        btn_layout.addWidget(cancel_btn)
        btn_layout.addWidget(save_btn)

        save_btn.clicked.connect(self._handle_check_save)
        initial_layout.addLayout(btn_layout, 3, 0, 1, 0)

        self.setLayout(initial_layout)

    def _handle_check_save(self):
        name = self.combo_box.currentText().split(" ")
        self.db.execute(
            """SELECT account_type FROM users WHERE last_name=? AND first_name=?;""",
            (name[0], name[1]),
        )
        acc_type = self.db.fetchone()[0]
        self.db.execute("""SELECT * FROM settings WHERE account_type=?;""", (acc_type,))
        sett = self.db.fetchone()
        if not sett is None:
            details = f"""The details are as follows:

                    Account: {self.combo_box.currentText()}
                    Amount: {self.amt_int.text()}
                    Date: {self.date_select.date().toPyDate().strftime("%Y-%m-%d")}"""

            msg = QMessageBox()
            msg.setStyleSheet(
                open(self.params["ctx"].get_resource("css/style.css")).read()
            )
            msg.setWindowFlags(Qt.WindowStaysOnTopHint)
            msg.setIconPixmap(
                QPixmap(self.params["ctx"].get_resource("icon/question.png"))
            )
            msg.setText(
                f"Are you sure you want to deposit \u20A6{self.amt_int.text()} into {self.combo_box.currentText()}'s account?"
            )
            msg.setWindowTitle(f"Account Deposit")
            msg.setDetailedText(details)
            msg.setStandardButtons(QMessageBox.No | QMessageBox.Yes)
            msg.setDefaultButton(QMessageBox.Yes)
            msg.buttonClicked.connect(self._handle_dw_save)
            msg.exec_()
        else:
            msg = QMessageBox()
            msg.setStyleSheet(
                open(self.params["ctx"].get_resource("css/style.css")).read()
            )
            msg.setWindowFlags(Qt.WindowStaysOnTopHint)
            msg.setIconPixmap(
                QPixmap(self.params["ctx"].get_resource("icon/high_priority.png"))
            )

            msg.setText(
                f"Cedar Rates have not been set for {acc_type.capitalize()} Accounts.\nSet Now?"
            )
            msg.setWindowTitle(f"Cedar Rates")
            msg.setStandardButtons(QMessageBox.No | QMessageBox.Yes)
            msg.setDefaultButton(QMessageBox.Yes)
            msg.buttonClicked.connect(self._handle_sett)
            msg.exec_()

    def _handle_sett(self, choice):
        if choice.text() == "&Yes":
            self.hide()
            self.params["parent"]["setting_btn"].click()

    def _handle_dw_save(self, choice):
        if choice.text() == "&Yes":
            user = self.combo_box.currentText().split(" ")
            amt = self.amt_int.text()
            amt = amt.replace(",", "")
            self.db.execute(
                """SELECT id FROM users WHERE last_name=? AND first_name=?;""",
                (user[0], user[1]),
            )
            user_id = self.db.fetchone()[0]
            msg = QMessageBox()
            msg.setStyleSheet(
                open(self.params["ctx"].get_resource("css/style.css")).read()
            )
            msg.setWindowTitle(f"Account Deposit")
            try:
                self.db.execute(
                    """SELECT balance,total FROM savings WHERE user_id=?""",
                    (user_id,),
                )
                savings = self.db.fetchone()
                bal = float(savings[0]) + float(amt)
                total = float(savings[1]) + float(amt)

                date = self.date_select.date().toPyDate().strftime("%Y-%m-%d")
                savings_date = datetime.strptime(date, "%Y-%m-%d").strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
                self.db.execute(
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
                self.db.execute(
                    f"""INSERT INTO deposits (
                        amount,
                        date,
                        user_id) VALUES (?,?,?);""",
                    (
                        amt,
                        date,
                        user_id,
                    ),
                )
                self.db.execute("""SELECT id FROM deposits ORDER BY id DESC LIMIT 1;""")
                last_deposit_id = self.db.fetchone()[0]
                self.db.execute(
                    f"""INSERT INTO deposit_interest (
                        amount,
                        date_added,
                        deposit_id,
                        user_id) VALUES (?,?,?,?);""",
                    (
                        amt,
                        date,
                        last_deposit_id,
                        user_id,
                    ),
                )

                self.params["db"].conn.commit()
                self.db.execute(
                    """SELECT account_type FROM users WHERE id=?;""",
                    (user_id,),
                )
                acc_type = self.db.fetchone()[0]
                self._check_shed(user_id, acc_type, last_deposit_id, amt, date)

                msg.setIconPixmap(
                    QPixmap(self.params["ctx"].get_resource("icon/success.png"))
                )
                msg.setWindowFlags(Qt.WindowStaysOnTopHint)
                msg.setText(f"Deposit successfully recorded")
                msg.buttonClicked.connect(self._clear)
            except Exception as e:
                msg.setIconPixmap(
                    QPixmap(self.params["ctx"].get_resource("icon/error.png"))
                )
                msg.setWindowFlags(Qt.WindowStaysOnTopHint)
                msg.setText(f"Error!\nPlease check the form again")
            msg.setDefaultButton(QMessageBox.Ok)
            msg.exec_()
            msg.show()

    def _calc(self, number):
        if not number == "":
            number = number.replace(",", "")
            new_numb = "{:,}".format(int(number))
            self.amt_int.setText(new_numb)

    def _check_shed(self, user_id, account_type, last_deposit_id, amount, date):
        py_date = datetime.strptime(date, "%Y-%m-%d").date()
        today = datetime.today().date()
        self.db.execute(
            """SELECT interest_start FROM settings WHERE account_type=? ORDER BY id DESC LIMIT 1;""",
            (account_type,),
        )
        intr_start = self.db.fetchone()[0]
        ins = intr_start.split(" ")
        time = ins[1].lower().replace("(s)", "")

        if time == "year":
            time = 52.143 * int(ins[0])
        elif time == "month":
            time = 4.345 * int(ins[0])
        interest_start = py_date + timedelta(weeks=time)

        if not py_date < today:
            deposit_interval = IntervalTrigger(
                seconds=1,
                start_date=interest_start.strftime("%Y-%m-%d %H:%M:%S"),
            )
            self.params["qtsched"].add_job(
                self.interest_schedule,
                trigger=deposit_interval,
                args=[
                    user_id,
                    last_deposit_id,
                ],
                id=f"dep_{last_deposit_id} interest schedule",
                replace_existing=True,
            )
        else:
            num_days = today - py_date
            self.db.execute(
                """SELECT account_type FROM users WHERE id=?;""", (user_id,)
            )
            account_type = self.db.fetchone()[0]
            self.db.execute(
                """SELECT interest_rate FROM settings WHERE account_type=? ORDER BY id DESC LIMIT 1;""",
                (account_type,),
            )
            interest_rate = self.db.fetchone()[0]
            interest_rate_per_day = float(interest_rate) / 100 / 365

            interest_per_num_days = (
                float(interest_rate_per_day) * float(num_days.days) * float(amount)
            )

            self.db.execute(
                """SELECT id FROM deposit_interest WHERE deposit_id=? AND user_id=? ORDER BY id DESC LIMIT 1;""",
                (
                    last_deposit_id,
                    user_id,
                ),
            )
            dep_intr_id = self.db.fetchone()[0]

            self.db.execute(
                f"""UPDATE deposit_interest SET
                    amount=?,
                    interest=?,
                    date_interest_start=?,
                    date_last_interest=?,
                    run_time=? WHERE id=? AND deposit_id=? AND user_id=?;""",
                (
                    amount,
                    round(interest_per_num_days),
                    interest_start,
                    today,
                    num_days.days,
                    dep_intr_id,
                    last_deposit_id,
                    user_id,
                ),
            )

            self.db.execute(
                """SELECT interest_earned, total
                    FROM savings WHERE user_id=?;""",
                (user_id,),
            )
            sav_intr = self.db.fetchone()

            intr_earned = sav_intr[0]
            total = sav_intr[1]

            intr_earned += round(interest_per_num_days)
            total += round(interest_per_num_days)

            self.db.execute(
                """UPDATE savings SET
                    interest_earned=?,
                    total=?,
                    date_updated=? WHERE user_id=?;""",
                (
                    round(intr_earned),
                    round(total),
                    datetime.today().now().strftime("%Y-%m-%d %H:%M:%S"),
                    user_id,
                ),
            )
            self.params["db"].conn.commit()

            tomorrow = today + timedelta(days=1)
            deposit_interval = IntervalTrigger(
                days=1,
                start_date=tomorrow.strftime("%Y-%m-%d %H:%M:%S"),
            )

            self.params["qtsched"].add_job(
                self.interest_schedule,
                trigger=deposit_interval,
                args=[
                    user_id,
                    last_deposit_id,
                ],
                id=f"dep_{last_deposit_id} interest schedule",
                replace_existing=True,
            )

    def _clear(self):
        self.hide()

    def _get_data_db(self):
        self.db.execute("""SELECT * FROM users;""")
        accounts = []
        for user in self.db.fetchall():
            accounts.append(f"{user[3]} {user[1]}")
        return accounts

    @staticmethod
    def interest_schedule(user_id, deposit_id):
        conn = sqlite3.connect(db_file)

        db = conn.cursor()
        db.execute("""SELECT account_type, status FROM users WHERE id=?;""", (user_id,))
        account = db.fetchone()
        account_type = account[0]
        status = account[1]

        if status == "active":
            db.execute(
                """SELECT * FROM deposit_interest WHERE deposit_id=? AND user_id=?;""",
                (deposit_id, user_id),
            )
            deposit_interest = db.fetchone()

            if not deposit_interest is None:
                run_time = deposit_interest[6]
                run_time += 1
                date_added = deposit_interest[3]
                date_elapsed = datetime.strptime(
                    date_added, "%Y-%m-%d"
                ).date() + timedelta(days=run_time)
                amount = deposit_interest[1]

                db.execute(
                    """SELECT interest_rate FROM settings WHERE account_type=? ORDER BY id DESC LIMIT 1;""",
                    (account_type,),
                )
                interest_rate = db.fetchone()[0]
                interest_rate_per_day = float(interest_rate) / 100 / 365

                interest_per_day = float(deposit_interest[2])
                cal = 0
                db.execute(
                    """SELECT interest_earned, total FROM savings WHERE user_id=?;""",
                    (user_id,),
                )
                sav_intr = db.fetchone()
                intr_earned = sav_intr[0]
                total = sav_intr[1]

                if interest_per_day == 0.0:
                    db.execute(
                        """SELECT interest_start FROM settings WHERE account_type=? ORDER BY id DESC LIMIT 1;""",
                        (account_type,),
                    )
                    intr_start = db.fetchone()[0]
                    ins = intr_start.split(" ")
                    time = ins[1].lower().replace("(s)", "")

                    if time == "year":
                        time = 365 * int(ins[0])
                    elif time == "month":
                        time = 30.417 * int(ins[0])

                    _months = time
                    _months_interest = _months * interest_rate_per_day * float(amount)

                    interest_per_day += _months_interest

                    db.execute(
                        """UPDATE deposit_interest SET
                            interest=?,
                            date_interest_start=?,
                            date_last_interest=?,
                            run_time=? WHERE deposit_id=? AND user_id=?;
                        """,
                        (
                            round(interest_per_day),
                            date_elapsed.strftime("%Y-%m-%d"),
                            date_elapsed.strftime("%Y-%m-%d"),
                            run_time,
                            deposit_id,
                            user_id,
                        ),
                    )
                    intr_earned += round(interest_per_day)
                    total += round(interest_per_day)
                else:
                    cal = float(amount) * float(interest_rate_per_day)
                    interest_per_day += cal

                    db.execute(
                        """UPDATE deposit_interest SET
                            interest=?,
                            date_last_interest=?,
                            run_time=? WHERE deposit_id=? AND user_id=?;""",
                        (
                            round(interest_per_day),
                            date_elapsed.strftime("%Y-%m-%d"),
                            run_time,
                            deposit_id,
                            user_id,
                        ),
                    )

                    intr_earned += round(cal)
                    total += round(cal)

                db.execute(
                    """UPDATE savings SET
                        interest_earned=?,
                        total=?,
                        date_updated=? WHERE user_id=?;""",
                    (
                        round(intr_earned),
                        round(total),
                        date_elapsed.strftime("%Y-%m-%d %H:%M:%S"),
                        user_id,
                    ),
                )

                conn.commit()
                db.close()
