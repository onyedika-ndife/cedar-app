from datetime import datetime

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from app import Worker
from app.ldw_user import USER_LDW
from app.loan_clear import LOAN_CLEAR


class LDW_LIST(QWidget):
    def __init__(self, params, context):
        super().__init__()
        self.params = params
        self.context = context
        self.table_data = [["member", []], ["staff", []]]
        self.search_date = {"from": None, "to": None}

        self.threadpool = QThreadPool()

        self._view()

    def _view(self):
        self.initial_layout = QVBoxLayout()
        self.initial_layout.setContentsMargins(0, 0, 0, 0)

        tab_widget = QTabWidget()
        member_wid = QWidget()
        member_wid_lay = QVBoxLayout()
        member_wid.setLayout(member_wid_lay)
        staff_wid = QWidget()
        staff_wid_lay = QVBoxLayout()
        staff_wid.setLayout(staff_wid_lay)

        self.initial_layout.addWidget(tab_widget)

        if self.context == "clear_loans":
            label_0 = QLabel(f"Select Member Account Loan")
            label_1 = QLabel(f"Select Staff Account Loan")
        else:
            label_0 = QLabel(f"Member {self.context.capitalize()}")
            label_1 = QLabel(f"Staff {self.context.capitalize()}")
        label_0.setObjectName("Header")
        label_1.setObjectName("Header")
        header_layout = QGridLayout()
        header_layout.setContentsMargins(0, 0, 0, 0)
        view_0 = self._create_table(0)
        view_1 = self._create_table(1)

        self.search_int_text_0 = QLineEdit()
        self.search_int_text_0.setPlaceholderText("Search...")
        self.search_int_date_from_0 = QDateEdit(calendarPopup=True)
        self.search_int_date_from_0.setDate(
            QDate(
                datetime.today().year, datetime.today().month, datetime.today().day - 1
            )
        )

        self.search_int_date_to_0 = QDateEdit(calendarPopup=True)
        self.search_int_date_to_0.setDate(
            QDate(datetime.today().year, datetime.today().month, datetime.today().day)
        )
        self.search_int_text_0.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.search_int_date_from_0.setFixedWidth(150)
        self.search_int_date_to_0.setFixedWidth(150)

        self.search_int_text_1 = QLineEdit()
        self.search_int_text_1.setPlaceholderText("Search...")
        self.search_int_date_from_1 = QDateEdit(calendarPopup=True)
        self.search_int_date_from_1.setDate(
            QDate(
                datetime.today().year, datetime.today().month, datetime.today().day - 1
            )
        )
        self.search_int_date_to_1 = QDateEdit(calendarPopup=True)
        self.search_int_date_to_1.setDate(
            QDate(datetime.today().year, datetime.today().month, datetime.today().day)
        )
        self.search_int_text_1.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.search_int_date_from_1.setFixedWidth(150)
        self.search_int_date_to_1.setFixedWidth(150)

        if self.table_data[0][1][0][0] == "ERROR":
            self.search_int_text_0.setDisabled(True)
            self.search_int_date_from_0.setDisabled(True)
            self.search_int_date_to_0.setDisabled(True)
        if self.table_data[1][1][0][0] == "ERROR":
            self.search_int_text_1.setDisabled(True)
            self.search_int_date_from_1.setDisabled(True)
            self.search_int_date_to_1.setDisabled(True)

        header_layout = QGridLayout()
        header_layout.setContentsMargins(0, 0, 0, 0)

        header_layout.addWidget(label_0, 0, 0, 1, 0)
        header_layout.addWidget(self.search_int_text_0, 0, 1, 1, 2)
        header_layout.addWidget(self.search_int_date_from_0, 1, 1)
        header_layout.addWidget(self.search_int_date_to_0, 1, 2)

        member_wid_lay.addLayout(header_layout)

        header_layout = QGridLayout()
        header_layout.setContentsMargins(0, 0, 0, 0)

        header_layout.addWidget(label_1, 0, 0, 1, 0)
        header_layout.addWidget(self.search_int_text_1, 0, 1, 1, 2)
        header_layout.addWidget(self.search_int_date_from_1, 1, 1)
        header_layout.addWidget(self.search_int_date_to_1, 1, 2)

        staff_wid_lay.addLayout(header_layout)

        self.search_int_text_0.textChanged.connect(
            lambda text: self._handle_search(text, 0)
        )
        self.search_int_text_1.textChanged.connect(
            lambda text: self._handle_search(text, 1)
        )

        self.search_int_date_from_0.dateChanged.connect(
            lambda: self._handle_dateChange("from", 0)
        )
        self.search_int_date_to_0.dateChanged.connect(
            lambda: self._handle_dateChange("to", 0)
        )
        self.search_int_date_from_1.dateChanged.connect(
            lambda: self._handle_dateChange("from", 1)
        )
        self.search_int_date_to_1.dateChanged.connect(
            lambda: self._handle_dateChange("to", 1)
        )

        member_wid_lay.addWidget(view_0)
        staff_wid_lay.addWidget(view_1)

        tab_widget.addTab(member_wid, "MEMBER")
        tab_widget.addTab(staff_wid, "STAFF")

        self.setLayout(self.initial_layout)

    def _create_table(self, acc_type):
        data = self._get_data_db(acc_type)
        table_view = QTableView()

        if acc_type == 0:
            self.model_1 = LDWTABLE(data=data[acc_type], context=self.context)
            table_view.setModel(self.model_1)
        else:
            self.model_2 = LDWTABLE(data=data[acc_type], context=self.context)
            table_view.setModel(self.model_2)
        table_view.setSortingEnabled(True)
        table_view.setSelectionMode(QAbstractItemView.SingleSelection)
        table_view.setSelectionBehavior(QAbstractItemView.SelectRows)
        table_view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        table_view.horizontalHeader().setStretchLastSection(True)
        table_view.horizontalHeader().setMinimumSectionSize(140)
        table_view.verticalHeader().setMinimumWidth(30)
        table_view.verticalHeader().setDefaultAlignment(Qt.AlignCenter)

        table_view.clicked.connect(self._handle_sic)

        return table_view

    def _handle_sic(self, i):
        if (
            i.column() == 0
            and not i.data() == "No Loan Data"
            and not i.data() == "No Deposit Data"
            and not i.data() == "No Withdrawal Data"
            and not i.data() == "No Loan Issued to Member"
            and not i.data() == "No Deposit by Member"
            and not i.data() == "No Withdrawal by Member"
            and not i.data() == "No Loan Issued to Staff"
            and not i.data() == "No Deposit by Staff"
            and not i.data() == "No Withdrawal by Staff"
        ):
            i = i.data().split(" ")
            self.db.execute(
                """SELECT * FROM users WHERE last_name=? AND first_name=?;""",
                (i[0], i[1]),
            )
            user_id = self.db.fetchone()[0]
            if not self.context == "clear_loans":
                view = USER_LDW(self.params, user_id, self.context)
                self.params["next"]["widget"].addWidget(view)
                self.params["next"]["widget"].setCurrentWidget(view)
            else:
                view = LOAN_CLEAR(self.params, user_id)
                view.exec_()

    def _handle_search(self, i, acc_type):
        # Pass the function to execute
        worker = Worker(
            self.execute_search_txt_fn, i, acc_type
        )  # Any other args, kwargs are passed to the run function

        if acc_type == 0:
            worker.signals.result.connect(self.model_1.update_item)
        else:
            worker.signals.result.connect(self.model_2.update_item)

        # Execute
        self.threadpool.start(worker)

    def execute_search_txt_fn(self, text, acc_type, result):
        if text.rstrip() == "":
            shw_lst = self.table_data[acc_type][1]
        else:
            shw_lst = []
            if not self.table_data[acc_type][1][0][0] == "ERROR":
                for account in self.table_data[acc_type][1]:
                    if self.context == "loans" or self.context == "clear_loans":
                        if (
                            text.lower() in account[0].lower()
                            or text.lower() in str(account[1]).lower()
                            or text.lower() in str(account[2]).lower()
                            or text.lower() in str(account[3]).lower()
                            or text.lower() in str(account[4]).lower()
                            or text.lower() in str(account[5]).lower()
                            or text.lower() in str(account[6]).lower()
                            or text.lower() in str(account[7]).lower()
                        ):
                            shw_lst.append(account)
                            if shw_lst.count(account) > 1:
                                shw_lst.remove(account)
                    elif self.context == "deposits" or self.context == "withdrawals":
                        if (
                            text.lower() in account[0].lower()
                            or text.lower() in str(account[1]).lower()
                        ):
                            shw_lst.append(account)
                            if shw_lst.count(account) > 1:
                                shw_lst.remove(account)
        return shw_lst

    def _handle_dateChange(self, context, acc_type):
        if context == "from":
            if acc_type == 0:
                self.search_date["from"] = self.search_int_date_from_0.date().toString(
                    Qt.ISODate
                )
            elif acc_type == 1:
                self.search_date["from"] = self.search_int_date_from_1.date().toString(
                    Qt.ISODate
                )
            self.search_date["to"] = str(datetime.today().date())
        elif context == "to":
            if acc_type == 0:
                self.search_date["from"] = self.search_int_date_from_0.date().toString(
                    Qt.ISODate
                )
                self.search_date["to"] = self.search_int_date_to_0.date().toString(
                    Qt.ISODate
                )
            elif acc_type == 1:
                self.search_date["from"] = self.search_int_date_from_1.date().toString(
                    Qt.ISODate
                )
                self.search_date["to"] = self.search_int_date_to_1.date().toString(
                    Qt.ISODate
                )

        worker = Worker(
            self.execute_search_date_fn,
            [
                datetime.strptime(self.search_date["from"], "%Y-%m-%d"),
                datetime.strptime(self.search_date["to"], "%Y-%m-%d"),
            ],
            acc_type,
        )  # Any other args, kwargs are passed to the run function

        if acc_type == 0:
            worker.signals.result.connect(self.model_1.update_item)
        else:
            worker.signals.result.connect(self.model_2.update_item)

        # Execute
        self.threadpool.start(worker)

    def execute_search_date_fn(self, date_range, acc_type, result):
        shw_lst = []
        for account in self.table_data[acc_type][1]:
            if self.context == "loans" or self.context == "clear_loans":
                if (
                    datetime.strptime(account[9].strftime("%Y-%m-%d"), "%Y-%m-%d")
                    >= date_range[0]
                    and datetime.strptime(account[9].strftime("%Y-%m-%d"), "%Y-%m-%d")
                    <= date_range[1]
                ):
                    shw_lst.append(account)
                    if shw_lst.count(account) > 1:
                        shw_lst.remove(account)
            elif self.context == "deposits" or self.context == "withdrawals":
                if (
                    datetime.strptime(account[2].strftime("%Y-%m-%d"), "%Y-%m-%d")
                    >= date_range[0]
                    and datetime.strptime(account[2].strftime("%Y-%m-%d"), "%Y-%m-%d")
                    <= date_range[1]
                ):
                    shw_lst.append(account)
                    if shw_lst.count(account) > 1:
                        shw_lst.remove(account)
        return shw_lst

    def _get_data_db(self, account_type):
        acc_type = "member" if account_type == 0 else "staff"
        self.db = self.params["db"].conn.cursor()
        self.db.execute("""SELECT * FROM users WHERE account_type=?;""", (acc_type,))
        users = self.db.fetchall()
        if len(users) > 0:
            for item in users:
                if self.context == "loans" or self.context == "clear_loans":
                    if self.context == "loans":
                        self.db.execute(
                            """SELECT * FROM loans WHERE user_id=? ORDER BY id DESC LIMIT 1;""",
                            (item[0],),
                        )
                    else:
                        self.db.execute(
                            """SELECT * FROM loans WHERE user_id=? AND status="not cleared" OR user_id=? AND status="pending" ORDER BY id DESC LIMIT 1;""",
                            (
                                item[0],
                                item[0],
                            ),
                        )
                    loan = self.db.fetchall()
                    if len(loan) > 0:
                        user = []
                        user.append(f"{item[3]} {item[1]}")
                        for i in loan:
                            if item[0] == i[11]:
                                user.append(i[1])
                                user.append(i[2])
                                user.append(i[3])
                                user.append(i[4])
                                user.append(i[5])
                                user.append(i[6].capitalize())
                                user.append(i[7])
                                user.append(datetime.strptime(i[8], "%Y-%m-%d"))
                                user.append(datetime.strptime(i[9], "%Y-%m-%d"))
                        self.table_data[account_type][1].append(user)
                elif self.context == "deposits":
                    self.db.execute(
                        """SELECT * FROM deposits WHERE user_id=? ORDER BY id DESC LIMIT 1;""",
                        (item[0],),
                    )
                    deposit = self.db.fetchall()
                    if len(deposit) > 0:
                        user = []
                        user.append(f"{item[3]} {item[1]}")
                        for i in deposit:
                            if item[0] == i[3]:
                                user.append(i[1])
                                user.append(datetime.strptime(i[2], "%Y-%m-%d"))
                        self.table_data[account_type][1].append(user)
                elif self.context == "withdrawals":
                    self.db.execute(
                        """SELECT * FROM withdrawals WHERE user_id=? ORDER BY id DESC LIMIT 1;""",
                        (item[0],),
                    )
                    withdrawal = self.db.fetchall()
                    if len(withdrawal) > 0:
                        user = []
                        user.append(f"{item[3]} {item[1]}")
                        for i in withdrawal:
                            if item[0] == i[4]:
                                user.append(i[1])
                                user.append(datetime.strptime(i[3], "%Y-%m-%d"))
                        self.table_data[account_type][1].append(user)
        else:
            if self.context == "loans":
                self.table_data[account_type][1] = [
                    [
                        "ERROR",
                        "No Loan Issued to {}".format(acc_type.capitalize()),
                    ]
                ]
            elif self.context == "clear_loans":
                if len(self.table_data[account_type][1]) == 0:
                    self.table_data[account_type][1] = [
                        [
                            "ERROR",
                            "No Pending Loan for {}".format(acc_type.capitalize()),
                        ]
                    ]
            elif self.context == "deposits":
                self.table_data[account_type][1] = [
                    [
                        "ERROR",
                        "No Deposit by {}".format(acc_type.capitalize()),
                    ]
                ]
            elif self.context == "withdrawals":
                self.table_data[account_type][1] = [
                    ["ERROR", "No Withdrawal by {}".format(acc_type.capitalize())]
                ]

        if self.context == "loans":
            if len(self.table_data[account_type][1]) == 0:
                self.table_data[account_type][1] = [
                    [
                        "ERROR",
                        "No Loan Issued to {}".format(acc_type.capitalize()),
                    ]
                ]
        elif self.context == "clear_loans":
            if len(self.table_data[account_type][1]) == 0:
                self.table_data[account_type][1] = [
                    [
                        "ERROR",
                        "No Pending Loan for {}".format(acc_type.capitalize()),
                    ]
                ]
        elif self.context == "deposits":
            if len(self.table_data[account_type][1]) == 0:
                self.table_data[account_type][1] = [
                    [
                        "ERROR",
                        "No Deposit by {}".format(acc_type.capitalize()),
                    ]
                ]
        elif self.context == "withdrawals":
            if len(self.table_data[account_type][1]) == 0:
                self.table_data[account_type][1] = [
                    [
                        "ERROR",
                        "No Withdrawal by {}".format(acc_type.capitalize()),
                    ]
                ]

        return self.table_data


class LDWTABLE(QAbstractTableModel):
    def __init__(self, data, context):
        super(LDWTABLE, self).__init__()
        self._data = data[1]
        self.context = context

    @pyqtSlot(list)
    def update_item(self, value):
        if self.context == "loans" or self.context == "clear_loans":
            ix = self.index(len(value), 10)
        elif self.context == "deposits" or self.context == "withdrawals":
            ix = self.index(len(value), 3)
        try:
            if self._data[0][0] == "ERROR":
                ix = self.index(len(value), 1)
        except Exception:
            pass
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
        value = self._data[index.row()][index.column()]
        if role == Qt.DisplayRole:
            if isinstance(value, datetime):
                return value.strftime("%B %d, %Y")
            if isinstance(value, float):
                if self.context == "loans" or self.context == "clear_loans":
                    return "\u20A6 {:,}".format(float(value))
                elif self.context == "deposits":
                    return "+\u20A6 {:,}".format(float(value))
                elif self.context == "withdrawals":
                    return "-\u20A6 {:,}".format(float(value))
            if self._data[0][0] == "ERROR":
                return self._data[0][1]
            return value
        if role == Qt.TextAlignmentRole:
            if not index.column() == 0:
                return Qt.AlignCenter
        if role == Qt.ForegroundRole:
            if self.context == "loans" or self.context == "clear_loans":
                if index.column() == 4:
                    return QColor("green")
                if index.column() == 5:
                    return QColor("red")
            elif self.context == "deposits":
                if isinstance(value, float):
                    return QColor("green")
            elif self.context == "withdrawals":
                if isinstance(value, float):
                    return QColor("red")

    def headerData(self, section, orientation, role):
        if orientation == Qt.Horizontal:
            if role == Qt.DisplayRole:
                if self.context == "loans" or self.context == "clear_loans":
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
                elif self.context == "deposits":
                    header = [
                        "Name",
                        "Amount Deposited",
                        "Date Deposited",
                    ]
                elif self.context == "withdrawals":
                    header = [
                        "Name",
                        "Amount Withdrawn",
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
        self.layoutAboutToBeChanged.emit()
        self._data.sort(reverse=order)
        self.layoutChanged.emit()

    def rowCount(self, index):
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
            if self.context == "loans" or self.context == "clear_loans":
                return 10
            elif self.context == "deposits" or self.context == "withdrawals":
                return 3

    def flags(self, index):
        return super(QAbstractTableModel, self).flags(index) | Qt.ItemIsUserCheckable
