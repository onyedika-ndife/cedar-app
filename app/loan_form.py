import sqlite3
from datetime import datetime, timedelta
from PyQt5.QtGui import QIcon, QRegExpValidator
from PyQt5.QtWidgets import (
    QVBoxLayout,
    QWidget,
    QLineEdit,
    QPushButton,
    QGroupBox,
    QHBoxLayout,
    QSizePolicy,
    QAction,
    QMainWindow,
    QStackedWidget,
    QGridLayout,
    QLabel,
    QTextEdit,
    QCalendarWidget,
    QRadioButton,
    QScrollArea,
    QMessageBox,
    QComboBox,
    QCompleter,
)
from PyQt5.QtCore import Qt, QSize, QDate, QRegExp


class LOAN_FORM(QWidget):
    def __init__(self, params):
        super().__init__()
        self.params = params

        self.db = self.params["db"].conn.cursor()
        self.db.execute("""SELECT * FROM users;""")

        self.accounts = []
        for user in self.db.fetchall():
            self.accounts.append(f"{user[3]} {user[2]} {user[1]}")
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
            # self.accCombo_comp.activated.connect(
            #     lambda text: self._handle_main_combo_change(text, "completer")
            # )
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
        group_1.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        group_1_hlay = QHBoxLayout()

        group_1_hlay.addWidget(QLabel("Fullname:"))
        self.fun = QLabel("-")
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
        group_2.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        group_2_layout.addWidget(QLabel("Date:"), 0, 0)
        self.date = QLabel(str(datetime.today().date().strftime("%B %d, %Y")))
        self.date.setObjectName("Loan")
        group_2_layout.addWidget(self.date, 0, 1, alignment=Qt.AlignRight)

        group_2_layout.addWidget(QLabel("Amount:"), 1, 0)
        self.loan_amt = QLineEdit()
        self.loan_amt.setValidator(QRegExpValidator(QRegExp("^[0-9]{1,},*")))
        # QRegExpValidator(QRegExp("^[1-9]{1,3}(,[0-9]{3})*$"))
        self.loan_amt.setDisabled(True)
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
        group_3.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        child_grid_1 = QGridLayout()

        child_grid_1.addWidget(QLabel("Account:"), 0, 0)

        self.guar_1_combo = QComboBox()
        self.guar_1_combo.setEditable(True)
        self.guar_1_combo.lineEdit().setPlaceholderText("--Select First Guarantor--")
        self.guar_1_combo.setCurrentIndex(-1)
        self.guar_1_combo.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.guar_1_combo.setDisabled(True)

        child_grid_1.addWidget(self.guar_1_combo, 0, 1)

        child_grid_1.addWidget(QLabel("Full Name:"), 1, 0)
        self.guarantor_1_fn = QLabel("-")
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
        group_4.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        child_grid_1 = QGridLayout()

        child_grid_1.addWidget(QLabel("Account:"), 0, 0)

        self.guar_2_combo = QComboBox()
        self.guar_2_combo.setEditable(True)
        self.guar_2_combo.lineEdit().setPlaceholderText("--Select Second Guarantor--")
        self.guar_2_combo.setCurrentIndex(-1)
        self.guar_2_combo.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.guar_2_combo.setDisabled(True)

        child_grid_1.addWidget(self.guar_2_combo, 0, 1)

        child_grid_1.addWidget(QLabel("Full Name:"), 1, 0)
        self.guarantor_2_fn = QLabel("-")
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

        main_widget_layout.addWidget(group_2, 1, 0)
        main_widget_layout.addWidget(group_1, 1, 1)
        main_widget_layout.addWidget(group_3, 2, 0)
        main_widget_layout.addWidget(group_4, 2, 1)

        btn_layout = QHBoxLayout()
        cancel_btn = QPushButton("Cancel")
        self.save_btn = QPushButton("Save")
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
                    name = choice.split(" ")
                    data = self._get_data_db(name)
                    if not data is None:
                        self.fun.setText(data["fullname"])
                        self.bal.setText("\u20A6{:,}".format(int(data["balance"])))
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

                        if data["outstanding_loan"]["status"] == "Cleared":
                            self.loan_stat.setStyleSheet("""color: green;""")
                        elif data["outstanding_loan"]["status"] == "Pending":
                            self.loan_stat.setStyleSheet("""color: blue;""")
                        else:
                            self.loan_stat.setStyleSheet("""color: red;""")

                        if (
                            data["status"].lower() == "active"
                            and not int(data["balance"]) == 0
                        ):
                            self.loan_amt.setDisabled(False)
                            self.loan_period.setDisabled(False)
                            if self.guar_1_combo.count() > 0:
                                self.guar_1_combo.clear()
                            self.guar_1_combo.addItems(self.g1_lst)
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
                            self.guar_1_combo_comp.activated.connect(
                                self._handle_one_combo_change
                            )
                            self.guar_1_combo.textActivated.connect(
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
                            due_date = datetime.today().date() + timedelta(weeks=time)

                            self.loan_due_date.setText(
                                str(due_date.strftime("%b %d, %Y"))
                            )
                            self.due_date = due_date.strftime("%Y-%m-%d")
                        else:
                            msg = QMessageBox()
                            msg.setIcon(QMessageBox.Critical)
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
                name = i.split(" ")
                data = self._get_data_db(name)

                self.guarantor_1_fn.setText(data["fullname"])
                self.guarantor_1_bal.setText("\u20A6{:,}".format(int(data["balance"])))
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

                if data["status"].lower() == "active" and not int(data["balance"]) == 0:
                    if self.guar_2_combo.count() > 0:
                        self.guar_2_combo.clear()
                    self.guar_2_combo.addItems(self.g2_lst)
                    self.guar_2_combo.setDisabled(False)

                    self.guar_2_combo_comp = QCompleter(self.g2_lst)
                    self.guar_2_combo.setCompleter(self.guar_2_combo_comp)
                    self.guar_2_combo_comp.setCompletionMode(QCompleter.PopupCompletion)
                    self.guar_2_combo_comp.setCaseSensitivity(Qt.CaseInsensitive)
                    self.guar_2_combo_comp.setFilterMode(Qt.MatchContains)
                    self.guar_2_combo_comp.activated.connect(
                        self._handle_two_combo_change
                    )
                    self.guar_2_combo.textActivated.connect(
                        self._handle_two_combo_change
                    )
                else:
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Critical)
                    msg.setWindowTitle("Error")
                    msg.setText("This account is illegible to be a guarantor.")
                    msg.setDefaultButton(QMessageBox.Ok)
                    msg.exec_()
            except Exception:
                pass

    def _handle_two_combo_change(self, i):
        if not i == "":
            try:
                name = i.split(" ")
                data = self._get_data_db(name)
                self.guarantor_2_fn.setText(data["fullname"])
                self.guarantor_2_bal.setText("\u20A6{:,}".format(int(data["balance"])))
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

                if data["status"].lower() == "active" and not int(data["balance"]) == 0:
                    self.save_btn.setDisabled(False)
                else:
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Critical)
                    msg.setWindowTitle("Error")
                    msg.setText("This account is illegible to be a guarantor.")
                    msg.setDefaultButton(QMessageBox.Ok)
                    msg.exec_()
            except Exception:
                pass

    def _check_save(self):
        details = f"""The details are as follows:
        Account: {self.fun.text()}
        Loan Amount: {self.loan_amt.text()}
        First Guarantor: {self.guarantor_1_fn.text()}
        Second Guarantor: {self.guarantor_2_fn.text()}
        Loan Period: {self.loan_period.text()}
        Due Date: {self.loan_due_date.text()}"""

        msg = QMessageBox()
        msg.setIcon(QMessageBox.Question)
        msg.setText(f"Are you sure you want to issue loan to {self.fun.text()}?")
        msg.setWindowTitle("Loan Issuance")
        msg.setDetailedText(details)
        msg.setStandardButtons(QMessageBox.No | QMessageBox.Yes)
        msg.setDefaultButton(QMessageBox.Yes)
        msg.buttonClicked.connect(self._confirm_save)
        msg.exec_()

    def _confirm_save(self, i):
        if i.text() == "&Yes":
            name = self.fun.text()
            data = self._get_data_db(name.split(" "))
            msg = QMessageBox()
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
                        amt,
                        self.guarantor_1_fn,
                        self.guarantor_2_fn,
                        amt,
                        self.loan_period.text(),
                        self.due_date,
                        datetime.today().now().strftime("%Y-%m-%d %H:%M:%S"),
                        data["id"],
                    ),
                )
                self.db.execute(
                    """UPDATE users SET
                        status=? WHERE id=?""",
                    ("inactive", data["id"]),
                )
                self.params["db"].conn.commit()
                msg.setIcon(QMessageBox.Information)
                msg.setText(f"Loan Issuance Successful")
                msg.buttonClicked.connect(self._clear_all)
                self.params["qtsched"].add_job(
                    self.loan_schedule,
                    "interval",
                    args=[
                        data["id"],
                    ],
                    id=f"{name} loan schedule",
                    weeks=4,
                    start_date=datetime.today().now().strftime("%Y-%m-%d %H:%M:%S"),
                    end_date=datetime.strptime(self.due_date, "%Y-%m-%d").strftime(
                        "%Y-%m-%d %H:%M:%S"
                    ),
                    replace_existing=True,
                )
            except Exception as e:
                print(e)
                msg.setIcon(QMessageBox.Critical)
                msg.setText(f"Error creating account, please check the form again")
            msg.setDefaultButton(QMessageBox.Ok)
            msg.exec_()

    def _clear_all(self):
        self.accCombo.clear()
        self.accCombo.addItems(self.accounts)
        self.fun.setText("-")
        self.bal.setText("-")
        self.dep.setText("-")
        self.wit.setText("-")
        self.loan.setText("-")
        self.cleared_amt.setText("-")
        self.curLia.setText("-")
        self.loan_stat.setText("-")
        self.loan_amt.setDisabled(True)
        self.loan_period.setText("-")
        self.loan_due_date.setText("-")
        self.guar_1_combo.clear()
        self.guar_2_combo.clear()
        self.guar_1_combo.setDisabled(True)
        self.guar_2_combo.setDisabled(True)
        self.guarantor_1_fn.setText("-")
        self.guarantor_1_bal.setText("-")
        self.guarantor_1_dep.setText("-")
        self.guarantor_1_wit.setText("-")
        self.guarantor_1_loan.setText("-")
        self.guarantor_1_cleared_amt.setText("-")
        self.guarantor_1_curLia.setText("-")
        self.guarantor_1_loan_stat.setText("-")
        self.guarantor_2_fn.setText("-")
        self.guarantor_2_bal.setText("-")
        self.guarantor_2_dep.setText("-")
        self.guarantor_2_wit.setText("-")
        self.guarantor_2_loan.setText("-")
        self.guarantor_2_cleared_amt.setText("-")
        self.guarantor_2_curLia.setText("-")
        self.guarantor_2_loan_stat.setText("-")

    def _calc(self, number):
        if not number == "":
            number = number.replace(",", "")
            new_numb = "{:,}".format(int(number))
            self.loan_amt.setText(new_numb)

    def _get_data_db(self, selected):
        if len(selected) == 3:
            self.db.execute(
                """SELECT * FROM users WHERE last_name=? AND middle_name=? AND first_name=?;""",
                (selected[0], selected[1], selected[2]),
            )
            user = self.db.fetchone()
            account = {
                "id": user[0],
                "fullname": f"{user[3]} {user[2]} {user[1]}",
                "account_type": user[8],
                "status": user[9],
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

            account["balance"] = savings[1] if savings else 0.0
            account["outstanding_loan"] = {
                "amount": "\u20A6{:,}".format(int(loans[1]))
                if not loans is None
                else "-",
                "cleared_amount": "\u20A6{:,}".format(int(loans[4]))
                if not loans is None
                else "-",
                "current_liability": "\u20A6{:,}".format(int(loans[5]))
                if not loans is None
                else "-",
                "status": loans[6].capitalize() if not loans is None else "-",
            }
            account["last_deposit"] = (
                "\u20A6{:,}".format(int(deposits[1])) if deposits else "-"
            )
            account["last_withdraw"] = (
                "\u20A6{:,}".format(int(withdrawals[1])) if withdrawals else "-"
            )

            return account
        else:
            return None

    @staticmethod
    def loan_schedule(user_id):
        conn = sqlite3.connect("./db.sqlite3")
        db = conn.cursor()

        db.execute("""SELECT account_type,status FROM users WHERE id=?;""", (user_id,))
        account = db.fetchone()
        db.execute(
            """SELECT loan_rate FROM settings WHERE account_type=? ORDER BY id DESC LIMIT 1;""",
            (account[0],),
        )
        loan_rate = db.fetchone()[0]
        if account[1].lower() == "inactive":
            db.execute(
                """SELECT current_liability FROM loans WHERE user_id=? AND status=? OR user_id=? AND status=? ORDER BY id DESC LIMIT 1;""",
                (
                    user_id,
                    "pending",
                    user_id,
                    "not cleared",
                ),
            )
            old_curr_lia = db.fetchone()[0]
            new_curr_lia = float(old_curr_lia) * int(loan_rate) / 100 + float(
                old_curr_lia
            )
            db.execute(
                """UPDATE loans SET current_liability=? WHERE user_id=? AND status=? OR user_id=? AND status=? ORDER BY id DESC LIMIT 1;""",
                (round(new_curr_lia), user_id, "pending", user_id, "not cleared"),
            )
            conn.commit()
            db.close()
