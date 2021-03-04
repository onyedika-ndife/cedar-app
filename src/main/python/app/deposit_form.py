from datetime import datetime

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from app import functions


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
        name = self.combo_box.currentText()
        self.db.execute(
            """SELECT account_type FROM users WHERE name=?;""",
            (name,),
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
            user = self.combo_box.currentText()
            amt = self.amt_int.text()
            amt = amt.replace(",", "")
            self.db.execute(
                """SELECT id, status FROM users WHERE name=?;""",
                (user,),
            )
            data = self.db.fetchone()
            user_id = data[0]
            user_status = data[1]
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

                functions.check_sched_deposit(
                    self.params,
                    user_id,
                    user_status,
                    acc_type,
                    last_deposit_id,
                    amt,
                    date,
                )

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

    def _clear(self):
        self.hide()

    def _get_data_db(self):
        self.db.execute("""SELECT * FROM users;""")
        accounts = []
        for user in self.db.fetchall():
            accounts.append(user[3])
        return accounts
