import sqlite3
from datetime import datetime, timedelta

from apscheduler.triggers.interval import IntervalTrigger
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from app import db_file


class LOAN_FORM(QWidget):
    def __init__(self, params):
        super().__init__()
        self.params = params

        self.db = self.params["db"].conn.cursor()
        self.db.execute("""SELECT * FROM users;""")

        self.accounts = []
        for user in self.db.fetchall():
            self.accounts.append(user[3])
        self.view()

    def view(self):
        initial_layout = QVBoxLayout()
        initial_layout.setContentsMargins(0, 0, 0, 0)
        label = QLabel("Loan Issuance Form")
        label.setFixedHeight(30)
        label.setObjectName("Header")

        initial_layout.addWidget(label)

        self.setLayout(initial_layout)

        scrollArea = QScrollArea()
        main_widget = QWidget()
        main_widget_layout = QGridLayout()
        main_widget.setLayout(main_widget_layout)

        scrollArea.setWidget(main_widget)
        scrollArea.setWidgetResizable(True)
        initial_layout.addWidget(scrollArea)

        accCombo = QLineEdit()
        self.accCombo = QComboBox()
        self.accCombo.setEditable(True)
        if len(self.accounts) > 0:
            self.accCombo.addItems(self.accounts)
            self.accCombo_comp = QCompleter(self.accounts)
            self.accCombo.setCompleter(self.accCombo_comp)
            self.accCombo_comp.setCompletionMode(QCompleter.PopupCompletion)
            self.accCombo_comp.setCaseSensitivity(Qt.CaseInsensitive)
            self.accCombo_comp.setFilterMode(Qt.MatchContains)
            self.accCombo.currentTextChanged.connect(self._handle_main_combo_change)
        else:
            self.accCombo.addItems(["No Account Registered"])
        self.accCombo.lineEdit().setPlaceholderText("--Select Account--")
        self.accCombo.setCurrentIndex(-1)
        self.accCombo.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        main_widget_layout.addWidget(self.accCombo, 0, 0, 1, 0)

        group_1 = QGroupBox("Account")
        group_1_layout = QGridLayout()
        group_1.setLayout(group_1_layout)
        group_1.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        group_1_hlay = QHBoxLayout()

        group_1_hlay.addWidget(QLabel("Fullname:"))
        self.fun = QLabel("-")
        self.fun.setObjectName("Loan")
        self.fun.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        group_1_hlay.addWidget(self.fun, alignment=Qt.AlignRight)

        group_1_layout.addLayout(group_1_hlay, 0, 0, 1, 0)

        child_grid_1 = QGridLayout()
        child_grid_2 = QGridLayout()

        child_grid_1.addWidget(QLabel("Balance:"), 0, 0)
        self.bal = QLabel("-")
        self.bal.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        child_grid_1.addWidget(self.bal, 0, 1, alignment=Qt.AlignRight)

        child_grid_1.addWidget(QLabel("Last Deposit:"), 1, 0)
        self.dep = QLabel("-")
        self.dep.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        child_grid_1.addWidget(self.dep, 1, 1, alignment=Qt.AlignRight)

        child_grid_1.addWidget(QLabel("Last Withdrawal:"), 2, 0)
        self.wit = QLabel("-")
        self.wit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        child_grid_1.addWidget(self.wit, 2, 1, alignment=Qt.AlignRight)

        child_grid_2.addWidget(QLabel("Last Loan:"), 0, 0)
        self.loan = QLabel("-")
        self.loan.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        child_grid_2.addWidget(self.loan, 0, 1, alignment=Qt.AlignRight)

        child_grid_2.addWidget(QLabel("Cleared Amount:"), 1, 0)
        self.cleared_amt = QLabel("-")
        self.cleared_amt.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        child_grid_2.addWidget(self.cleared_amt, 1, 1, alignment=Qt.AlignRight)

        child_grid_2.addWidget(QLabel("Current Liability:"), 2, 0)
        self.curLia = QLabel("-")
        self.curLia.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        child_grid_2.addWidget(self.curLia, 2, 1, alignment=Qt.AlignRight)

        child_grid_2.addWidget(QLabel("Loan Status:"), 3, 0)
        self.loan_stat = QLabel("-")
        self.loan_stat.setObjectName("Loan")
        self.loan_stat.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        child_grid_2.addWidget(self.loan_stat, 3, 1, alignment=Qt.AlignRight)

        group_1_layout.addLayout(child_grid_1, 1, 0)
        group_1_layout.addLayout(child_grid_2, 1, 1)

        group_2 = QGroupBox("Loan")
        group_2_layout = QGridLayout()
        group_2.setLayout(group_2_layout)
        group_2.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        group_2_layout.addWidget(QLabel("Date:"), 0, 0)
        self.date = QDateEdit(calendarPopup=True)
        self.date.setDate(QDate.currentDate())
        self.date.setDisabled(True)
        self.date.dateChanged.connect(self._handle_date_change)
        self.date.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        group_2_layout.addWidget(self.date, 0, 1)

        group_2_layout.addWidget(QLabel("Amount:"), 1, 0)
        self.loan_amt = QLineEdit()
        self.loan_amt.setValidator(QRegExpValidator(QRegExp("^[0-9]{1,},*")))
        self.loan_amt.setDisabled(True)
        self.loan_amt.setClearButtonEnabled(True)
        group_2_layout.addWidget(self.loan_amt, 1, 1)

        self.loan_amt.textChanged.connect(self._calc)

        group_2_layout.addWidget(QLabel("Loan Duration:"), 2, 0)

        self.loan_period = QLabel("-")

        group_2_layout.addWidget(self.loan_period, 2, 1, alignment=Qt.AlignRight)

        group_2_layout.addWidget(QLabel("Due Date:"), 3, 0)
        self.loan_due_date = QLabel("-")
        group_2_layout.addWidget(self.loan_due_date, 3, 1, alignment=Qt.AlignRight)

        group_3 = QGroupBox("(1) Guarantor")
        group_3_layout = QGridLayout()
        group_3.setLayout(group_3_layout)
        group_3.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        child_grid_1 = QGridLayout()

        child_grid_1.addWidget(QLabel("Account:"), 0, 0)

        self.guar_1_combo = QComboBox()
        self.guar_1_combo.setEditable(True)
        self.guar_1_combo.lineEdit().setPlaceholderText("--Select First Guarantor--")
        self.guar_1_combo.setCurrentIndex(-1)
        self.guar_1_combo.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.guar_1_combo.setDisabled(True)

        child_grid_1.addWidget(self.guar_1_combo, 0, 1)

        child_grid_1.addWidget(QLabel("Fullname:"), 1, 0)
        self.guarantor_1_fn = QLabel("-")
        self.guarantor_1_fn.setObjectName("Loan")
        self.guarantor_1_fn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        child_grid_1.addWidget(self.guarantor_1_fn, 1, 1, alignment=Qt.AlignRight)

        group_3_layout.addLayout(child_grid_1, 0, 0, 1, 0)

        child_grid_1 = QGridLayout()
        child_grid_2 = QGridLayout()

        child_grid_1.addWidget(QLabel("Balance:"), 0, 0)
        self.guarantor_1_bal = QLabel("-")
        self.guarantor_1_bal.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        child_grid_1.addWidget(self.guarantor_1_bal, 0, 1, alignment=Qt.AlignRight)

        child_grid_1.addWidget(QLabel("Last Deposit:"), 1, 0)
        self.guarantor_1_dep = QLabel("-")
        self.guarantor_1_dep.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        child_grid_1.addWidget(self.guarantor_1_dep, 1, 1, alignment=Qt.AlignRight)

        child_grid_1.addWidget(QLabel("Last Withdrawal:"), 2, 0)
        self.guarantor_1_wit = QLabel("-")
        self.guarantor_1_wit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        child_grid_1.addWidget(self.guarantor_1_wit, 2, 1, alignment=Qt.AlignRight)

        child_grid_2.addWidget(QLabel("Last Loan:"), 0, 0)
        self.guarantor_1_loan = QLabel("-")
        self.guarantor_1_loan.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        child_grid_2.addWidget(self.guarantor_1_loan, 0, 1, alignment=Qt.AlignRight)

        child_grid_2.addWidget(QLabel("Cleared Amount:"), 1, 0)
        self.guarantor_1_cleared_amt = QLabel("-")
        self.guarantor_1_cleared_amt.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Fixed
        )
        child_grid_2.addWidget(
            self.guarantor_1_cleared_amt, 1, 1, alignment=Qt.AlignRight
        )

        child_grid_2.addWidget(QLabel("Current Liability:"), 2, 0)
        self.guarantor_1_curLia = QLabel("-")
        self.guarantor_1_curLia.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        child_grid_2.addWidget(self.guarantor_1_curLia, 2, 1, alignment=Qt.AlignRight)

        child_grid_2.addWidget(QLabel("Loan Status:"), 3, 0)
        self.guarantor_1_loan_stat = QLabel("-")
        self.guarantor_1_loan_stat.setObjectName("Loan")
        self.guarantor_1_loan_stat.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Fixed
        )
        child_grid_2.addWidget(
            self.guarantor_1_loan_stat, 3, 1, alignment=Qt.AlignRight
        )

        group_3_layout.addLayout(child_grid_1, 1, 0)
        group_3_layout.addLayout(child_grid_2, 1, 1)

        group_4 = QGroupBox("(2) Guarantor")
        group_4_layout = QGridLayout()
        group_4.setLayout(group_4_layout)
        group_4.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        child_grid_1 = QGridLayout()

        child_grid_1.addWidget(QLabel("Account:"), 0, 0)

        self.guar_2_combo = QComboBox()
        self.guar_2_combo.setEditable(True)
        self.guar_2_combo.lineEdit().setPlaceholderText("--Select Second Guarantor--")
        self.guar_2_combo.setCurrentIndex(-1)
        self.guar_2_combo.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.guar_2_combo.setDisabled(True)

        child_grid_1.addWidget(self.guar_2_combo, 0, 1)

        child_grid_1.addWidget(QLabel("Fullname:"), 1, 0)
        self.guarantor_2_fn = QLabel("-")
        self.guarantor_2_fn.setObjectName("Loan")
        self.guarantor_2_fn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        child_grid_1.addWidget(self.guarantor_2_fn, 1, 1, alignment=Qt.AlignRight)

        group_4_layout.addLayout(child_grid_1, 0, 0, 1, 0)

        child_grid_1 = QGridLayout()
        child_grid_2 = QGridLayout()

        child_grid_1.addWidget(QLabel("Balance:"), 0, 0)
        self.guarantor_2_bal = QLabel("-")
        self.guarantor_2_bal.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        child_grid_1.addWidget(self.guarantor_2_bal, 0, 1, alignment=Qt.AlignRight)

        child_grid_1.addWidget(QLabel("Last Deposit:"), 1, 0)
        self.guarantor_2_dep = QLabel("-")
        self.guarantor_2_dep.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        child_grid_1.addWidget(self.guarantor_2_dep, 1, 1, alignment=Qt.AlignRight)

        child_grid_1.addWidget(QLabel("Last Withdrawal:"), 2, 0)
        self.guarantor_2_wit = QLabel("-")
        self.guarantor_2_wit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        child_grid_1.addWidget(self.guarantor_2_wit, 2, 1, alignment=Qt.AlignRight)

        child_grid_2.addWidget(QLabel("Last Loan:"), 0, 0)
        self.guarantor_2_loan = QLabel("-")
        self.guarantor_2_loan.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        child_grid_2.addWidget(self.guarantor_2_loan, 0, 1, alignment=Qt.AlignRight)

        child_grid_2.addWidget(QLabel("Cleared Amount:"), 1, 0)
        self.guarantor_2_cleared_amt = QLabel("-")
        self.guarantor_2_cleared_amt.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Fixed
        )
        child_grid_2.addWidget(
            self.guarantor_2_cleared_amt, 1, 1, alignment=Qt.AlignRight
        )

        child_grid_2.addWidget(QLabel("Current Liability:"), 2, 0)
        self.guarantor_2_curLia = QLabel("-")
        self.guarantor_2_curLia.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        child_grid_2.addWidget(self.guarantor_2_curLia, 2, 1, alignment=Qt.AlignRight)

        child_grid_2.addWidget(QLabel("Loan Status:"), 3, 0)
        self.guarantor_2_loan_stat = QLabel("-")
        self.guarantor_2_loan_stat.setObjectName("Loan")
        self.guarantor_2_loan_stat.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Fixed
        )
        child_grid_2.addWidget(
            self.guarantor_2_loan_stat, 3, 1, alignment=Qt.AlignRight
        )

        group_4_layout.addLayout(child_grid_1, 1, 0)
        group_4_layout.addLayout(child_grid_2, 1, 1)

        main_widget_layout.addWidget(group_2, 1, 0, alignment=Qt.AlignTop)
        main_widget_layout.addWidget(group_1, 1, 1)
        main_widget_layout.addWidget(group_3, 2, 0, alignment=Qt.AlignTop)
        main_widget_layout.addWidget(group_4, 2, 1, alignment=Qt.AlignTop)

        btn_layout = QHBoxLayout()
        cancel_btn = QPushButton("Cancel")
        self.save_btn = QPushButton("Issue Loan")
        cancel_btn.setFixedHeight(35)
        self.save_btn.setFixedHeight(35)
        self.save_btn.setDisabled(True)

        cancel_btn.clicked.connect(self.params["parent"]["self"]._back)
        self.save_btn.clicked.connect(self._check_save)

        btn_layout.addWidget(cancel_btn)
        btn_layout.addWidget(self.save_btn)

        initial_layout.addLayout(btn_layout)

    def _handle_main_combo_change(self, choice):
        if not choice == "":
            if not choice.lower() == "no account registered":
                chosen = []
                self.g1_lst = []
                try:
                    name = choice
                    data = self._get_data_db(name)
                    if not data is None:
                        self.fun.setText(data["fullname"])
                        self.bal.setText("\u20A6 {:,}".format(int(data["balance"])))
                        self.dep.setText(data["last_deposit"])
                        self.wit.setText(data["last_withdraw"])
                        self.loan.setText(data["outstanding_loan"]["amount"])
                        self.cleared_amt.setText(
                            data["outstanding_loan"]["cleared_amount"]
                        )
                        self.curLia.setText(
                            data["outstanding_loan"]["current_liability"]
                        )
                        self.loan_stat.setText(data["outstanding_loan"]["status"])

                        chosen.append(choice)
                        for item in self.accounts:
                            if not item == chosen[0]:
                                self.g1_lst.append(item)

                        if data["outstanding_loan"]["status"].lower() == "cleared":
                            self.loan_stat.setStyleSheet("""color: green;""")
                        elif data["outstanding_loan"]["status"].lower() == "pending":
                            self.loan_stat.setStyleSheet("""color: blue;""")
                        else:
                            self.loan_stat.setStyleSheet("""color: red;""")

                        if (
                            data["status"].lower() == "active"
                            and not int(data["balance"]) == 0
                            and (
                                data["outstanding_loan"]["status"].lower() == "cleared"
                                or data["outstanding_loan"]["status"].lower() == "-"
                            )
                        ):
                            self.date.setDisabled(False)
                            self.loan_amt.setDisabled(False)
                            self.loan_period.setDisabled(False)
                            self.guar_1_combo.addItems(self.g1_lst)
                            self.guar_1_combo.setCurrentIndex(-1)
                            self.guar_1_combo.setDisabled(False)

                            self.guar_1_combo_comp = QCompleter(self.g1_lst)
                            self.guar_1_combo.setCompleter(self.guar_1_combo_comp)
                            self.guar_1_combo_comp.setCompletionMode(
                                QCompleter.PopupCompletion
                            )
                            self.guar_1_combo_comp.setCaseSensitivity(
                                Qt.CaseInsensitive
                            )
                            self.guar_1_combo_comp.setFilterMode(Qt.MatchContains)
                            self.guar_1_combo.currentTextChanged.connect(
                                self._handle_one_combo_change
                            )

                            self.db.execute(
                                """SELECT * FROM settings WHERE account_type=?;""",
                                (data["account_type"],),
                            )
                            self.set_data = self.db.fetchone()
                            self.loan_period.setText(self.set_data[4])

                            dur = self.set_data[4].split(" ")
                            time = dur[1].lower().replace("(s)", "")

                            if time == "year":
                                time = 52.143 * int(dur[0])
                            elif time == "month":
                                time = 4.345 * int(dur[0])
                            due_date = self.date.date().toPyDate() + timedelta(
                                weeks=time
                            )

                            self.loan_due_date.setText(
                                str(due_date.strftime("%b %d, %Y"))
                            )
                            self.due_date = due_date.strftime("%Y-%m-%d")
                        else:
                            msg = QMessageBox()
                            msg.setStyleSheet(
                                open(
                                    self.params["ctx"].get_resource("css/style.css")
                                ).read()
                            )
                            msg.setIconPixmap(
                                QPixmap(
                                    self.params["ctx"].get_resource("icon/error.png")
                                )
                            )
                            msg.setWindowTitle("Error")
                            msg.setText("This account is illegible to request loans.")
                            msg.setDefaultButton(QMessageBox.Ok)
                            msg.exec_()
                            msg.show()
                except Exception as e:
                    pass

    def _handle_one_combo_change(self, i):
        if not i == "":
            chosen = []
            self.g2_lst = []
            try:
                name = i
                data = self._get_data_db(name)

                self.guarantor_1_fn.setText(data["fullname"])
                self.guarantor_1_bal.setText("\u20A6 {:,}".format(int(data["balance"])))
                self.guarantor_1_dep.setText(data["last_deposit"])
                self.guarantor_1_wit.setText(data["last_withdraw"])
                self.guarantor_1_loan.setText(data["outstanding_loan"]["amount"])
                self.guarantor_1_cleared_amt.setText(
                    data["outstanding_loan"]["cleared_amount"]
                )
                self.guarantor_1_curLia.setText(
                    data["outstanding_loan"]["current_liability"]
                )
                self.guarantor_1_loan_stat.setText(data["outstanding_loan"]["status"])

                chosen.append(i)
                for item in self.g1_lst:
                    if not item == chosen[0]:
                        self.g2_lst.append(item)

                if data["outstanding_loan"]["status"] == "Cleared":
                    self.guarantor_1_loan_stat.setStyleSheet("""color: green;""")
                elif data["outstanding_loan"]["status"] == "Pending":
                    self.guarantor_1_loan_stat.setStyleSheet("""color: blue;""")
                else:
                    self.guarantor_1_loan_stat.setStyleSheet("""color: red;""")

                if (
                    data["status"].lower() == "active"
                    and not int(data["balance"]) == 0
                    and (
                        data["outstanding_loan"]["status"].lower() == "cleared"
                        or data["outstanding_loan"]["status"].lower() == "-"
                    )
                ):
                    if self.guar_2_combo.count() > 0:
                        self.guar_2_combo.clear()
                    self.guar_2_combo.addItems(self.g2_lst)
                    self.guar_2_combo.setCurrentIndex(-1)
                    self.guar_2_combo.setDisabled(False)

                    self.guar_2_combo_comp = QCompleter(self.g2_lst)
                    self.guar_2_combo.setCompleter(self.guar_2_combo_comp)
                    self.guar_2_combo_comp.setCompletionMode(QCompleter.PopupCompletion)
                    self.guar_2_combo_comp.setCaseSensitivity(Qt.CaseInsensitive)
                    self.guar_2_combo_comp.setFilterMode(Qt.MatchContains)
                    self.guar_2_combo.currentTextChanged.connect(
                        self._handle_two_combo_change
                    )
                else:
                    msg = QMessageBox()
                    msg.setStyleSheet(
                        open(self.params["ctx"].get_resource("css/style.css")).read()
                    )
                    msg.setIconPixmap(
                        QPixmap(self.params["ctx"].get_resource("icon/error.png"))
                    )
                    msg.setWindowTitle("Error")
                    msg.setText("This account is illegible to be a guarantor.")
                    msg.setDefaultButton(QMessageBox.Ok)
                    msg.exec_()
            except Exception:
                pass

    def _handle_two_combo_change(self, i):
        if not i == "":
            try:
                name = i
                data = self._get_data_db(name)
                self.guarantor_2_fn.setText(data["fullname"])
                self.guarantor_2_bal.setText("\u20A6 {:,}".format(int(data["balance"])))
                self.guarantor_2_dep.setText(data["last_deposit"])
                self.guarantor_2_wit.setText(data["last_withdraw"])
                self.guarantor_2_loan.setText(data["outstanding_loan"]["amount"])
                self.guarantor_2_cleared_amt.setText(
                    data["outstanding_loan"]["cleared_amount"]
                )
                self.guarantor_2_curLia.setText(
                    data["outstanding_loan"]["current_liability"]
                )
                self.guarantor_2_loan_stat.setText(data["outstanding_loan"]["status"])

                if data["outstanding_loan"]["status"] == "Cleared":
                    self.guarantor_2_loan_stat.setStyleSheet("""color: green;""")
                elif data["outstanding_loan"]["status"] == "Pending":
                    self.guarantor_2_loan_stat.setStyleSheet("""color: blue;""")
                else:
                    self.guarantor_2_loan_stat.setStyleSheet("""color: red;""")

                if (
                    data["status"].lower() == "active"
                    and not int(data["balance"]) == 0
                    and (
                        data["outstanding_loan"]["status"].lower() == "cleared"
                        or data["outstanding_loan"]["status"].lower() == "-"
                    )
                ):
                    self.save_btn.setDisabled(False)
                else:
                    msg = QMessageBox()
                    msg.setStyleSheet(
                        open(self.params["ctx"].get_resource("css/style.css")).read()
                    )
                    msg.setIconPixmap(
                        QPixmap(self.params["ctx"].get_resource("icon/error.png"))
                    )
                    msg.setWindowTitle("Error")
                    msg.setText("This account is illegible to be a guarantor.")
                    msg.setDefaultButton(QMessageBox.Ok)
                    msg.exec_()
            except Exception:
                pass

    def _handle_date_change(self):

        dur = self.set_data[4].split(" ")
        time = dur[1].lower().replace("(s)", "")

        if time == "year":
            time = 52.143 * int(dur[0])
        elif time == "month":
            time = 4.345 * int(dur[0])
        due_date = self.date.date().toPyDate() + timedelta(weeks=time)

        self.loan_due_date.setText(str(due_date.strftime("%b %d, %Y")))
        self.due_date = due_date.strftime("%Y-%m-%d")

    def _check_save(self):
        name = self.fun.text()
        self.db.execute(
            """SELECT account_type FROM users WHERE name=?;""",
            (name,),
        )
        acc_type = self.db.fetchone()[0]
        self.db.execute("""SELECT * FROM settings WHERE account_type=?;""", (acc_type,))
        sett = self.db.fetchone()
        if not sett is None:
            details = f"""The details are as follows:
            Account: {self.fun.text()}
            Loan Amount: {self.loan_amt.text()}
            First Guarantor: {self.guarantor_1_fn.text()}
            Second Guarantor: {self.guarantor_2_fn.text()}
            Loan Period: {self.loan_period.text()}
            Due Date: {self.loan_due_date.text()}"""

            msg = QMessageBox()
            msg.setStyleSheet(
                open(self.params["ctx"].get_resource("css/style.css")).read()
            )
            msg.setIconPixmap(
                QPixmap(self.params["ctx"].get_resource("icon/question.png"))
            )
            msg.setText(
                f"Are you sure you want to issue loan of \u20A6{self.loan_amt.text()} to {self.fun.text()}?"
            )
            msg.setWindowTitle("Loan Issuance")
            msg.setDetailedText(details)
            msg.setStandardButtons(QMessageBox.No | QMessageBox.Yes)
            msg.setDefaultButton(QMessageBox.Yes)
            msg.buttonClicked.connect(self._confirm_save)
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
            self.params["parent"]["setting_btn"].click()

    def _confirm_save(self, i):
        if i.text() == "&Yes":
            name = self.fun.text()
            data = self._get_data_db(name)
            msg = QMessageBox()
            msg.setStyleSheet(
                open(self.params["ctx"].get_resource("css/style.css")).read()
            )
            msg.setWindowTitle("Loan Issuance")
            amt = self.loan_amt.text()
            amt = amt.replace(",", "")
            try:
                self.db.execute(
                    """INSERT INTO loans (
                        amount,
                        guarantor_one,
                        guarantor_two,
                        current_liability,
                        loan_period,
                        loan_due_date,
                        date_issued,
                        user_id) VALUES (?,?,?,?,?,?,?,?)""",
                    (
                        float(amt),
                        self.guarantor_1_fn.text(),
                        self.guarantor_2_fn.text(),
                        float(amt),
                        self.loan_period.text(),
                        self.due_date,
                        self.date.date().toPyDate().strftime("%Y-%m-%d"),
                        data["id"],
                    ),
                )
                self.params["db"].conn.commit()
                msg.setIconPixmap(
                    QPixmap(self.params["ctx"].get_resource("icon/success.png"))
                )
                msg.setText(f"Loan Issuance Successful")
                msg.buttonClicked.connect(self._clear_all)

                self._check_shed(
                    data["id"], name, self.date.date().toPyDate(), self.due_date
                )

            except Exception as e:
                msg.setIconPixmap(
                    QPixmap(self.params["ctx"].get_resource("icon/error.png"))
                )
                msg.setText(f"Error creating account, please check the form again")
            msg.setDefaultButton(QMessageBox.Ok)
            msg.exec_()

    def _check_shed(self, user_id, name, start_date, end_date):
        self.db.execute(
            """SELECT id FROM loans WHERE user_id=? ORDER BY id DESC LIMIT 1;""",
            (user_id,),
        )
        loan_id = self.db.fetchone()[0]
        today = datetime.today().date()

        if not start_date < today:
            loan_interval = IntervalTrigger(
                weeks=4.345,
                start_date=start_date,
                end_date=datetime.strptime(end_date, "%Y-%m-%d").date(),
            )
            self.params["qtsched"].add_job(
                self.loan_schedule,
                trigger=loan_interval,
                args=[
                    user_id,
                    loan_id,
                ],
                id=f"{name} loan schedule",
                replace_existing=True,
            )
        else:
            num_mon = today - start_date
            num_mon = num_mon.days / 30.417
            num_mon = round(num_mon)
            self.db.execute(
                """SELECT account_type, status FROM users WHERE id=?;""", (user_id,)
            )
            account = self.db.fetchone()
            self.db.execute(
                """SELECT loan_rate FROM settings WHERE account_type=? ORDER BY id DESC LIMIT 1;""",
                (account[0],),
            )
            loan_rate = self.db.fetchone()[0]

            self.db.execute(
                """SELECT * FROM loans
                    WHERE id=? AND user_id=?;""",
                (
                    loan_id,
                    user_id,
                ),
            )
            loan = self.db.fetchone()

            if not loan is None:
                amount = loan[1]
                old_curr_lia = loan[5]

                due_date = datetime.strptime(loan[8], "%Y-%m-%d").date()
                date_issued = datetime.strptime(loan[9], "%Y-%m-%d").date()
                run_time = due_date - date_issued
                run_time = run_time.days / 30.417

                interest_per_month = (
                    float(amount) * int(loan_rate) / 100 * round(run_time)
                )
                new_curr_lia = float(old_curr_lia) + float(interest_per_month)

                self.db.execute(
                    """UPDATE loans SET
                        current_liability=?, run_time=?
                        WHERE id=? AND user_id=?;""",
                    (
                        new_curr_lia,
                        round(run_time),
                        loan_id,
                        user_id,
                    ),
                )

                self.db.execute(
                    """UPDATE users SET
                        status=? WHERE id=?""",
                    ("inactive", user_id),
                )

                self.params["db"].conn.commit()

    def _clear_all(self):
        self.params["parent"]["back_btn"].click()

    def _calc(self, number):
        if not number == "":
            number = number.replace(",", "")
            new_numb = "{:,}".format(int(number))
            self.loan_amt.setText(new_numb)

    def _get_data_db(self, selected):
        if not selected.lower() == "no account registered":
            self.db.execute(
                """SELECT * FROM users WHERE name=?;""",
                (selected,),
            )
            user = self.db.fetchone()
            account = {
                "id": user[0],
                "fullname": user[3],
                "account_type": user[7],
                "status": user[8],
            }

            self.db.execute(
                """SELECT * FROM savings WHERE user_id=?;""",
                (account["id"],),
            )
            savings = self.db.fetchone()

            self.db.execute(
                """SELECT * FROM loans WHERE user_id=? ORDER BY id DESC LIMIT 1;""",
                (account["id"],),
            )
            loans = self.db.fetchone()

            self.db.execute(
                """SELECT * FROM deposits WHERE user_id=? ORDER BY id DESC LIMIT 1;""",
                (account["id"],),
            )
            deposits = self.db.fetchone()

            self.db.execute(
                """SELECT * FROM withdrawals WHERE user_id=? ORDER BY id DESC LIMIT 1;""",
                (account["id"],),
            )
            withdrawals = self.db.fetchone()

            account["balance"] = savings[3] if savings else 0.0
            account["outstanding_loan"] = {
                "amount": "\u20A6 {:,}".format(int(loans[1]))
                if not loans is None
                else "-",
                "cleared_amount": "\u20A6 {:,}".format(int(loans[4]))
                if not loans is None
                else "-",
                "current_liability": "\u20A6 {:,}".format(int(loans[5]))
                if not loans is None
                else "-",
                "status": loans[6].capitalize() if not loans is None else "-",
            }
            account["last_deposit"] = (
                "\u20A6 {:,}".format(int(deposits[1])) if deposits else "-"
            )
            account["last_withdraw"] = (
                "\u20A6 {:,}".format(int(withdrawals[1])) if withdrawals else "-"
            )

            return account
        else:
            return None

    @staticmethod
    def loan_schedule(user_id, loan_id):
        conn = sqlite3.connect(db_file)
        db = conn.cursor()

        db.execute("""SELECT account_type, status FROM users WHERE id=?;""", (user_id,))
        account = db.fetchone()
        db.execute(
            """SELECT loan_rate FROM settings WHERE account_type=? ORDER BY id DESC LIMIT 1;""",
            (account[0],),
        )
        loan_rate = db.fetchone()[0]

        db.execute(
            """SELECT * FROM loans
                WHERE id=? AND user_id=?;""",
            (
                loan_id,
                user_id,
            ),
        )
        loan = db.fetchone()

        if not loan is None:
            amount = loan[1]
            old_curr_lia = loan[5]
            loan_period = loan[7].split(" ")
            time = loan_period[1].lower().replace("(s)", "")

            if time == "year":
                time = 52.143 * int(loan_period[0])
            elif time == "month":
                time = 4.345 * int(loan_period[0])

            time = timedelta(weeks=time).days

            due_date = datetime.strptime(loan[8], "%Y-%m-%d").date()
            date_issued = datetime.strptime(loan[9], "%Y-%m-%d").date()
            run_time = loan[10]
            run_time += 1
            run_time_days = run_time * 30.417

            days_elapsed = date_issued + timedelta(days=run_time_days)

            interest_per_month = float(amount) * int(loan_rate) / 100
            new_curr_lia = float(old_curr_lia) + float(interest_per_month)

            if days_elapsed.days == time:
                db.execute(
                    """UPDATE users SET
                        status=? WHERE id=?""",
                    ("inactive", user_id),
                )

            db.execute(
                """UPDATE loans SET
                    current_liability=?, run_time=? WHERE id=? AND user_id=?;""",
                (
                    new_curr_lia,
                    round(run_time),
                    loan_id,
                    user_id,
                ),
            )
            conn.commit()
            db.close()
