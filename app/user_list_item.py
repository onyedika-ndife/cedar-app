from datetime import datetime
from PyQt5.QtGui import QIcon, QDoubleValidator
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
    QToolBar,
    QLayout,
)
from PyQt5.QtCore import Qt, QDate
from .ldw_list_user import USER_LDW
from .user_add_form import ADD_USER


class USER(QWidget):
    def __init__(self, params, user_id):
        super().__init__()
        self.params = params
        self.user_id = user_id
        self.db = self.params["db"].conn.cursor()
        self.account = self.get_db_data()

        self._view()

    def _view(self):

        initial_layout = QVBoxLayout()
        initial_layout.setContentsMargins(0, 0, 0, 0)

        btn_widget = QWidget()
        btn_layout = QHBoxLayout()
        btn_layout.setContentsMargins(0, 0, 0, 0)
        btn_widget.setLayout(btn_layout)
        edit_btn = QPushButton("Edit Account")
        edit_btn.setToolTip("Edit account details")
        delete_btn = QPushButton("Delete Account")
        delete_btn.setToolTip("Delete current account")

        edit_btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        delete_btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        header = QLabel("Account Details")
        header.setObjectName("Header")

        btn_layout.addWidget(header, alignment=Qt.AlignLeft)
        btn_layout.addWidget(edit_btn, alignment=Qt.AlignRight)
        btn_layout.addWidget(delete_btn)

        initial_layout.addWidget(btn_widget)

        edit_btn.clicked.connect(lambda: self._handle_toolbar_btn({"text": "edit"}))
        delete_btn.clicked.connect(lambda: self._handle_toolbar_btn({"text": "delete"}))

        scrollArea = QScrollArea()
        main_widget = QWidget()
        main_widget_layout = QGridLayout()
        main_widget.setLayout(main_widget_layout)
        scrollArea.setWidget(main_widget)
        scrollArea.setWidgetResizable(True)

        group_1 = QGroupBox("Personal Details")
        group_1.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        group_1_layout = QGridLayout()
        group_1.setLayout(group_1_layout)

        # positions = [(i, j) for i in range(5) for j in range(4)]
        rows = [(i, 0) for i in range(len(self.account["details"].items()))]
        columns = []

        for row, item in zip(rows, self.account["details"].keys()):
            group_1_layout.addWidget(QLabel(item), *row)
            columns.append((row[0], 1))
        for column, item in zip(columns, self.account["details"].values()):
            group_1_layout.addWidget(
                QLabel(str(item)), *column, alignment=Qt.AlignRight
            )

        group_2 = QGroupBox("Next of Kin")
        group_2.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        group_2_layout = QGridLayout()
        group_2.setLayout(group_2_layout)

        rows = [(i, 0) for i in range(len(self.account["next_of_kin"].items()))]

        for row, item in zip(rows, self.account["next_of_kin"].keys()):
            group_2_layout.addWidget(QLabel(item), *row)
            columns.append((row[0], 1))
        for column, item in zip(columns, self.account["next_of_kin"].values()):
            group_2_layout.addWidget(
                QLabel(str(item)), *column, alignment=Qt.AlignRight
            )

        group_3 = QGroupBox("Company")
        group_3.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        group_3_layout = QGridLayout()
        group_3.setLayout(group_3_layout)

        rows = [(i, 0) for i in range(len(self.account["company"].items()))]

        for row, item in zip(rows, self.account["company"].keys()):
            group_3_layout.addWidget(QLabel(item), *row)
            columns.append((row[0], 1))
        for column, item in zip(columns, self.account["company"].values()):
            group_3_layout.addWidget(
                QLabel(str(item)), *column, alignment=Qt.AlignRight
            )

        _left_layout = QVBoxLayout()

        group_4 = QGroupBox("Savings")
        group_4.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        group_4_layout = QGridLayout()
        group_4.setLayout(group_4_layout)

        rows = [(i, 0) for i in range(len(self.account["savings"].items()))]

        for row, item in zip(rows, self.account["savings"].keys()):
            group_4_layout.addWidget(QLabel(item), *row)
            columns.append((row[0], 1))
        for column, item in zip(columns, self.account["savings"].values()):
            group_4_layout.addWidget(
                QLabel(str(item)), *column, alignment=Qt.AlignRight
            )

        group_5 = QGroupBox("Last Loan")
        group_5.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        group_5_layout = QGridLayout()
        group_5.setLayout(group_5_layout)

        if len(self.account["last_loan"].items()) > 0:
            rows = [(i, 0) for i in range(len(self.account["last_loan"].items()))]
            for row, item in zip(rows, self.account["last_loan"].keys()):
                group_5_layout.addWidget(QLabel(item), *row)
                columns.append((row[0], 1))
            for column, item in zip(columns, self.account["last_loan"].values()):
                group_5_layout.addWidget(
                    QLabel(str(item)), *column, alignment=Qt.AlignRight
                )
            go_loan = QPushButton("View Loans")
            go_loan.clicked.connect(lambda: self._go_to({"text": go_loan.text()}))
            group_5_layout.addWidget(
                go_loan, len(self.account["last_loan"].items()) + 1, 0, 1, 0
            )
        else:
            no_data = QLabel("No recent Loan")
            no_data.setObjectName("no_data")
            group_5_layout.addWidget(no_data, 0, 0, 1, 0)

        group_6 = QGroupBox("Last Deposit")
        group_6.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        group_6_layout = QGridLayout()
        group_6.setLayout(group_6_layout)

        if len(self.account["last_deposit"].items()) > 0:
            rows = [(i, 0) for i in range(len(self.account["last_deposit"].items()))]

            for row, item in zip(rows, self.account["last_deposit"].keys()):
                group_6_layout.addWidget(QLabel(item), *row)
                columns.append((row[0], 1))
            for column, item in zip(columns, self.account["last_deposit"].values()):
                group_6_layout.addWidget(
                    QLabel(str(item)), *column, alignment=Qt.AlignRight
                )

            go_deposit = QPushButton("View Deposits")
            go_deposit.clicked.connect(lambda: self._go_to({"text": go_deposit.text()}))
            group_6_layout.addWidget(
                go_deposit, len(self.account["last_deposit"].items()) + 1, 0, 1, 0
            )
        else:
            no_data = QLabel("No recent Deposit")
            no_data.setObjectName("no_data")
            group_6_layout.addWidget(no_data, 0, 0, 1, 0)

        group_7 = QGroupBox("Last Withdrawal")
        group_7.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        group_7_layout = QGridLayout()
        group_7.setLayout(group_7_layout)

        if len(self.account["last_withdrawal"].items()) > 0:
            rows = [(i, 0) for i in range(len(self.account["last_withdrawal"].items()))]

            for row, item in zip(rows, self.account["last_withdrawal"].keys()):
                group_7_layout.addWidget(QLabel(item), *row)
                columns.append((row[0], 1))
            for column, item in zip(columns, self.account["last_withdrawal"].values()):
                group_7_layout.addWidget(
                    QLabel(str(item)), *column, alignment=Qt.AlignRight
                )

            go_withdraw = QPushButton("View Withdrawals")
            go_withdraw.clicked.connect(
                lambda: self._go_to({"text": go_withdraw.text()})
            )
            group_7_layout.addWidget(
                go_withdraw, len(self.account["last_withdrawal"].items()) + 1, 0, 1, 0
            )
        else:
            no_data = QLabel("No recent Withdrawal")
            no_data.setObjectName("no_data")
            group_7_layout.addWidget(no_data, 0, 0, 1, 0)

        _left_layout.addWidget(group_4)
        _left_layout.addWidget(group_5)
        _left_layout.addWidget(group_6)
        _left_layout.addWidget(group_7, alignment=Qt.AlignTop)

        main_widget_layout.addWidget(group_1, 0, 0)
        main_widget_layout.addWidget(group_2, 1, 0)
        main_widget_layout.addWidget(group_3, 2, 0, alignment=Qt.AlignTop)
        main_widget_layout.addLayout(_left_layout, 0, 1, 0, 1)
        initial_layout.addWidget(scrollArea)
        self.setLayout(initial_layout)

    def _go_to(self, params):
        text = params["text"].lower().replace("view ", "")
        view = USER_LDW(self.params, self.user_id, text)
        self.params["next"]["widget"].addWidget(view)
        self.params["next"]["widget"].setCurrentWidget(view)

    def _handle_toolbar_btn(self, params):
        if params["text"] == "edit":
            view = ADD_USER(self.params, user=self.account)
            self.params["next"]["widget"].addWidget(view)
            self.params["next"]["widget"].setCurrentWidget(view)
        elif params["text"] == "delete":
            msg = QMessageBox()
            msg.setWindowTitle("Account Deletion")
            msg.setIcon(QMessageBox.Question)
            msg.setText(f"Are you sure you want to delete this account?")
            msg.setStandardButtons(QMessageBox.No | QMessageBox.Yes)
            msg.setDefaultButton(QMessageBox.Yes)
            msg.buttonClicked.connect(self._delete)
            msg.exec_()
            msg.show()

    def _delete(self, choice):
        if choice.text() == "&Yes":
            self.db.execute(
                """DELETE FROM users WHERE id=?;""", (self.account["details"]["id"],)
            )
            self.db.execute(
                """DELETE FROM next_of_kin WHERE user_id=?;""",
                (self.account["details"]["id"],),
            )
            self.db.execute(
                """DELETE FROM company WHERE user_id=?;""",
                (self.account["details"]["id"],),
            )
            self.db.execute(
                """DELETE FROM savings WHERE user_id=?;""",
                (self.account["details"]["id"],),
            )
            self.db.execute(
                """DELETE FROM loans WHERE user_id=?;""",
                (self.account["details"]["id"],),
            )
            self.db.execute(
                """DELETE FROM next_of_kin WHERE user_id=?;""",
                (self.account["details"]["id"],),
            )
            self.db.execute(
                """DELETE FROM withdrawals WHERE user_id=?;""",
                (self.account["details"]["id"],),
            )
            self.db.execute(
                """DELETE FROM deposits WHERE user_id=?;""",
                (self.account["details"]["id"],),
            )
            self.params["db"].conn.commit()

    def get_db_data(self):
        account = {
            "details": {},
            "next_of_kin": {},
            "company": {},
            "savings": {},
            "last_loan": {},
            "last_deposit": {},
            "last_withdrawal": {},
        }
        self.db.execute("""SELECT * FROM users WHERE id=?;""", (self.user_id,))
        for item in self.db.fetchall():
            account["details"]["id"] = item[0]
            account["details"]["Name"] = f"{item[3]} {item[2]} {item[1]}"
            account["details"]["Date of Birth"] = datetime.strptime(
                item[4], "%Y-%m-%d"
            ).strftime("%b %d, %Y")
            account["details"]["Phonenumber"] = item[5]
            account["details"]["Email"] = item[6]
            account["details"]["Address"] = item[7]
            account["details"]["Member or Staff"] = item[8].capitalize()
            account["details"]["Account Status"] = item[9].capitalize()
            account["details"]["Date Registered"] = datetime.strptime(
                item[10], "%Y-%m-%d %H:%M:%S"
            ).strftime("%b %d, %Y  %H:%M")

        self.db.execute(
            """SELECT * FROM next_of_kin WHERE user_id=?;""", (self.user_id,)
        )
        for item in self.db.fetchall():
            account["next_of_kin"]["Name"] = f"{item[3]} {item[2]} {item[1]}"
            account["next_of_kin"]["Phonenumber"] = item[4]
            account["next_of_kin"]["Address"] = item[5]
            account["next_of_kin"]["Relationship"] = item[6]

        self.db.execute("""SELECT * FROM company WHERE user_id=?;""", (self.user_id,))
        for item in self.db.fetchall():
            account["company"]["Name"] = item[1]
            account["company"]["Telephone"] = item[2]
            account["company"]["Address"] = item[3]

        self.db.execute("""SELECT * FROM savings WHERE user_id=?;""", (self.user_id,))
        for item in self.db.fetchall():
            account["savings"]["Balance"] = "\u20A6 {:,}".format(int(item[1]))
            account["savings"]["Interest Earned"] = "\u20A6 {:,}".format(int(item[2]))
            account["savings"]["Total Amount"] = "\u20A6 {:,}".format(int(item[3]))
            account["savings"]["Last Updated"] = datetime.strptime(
                item[4], "%Y-%m-%d %H:%M:%S"
            ).strftime("%b %d, %Y  %H:%M")

        self.db.execute(
            """SELECT * FROM loans WHERE user_id=? ORDER BY id DESC LIMIT 1;""",
            (self.user_id,),
        )
        loan = self.db.fetchall()
        if len(loan) > 0:
            for item in loan:
                account["last_loan"]["Amount"] = "\u20A6 {:,}".format(int(item[1]))
                account["last_loan"]["First Guarantor"] = item[2]
                account["last_loan"]["Second Guarantor"] = item[3]
                account["last_loan"]["Clear Amount"] = "\u20A6 {:,}".format(
                    int(item[4])
                )
                account["last_loan"]["Current Liability"] = "\u20A6 {:,}".format(
                    int(item[5])
                )
                account["last_loan"]["Loan Status"] = item[6].capitalize()
                account["last_loan"]["Loan Duration"] = item[7].capitalize()
                account["last_loan"]["Due Date"] = datetime.strptime(
                    item[8], "%Y-%m-%d"
                ).strftime("%b %d, %Y")
                account["last_loan"]["Date Issued"] = datetime.strptime(
                    item[9], "%Y-%m-%d %H:%M:%S"
                ).strftime("%b %d, %Y  %H:%M")

            self.db.execute(
                """SELECT * FROM users WHERE id=?;""",
                (account["last_loan"]["First Guarantor"],),
            )
            for item in self.db.fetchall():
                account["last_loan"][
                    "First Guarantor"
                ] = f"{item[3]} {item[2]} {item[1]}"
            self.db.execute(
                """SELECT * FROM users WHERE id=?;""",
                (account["last_loan"]["Second Guarantor"],),
            )
            for item in self.db.fetchall():
                account["last_loan"][
                    "Second Guarantor"
                ] = f"{item[3]} {item[2]} {item[1]}"

        self.db.execute(
            """SELECT * FROM deposits WHERE user_id=? ORDER BY id DESC LIMIT 1;""",
            (self.user_id,),
        )
        deposit = self.db.fetchall()
        if len(deposit) > 0:
            for item in deposit:
                account["last_deposit"]["Amount"] = "\u20A6 {:,}".format(int(item[1]))
                account["last_deposit"]["Date Deposited"] = datetime.strptime(
                    item[2], "%Y-%m-%d %H:%M:%S"
                ).strftime("%b %d, %Y  %H:%M")

        self.db.execute(
            """SELECT * FROM withdrawals WHERE user_id=? ORDER BY id DESC LIMIT 1;""",
            (self.user_id,),
        )
        withdrawal = self.db.fetchall()
        if len(withdrawal) > 0:
            for item in withdrawal:
                account["last_withdrawal"]["Amount"] = "\u20A6 {:,}".format(
                    int(item[1])
                )
                account["last_withdrawal"]["Date Withdrawn"] = datetime.strptime(
                    item[2], "%Y-%m-%d %H:%M:%S"
                ).strftime("%b %d, %Y  %H:%M")

        return account
