import traceback, sys
from PyQt5.QtGui import QIcon
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
    QCheckBox,
    QTabWidget,
)
from PyQt5.QtCore import (
    Qt,
    QAbstractTableModel,
    QModelIndex,
    QRunnable,
    QThreadPool,
    QObject,
    pyqtSlot,
    pyqtSignal,
    QPersistentModelIndex,
)
from .user_list_item import USER


class USER_LIST(QWidget):
    def __init__(self, params):
        super().__init__()
        self.params = params

        self.table_data = [["member", []], ["staff", []]]

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

        label_0 = QLabel(f"Member List")
        label_1 = QLabel(f"Staff List")

        label_0.setObjectName("Header")
        label_1.setObjectName("Header")

        header_layout = QGridLayout()
        header_layout.setContentsMargins(0, 0, 0, 0)

        header_layout.addWidget(label_0, 0, 0, alignment=Qt.AlignLeft)

        self.search_int_0 = QLineEdit()
        self.search_int_0.setPlaceholderText("Search Member...")
        self.search_int_0.setFixedWidth(300)
        header_layout.addWidget(self.search_int_0, 0, 1, alignment=Qt.AlignRight)
        member_wid_lay.addLayout(header_layout)

        header_layout = QGridLayout()
        header_layout.setContentsMargins(0, 0, 0, 0)

        header_layout.addWidget(label_1, 0, 0, alignment=Qt.AlignLeft)

        self.search_int_1 = QLineEdit()
        self.search_int_1.setPlaceholderText("Search Staff...")
        self.search_int_1.setFixedWidth(300)
        header_layout.addWidget(self.search_int_1, 0, 1, alignment=Qt.AlignRight)
        staff_wid_lay.addLayout(header_layout)

        view_0 = self._create_table(0)
        member_wid_lay.addWidget(view_0)

        view_1 = self._create_table(1)
        staff_wid_lay.addWidget(view_1)

        tab_widget.addTab(member_wid, "MEMBER")
        tab_widget.addTab(staff_wid, "STAFF")
        tab_widget.tabBar().setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self.search_int_0.textChanged.connect(lambda x: self._handle_search(x, 0))
        self.search_int_1.textChanged.connect(lambda x: self._handle_search(x, 1))

        self.setLayout(self.initial_layout)

    def _create_table(self, acc_type):
        data = self._get_data_db(acc_type)
        table_view = QTableView()

        if acc_type == 0:
            self.model_1 = CustomTableModel(data=data[acc_type])
            table_view.setModel(self.model_1)
        else:
            self.model_2 = CustomTableModel(data=data[acc_type])
            table_view.setModel(self.model_2)

        table_view.setSortingEnabled(True)
        table_view.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        table_view.horizontalHeader().setStretchLastSection(True)
        table_view.verticalHeader().setMinimumWidth(30)
        table_view.verticalHeader().setDefaultAlignment(Qt.AlignCenter)

        table_view.clicked.connect(self._handle_sic)

        return table_view

    def _handle_sic(self, i):
        if not i.data() == "No Account Registered":
            i = i.data().split(" ")
            self.db.execute(
                """SELECT * FROM users WHERE last_name=? AND first_name=? AND middle_name=?;""",
                (i[0], i[1], i[2]),
            )
            user_id = self.db.fetchone()
            self.threadpool.clear()
            view = USER(self.params, user_id[0])
            self.params["next"]["widget"].addWidget(view)
            self.params["next"]["widget"].setCurrentWidget(view)

    def _handle_search(self, i, acc_type):
        # Pass the function to execute
        worker = Worker(
            self.execute_search_fn, i, acc_type
        )  # Any other args, kwargs are passed to the run function

        if acc_type == 0:
            worker.signals.result.connect(self.model_1.update_item)
        else:
            worker.signals.result.connect(self.model_2.update_item)

        # Execute
        self.threadpool.start(worker)

    def execute_search_fn(self, text, acc_type, result):
        if text.rstrip() == "":
            shw_lst = self.table_data[acc_type][1]
        else:
            shw_lst = []
            if not self.table_data[acc_type][1][0][0] == "ERROR":
                for account in self.table_data[acc_type][1]:
                    if text.lower() in account[1].lower():
                        shw_lst.append(account)
                        if shw_lst.count(account) > 1:
                            shw_lst.remove(account)

        return shw_lst

    def _get_data_db(self, account_type):
        acc_type = "member" if account_type == 0 else "staff"
        self.db = self.params["db"].conn.cursor()
        self.db.execute(
            """SELECT * FROM users WHERE account_type=? ORDER BY last_name ASC;""",
            (acc_type,),
        )
        users = self.db.fetchall()

        if len(users) > 0:
            for user in users:
                self.table_data[account_type][1].append(
                    ("Name", f"{user[3]} {user[1]} {user[2]}")
                )
        else:
            self.table_data[account_type][1] = [
                [
                    "ERROR",
                    "No Account Registered",
                ]
            ]
        return self.table_data


class CustomTableModel(QAbstractTableModel):
    def __init__(self, data):
        super(CustomTableModel, self).__init__()
        self._data = data[1]
        self.checks = {}

    @pyqtSlot(list)
    def update_item(self, value, role=Qt.DisplayRole):
        ix = self.index(len(value), 1)
        self.setData(ix, value, role)

    def setData(self, index, value, role):
        if role == Qt.DisplayRole:
            self._data = value
            self.dataChanged.emit(index, index)
            return True
        return False

    def data(self, index, role=Qt.DisplayRole):
        value = self._data[index.row()][1]
        if role == Qt.DisplayRole:
            return value

    def headerData(self, section, orientation, role):
        if orientation == Qt.Horizontal:
            if role == Qt.DisplayRole:
                if self._data[0][0] == "ERROR":
                    return self._data[0][0]

                return self._data[section][0]
        if orientation == Qt.Vertical:
            if role == Qt.TextAlignmentRole:
                return Qt.AlignCenter
            return section + 1

    def sort(self, column, order):
        self.layoutAboutToBeChanged.emit()
        self._data.sort(reverse=order)
        self.layoutChanged.emit()

    def rowCount(self, parent=QModelIndex()):
        return len(self._data)

    def columnCount(self, parent=QModelIndex()):
        return 1

    def flags(self, index):
        return Qt.ItemIsEnabled | Qt.ItemIsUserCheckable


class WorkerSignals(QObject):
    """
    Defines the signals available from a running worker thread.

    Supported signals are:

    finished
        No data

    error
        `tuple` (exctype, value, traceback.format_exc() )

    result
        `object` data returned from processing, anything

    progress
        `int` indicating % progress

    """

    result = pyqtSignal(list)


class Worker(QRunnable):
    """
    Worker thread

    Inherits from QRunnable to handler worker thread setup, signals and wrap-up.

    :param callback: The function callback to run on this worker thread. Supplied args and
                     kwargs will be passed through to the runner.
    :type callback: function
    :param args: Arguments to pass to the callback function
    :param kwargs: Keywords to pass to the callback function

    """

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