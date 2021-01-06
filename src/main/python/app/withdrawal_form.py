from app import Worker
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from datetime import datetime


class WITHDRAWAL_FORM(QWidget):
    def __init__(self, params):
        super().__init__()
        self.params = params
        self.threadpool = QThreadPool()

        self.db = self.params["db"].conn.cursor()
        self.db.execute("""SELECT * FROM users;""")

        self.accounts = []
        for user in self.db.fetchall():
            self.accounts.append(f"{user[3]} {user[1]}")
        self.view()

    def view(self):
        initial_layout = QVBoxLayout()
        initial_layout.setContentsMargins(0, 0, 0, 0)
        label = QLabel("Withdrawal Form")
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

        group_1 = QGroupBox("Withdraw")
        group_1_layout = QGridLayout()
        group_1.setLayout(group_1_layout)
        group_1.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        group_1_layout.addWidget(QLabel("Date:"), 0, 0)
        self.date = QDateEdit(calendarPopup=True)
        self.date.setDate(QDate.currentDate())
        self.date.setDisabled(True)
        self.date.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        group_1_layout.addWidget(self.date, 0, 1)

        group_1_layout.addWidget(QLabel("Amount:"), 1, 0)
        self.withdraw_amt = QLineEdit()
        self.withdraw_amt.setValidator(QRegExpValidator(QRegExp("^[0-9]{1,},*")))
        self.withdraw_amt.setDisabled(True)
        self.withdraw_amt.setClearButtonEnabled(True)
        group_1_layout.addWidget(self.withdraw_amt, 1, 1)

        self.withdraw_amt.textChanged.connect(self._calc)

        self.useInterest = QCheckBox("Withdraw only Interest")
        self.useInterest.setObjectName("Loan")
        self.useInterest.toggled.connect(self._handle_useIntr)
        self.useInterest.setDisabled(True)
        group_1_layout.addWidget(self.useInterest, 2, 0, 1, 0)

        group_2 = QGroupBox("Account")
        group_2_layout = QGridLayout()
        group_2.setLayout(group_2_layout)
        group_2.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        group_2_hlay = QHBoxLayout()

        group_2_hlay.addWidget(QLabel("Fullname:"))
        self.fun = QLabel("-")
        self.fun.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        group_2_hlay.addWidget(self.fun, alignment=Qt.AlignRight)

        group_2_layout.addLayout(group_2_hlay, 0, 0, 1, 0)

        child_grid_1 = QGridLayout()
        child_grid_2 = QGridLayout()

        child_grid_1.addWidget(QLabel("Balance:"), 0, 0)
        self.bal = QLabel("-")
        self.bal.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        child_grid_1.addWidget(self.bal, 0, 1, alignment=Qt.AlignRight)

        child_grid_1.addWidget(QLabel("Interest Earned:"), 1, 0)
        self.intr = QLabel("-")
        self.intr.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        child_grid_1.addWidget(self.intr, 1, 1, alignment=Qt.AlignRight)

        child_grid_1.addWidget(QLabel("Last Withdrawal:"), 2, 0)
        self.wit = QLabel("-")
        self.wit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        child_grid_1.addWidget(self.wit, 2, 1, alignment=Qt.AlignRight)

        child_grid_1.addWidget(QLabel("Account Status:"), 3, 0)
        self.acc_stat = QLabel("-")
        self.acc_stat.setObjectName("Loan")
        self.acc_stat.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        child_grid_1.addWidget(self.acc_stat, 3, 1, alignment=Qt.AlignRight)

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

        group_2_layout.addLayout(child_grid_1, 1, 0)
        group_2_layout.addLayout(child_grid_2, 1, 1)

        group_3 = QGroupBox("Guarantee(s)")
        group_3_layout = QGridLayout()
        group_3.setLayout(group_3_layout)
        group_3.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        view = self._create_table()

        group_3_layout.addWidget(view)

        main_widget_layout.addWidget(group_1, 1, 0, alignment=Qt.AlignTop)
        main_widget_layout.addWidget(group_2, 1, 1)
        main_widget_layout.addWidget(group_3, 2, 0, 1, 0)

        btn_layout = QHBoxLayout()
        cancel_btn = QPushButton("Cancel")
        self.save_btn = QPushButton("Withdraw")
        cancel_btn.setFixedHeight(35)
        self.save_btn.setFixedHeight(35)
        self.save_btn.setDisabled(True)

        cancel_btn.clicked.connect(self.params["parent"]["self"]._back)
        self.save_btn.clicked.connect(self._check_save)

        btn_layout.addWidget(cancel_btn)
        btn_layout.addWidget(self.save_btn)

        initial_layout.addLayout(btn_layout)

    def _create_table(self):
        table_view = QTableView()
        self.model = WITHDRAWFORMTABLE(data=None)
        table_view.setModel(self.model)
        table_view.setSortingEnabled(True)
        table_view.setSelectionMode(QAbstractItemView.SingleSelection)
        table_view.setSelectionBehavior(QAbstractItemView.SelectRows)
        table_view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        table_view.horizontalHeader().setMinimumSectionSize(140)
        table_view.horizontalHeader().setStretchLastSection(True)
        table_view.verticalHeader().setMinimumWidth(30)
        table_view.verticalHeader().setDefaultAlignment(Qt.AlignCenter)

        return table_view

    def _handle_main_combo_change(self, choice):
        if not choice == "" and not choice.lower() == "no account registered":
            try:
                name = choice.split(" ")
                self.user = self._get_data_db(name)

                self.fun.setText(self.user["fullname"])
                self.bal.setText(self.user["balance"])
                self.intr.setText(self.user["interest"])
                self.wit.setText(self.user["last_withdraw"])
                self.acc_stat.setText(self.user["status"])
                self.loan.setText(self.user["outstanding_loan"]["amount"])
                self.cleared_amt.setText(
                    self.user["outstanding_loan"]["cleared_amount"]
                )
                self.curLia.setText(self.user["outstanding_loan"]["current_liability"])
                self.loan_stat.setText(self.user["outstanding_loan"]["status"])

                guarantees = self._get_guarantee(self.user)

                if self.user["status"].lower() == "active":
                    self.date.setDisabled(False)
                    self.withdraw_amt.setDisabled(False)
                    self.useInterest.setDisabled(False)
                    self.save_btn.setDisabled(False)
                    self.acc_stat.setStyleSheet("""color: green;""")
                else:
                    self.date.setDisabled(True)
                    self.withdraw_amt.setDisabled(True)
                    self.useInterest.setDisabled(True)
                    self.save_btn.setDisabled(True)
                    self.acc_stat.setStyleSheet("""color: red;""")
                    self._check_eligibility(guarantees)

                if self.user["outstanding_loan"]["status"].lower() == "cleared":
                    self.loan_stat.setStyleSheet("""color: green;""")
                elif (
                    self.user["outstanding_loan"]["status"].lower() == "pending"
                    or self.user["outstanding_loan"]["status"].lower() == "not cleared"
                ):
                    self.loan_stat.setStyleSheet("""color: red;""")

                worker = Worker(
                    self.execute_this_fn, guarantees
                )  # Any other args, kwargs are passed to the run function
                worker.signals.result.connect(self.model.update_item)
                # Execute
                self.threadpool.start(worker)
            except Exception:
                pass

    def _check_eligibility(self, guarantees):
        msg = QMessageBox()
        msg.setStyleSheet(open(self.params["ctx"].get_resource("css/style.css")).read())
        msg.setWindowTitle("Info")
        msg.setIconPixmap(QPixmap(self.params["ctx"].get_resource("icon/error.png")))

        gura_list = []
        if not guarantees[0][0] == "ERROR":
            for guarantee in guarantees:
                dur = guarantee[7].split(" ")
                time = dur[1].lower().replace("(s)", "")
                if time == "month":
                    time = 4 * int(dur[0])
                    due_date = datetime.today().date() + timedelta(weeks=time)
                elif time == "week":
                    time = int(dur[0])
                    due_date = datetime.today().date() + timedelta(weeks=time)
                elif time == "day":
                    time = int(dur[0])
                    due_date = datetime.today().date() + timedelta(days=time)

                today = datetime.today().date()
                if (
                    guarantee[6].lower() == "pending"
                    and today > due_date
                    or guarantee[6].lower() == "not cleared"
                    and today > due_date
                ):
                    gura_list.append(guarantee[0])
        if len(gura_list) > 0:
            msg.setText("Account Frozen")
            msg.setDetailedText(
                "This account has been frozen and therefore cannot make withdrawal due to one or more guarantee(s) not clearing up loans before due date."
            )
        else:
            msg.setText("Account Frozen")
            msg.setDetailedText(
                "This account has been frozen and therefore cannot make withdrawal due to not clearing up loans before due date."
            )
        msg.setDefaultButton(QMessageBox.Ok)
        msg.exec_()

    def _check_save(self):
        details = f"""The details are as follows:
        Account: {self.fun.text()}
        Amount: {self.withdraw_amt.text()}
        Date: {self.date.date().toPyDate().strftime("%Y-%m-%d")}"""

        msg = QMessageBox()
        msg.setStyleSheet(open(self.params["ctx"].get_resource("css/style.css")).read())
        msg.setIconPixmap(QPixmap(self.params["ctx"].get_resource("icon/question.png")))
        msg.setText(
            f"Are you sure you want to withdraw \u20A6{self.withdraw_amt.text()} for {self.fun.text()}?"
        )
        msg.setWindowTitle("Withdraw")
        msg.setDetailedText(details)
        msg.setStandardButtons(QMessageBox.No | QMessageBox.Yes)
        msg.setDefaultButton(QMessageBox.Yes)
        msg.buttonClicked.connect(self._confirm_save)
        msg.exec_()
        msg.show()

    def _confirm_save(self, i):
        if i.text() == "&Yes":
            name = self.fun.text()
            msg = QMessageBox()
            msg.setStyleSheet(
                open(self.params["ctx"].get_resource("css/style.css")).read()
            )
            msg.setWindowTitle("Account Withdrawal")
            amt = self.withdraw_amt.text()
            amt = amt.replace(",", "")
            try:
                self.db.execute(
                    """SELECT balance,interest_earned,total FROM savings WHERE user_id=?""",
                    (self.user["id"],),
                )
                savings = self.db.fetchone()
                date = self.date.date().toPyDate().strftime("%Y-%m-%d")
                savings_date = datetime.strptime(date, "%Y-%m-%d").strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
                if not self.useInterest.isChecked():
                    if float(savings[0]) >= float(amt):
                        bal = float(savings[0]) - float(amt)
                        total = float(savings[2]) - float(amt)
                        self.db.execute(
                            """UPDATE savings SET
                                balance=?,
                                total=?,
                                date_updated=? WHERE user_id=?;""",
                            (
                                bal,
                                total,
                                savings_date,
                                self.user["id"],
                            ),
                        )
                        self.db.execute(
                            """INSERT INTO withdrawals (
                                amount,
                                withdrawn_from,
                                date,
                                user_id) VALUES (?,?,?,?)""",
                            (
                                float(amt),
                                "balance",
                                date,
                                self.user["id"],
                            ),
                        )
                        self.alter_dep_intr(user_id=self.user["id"], amount=amt)
                        self.params["db"].conn.commit()
                        msg.setIconPixmap(
                            QPixmap(self.params["ctx"].get_resource("icon/success.png"))
                        )
                        msg.setText(f"Withdrawal successfully recorded")
                        msg.buttonClicked.connect(self._clear_all)
                    else:
                        msg.setIconPixmap(
                            QPixmap(self.params["ctx"].get_resource("icon/error.png"))
                        )
                        msg.setText(f"Insufficient Balance")
                else:
                    if float(savings[1]) >= float(amt):
                        intr = float(savings[1]) - float(amt)
                        total = float(savings[2]) - float(amt)
                        self.db.execute(
                            """UPDATE savings SET
                                interest_earned=?,
                                total=?,
                                date_updated=? WHERE user_id=?;""",
                            (
                                intr,
                                total,
                                savings_date,
                                self.user["id"],
                            ),
                        )
                        self.db.execute(
                            """INSERT INTO withdrawals (
                                amount,
                                withdrawn_from,
                                date,
                                user_id) VALUES (?,?,?,?)""",
                            (
                                float(amt),
                                "interest",
                                date,
                                self.user["id"],
                            ),
                        )
                        self.params["db"].conn.commit()
                        msg.setIconPixmap(
                            QPixmap(self.params["ctx"].get_resource("icon/success.png"))
                        )
                        msg.setText(f"Withdrawal successfully recorded")
                        msg.buttonClicked.connect(self._clear_all)
                    else:
                        msg.setIconPixmap(
                            QPixmap(self.params["ctx"].get_resource("icon/error.png"))
                        )
                        msg.setText(f"Insufficient Balance for Interest")
            except Exception as e:
                msg.setIconPixmap(
                    QPixmap(self.params["ctx"].get_resource("icon/error.png"))
                )
                msg.setText(f"Error!\nPlease check the form again")
            msg.setDefaultButton(QMessageBox.Ok)
            msg.exec_()
            msg.show()

    def _clear_all(self):
        self.params["parent"]["back_btn"].click()

    def _calc(self, number):
        self.new_bal, self.new_intr = None, None
        if not number == "":
            number = number.replace(",", "")
            self.withdraw_amt.setText("{:,}".format(int(number)))

            old_bal = self.user["balance"].replace("\u20A6", "").replace(",", "")
            old_intr = self.user["interest"].replace("\u20A6", "").replace(",", "")

            if self.useInterest.isChecked():
                if float(old_intr) >= float(number):
                    self.new_intr = float(old_intr) - float(number)
                    self.intr.setText("\u20A6 {:,}".format(int(self.new_intr)))
                else:
                    self.withdraw_amt.setText(old_intr)
            else:
                if float(old_bal) >= float(number):
                    self.new_bal = float(old_bal) - float(number)
                    self.bal.setText("\u20A6 {:,}".format(int(self.new_bal)))
                else:
                    self.withdraw_amt.setText(old_bal)
        else:
            self.bal.setText(self.user["balance"])
            self.intr.setText(self.user["interest"])

    def _handle_useIntr(self, state):
        number = self.withdraw_amt.text().replace(",", "")
        old_bal = self.user["balance"].replace("\u20A6 ", "").replace(",", "")
        old_intr = self.user["interest"].replace("\u20A6 ", "").replace(",", "")
        if not number == "":
            if state:
                self.bal.setText(self.user["balance"])
                if float(old_intr) >= float(number):
                    self.new_intr = float(old_intr) - float(number)
                    self.intr.setText("\u20A6 {:,}".format(int(self.new_intr)))
                else:
                    self.withdraw_amt.setText(old_intr)
            else:
                self.intr.setText(self.user["interest"])
                if float(old_bal) >= float(number):
                    self.new_bal = float(old_bal) - float(number)
                    self.bal.setText("\u20A6 {:,}".format(int(self.new_bal)))
                else:
                    self.withdraw_amt.setText(old_bal)
        else:
            self.withdraw_amt.setText(old_intr)

    def _get_data_db(self, selected):
        if not selected[0] == "":
            self.db.execute(
                """SELECT * FROM users WHERE last_name=? AND first_name=?;""",
                (selected[0], selected[1]),
            )
            user = self.db.fetchone()
            account = {
                "id": user[0],
                "fullname": f"{user[3]} {user[1]}",
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

            account["balance"] = (
                "\u20A6 {:,}".format(int(savings[1])) if savings else "\u20A6 0.0"
            )
            account["interest"] = (
                "\u20A6 {:,}".format(int(savings[2])) if savings else "\u20A6 0.0"
            )
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

            account["last_withdraw"] = (
                "\u20A6 {:,}".format(int(withdrawals[1]))
                if not withdrawals is None
                else "-"
            )

            return account
        else:
            return None

    def _get_guarantee(self, data):
        name = self.user["fullname"]
        accounts = []
        self.db.execute(
            """SELECT * FROM loans
                WHERE guarantor_one=? 
                OR guarantor_two=?;""",
            (name, name),
        )
        guarantees = self.db.fetchall()
        if len(guarantees) > 0:
            user = []
            for item in guarantees:
                self.db.execute(
                    """SELECT first_name,last_name FROM users WHERE id=?;""",
                    (item[10],),
                )
                name = self.db.fetchone()
                user.append(f"{name[1]} {name[0]}")
                user.append(item[1])
                user.append(item[2])
                user.append(item[3])
                user.append(item[4])
                user.append(item[5])
                user.append(item[6].capitalize())
                user.append(item[7])
                user.append(datetime.strptime(item[8], "%Y-%m-%d"))
                user.append(datetime.strptime(item[9], "%Y-%m-%d"))
            accounts.append(user)
        if len(accounts) == 0:
            accounts = [["ERROR", "No Guarantee(s)"]]
        return accounts

    def execute_this_fn(self, accounts, result):
        return accounts

    def alter_dep_intr(self, user_id, amount):
        self.db.execute(
            """SELECT amount, deposit_id, date_added FROM deposit_interest WHERE user_id=? ORDER BY id DESC;""",
            (user_id,),
        )
        deposit_interest = self.db.fetchall()
        final = 0
        _lst = []
        for item in deposit_interest:
            final += float(item[0])
            if final >= float(amount):
                _lst.append(item[1])
                _lst.append(final)
                _lst.append(item[2])
                break
            self.db.execute(
                """DELETE FROM apscheduler_jobs WHERE apscheduler_jobs.id=?;""",
                (f"dep_{item[1]} interest schedule",),
            )
            self.db.execute(
                """INSERT INTO deleted (
                    deleted_amount,
                    deleted_date,
                    date,
                    user_id) VALUES (?,?,?,?,?);""",
                (
                    item[0],
                    item[2],
                    datetime.today().date(),
                    user_id,
                ),
            )
            self.db.execute(
                """DELETE FROM deposit_interest WHERE deposit_id=?;""", (item[1],)
            )

        new_amt = float(_lst[1]) - float(amount)
        if not new_amt == 0.0:
            self.db.execute(
                """UPDATE deposit_interest SET
                    amount=? WHERE deposit_id=?;""",
                (new_amt, _lst[0]),
            )
            self.db.execute(
                """INSERT INTO deleted (
                deleted_id,
                deleted_amount,
                deleted_date,
                date,
                user_id) VALUES (?,?,?,?,?);""",
                (
                    _lst[0],
                    amount,
                    _lst[2],
                    datetime.today().date(),
                    user_id,
                ),
            )
        else:
            self.db.execute(
                """DELETE FROM apscheduler_jobs WHERE apscheduler_jobs.id=?;""",
                (f"dep_{_lst[0]} interest schedule",),
            )
            self.db.execute(
                """INSERT INTO deleted (
                deleted_id,
                deleted_amount,
                deleted_date,
                date,
                user_id) VALUES (?,?,?,?,?);""",
                (
                    _lst[0],
                    _lst[1],
                    _lst[2],
                    datetime.today().date(),
                    user_id,
                ),
            )
            self.db.execute(
                """DELETE FROM deposit_interest WHERE deposit_id=?;""", (_lst[0],)
            )
        self.params["db"].conn.commit()


class WITHDRAWFORMTABLE(QAbstractTableModel):
    def __init__(self, data):
        super(WITHDRAWFORMTABLE, self).__init__()
        self._data = data

    @pyqtSlot(list)
    def update_item(self, value):
        try:
            if self._data[0][0] == "ERROR":
                ix = self.index(len(value), 1)
        except Exception:
            pass
        ix = self.index(len(value), 10)
        self.setData(ix, value, Qt.DisplayRole)

    def setData(self, index, value, role):
        if role == Qt.DisplayRole:
            self._data = value
            self.layoutAboutToBeChanged.emit()
            self.dataChanged.emit(index, index)
            self.layoutChanged.emit()
            return True
        return False

    def data(self, index, role):
        if not self._data is None:
            value = (
                self._data[index.row()][index.column()]
                if not self._data[0][0] == "ERROR"
                else self._data[0][1]
            )
            if role == Qt.DisplayRole:
                if isinstance(value, datetime):
                    return value.strftime("%B %d, %Y")
                if isinstance(value, float):
                    return "\u20A6 {:,}".format(float(value))
                return value
            if role == Qt.TextAlignmentRole:
                if (
                    isinstance(value, float)
                    or isinstance(value, datetime)
                    or index.column() == 6
                ):
                    return Qt.AlignCenter
            if role == Qt.ForegroundRole:
                if index.column() == 4:
                    return QColor("green")
                if index.column() == 5:
                    return QColor("red")

    def headerData(self, section, orientation, role):
        if orientation == Qt.Horizontal:
            if role == Qt.DisplayRole:
                header = [
                    "Name",
                    "Amount Loaned",
                    "First Guarantor",
                    "Second Guarantor",
                    "Cleared Amount",
                    "Current Liability",
                    "Loan Status",
                    "Loan Duration",
                    "Loan Due Date",
                    "Date Requested",
                ]
                try:
                    if self._data[0][0] == "ERROR":
                        return "Data"
                except Exception:
                    pass
                return header[section]
        if orientation == Qt.Vertical:
            if not self._data[0][0] == "ERROR":
                if role == Qt.TextAlignmentRole:
                    return Qt.AlignCenter
                return section + 1

    def sort(self, column, order):
        if not self._data is None:
            self.layoutAboutToBeChanged.emit()
            self._data.sort(reverse=order)
            self.layoutChanged.emit()

    def rowCount(self, index):
        if self._data is None:
            return -1
        return len(self._data)

    def columnCount(self, index):
        try:
            if self._data[0][0] == "ERROR":
                return 1
        except Exception:
            pass
        try:
            return len(self._data[0])
        except Exception:
            return 10

    def flags(self, index):
        return super(QAbstractTableModel, self).flags(index) | Qt.ItemIsUserCheckable
