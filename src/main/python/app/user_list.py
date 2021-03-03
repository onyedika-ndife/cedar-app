import os

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from app import Worker
from app.user import USER


class USER_LIST(QWidget):
    def __init__(self, params):
        super().__init__()
        self.params = params

        self.table_data = [["member", []], ["staff", []]]

        self.threadpool = QThreadPool()
        self.selected_list_0 = None
        self.selected_list_1 = None

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

        btn_widget_0 = QWidget()
        btn_layout_0 = QHBoxLayout()
        btn_layout_0.setContentsMargins(0, 0, 0, 0)
        btn_widget_0.setLayout(btn_layout_0)

        self.sel_chk_0 = QCheckBox("Select")
        self.sel_chk_0.clicked.connect(
            lambda: self._handle_toolbar_btn(
                {"text": "select", "acc_type": 0, "self": self.sel_chk_0}
            )
        )
        self.del_sel_btn_0 = QPushButton(
            QIcon(self.params["ctx"].get_resource("icon/delete.png")), "Delete Selected"
        )
        self.del_sel_btn_0.setDisabled(True)

        btn_widget_1 = QWidget()
        btn_layout_1 = QHBoxLayout()
        btn_layout_1.setContentsMargins(0, 0, 0, 0)
        btn_widget_1.setLayout(btn_layout_1)

        self.sel_chk_1 = QCheckBox("Select")
        self.sel_chk_1.clicked.connect(
            lambda: self._handle_toolbar_btn(
                {"text": "select", "acc_type": 1, "self": self.sel_chk_1}
            )
        )

        self.del_sel_btn_1 = QPushButton(
            QIcon(self.params["ctx"].get_resource("icon/delete.png")), "Delete Selected"
        )
        self.del_sel_btn_1.setDisabled(True)

        self.sel_chk_0.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.del_sel_btn_0.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.sel_chk_1.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.del_sel_btn_1.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        btn_layout_0.addWidget(self.sel_chk_0)
        btn_layout_0.addWidget(self.del_sel_btn_0)

        btn_layout_1.addWidget(self.sel_chk_1)
        btn_layout_1.addWidget(self.del_sel_btn_1)

        self.del_sel_btn_0.clicked.connect(
            lambda: self._handle_toolbar_btn({"text": "delete", "acc_type": 0})
        )
        self.del_sel_btn_1.clicked.connect(
            lambda: self._handle_toolbar_btn({"text": "delete", "acc_type": 1})
        )

        header_layout = QGridLayout()
        header_layout.setContentsMargins(0, 0, 0, 0)

        header_layout.addWidget(label_0, 0, 0, alignment=Qt.AlignLeft)
        header_layout.addWidget(btn_widget_0, 1, 0, alignment=Qt.AlignLeft)

        self.search_int_0 = QLineEdit()
        self.search_int_0.setPlaceholderText("Search for Member...")
        self.search_int_0.setFixedWidth(300)
        header_layout.addWidget(self.search_int_0, 1, 1, alignment=Qt.AlignRight)
        member_wid_lay.addLayout(header_layout)

        header_layout = QGridLayout()
        header_layout.setContentsMargins(0, 0, 0, 0)

        header_layout.addWidget(label_1, 0, 0, alignment=Qt.AlignLeft)
        header_layout.addWidget(btn_widget_1, 1, 0, alignment=Qt.AlignLeft)

        self.search_int_1 = QLineEdit()
        self.search_int_1.setPlaceholderText("Search for Staff...")
        self.search_int_1.setFixedWidth(300)
        header_layout.addWidget(self.search_int_1, 1, 1, alignment=Qt.AlignRight)
        staff_wid_lay.addLayout(header_layout)

        view_0 = self._create_table(0)
        member_wid_lay.addWidget(view_0)

        view_1 = self._create_table(1)
        staff_wid_lay.addWidget(view_1)

        if self.table_data[0][1][0][0] == "ERROR":
            self.search_int_0.setDisabled(True)
            self.sel_chk_0.setDisabled(True)
        if self.table_data[1][1][0][0] == "ERROR":
            self.search_int_1.setDisabled(True)
            self.sel_chk_1.setDisabled(True)
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
            self.model_1 = USERLISTTABLE(data=data[acc_type])
            table_view.setModel(self.model_1)
        else:
            self.model_2 = USERLISTTABLE(data=data[acc_type])
            table_view.setModel(self.model_2)

        table_view.setSortingEnabled(True)
        table_view.setSelectionMode(QAbstractItemView.SingleSelection)
        table_view.setSelectionBehavior(QAbstractItemView.SelectRows)
        table_view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        table_view.horizontalHeader().setStretchLastSection(True)
        table_view.horizontalHeader().setMinimumSectionSize(140)
        table_view.verticalHeader().setMinimumWidth(30)
        table_view.verticalHeader().setDefaultAlignment(Qt.AlignCenter)

        table_view.clicked.connect(lambda x: self._check(acc_type, x))
        table_view.doubleClicked.connect(self._handle_double_click)

        return table_view

    def _handle_double_click(self, i):
        if i.column() == 0:
            if not i.data() == "No Account Registered":
                i = i.data()
                self.db.execute(
                    """SELECT id FROM users WHERE name=?;""",
                    (i,),
                )
                user_id = self.db.fetchone()[0]
                view = USER(self.params, user_id)
                self.threadpool.clear()
                self.params["next"]["widget"].addWidget(view)
                self.params["next"]["widget"].setCurrentWidget(view)

    def _check(self, acc_type, i):
        if i.column() == 0:
            check_state = i.model().checkState(QPersistentModelIndex(i))
            i.model().setData(i, 0 if check_state == 2 else 2, Qt.CheckStateRole)
            if acc_type == 0:
                self.sel_chk_0.setTristate(True)
                if len(i.model().selected) > 0:
                    self.selected_list_0 = i.model().selected
                    self.del_sel_btn_0.setDisabled(False)
                    if len(i.model()._data) == len(self.selected_list_0):
                        self.sel_chk_0.setCheckState(2)
                    else:
                        self.sel_chk_0.setCheckState(1)
                else:
                    self.sel_chk_0.setCheckState(0)
                    self.del_sel_btn_0.setDisabled(True)

            elif acc_type == 1:
                self.sel_chk_1.setTristate(True)
                if len(i.model().selected) > 0:
                    self.selected_list_1 = i.model().selected
                    self.del_sel_btn_1.setDisabled(False)
                    if len(i.model()._data) == len(self.selected_list_1):
                        self.sel_chk_1.setCheckState(2)
                    else:
                        self.sel_chk_1.setCheckState(1)
                else:
                    self.sel_chk_1.setCheckState(0)
                    self.del_sel_btn_1.setDisabled(True)

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
                    if text.lower() in account[0].lower():
                        shw_lst.append(account)
                        if shw_lst.count(account) > 1:
                            shw_lst.remove(account)
        return shw_lst

    def _get_data_db(self, account_type):
        acc_type = "member" if account_type == 0 else "staff"
        self.db = self.params["db"].conn.cursor()
        self.db.execute(
            """SELECT id, name FROM users WHERE account_type=? ORDER BY name ASC;""",
            (acc_type,),
        )
        users = self.db.fetchall()

        if len(users) > 0:
            for user in users:
                self.db.execute(
                    """SELECT total FROM savings WHERE user_id=?;""", (user[0],)
                )
                user_acc_bal = self.db.fetchone()[0]
                self.table_data[account_type][1].append([f"{user[1]}", user_acc_bal])
        else:
            self.table_data[account_type][1] = [
                [
                    "ERROR",
                    "No Account Registered",
                ]
            ]
        return self.table_data

    def _handle_toolbar_btn(self, params):
        if params["text"] == "select":
            if params["acc_type"] == 0:
                self.sel_chk_0.setTristate(False)
                for row in range(self.model_1.rowCount()):
                    for column in range(self.model_1.columnCount()):
                        item = self.model_1.index(row, column)
                        if params["self"].isChecked():
                            self.selected_list_0 = self.model_1.selected
                            self.model_1.setData(item, 2, Qt.CheckStateRole)
                            self.del_sel_btn_0.setDisabled(False)
                        else:
                            self.model_1.setData(item, 0, Qt.CheckStateRole)
                            self.del_sel_btn_0.setDisabled(True)
                self.selected_list_0 = self.model_1.selected

            elif params["acc_type"] == 1:
                self.sel_chk_1.setTristate(False)
                for row in range(self.model_2.rowCount()):
                    for column in range(self.model_2.columnCount()):
                        item = self.model_2.index(row, column)
                        if params["self"].isChecked():
                            self.model_2.setData(item, 2, Qt.CheckStateRole)
                            self.del_sel_btn_1.setDisabled(False)
                        else:
                            self.model_2.setData(item, 0, Qt.CheckStateRole)
                            self.del_sel_btn_1.setDisabled(True)
                self.selected_list_1 = self.model_2.selected

        elif params["text"] == "delete":
            msg = QMessageBox()
            msg.setStyleSheet(
                open(self.params["ctx"].get_resource("css/style.css")).read()
            )
            msg.setWindowTitle("Account Deletion")
            msg.setIconPixmap(
                QPixmap(self.params["ctx"].get_resource("icon/question.png"))
            )
            msg.setText(f"Are you sure you want to delete selected account(s)?")
            msg.setStandardButtons(QMessageBox.No | QMessageBox.Yes)
            msg.setDefaultButton(QMessageBox.Yes)
            msg.buttonClicked.connect(
                lambda x: self._del_selected(x, acc_type=params["acc_type"])
            )
            msg.exec_()
            msg.show()

    def _del_selected(self, choice, acc_type):
        if choice.text() == "&Yes":
            _list = self.selected_list_0 if acc_type == 0 else self.selected_list_1

            for user in _list:
                self.db.execute(
                    """SELECT id, profile_picture FROM users WHERE name=?;""",
                    (user,),
                )
                usr = self.db.fetchone()

                self.db.execute(
                    """SELECT id FROM deposits WHERE user_id=?;""", (usr[0],)
                )
                dep_ids = self.db.fetchall()
                if len(dep_ids) > 0:
                    for dep_id in dep_ids:
                        self.db.execute(
                            """DELETE FROM apscheduler_jobs WHERE apscheduler_jobs.id=?;""",
                            (f"dep_{dep_id[0]} interest schedule",),
                        )
                self.db.execute(
                    """DELETE FROM apscheduler_jobs WHERE apscheduler_jobs.id=?;""",
                    (f"{user} loan schedule",),
                )
                self.db.execute(
                    """DELETE FROM next_of_kin WHERE user_id=?;""",
                    (usr[0],),
                )
                self.db.execute(
                    """DELETE FROM company WHERE user_id=?;""",
                    (usr[0],),
                )
                self.db.execute(
                    """DELETE FROM savings WHERE user_id=?;""",
                    (usr[0],),
                )
                self.db.execute(
                    """DELETE FROM loans WHERE user_id=?;""",
                    (usr[0],),
                )

                self.db.execute(
                    """DELETE FROM withdrawals WHERE user_id=?;""",
                    (usr[0],),
                )
                self.db.execute(
                    """DELETE FROM deposits WHERE user_id=?;""",
                    (usr[0],),
                )
                self.db.execute(
                    """DELETE FROM deposit_interest WHERE user_id=?;""",
                    (usr[0],),
                )
                if not usr[1] == "":
                    os.remove(usr[1])
                self.db.execute(
                    """DELETE FROM users WHERE id=?;""",
                    (usr[0],),
                )

                self.params["db"].conn.commit()
            msg = QMessageBox()
            msg.setStyleSheet(
                open(self.params["ctx"].get_resource("css/style.css")).read()
            )
            msg.setWindowTitle("Account Deletion")
            msg.setIconPixmap(
                QPixmap(self.params["ctx"].get_resource("icon/success.png"))
            )
            msg.setText(f"Account(s) deleted successfully")
            msg.setDefaultButton(QMessageBox.Ok)
            msg.buttonClicked.connect(lambda: self.params["parent"]["back_btn"].click())
            msg.exec_()
            msg.show()


class USERLISTTABLE(QAbstractTableModel):
    def __init__(self, data):
        super(USERLISTTABLE, self).__init__()
        self._data = data[1]
        self.checks = {}
        self.selected = []

    @pyqtSlot(list)
    def update_item(self, value, role=Qt.DisplayRole):
        ix = self.index(len(value), 1)
        self.setData(ix, value, role)

    def setData(self, index, value, role):
        if role == Qt.DisplayRole:
            self._data = value
            try:
                if not self._data[0][0] == "ERROR":
                    self.layoutAboutToBeChanged.emit()
                    self.dataChanged.emit(index, index)
                    self.layoutChanged.emit()
                return True
            except Exception:
                pass
            self.layoutAboutToBeChanged.emit()
            self.dataChanged.emit(index, index)
            self.layoutChanged.emit()
        if role == Qt.CheckStateRole:
            if not self._data[0][0] == "ERROR":
                self.layoutAboutToBeChanged.emit()
                self.checks[QPersistentModelIndex(index)] = value
                selected_data_row = QPersistentModelIndex(index).row()

                selected_data = (
                    QPersistentModelIndex(index).model().index(selected_data_row, 0)
                )
                self.selected.append(selected_data.data())
                if self.selected.count(selected_data.data()) > 1:
                    self.selected.remove(selected_data.data())

                if self.checks[QPersistentModelIndex(index)] == 0:
                    self.selected.remove(selected_data.data())

                self.layoutChanged.emit()
                return True
        return False

    def data(self, index, role=Qt.DisplayRole):
        value = self._data[index.row()][index.column()]
        try:
            if not self._data[0][0] == "ERROR":
                if role == Qt.DisplayRole:
                    if isinstance(value, float):
                        return "\u20A6 {:,}".format(float(round(value, 2)))
                    return value
                elif role == Qt.TextAlignmentRole:
                    if index.column() == 1:
                        return Qt.AlignCenter
                elif role == Qt.CheckStateRole:
                    if index.column() == 0:
                        return self.checkState(QPersistentModelIndex(index))
            else:
                if role == Qt.DisplayRole:
                    return self._data[index.row()][1]
        except:
            pass
        if role == Qt.DisplayRole:
            return value

    def headerData(self, section, orientation, role):
        if orientation == Qt.Horizontal:
            if role == Qt.DisplayRole:
                try:
                    if self._data[0][0] == "ERROR":
                        header = ["Data"]
                except Exception:
                    pass
                header = ["Name", "Balance"]

                return header[section]
        if orientation == Qt.Vertical:
            if not self._data[0][0] == "ERROR":
                if role == Qt.TextAlignmentRole:
                    return Qt.AlignCenter
                return section + 1

    def sort(self, column, order):
        self.layoutAboutToBeChanged.emit()
        if order == Qt.DescendingOrder:
            self._data.sort()
        else:
            self._data.reverse()

        self.layoutChanged.emit()

    def rowCount(self, parent=QModelIndex()):
        return len(self._data)

    def columnCount(self, parent=QModelIndex()):
        try:
            if self._data[0][0] == "ERROR":
                return 1
        except Exception:
            pass
        return 2

    def checkState(self, index):
        if index in self.checks.keys():
            return self.checks[index]
        else:
            return Qt.Unchecked

    def flags(self, index):
        f1 = QAbstractTableModel.flags(self, index)
        f1 |= Qt.ItemIsEnabled | Qt.ItemIsUserCheckable
        return f1
