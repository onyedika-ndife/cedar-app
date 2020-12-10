import sqlite3
from datetime import datetime, timedelta
from PyQt5.QtGui import QIcon, QColor, QRegExpValidator
from PyQt5.QtWidgets import (
    QVBoxLayout,
    QWidget,
    QPushButton,
    QGroupBox,
    QHBoxLayout,
    QSizePolicy,
    QAction,
    QStackedWidget,
    QToolBar,
    QLabel,
    QHeaderView,
    QTableView,
    QLineEdit,
    QScrollArea,
    QGridLayout,
    QDateEdit,
    QComboBox,
    QTabWidget,
    QDialog,
    QCompleter,
    QMessageBox,
)
from PyQt5.QtCore import Qt, QRegExp

from .ldw_list_user import USER_LDW


class DEPOSIT_FORM(QDialog):
    def __init__(self, params):
        super().__init__()
        self.params = params
        self.db = self.params["db"].conn.cursor()

        self.accounts = self._get_data_db()

        self.setStyleSheet(open("./assets/css/style.css").read())
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
        self.amt_int.textChanged.connect(self._calc)
        initial_layout.addWidget(amt_lbl, 1, 0)
        initial_layout.addWidget(self.amt_int, 1, 1)
        amt_lbl.setObjectName("DW")

        date_lbl = QLabel("Date:")
        date = QLabel(str(datetime.today().date().strftime("%B %d, %Y")))
        initial_layout.addWidget(date_lbl, 2, 0)
        initial_layout.addWidget(date, 2, 1, alignment=Qt.AlignRight)
        date.setObjectName("DW")
        date_lbl.setObjectName("DW")

        btn_layout = QHBoxLayout()
        btn_layout.setContentsMargins(0, 0, 0, 0)

        save_btn = QPushButton("Save")
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
        details = f"""The details are as follows:
                
                Account: {self.combo_box.currentText()}
                Amount: {self.amt_int.text()}
                Date: {datetime.today().now().strftime("%Y-%m-%d %H:%M:%S")}"""
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Question)
        msg.setText(
            f"Are you sure you want to record {self.combo_box.currentText()}'s deposit?"
        )
        msg.setWindowTitle(f"Account Deposit")
        msg.setDetailedText(details)
        msg.setStandardButtons(QMessageBox.No | QMessageBox.Yes)
        msg.setDefaultButton(QMessageBox.Yes)
        msg.buttonClicked.connect(self._handle_dw_save)
        msg.exec_()

    def _handle_dw_save(self, choice):
        if choice.text() == "&Yes":
            user = self.combo_box.currentText().split(" ")
            amt = self.amt_int.text()
            amt = amt.replace(",", "")
            self.db.execute(
                """SELECT id FROM users WHERE first_name=? AND middle_name=? AND last_name=?;""",
                (user[2], user[1], user[0]),
            )
            user_id = self.db.fetchone()[0]
            msg = QMessageBox()
            msg.setWindowTitle(f"Account Deposit")
            try:
                self.db.execute(
                    """SELECT balance,total FROM savings WHERE user_id=?""",
                    (user_id,),
                )
                savings = self.db.fetchone()
                bal = float(savings[0]) + float(amt)
                total = float(savings[1]) + float(amt)
                self.db.execute(
                    """UPDATE savings SET
                            balance=?,
                            total=?,
                            date_updated=? WHERE user_id=?""",
                    (
                        bal,
                        total,
                        datetime.today().now().strftime("%Y-%m-%d %H:%M:%S"),
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
                        datetime.today().now().strftime("%Y-%m-%d %H:%M:%S"),
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
                        datetime.today().now().strftime("%Y-%m-%d %H:%M:%S"),
                        last_deposit_id,
                        user_id,
                    ),
                )
                self.params["db"].conn.commit()

                interest_start = datetime.today().now() + timedelta(weeks=13.036)

                self.params["qtsched"].add_job(
                    self.interest_schedule,
                    "interval",
                    args=[
                        user_id,
                        last_deposit_id,
                    ],
                    id=f"deposit_{last_deposit_id} interest schedule",
                    days=1,
                    start_date=interest_start.strftime("%Y-%m-%d %H:%M:%S"),
                    replace_existing=True,
                )
                msg.setIcon(QMessageBox.Information)
                msg.setText(f"Deposit successfully recorded")
                msg.buttonClicked.connect(self._clear)
            except Exception as e:
                print(e)
                msg.setIcon(QMessageBox.Critical)
                msg.setText(f"Error!\nPlease check the form again")

            msg.setDefaultButton(QMessageBox.Ok)
            msg.exec_()
            msg.show()

    def _calc(self, number):
        if not number == "":
            number = number.replace(",", "")
            new_numb = "{:,}".format(int(number))
            self.amt_int.setText(new_numb)

    def _clear(self):
        self.combo_box.clear()
        self.combo_box.addItems(self.accounts)
        self.amt_int.clear()

    def _get_data_db(self):
        self.db.execute("""SELECT * FROM users;""")
        accounts = []
        for user in self.db.fetchall():
            accounts.append(f"{user[3]} {user[2]} {user[1]}")
        return accounts

    @staticmethod
    def interest_schedule(user_id, deposit_id):
        conn = sqlite3.connect("./db.sqlite3")
        db = conn.cursor()
        db.execute("""SELECT account_type FROM users WHERE id=?;""", (user_id,))
        account_type = db.fetchone()[0]

        db.execute(
            """SELECT * FROM deposit_interest WHERE deposit_id=? AND user_id=?;""",
            (deposit_id, user_id),
        )
        deposit_interest = db.fetchone()

        if not deposit_interest is None:
            amount = deposit_interest[1]

            db.execute(
                """SELECT interest_rate FROM settings WHERE account_type=? ORDER BY id DESC LIMIT 1;""",
                (account_type,),
            )
            interest_rate = db.fetchone()[0]
            interest_rate_per_day = float(interest_rate) / 100 / 365

            interest_per_day = float(deposit_interest[2])

            if interest_per_day == 0.0:
                _3_months = 91.25
                _3_months_interest = _3_months * interest_rate_per_day * amount

                interest_per_day += _3_months_interest
            else:
                interest_per_day += float(amount) * float(interest_rate_per_day)

            if deposit_interest[4] == "":
                db.execute(
                    """UPDATE deposit_interest SET
                        interest=?,
                        date_interest_start=?,
                        date_last_interest=?,
                        WHERE deposit_id=?AND user_id=?;
                    """,
                    (
                        interest_per_day,
                        datetime.today().now().strftime("%Y-%m-%d %H:%M:%S"),
                        datetime.today().now().strftime("%Y-%m-%d %H:%M:%S"),
                        deposit_id,
                        user_id,
                    ),
                )

            db.execute(
                """UPDATE deposit_interest SET
                    interest=?,
                    date_last_interest=?
                    WHERE deposit_id=? AND user_id=?;
                """,
                (
                    interest_per_day,
                    datetime.today().now().strftime("%Y-%m-%d %H:%M:%S"),
                    deposit_id,
                    user_id,
                ),
            )

            db.execute(
                """SELECT interest FROM deposit_interest WHERE user_id=?;""", (user_id,)
            )
            dep_intr = db.fetchall()
            db.execute(
                """SELECT interest_earned, total FROM savings WHERE user_id=?;""",
                (user_id,),
            )
            sav_intr = db.fetchone()
            interest_earned = 0
            for interest in dep_intr:
                interest_earned += interest[0]
            sav_intr[0] += interest_earned
            sav_intr[1] += interest_earned
            db.execute(
                """UPDATE savings SET
                    interest_earned=?,
                    total=?,
                    date_updated=? WHERE user_id=?;""",
                (
                    sav_intr[0],
                    sav_intr[1],
                    datetime.today().now().strftime("%Y-%m-%d %H:%M:%S"),
                    user_id,
                ),
            )
            conn.commit()
            db.close()
