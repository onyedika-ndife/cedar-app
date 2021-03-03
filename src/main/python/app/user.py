from datetime import datetime

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from app.ldw_user import USER_LDW
from app.user_add import ADD_USER


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
        edit_btn = QPushButton(
            QIcon(self.params["ctx"].get_resource("icon/edit_profile.png")),
            "Edit Account",
        )
        edit_btn.setToolTip("Edit account details")
        delete_btn = QPushButton(
            QIcon(self.params["ctx"].get_resource("icon/delete_user.png")),
            "Delete Account",
        )
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
        pro_pic_lay = QGridLayout()
        picture = QLabel()
        picture.setScaledContents(True)
        picture.setFixedSize(150, 150)
        pro_pic_lay.addWidget(picture, 0, 0, 4, 1)

        rows = [(i, 1) for i in range(0, 4)]

        columns = []
        keys = list(self.account["details"].keys())

        for row, item in zip(rows, keys[1:5]):
            label = QLabel(f"{item}:")
            label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            if row == (3, 1):
                pro_pic_lay.addWidget(label, *row, alignment=Qt.AlignTop)
            else:
                pro_pic_lay.addWidget(label, *row)
            columns.append((row[0], 2))
        values = list(self.account["details"].values())
        if not values[0] == "":
            picture.setPixmap(QPixmap(values[0]))
        else:
            picture.setPixmap(
                QPixmap(self.params["ctx"].get_resource("image/avatar.png"))
            )

        for column, item in zip(columns, values[1:5]):
            label = QLabel(str(item if not item == "" else "-"))
            label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            label.setAlignment(Qt.AlignRight)
            if column == (3, 2):
                pro_pic_lay.addWidget(label, *column, alignment=Qt.AlignTop)
            else:
                pro_pic_lay.addWidget(label, *column)

        group_1_layout.addLayout(pro_pic_lay, 0, 0, 1, 2)

        rows = [
            (i, 0)
            for i in range(
                len(self.account["details"].items()) - 5,
                len(self.account["details"].items()),
            )
        ]
        columns = []
        for row, item in zip(rows, keys[5:]):
            group_1_layout.addWidget(QLabel(f"{item}:"), *row)
            columns.append((row[0], 1))

        for column, item in zip(columns, values[5:]):
            group_1_layout.addWidget(
                QLabel(str(item if not item == "" else "-")),
                *column,
                alignment=Qt.AlignRight,
            )

        group_2 = QGroupBox("Next of Kin")
        group_2.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        group_2_layout = QGridLayout()
        group_2.setLayout(group_2_layout)

        rows = [(i, 0) for i in range(len(self.account["next_of_kin"].items()))]
        columns = []
        for row, item in zip(rows, self.account["next_of_kin"].keys()):
            group_2_layout.addWidget(QLabel(f"{item}:"), *row)
            columns.append((row[0], 1))
        for column, item in zip(columns, self.account["next_of_kin"].values()):
            group_2_layout.addWidget(
                QLabel(str(item if not item.rstrip() == "" else "-")),
                *column,
                alignment=Qt.AlignRight,
            )

        group_3 = QGroupBox("Company")
        group_3.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        group_3_layout = QGridLayout()
        group_3.setLayout(group_3_layout)

        rows = [(i, 0) for i in range(len(self.account["company"].items()))]
        columns = []
        for row, item in zip(rows, self.account["company"].keys()):
            group_3_layout.addWidget(QLabel(f"{item}:"), *row)
            columns.append((row[0], 1))
        for column, item in zip(columns, self.account["company"].values()):
            group_3_layout.addWidget(
                QLabel(str(item if not item == "" else "-")),
                *column,
                alignment=Qt.AlignRight,
            )

        _left_layout = QVBoxLayout()

        group_4 = QGroupBox("Savings")
        group_4.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        group_4_layout = QGridLayout()
        group_4.setLayout(group_4_layout)

        rows = [(i, 0) for i in range(len(self.account["savings"].items()))]
        columns = []
        for row, item in zip(rows, self.account["savings"].keys()):
            group_4_layout.addWidget(QLabel(f"{item}:"), *row)
            columns.append((row[0], 1))
        for column, item in zip(columns, self.account["savings"].values()):
            group_4_layout.addWidget(
                QLabel(str(item if not item == "" else "-")),
                *column,
                alignment=Qt.AlignRight,
            )

        group_5 = QGroupBox("Last Loan")
        group_5.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        group_5_layout = QGridLayout()
        group_5.setLayout(group_5_layout)

        if len(self.account["last_loan"].items()) > 0:
            rows = [(i, 0) for i in range(len(self.account["last_loan"].items()))]
            columns = []
            for row, item in zip(rows, self.account["last_loan"].keys()):
                group_5_layout.addWidget(QLabel(f"{item}:"), *row)
                columns.append((row[0], 1))
            for column, item in zip(columns, self.account["last_loan"].values()):
                group_5_layout.addWidget(
                    QLabel(str(item if not item == "" else "-")),
                    *column,
                    alignment=Qt.AlignRight,
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
            columns = []

            for row, item in zip(rows, self.account["last_deposit"].keys()):
                group_6_layout.addWidget(QLabel(f"{item}:"), *row)
                columns.append((row[0], 1))
            for column, item in zip(columns, self.account["last_deposit"].values()):
                group_6_layout.addWidget(
                    QLabel(str(item if not item == "" else "-")),
                    *column,
                    alignment=Qt.AlignRight,
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
            columns = []

            for row, item in zip(rows, self.account["last_withdrawal"].keys()):
                group_7_layout.addWidget(QLabel(f"{item}:"), *row)
                columns.append((row[0], 1))
            for column, item in zip(columns, self.account["last_withdrawal"].values()):
                group_7_layout.addWidget(
                    QLabel(str(item if not item == "" else "-")),
                    *column,
                    alignment=Qt.AlignRight,
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
            msg.setStyleSheet(
                open(self.params["ctx"].get_resource("css/style.css")).read()
            )
            msg.setWindowTitle("Account Deletion")
            msg.setIconPixmap(
                QPixmap(self.params["ctx"].get_resource("icon/question.png"))
            )
            msg.setText(f"Are you sure you want to delete this account?")
            msg.setStandardButtons(QMessageBox.No | QMessageBox.Yes)
            msg.setDefaultButton(QMessageBox.Yes)
            msg.buttonClicked.connect(self._delete)
            msg.exec_()
            msg.show()

    def _delete(self, choice):
        if choice.text() == "&Yes":
            self.db.execute(
                """SELECT id FROM deposits WHERE user_id=?""",
                (self.account["details"]["id"],),
            )
            dep_ids = self.db.fetchall()
            if len(dep_ids) > 0:
                for dep_id in dep_ids:
                    self.db.execute(
                        """DELETE FROM apscheduler_jobs WHERE apscheduler_jobs.id=?;""",
                        (f"dep_{dep_id} interest schedule",),
                    )

            self.db.execute(
                """DELETE FROM apscheduler_jobs WHERE apscheduler_jobs.id=?;""",
                (f"{self.account['details']['Name']} loan schedule",),
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
                """DELETE FROM withdrawals WHERE user_id=?;""",
                (self.account["details"]["id"],),
            )
            self.db.execute(
                """DELETE FROM deposits WHERE user_id=?;""",
                (self.account["details"]["id"],),
            )
            self.db.execute(
                """DELETE FROM deposit_interest WHERE user_id=?;""",
                (self.account["details"]["id"],),
            )

            self.db.execute(
                """DELETE FROM users WHERE id=?;""", (self.account["details"]["id"],)
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
            msg.setText(f"Account deleted successfully")
            msg.setDefaultButton(QMessageBox.Ok)
            msg.buttonClicked.connect(self._back)
            msg.exec_()
            msg.show()

    def _back(self):
        self.params["parent"]["back_btn"].click()
        self.params["parent"]["back_btn"].click()

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
            print(item[2])
            account["details"]["Image"] = item[9]
            account["details"]["Account Number"] = item[1]
            account["details"]["Name"] = f"{item[3]}"
            account["details"]["Shares"] = "\u20A6 {:,}".format(
                float(round(item[2] if not item[2] == "" else 0.0, 2))
            )
            account["details"]["Account Type"] = item[7].capitalize()
            account["details"]["Phonenumber"] = item[4]
            account["details"]["Email"] = item[5]
            account["details"]["Address"] = item[6]
            account["details"]["Account Status"] = item[8].capitalize()
            account["details"]["Date Registered"] = datetime.strptime(
                item[10], "%Y-%m-%d %H:%M:%S"
            ).strftime("%b %d, %Y  %H:%M")

        self.db.execute(
            """SELECT * FROM next_of_kin WHERE user_id=?;""", (self.user_id,)
        )
        for item in self.db.fetchall():
            account["next_of_kin"]["Name"] = item[1]
            account["next_of_kin"]["Phonenumber"] = item[2]
            account["next_of_kin"]["Address"] = item[3]
            account["next_of_kin"]["Relationship"] = item[4]

        self.db.execute("""SELECT * FROM company WHERE user_id=?;""", (self.user_id,))
        for item in self.db.fetchall():
            account["company"]["Name"] = item[1]
            account["company"]["Telephone"] = item[2]
            account["company"]["Address"] = item[3]

        self.db.execute("""SELECT * FROM savings WHERE user_id=?;""", (self.user_id,))
        for item in self.db.fetchall():
            account["savings"]["Balance"] = "\u20A6 {:,}".format(
                float(round(item[1], 2))
            )
            account["savings"]["Interest Earned"] = "\u20A6 {:,}".format(
                float(round(item[2], 2))
            )
            account["savings"]["Total Amount"] = "\u20A6 {:,}".format(
                float(round(item[3], 2))
            )
            account["savings"]["Last Updated"] = datetime.strptime(
                item[4], "%Y-%m-%d %H:%M:%S"
            ).strftime("%b %d, %Y  %H:%M")

        self.db.execute(
            """SELECT * FROM loans WHERE user_id=? ORDER BY id DESC LIMIT 1;""",
            (self.user_id,),
        )
        loan = self.db.fetchone()
        if not loan is None:
            account["last_loan"]["Amount"] = "\u20A6 {:,}".format(
                float(round(loan[1], 2))
            )
            account["last_loan"]["First Guarantor"] = loan[2]
            account["last_loan"]["Second Guarantor"] = loan[3]
            account["last_loan"]["Clear Amount"] = "\u20A6 {:,}".format(
                float(round(loan[4], 2))
            )
            account["last_loan"]["Current Liability"] = "\u20A6 {:,}".format(
                float(round(loan[5], 2))
            )
            account["last_loan"]["Loan Status"] = loan[6].capitalize()
            account["last_loan"]["Loan Duration"] = loan[7].capitalize()
            account["last_loan"]["Due Date"] = datetime.strptime(
                loan[8], "%Y-%m-%d"
            ).strftime("%b %d, %Y")
            account["last_loan"]["Date Issued"] = datetime.strptime(
                loan[9], "%Y-%m-%d"
            ).strftime("%b %d, %Y")

        self.db.execute(
            """SELECT * FROM deposits WHERE user_id=? ORDER BY id DESC LIMIT 1;""",
            (self.user_id,),
        )
        deposit = self.db.fetchone()
        if not deposit is None:
            account["last_deposit"]["Amount"] = "\u20A6 {:,}".format(float(deposit[1]))
            account["last_deposit"]["Date Deposited"] = datetime.strptime(
                deposit[2], "%Y-%m-%d"
            ).strftime("%b %d, %Y")

        self.db.execute(
            """SELECT * FROM withdrawals WHERE user_id=? ORDER BY id DESC LIMIT 1;""",
            (self.user_id,),
        )
        withdrawal = self.db.fetchone()
        if not withdrawal is None:
            account["last_withdrawal"]["Amount"] = "\u20A6 {:,}".format(
                float(round(withdrawal[1], 2))
            )
            account["last_withdrawal"]["Date Withdrawn"] = datetime.strptime(
                withdrawal[3], "%Y-%m-%d"
            ).strftime("%b %d, %Y")

        return account
