from datetime import datetime, timedelta
from PyQt5.QtGui import QIcon, QRegExpValidator, QColor
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
    QTableView,
    QHeaderView,
    QCheckBox,
)
from PyQt5.QtCore import (
    Qt,
    QSize,
    QDate,
    QRegExp,
    QAbstractTableModel,
    pyqtSlot,
    pyqtSignal,
    QModelIndex,
    QRunnable,
    QThreadPool,
    QObject,
)


class WITHDRAWAL_FORM(QWidget):
    def __init__(self, params):
        super().__init__()
        self.params = params
        self.threadpool = QThreadPool()

        self.db = self.params["db"].conn.cursor()
        self.db.execute("""SELECT * FROM users;""")

        self.accounts = []
        for user in self.db.fetchall():
            self.accounts.append(f"{user[3]} {user[1]} {user[2]}")
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
        self.date = QLabel(str(datetime.today().date().strftime("%B %d, %Y")))
        self.date.setObjectName("Loan")
        group_1_layout.addWidget(self.date, 0, 1, alignment=Qt.AlignRight)

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

        child_grid_1.addWidget(QLabel("Last Deposit:"), 1, 0)
        self.dep = QLabel("-")
        self.dep.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        child_grid_1.addWidget(self.dep, 1, 1, alignment=Qt.AlignRight)

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
        self.save_btn = QPushButton("Save")
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
        self.model = CustomTableModel(data=None)
        table_view.setModel(self.model)
        table_view.setSortingEnabled(True)
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
                data = self._get_data_db(name)

                self.fun.setText(data["fullname"])
                self.bal.setText("\u20A6{:,}".format(int(data["balance"])))
                self.dep.setText(data["last_deposit"])
                self.wit.setText(data["last_withdraw"])
                self.acc_stat.setText(data["status"])
                self.loan.setText(data["outstanding_loan"]["amount"])
                self.cleared_amt.setText(data["outstanding_loan"]["cleared_amount"])
                self.curLia.setText(data["outstanding_loan"]["current_liability"])
                self.loan_stat.setText(data["outstanding_loan"]["status"])

                guarantees = self._get_guarantee(data)

                if data["status"].lower() == "active":
                    self.withdraw_amt.setDisabled(False)
                    self.useInterest.setDisabled(False)
                    self.save_btn.setDisabled(False)
                    self.acc_stat.setStyleSheet("""color: green;""")
                else:
                    self.acc_stat.setStyleSheet("""color: red;""")
                    self._check_eligibility(guarantees)

                if data["outstanding_loan"]["status"] == "Cleared":
                    self.loan_stat.setStyleSheet("""color: green;""")
                elif (
                    data["outstanding_loan"]["status"] == "Pending"
                    or data["outstanding_loan"]["status"] == "Not Cleared"
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
        msg.setWindowTitle("Info")
        msg.setIcon(QMessageBox.Critical)

        gura_list = []
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
        Date: {datetime.today().date()}"""

        msg = QMessageBox()
        msg.setIcon(QMessageBox.Question)
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
            data = self._get_data_db(name.split(" "))
            msg = QMessageBox()
            msg.setWindowTitle("Account Withdrawal")
            amt = self.withdraw_amt.text()
            amt = amt.replace(",", "")
            try:
                self.db.execute(
                    """SELECT total FROM savings WHERE user_id=?""",
                    (data["id"],),
                )
                savings = self.db.fetchone()[0]
                if float(savings) >= float(amt):
                    bal = float(savings) - float(amt)
                    self.db.execute(
                        """UPDATE savings SET
                            balance=?,
                            date_updated=? WHERE user_id=?;""",
                        (
                            bal,
                            datetime.today().now().strftime("%Y-%m-%d %H:%M:%S"),
                            data["id"],
                        ),
                    )
                    self.db.execute(
                        """INSERT INTO withdrawals (
                            amount,
                            date,
                            user_id) VALUES (?,?,?)""",
                        (
                            amt,
                            datetime.today().now().strftime("%Y-%m-%d %H:%M:%S"),
                            data["id"],
                        ),
                    )
                    self.alter_dep_intr(user_id=data["id"], amount=amt)
                    self.params["db"].conn.commit()
                    msg.setIcon(QMessageBox.Information)
                    msg.setText(f"Withdrawal successfully recorded")
                    msg.buttonClicked.connect(self._clear_all)
                else:
                    msg.setIcon(QMessageBox.Critical)
                    msg.setText(f"Insufficient Balance")
            except Exception as e:
                msg.setIcon(QMessageBox.Critical)
                msg.setText(f"Error!\nPlease check the form again")
            msg.setDefaultButton(QMessageBox.Ok)
            msg.exec_()
            msg.show()

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
        self.withdraw_amt.setDisabled(True)

    def _calc(self, number):
        if not number == "":
            number = number.replace(",", "")
            new_numb = "{:,}".format(int(number))
            self.withdraw_amt.setText(new_numb)

    def _handle_useIntr(self, state):
        if state:
            name = self.fun.text()
            data = self._get_data_db(name.split(" "))
            self.db.execute(
                """SELECT interest_earned FROM savings WHERE user_id=?;""",
                (data["id"],),
            )
            interest_earned = self.db.fetchone()[0]
            interest_earned = "{:,}".format(int(interest_earned))
            self.withdraw_amt.setText(interest_earned)
        else:
            self.withdraw_amt.clear()

    def _get_data_db(self, selected):
        if not selected[0] == "":
            self.db.execute(
                """SELECT * FROM users WHERE last_name=? AND first_name=? AND middle_name=?;""",
                (selected[0], selected[1], selected[2]),
            )
            user = self.db.fetchone()
            account = {
                "id": user[0],
                "fullname": f"{user[3]} {user[1]} {user[2]}",
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
                "\u20A6{:,}".format(int(deposits[1])) if not deposits is None else "-"
            )
            account["last_withdraw"] = (
                "\u20A6{:,}".format(int(withdrawals[1]))
                if not withdrawals is None
                else "-"
            )

            return account
        else:
            return None

    def _get_guarantee(self, data):
        name = data["fullname"]
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
                    """SELECT first_name,middle_name,last_name FROM users WHERE id=?;""",
                    (item[10],),
                )
                name = self.db.fetchone()
                user.append(f"{name[2]} {name[1]} {name[0]}")
                user.append(item[1])
                user.append(item[2])
                user.append(item[3])
                user.append(item[4])
                user.append(item[5])
                user.append(item[6].capitalize())
                user.append(item[7])
                user.append(datetime.strptime(item[8], "%Y-%m-%d"))
                user.append(datetime.strptime(item[9], "%Y-%m-%d %H:%M:%S"))
            accounts.append(user)
        else:
            accounts = [["ERROR", "No Guarantee(s)"]]
        return accounts

    def execute_this_fn(self, accounts, result):
        return accounts

    def alter_dep_intr(self, user_id, amount):
        self.db.execute(
            """SELECT amount, deposit_id FROM deposit_interest WHERE user_id=? ORDER BY id DESC;""",
            (user_id,),
        )
        deposit_interest = self.db.fetchall()
        final = 0
        _lst = []
        for item in deposit_interest:
            final += item[0]
            if final >= float(amount):
                _lst.append(item[1])
                _lst.append(final)
                break
            self.db.execute(
                """DELETE * FROM deposit_interest WHERE deposit_id=?;""", (item[1],)
            )
            self.params["qtsched"].remove_job(
                job_id=f"deposit_{item[1]} interest schedule"
            )
        new_amt = float(_lst[1]) - amount
        if not new_amt == 0.0:
            self.db.execute(
                """UPDATE deposit_interest SET
                    amount=? WHERE deposit_id=?;""",
                (new_amt, _lst[0]),
            )
        else:
            self.db.execute(
                """DELETE * FROM deposit_interest WHERE deposit_id=?;""", (_lst[0],)
            )
            self.params["qtsched"].remove_job(
                job_id=f"deposit_{_lst[0]} interest schedule"
            )
        self.params["db"].conn.commit()


class CustomTableModel(QAbstractTableModel):
    def __init__(self, data):
        super(CustomTableModel, self).__init__()
        self._data = data

    @pyqtSlot(list)
    def update_item(self, value):
        if not value[0][0] == "ERROR":
            ix = self.index(len(value), 10)
            self.setData(ix, value, Qt.DisplayRole)

    def setData(self, index, value, role):
        if role == Qt.DisplayRole:
            self._data = value
            self.dataChanged.emit(index, index)
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
                    if index.column() == 8:
                        return value.strftime("%b %d, %Y")
                    return value.strftime("%b %d, %Y  %H:%M:%S")
                if isinstance(value, float):
                    return "\u20A6{:,}".format(float(value))
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
                return header[section]
        if orientation == Qt.Vertical:
            if role == Qt.TextAlignmentRole:
                return Qt.AlignCenter
            return section + 1

    def sort(self, column, order):
        if not self._data is None:
            self.layoutAboutToBeChanged.emit()
            self._data.sort(reverse=order)
            self.layoutChanged.emit()

    def rowCount(self, index):
        row_count = len(self._data) if not self._data is None else 1
        return row_count

    def columnCount(self, index):
        col_count = 10
        return col_count

    def flags(self, index):
        return super(QAbstractTableModel, self).flags(index) | Qt.ItemIsUserCheckable


class WorkerSignals(QObject):
    result = pyqtSignal(list)


class Worker(QRunnable):
    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()

        # Store constructor arguments (re-used for processing)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()
        self.kwargs["result"] = self.signals.result

    def run(self):
        """
        Initialise the runner function with passed args, kwargs.
        """

        # Retrieve args/kwargs here; and fire processing using them
        result = self.fn(*self.args, **self.kwargs)
        self.signals.result.emit(result)