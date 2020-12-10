import traceback, sys
from datetime import datetime
from PyQt5.QtGui import QIcon, QColor
from PyQt5.QtWidgets import (
    QVBoxLayout,
    QWidget,
    QPushButton,
    QGroupBox,
    QHBoxLayout,
    QSizePolicy,
    QAction,
    QMainWindow,
    QStackedWidget,
    QToolBar,
    QLabel,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QTableView,
    QLineEdit,
    QScrollArea,
    QGridLayout,
    QSpacerItem,
    QSizePolicy,
    QDateEdit,
)
from PyQt5.QtCore import (
    Qt,
    QDate,
    QAbstractTableModel,
    QModelIndex,
    QRunnable,
    QThreadPool,
    QObject,
    pyqtSlot,
    pyqtSignal,
    QVariant,
    QPersistentModelIndex,
)

# from .user_list_item import USER


class USER_LDW(QWidget):
    def __init__(self, params, user_id, context):
        super().__init__()
        self.params = params
        self.user_id = user_id
        self.context = context

        self.search_date = {"from": None, "to": None}
        self.for_account = "member"

        self.table_data = self._get_data_db()

        self.threadpool = QThreadPool()

        self._view()

    def _view(self):
        self.initial_layout = QVBoxLayout()
        self.initial_layout.setContentsMargins(0, 0, 0, 0)
        header_layout = QGridLayout()
        header_layout.setContentsMargins(0, 0, 0, 0)
        label = QLabel(f"{self.context.replace('s','').capitalize()} History for")
        label.setStyleSheet(
            """font-size: 18px;
            text-transform: capitalize;"""
        )
        label_name = QLabel(f"{self.user}")
        label_name.setStyleSheet(
            """font-size: 25px;
            text-transform: capitalize;"""
        )
        header_layout.addWidget(label, 0, 0)
        header_layout.addWidget(label_name, 1, 0)

        date_lay = QHBoxLayout()
        self.search_int_date_from = QDateEdit(calendarPopup=True)
        self.search_int_date_from.setDate(
            QDate(
                datetime.today().year, datetime.today().month, datetime.today().day - 1
            )
        )
        self.search_int_date_from.setFixedWidth(150)
        date_lay.addWidget(QLabel("From:"), alignment=Qt.AlignRight)
        date_lay.addWidget(self.search_int_date_from)
        header_layout.addLayout(date_lay, 0, 1)

        date_lay = QHBoxLayout()
        self.search_int_date_to = QDateEdit(calendarPopup=True)
        self.search_int_date_to.setDate(
            QDate(datetime.today().year, datetime.today().month, datetime.today().day)
        )
        self.search_int_date_to.setFixedWidth(150)
        date_lay.addWidget(QLabel("To:"), alignment=Qt.AlignRight)
        date_lay.addWidget(self.search_int_date_to)
        header_layout.addLayout(date_lay, 1, 1)

        self.initial_layout.addLayout(header_layout)

        self._create_table(data=self.table_data)
        self.initial_layout.addWidget(self.table_view)

        self.search_int_date_from.dateChanged.connect(
            lambda: self._handle_dateChange("from")
        )
        self.search_int_date_to.dateChanged.connect(
            lambda: self._handle_dateChange("to")
        )

        self.setLayout(self.initial_layout)

    def _create_table(self, data):
        self.model = CustomTableModel(data=data, context=self.context)
        self.table_view = QTableView()
        self.table_view.setModel(self.model)
        self.table_view.setSortingEnabled(True)
        self.table_view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_view.horizontalHeader().setStretchLastSection(True)
        self.table_view.horizontalHeader().setMinimumSectionSize(140)
        self.table_view.verticalHeader().setMinimumWidth(30)
        self.table_view.verticalHeader().setDefaultAlignment(Qt.AlignCenter)

    def _handle_dateChange(self, context):
        if context == "from":
            self.search_date["from"] = self.search_int_date_from.date().toString(
                Qt.ISODate
            )
            self.search_date["to"] = str(datetime.today().date())
        elif context == "to":
            self.search_date["from"] = self.search_int_date_from.date().toString(
                Qt.ISODate
            )
            self.search_date["to"] = self.search_int_date_to.date().toString(Qt.ISODate)
        # Pass the function to execute
        worker = Worker(
            self.execute_this_fn,
            [
                datetime.strptime(self.search_date["from"], "%Y-%m-%d"),
                datetime.strptime(self.search_date["to"], "%Y-%m-%d"),
            ],
        )  # Any other args, kwargs are passed to the run function

        worker.signals.result.connect(self.model.update_item)

        # Execute
        self.threadpool.start(worker)

    def execute_this_fn(self, date_range, result):
        shw_lst = []
        for account in self.table_data:
            if self.context == "loans":
                if (
                    datetime.strptime(account[8].strftime("%Y-%m-%d"), "%Y-%m-%d")
                    >= date_range[0]
                    and datetime.strptime(account[8].strftime("%Y-%m-%d"), "%Y-%m-%d")
                    <= date_range[1]
                ):
                    shw_lst.append(account)
                    if shw_lst.count(account) > 1:
                        shw_lst.remove(account)
            elif self.context == "deposits" or self.context == "withdrawals":
                if (
                    datetime.strptime(account[1].strftime("%Y-%m-%d"), "%Y-%m-%d")
                    >= date_range[0]
                    and datetime.strptime(account[1].strftime("%Y-%m-%d"), "%Y-%m-%d")
                    <= date_range[1]
                ):
                    shw_lst.append(account)
                    if shw_lst.count(account) > 1:
                        shw_lst.remove(account)
        return shw_lst

    def _get_data_db(self):
        data = []
        self.db = self.params["db"].conn.cursor()
        self.db.execute(
            """SELECT first_name,middle_name,last_name FROM users WHERE id=?;""",
            (self.user_id,),
        )
        name = self.db.fetchone()
        self.user = f"{name[2]} {name[0]} {name[1]}"

        if self.context == "loans":
            self.db.execute(
                """SELECT * FROM loans WHERE user_id=? ORDER BY date_issued DESC;""",
                (self.user_id,),
            )
            loans = self.db.fetchall()
            for item in loans:
                loan = []
                loan.append(item[1])
                loan.append(item[2])
                loan.append(item[3])
                loan.append(item[4])
                loan.append(item[5])
                loan.append(item[6].capitalize())
                loan.append(item[7])
                loan.append(datetime.strptime(item[8], "%Y-%m-%d"))
                loan.append(datetime.strptime(item[9], "%Y-%m-%d %H:%M:%S"))
                data.append(loan)
        elif self.context == "deposits":
            self.db.execute(
                """SELECT * FROM deposits WHERE user_id=? ORDER BY date DESC;""",
                (self.user_id,),
            )
            deposits = self.db.fetchall()
            for item in deposits:
                deposit = []
                deposit.append(item[1])
                deposit.append(datetime.strptime(item[2], "%Y-%m-%d %H:%M:%S"))
                data.append(deposit)
        elif self.context == "withdrawals":
            self.db.execute(
                """SELECT * FROM withdrawals WHERE user_id=? ORDER BY date DESC;""",
                (self.user_id,),
            )
            withdrawals = self.db.fetchall()
            for item in withdrawals:
                withdrawal = []
                withdrawal.append(item[1])
                withdrawal.append(datetime.strptime(item[2], "%Y-%m-%d %H:%M:%S"))
                data.append(withdrawal)
        return data


class CustomTableModel(QAbstractTableModel):
    def __init__(self, data, context):
        super(CustomTableModel, self).__init__()
        self._data = data
        self.context = context

    @pyqtSlot(list)
    def update_item(self, value):
        if self.context == "loans":
            ix = self.index(len(value), 9)
        elif self.context == "deposits" or self.context == "withdrawals":
            ix = self.index(len(value), 2)
        self.setData(ix, value, Qt.DisplayRole)

    def setData(self, index, value, role):
        if role == Qt.DisplayRole:
            self._data = value
            self.dataChanged.emit(index, index)
            return True
        if role == Qt.CheckStateRole:
            return True
        return False

    def data(self, index, role):
        value = self._data[index.row()][index.column()]
        if role == Qt.DisplayRole:
            if isinstance(value, datetime):
                if index.column() == 7:
                    return value.strftime("%b %d, %Y")
                return value.strftime("%b %d, %Y  %H:%M:%S")
            if isinstance(value, float):
                if self.context == "loans":
                    return "\u20A6{:,}".format(float(value))
                elif self.context == "deposits":
                    return "+\u20A6{:,}".format(float(value))
                elif self.context == "withdrawals":
                    return "-\u20A6{:,}".format(float(value))
            return value
        if role == Qt.TextAlignmentRole:
            return Qt.AlignCenter
        if role == Qt.ForegroundRole:
            if self.context == "loans":
                if index.column() == 3:
                    return QColor("green")
                if index.column() == 4:
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
                if self.context == "loans":
                    header = [
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
                        "Amount Deposited",
                        "Date Deposited",
                    ]
                elif self.context == "withdrawals":
                    header = [
                        "Amount Withdrawn",
                        "Date Requested",
                    ]
                return header[section]
        if orientation == Qt.Vertical:
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
        return len(self._data[0])

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