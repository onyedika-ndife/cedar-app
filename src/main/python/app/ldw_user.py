import sqlite3
from datetime import datetime, timedelta

from apscheduler.triggers.interval import IntervalTrigger
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from app import Worker, db_file


class USER_LDW(QWidget):
    def __init__(self, params, user_id, context):
        super().__init__()
        self.params = params
        self.user_id = user_id
        self.context = context

        self.search_date = {"from": None, "to": None}
        self.for_account = "member"
        self.selected_list = None

        self.table_data = self._get_data_db()

        self.threadpool = QThreadPool()

        self._view()

    def _view(self):
        self.initial_layout = QVBoxLayout()
        self.initial_layout.setContentsMargins(0, 0, 0, 0)
        header_layout = QGridLayout()
        header_layout.setContentsMargins(0, 0, 0, 0)
        last_index = self.context.rfind("s")
        new_context = self.context[:last_index]
        label = QLabel(f"{new_context.capitalize()} History for")
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

        btn_widget = QWidget()
        btn_layout = QHBoxLayout()
        btn_layout.setContentsMargins(0, 0, 0, 0)
        btn_widget.setLayout(btn_layout)

        self.sel_chk = QCheckBox("Select")
        self.sel_chk.clicked.connect(
            lambda: self._handle_toolbar_btn({"text": "select", "self": self.sel_chk})
        )
        self.del_sel_btn = QPushButton(
            QIcon(self.params["ctx"].get_resource("icon/delete.png")), "Delete Selected"
        )
        self.del_sel_btn.setDisabled(True)

        self.sel_chk.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.del_sel_btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self.del_sel_btn.clicked.connect(
            lambda: self._handle_toolbar_btn({"text": "delete"})
        )

        btn_layout.addWidget(self.sel_chk)
        btn_layout.addWidget(self.del_sel_btn)

        header_layout.addWidget(btn_widget, 2, 0, alignment=Qt.AlignLeft)

        date_lay = QHBoxLayout()
        self.search_int_date_from = QDateEdit(calendarPopup=True)
        self.search_int_date_from.setDate(
            QDate(
                datetime.today().year, datetime.today().month, datetime.today().day - 1
            )
        )
        self.search_int_date_from.setFixedWidth(150)
        date_lay.addWidget(QLabel("Search from:"), alignment=Qt.AlignRight)
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
        self.model = LDWUSERTABLE(data=data, context=self.context)
        self.table_view = QTableView()
        self.table_view.setModel(self.model)
        # self.table_view.setSortingEnabled(True)
        self.table_view.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table_view.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table_view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_view.horizontalHeader().setStretchLastSection(True)
        self.table_view.horizontalHeader().setMinimumSectionSize(140)
        self.table_view.verticalHeader().setMinimumWidth(30)
        self.table_view.verticalHeader().setDefaultAlignment(Qt.AlignCenter)

        self.table_view.clicked.connect(self._check)

    def _handle_toolbar_btn(self, params):
        if params["text"] == "select":
            self.sel_chk.setTristate(False)
            for row in range(self.model.rowCount()):
                for column in range(self.model.columnCount()):
                    item = self.model.index(row, column)
                    if params["self"].isChecked():
                        if item.column() == 0:
                            self.model.setData(item, 2, Qt.CheckStateRole)
                        self.del_sel_btn.setDisabled(False)
                    else:
                        self.model.setData(item, 0, Qt.CheckStateRole)
                        self.del_sel_btn.setDisabled(True)
            self.selected_list = self.model.selected

        elif params["text"] == "delete":
            msg = QMessageBox()
            msg.setStyleSheet(
                open(self.params["ctx"].get_resource("css/style.css")).read()
            )
            context = self.context[:-1].capitalize()

            msg.setWindowTitle(f"{context} Deletion")
            msg.setIconPixmap(
                QPixmap(self.params["ctx"].get_resource("icon/question.png"))
            )
            msg.setText(f"Are you sure you want to delete selected {context}(s)?")
            msg.setStandardButtons(QMessageBox.No | QMessageBox.Yes)
            msg.setDefaultButton(QMessageBox.Yes)
            msg.buttonClicked.connect(self._del_selected)
            msg.exec_()
            msg.show()

    def _check(self, i):
        check_state = i.model().checkState(QPersistentModelIndex(i))
        i.model().setData(i, 0 if check_state == 2 else 2, Qt.CheckStateRole)

        self.sel_chk.setTristate(True)
        if len(i.model().selected) > 0:
            self.selected_list = i.model().selected
            self.del_sel_btn.setDisabled(False)
            if len(i.model()._data) == len(self.selected_list):
                self.sel_chk.setCheckState(2)
            else:
                self.sel_chk.setCheckState(1)
        else:
            self.sel_chk.setCheckState(0)
            self.del_sel_btn.setDisabled(True)

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
            """SELECT name FROM users WHERE id=?;""",
            (self.user_id,),
        )
        name = self.db.fetchone()
        self.user = name[0]

        if self.context == "loans":
            self.db.execute(
                """SELECT * FROM loans WHERE user_id=? ORDER BY id DESC;""",
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
                loan.append(datetime.strptime(item[9], "%Y-%m-%d"))
                data.append(loan)
        elif self.context == "deposits":
            self.db.execute(
                """SELECT * FROM deposits WHERE user_id=? ORDER BY id DESC;""",
                (self.user_id,),
            )
            deposits = self.db.fetchall()
            for item in deposits:
                deposit = []
                deposit.append(item[1])
                deposit.append(datetime.strptime(item[2], "%Y-%m-%d"))
                data.append(deposit)
        elif self.context == "withdrawals":
            self.db.execute(
                """SELECT * FROM withdrawals WHERE user_id=? ORDER BY id DESC;""",
                (self.user_id,),
            )
            withdrawals = self.db.fetchall()
            for item in withdrawals:
                withdrawal = []
                withdrawal.append(item[1])
                withdrawal.append(datetime.strptime(item[3], "%Y-%m-%d"))
                data.append(withdrawal)
        return data

    def _del_selected(self, choice):
        if choice.text() == "&Yes":
            for item in self.selected_list:
                self.db.execute(
                    """SELECT balance, interest_earned, total FROM savings WHERE user_id=?;""",
                    (self.user_id,),
                )
                savings = self.db.fetchone()

                bal = savings[0]
                sav_intr = savings[1]
                total = savings[2]

                if self.context == "loans":
                    amt = item[0].replace("\u20A6 ", "").replace(",", "")
                    date = datetime.strptime(item[1], "%B %d, %Y").strftime("%Y-%m-%d")

                    self.db.execute(
                        """DELETE FROM apscheduler_jobs WHERE apscheduler_jobs.id=?;""",
                        (f"{self.user} loan schedule",),
                    )

                    self.db.execute(
                        """DELETE FROM loans WHERE user_id=? AND amount=? AND date_issued=?;""",
                        (self.user_id, amt, date),
                    )

                    self.params["db"].conn.commit()
                elif self.context == "deposits":
                    amt = item[0].replace("+\u20A6 ", "").replace(",", "")
                    date = datetime.strptime(item[1], "%B %d, %Y").strftime("%Y-%m-%d")

                    self.db.execute(
                        """SELECT id FROM deposits WHERE user_id=? AND amount=? AND date=?;""",
                        (self.user_id, amt, date),
                    )
                    dep_id = self.db.fetchone()[0]

                    self.db.execute(
                        """SELECT interest FROM deposit_interest WHERE user_id=? AND amount=? AND date_added=? AND deposit_id=?;""",
                        (self.user_id, amt, date, dep_id),
                    )
                    dep_intr = self.db.fetchone()
                    dep_intr = dep_intr[0] if not dep_intr is None else 0.0
                    bal = float(bal) - float(amt)
                    sav_intr = float(sav_intr) - float(dep_intr)
                    total = float(total) - float(amt) - float(dep_intr)

                    self.db.execute(
                        """UPDATE savings SET
                            balance=?,
                            interest_earned=?,
                            total=? WHERE user_id=?;""",
                        (
                            bal,
                            sav_intr,
                            total,
                            self.user_id,
                        ),
                    )

                    self.db.execute(
                        """DELETE FROM deposit_interest WHERE
                            user_id=? AND
                            amount=? AND
                            date_added=? AND
                            deposit_id=?;""",
                        (
                            self.user_id,
                            amt,
                            date,
                            dep_id,
                        ),
                    )

                    self.db.execute(
                        """DELETE FROM apscheduler_jobs WHERE
                            apscheduler_jobs.id=?;""",
                        (f"dep_{dep_id} interest schedule",),
                    )

                    self.db.execute(
                        """DELETE FROM deposits WHERE
                            id=? AND
                            user_id=? AND
                            amount=? AND
                            date=?;""",
                        (
                            dep_id,
                            self.user_id,
                            amt,
                            date,
                        ),
                    )
                    self.params["db"].conn.commit()
                elif self.context == "withdrawals":
                    amt = item[0].replace("-\u20A6 ", "").replace(",", "")
                    date = datetime.strptime(item[1], "%B %d, %Y").strftime("%Y-%m-%d")
                    self.db.execute(
                        """SELECT withdrawn_from FROM withdrawals WHERE user_id=? AND amount=? AND date=?;""",
                        (self.user_id, amt, date),
                    )
                    with_from = self.db.fetchone()[0]
                    if with_from == "balance":
                        bal = float(bal) + float(amt)
                        total = float(total) + float(amt)
                        self.db.execute(
                            """UPDATE savings SET balance=?, total=? WHERE user_id=?;""",
                            (
                                bal,
                                total,
                                self.user_id,
                            ),
                        )
                        self.db.execute(
                            """SELECT 
                            deleted_amount,
                            deleted_date 
                            FROM deleted WHERE user_id=? AND date=?;""",
                            (
                                self.user_id,
                                date,
                            ),
                        )
                        deleted = self.db.fetchone()

                        self.db.execute(
                            f"""INSERT INTO deposits (
                                amount,
                                date,
                                user_id) VALUES (?,?,?);""",
                            (
                                amt,
                                deleted[1],
                                self.user_id,
                            ),
                        )
                        self.db.execute(
                            """SELECT id FROM deposits ORDER BY id DESC LIMIT 1;"""
                        )
                        last_deposit_id = self.db.fetchone()[0]
                        self.db.execute(
                            f"""INSERT INTO deposit_interest (
                                amount,
                                date_added,
                                deposit_id,
                                user_id) VALUES (?,?,?,?);""",
                            (
                                amt,
                                deleted[1],
                                last_deposit_id,
                                self.user_id,
                            ),
                        )

                        self.db.execute(
                            """DELETE FROM withdrawals WHERE user_id=? AND amount=? AND date=?;""",
                            (self.user_id, amt, date),
                        )

                        self.params["db"].conn.commit()

                        interest_start = datetime.strptime(
                            deleted[1], "%Y-%m-%d"
                        ) + timedelta(weeks=13.036)

                        deposit_interval = IntervalTrigger(
                            days=1,
                            start_date=interest_start.strftime("%Y-%m-%d %H:%M:%S"),
                        )

                        self.params["qtsched"].add_job(
                            self.interest_schedule,
                            trigger=deposit_interval,
                            args=[
                                self.user_id,
                                last_deposit_id,
                            ],
                            id=f"dep_{last_deposit_id} interest schedule",
                            replace_existing=True,
                        )

                    elif with_from == "interest":
                        sav_intr = float(sav_intr) + float(amt)
                        total = float(total) + float(amt)
                        self.db.execute(
                            """UPDATE savings SET interest_earned=?, total=? WHERE user_id=?;""",
                            (
                                sav_intr,
                                total,
                                self.user_id,
                            ),
                        )
                        self.db.execute(
                            """DELETE FROM withdrawals WHERE user_id=? AND amount=? AND date=?;""",
                            (self.user_id, amt, date),
                        )

                        self.params["db"].conn.commit()

            msg = QMessageBox()
            msg.setStyleSheet(
                open(self.params["ctx"].get_resource("css/style.css")).read()
            )
            msg.setWindowTitle(f"{self.context[:-1].capitalize()} Deletion")
            msg.setIconPixmap(
                QPixmap(self.params["ctx"].get_resource("icon/success.png"))
            )
            msg.setText(f"{self.context[:-1].capitalize()} deleted successfully")
            msg.setDefaultButton(QMessageBox.Ok)
            msg.buttonClicked.connect(self._back)
            msg.exec_()
            msg.show()

    def _back(self):
        self.params["parent"]["back_btn"].click()
        self.params["parent"]["back_btn"].click()

    @staticmethod
    def interest_schedule(user_id, deposit_id):
        conn = sqlite3.connect(db_file)

        db = conn.cursor()
        db.execute("""SELECT account_type FROM users WHERE id=?;""", (user_id,))
        account = db.fetchone()
        account_type = account[0]
        status = account[1]

        if status == "active":
            db.execute(
                """SELECT * FROM deposit_interest WHERE deposit_id=? AND user_id=?;""",
                (deposit_id, user_id),
            )
            deposit_interest = db.fetchone()

            if not deposit_interest is None:
                run_time = deposit_interest[6]
                run_time += 1
                date_added = deposit_interest[3]
                date_elapsed = datetime.strptime(
                    date_added, "%Y-%m-%d"
                ).date() + timedelta(days=run_time)
                amount = deposit_interest[1]

                db.execute(
                    """SELECT interest_rate FROM settings WHERE account_type=? ORDER BY id DESC LIMIT 1;""",
                    (account_type,),
                )
                interest_rate = db.fetchone()[0]
                interest_rate_per_day = float(interest_rate) / 100 / 365

                interest_per_day = float(deposit_interest[2])

                cal = 0
                db.execute(
                    """SELECT interest_earned, total FROM savings WHERE user_id=?;""",
                    (user_id,),
                )
                sav_intr = db.fetchone()
                intr_earned = sav_intr[0]
                total = sav_intr[1]

                if interest_per_day == 0.0:
                    db.execute(
                        """SELECT interest_start FROM settings WHERE account_type=? ORDER BY id DESC LIMIT 1;""",
                        (account_type,),
                    )
                    intr_start = db.fetchone()[0]
                    ins = intr_start.split(" ")
                    time = ins[1].lower().replace("(s)", "")

                    if time == "year":
                        time = 365 * int(ins[0])
                    elif time == "month":
                        time = 30.417 * int(ins[0])

                    _months = time
                    _months_interest = _months * interest_rate_per_day * float(amount)

                    interest_per_day += _months_interest

                    db.execute(
                        """UPDATE deposit_interest SET
                            interest=?,
                            date_interest_start=?,
                            date_last_interest=?,
                            run_time=? WHERE deposit_id=? AND user_id=?;
                        """,
                        (
                            round(interest_per_day),
                            date_elapsed.strftime("%Y-%m-%d"),
                            date_elapsed.strftime("%Y-%m-%d"),
                            run_time,
                            deposit_id,
                            user_id,
                        ),
                    )
                    intr_earned += round(interest_per_day)
                    total += round(interest_per_day)
                else:
                    cal = float(amount) * float(interest_rate_per_day)
                    interest_per_day += cal

                    db.execute(
                        """UPDATE deposit_interest SET
                            interest=?,
                            date_last_interest=?,
                            run_time=? WHERE deposit_id=? AND user_id=?;""",
                        (
                            round(interest_per_day),
                            date_elapsed.strftime("%Y-%m-%d"),
                            run_time,
                            deposit_id,
                            user_id,
                        ),
                    )

                    intr_earned += round(cal)
                    total += round(cal)

                db.execute(
                    """UPDATE savings SET
                        interest_earned=?,
                        total=?,
                        date_updated=? WHERE user_id=?;""",
                    (
                        round(intr_earned),
                        round(total),
                        date_elapsed.strftime("%Y-%m-%d"),
                        user_id,
                    ),
                )
                conn.commit()
                db.close()


class LDWUSERTABLE(QAbstractTableModel):
    def __init__(self, data, context):
        super(LDWUSERTABLE, self).__init__()
        self._data = data
        self.context = context
        self.checks = {}
        self.selected = []

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
            self.layoutAboutToBeChanged.emit()
            self.dataChanged.emit(index, index)
            self.layoutChanged.emit()
            return True
        if role == Qt.CheckStateRole:
            self.layoutAboutToBeChanged.emit()
            self.checks[QPersistentModelIndex(index)] = value
            selected_data_row = QPersistentModelIndex(index).row()
            if self.context == "deposits" or self.context == "withdrawals":
                selected_data_column_1_data = (
                    QPersistentModelIndex(index).model().index(selected_data_row, 0)
                )
                selected_data_column_2_data = (
                    QPersistentModelIndex(index).model().index(selected_data_row, 1)
                )
            else:
                selected_data_column_1_data = (
                    QPersistentModelIndex(index).model().index(selected_data_row, 0)
                )
                selected_data_column_2_data = (
                    QPersistentModelIndex(index).model().index(selected_data_row, 8)
                )
            selected_data = []
            selected_data.append(selected_data_column_1_data.data())
            selected_data.append(selected_data_column_2_data.data())

            self.selected.append(selected_data)
            if self.selected.count(selected_data) > 1:
                self.selected.remove(selected_data)

            if self.checks[QPersistentModelIndex(index)] == 0:
                self.selected.remove(selected_data)
            self.layoutChanged.emit()
            return True
        return False

    def data(self, index, role):
        value = self._data[index.row()][index.column()]
        if role == Qt.DisplayRole:
            if isinstance(value, datetime):
                return value.strftime("%B %d, %Y")
            if isinstance(value, float):
                if self.context == "loans":
                    return "\u20A6 {:,}".format(float(round(value, 2)))
                elif self.context == "deposits":
                    return "+\u20A6 {:,}".format(float(round(value, 2)))
                elif self.context == "withdrawals":
                    return "-\u20A6 {:,}".format(float(round(value, 2)))
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
        if role == Qt.CheckStateRole:
            if index.column() == 0:
                return self.checkState(QPersistentModelIndex(index))

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
        if order == Qt.DescendingOrder:
            self._data.sort()
        else:
            self._data.reverse()
        self.layoutChanged.emit()

    def rowCount(self, parent=QModelIndex()):
        return len(self._data)

    def columnCount(self, parent=QModelIndex()):
        try:
            return len(self._data[0])
        except Exception:
            if self.context == "loans" or self.context == "clear_loans":
                return 9
            elif self.context == "deposits" or self.context == "withdrawals":
                return 2

    def checkState(self, index):
        if index in self.checks.keys():
            return self.checks[index]
        else:
            return Qt.Unchecked

    def flags(self, index):
        return super(QAbstractTableModel, self).flags(index) | Qt.ItemIsUserCheckable
