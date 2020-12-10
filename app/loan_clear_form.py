from datetime import datetime, timedelta
from PyQt5.QtGui import QIcon, QDoubleValidator, QRegExpValidator
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
    QCheckBox,
    QDialog,
)
from PyQt5.QtCore import Qt, QSize, QDate, QRegExp


class LOAN_CLEAR(QDialog):
    def __init__(self, params, user_id):
        super().__init__()
        self.setStyleSheet(open("./assets/css/style.css").read())
        self.setWindowTitle("Loan Clearance Form - Cedar")
        self.setMinimumWidth(680)
        self.params = params

        self.db = self.params["db"].conn.cursor()

        self.user_data = self._get_data_db(user_id)

        self._view()

    def _view(self):
        initial_layout = QVBoxLayout()
        scrollArea = QScrollArea()
        main_widget = QWidget()
        main_widget_layout = QGridLayout()
        main_widget.setLayout(main_widget_layout)

        scrollArea.setWidget(main_widget)
        scrollArea.setWidgetResizable(True)
        initial_layout.addWidget(scrollArea)

        name_lay = QHBoxLayout()
        name_lay.setContentsMargins(0, 0, 0, 0)
        nam_lbl = QLabel("Account:")
        self.nam_int = QLabel(self.user_data["fullname"])
        nam_lbl.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.nam_int.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        nam_lbl.setObjectName("Header")
        self.nam_int.setObjectName("Header")
        name_lay.addWidget(nam_lbl)
        name_lay.addWidget(self.nam_int, alignment=Qt.AlignRight)

        group_1 = QGroupBox("Clearance")
        group_1.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        group_1_layout = QGridLayout()
        group_1.setLayout(group_1_layout)

        group_1_layout.addWidget(QLabel("Date:"), 0, 0)
        self.date = QLabel(str(datetime.today().date().strftime("%B %d, %Y")))
        self.date.setObjectName("Loan")
        group_1_layout.addWidget(self.date, 0, 1, alignment=Qt.AlignRight)

        group_1_layout.addWidget(QLabel("Amount:"), 1, 0)
        self.clear_amt = QLineEdit()
        self.clear_amt.setValidator(QRegExpValidator(QRegExp("^[0-9]{1,},*")))
        self.clear_amt.setClearButtonEnabled(True)
        group_1_layout.addWidget(self.clear_amt, 1, 1)

        self.clear_amt.textChanged.connect(self._calc)

        self.useSavings = QCheckBox("Deduct from Savings")
        self.useSavings.setObjectName("Loan")
        self.useSavings.toggled.connect(self._handle_useSav)
        group_1_layout.addWidget(self.useSavings, 2, 0, 1, 0)

        group_2 = QGroupBox("Account")
        group_2.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        group_2_layout = QGridLayout()
        group_2.setLayout(group_2_layout)

        child_grid_1 = QGridLayout()
        child_grid_2 = QGridLayout()

        child_grid_1.addWidget(QLabel("Balance:"), 0, 0)
        self.bal = QLabel(self.user_data["total_balance"])
        self.bal.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        child_grid_1.addWidget(self.bal, 0, 1, alignment=Qt.AlignRight)

        child_grid_1.addWidget(QLabel("Account Type:"), 1, 0)
        self.acc_type = QLabel(self.user_data["account_type"])
        self.acc_type.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        child_grid_1.addWidget(self.acc_type, 1, 1, alignment=Qt.AlignRight)

        child_grid_1.addWidget(QLabel("Account Status:"), 2, 0)
        self.acc_stat = QLabel(self.user_data["status"])
        self.acc_stat.setObjectName("Loan")
        self.acc_stat.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        child_grid_1.addWidget(self.acc_stat, 2, 1, alignment=Qt.AlignRight)

        child_grid_2.addWidget(QLabel("Loan Amount:"), 0, 0)
        self.loan = QLabel(self.user_data["loan"]["amount"])
        self.loan.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        child_grid_2.addWidget(self.loan, 0, 1, alignment=Qt.AlignRight)

        child_grid_2.addWidget(QLabel("Cleared Amount:"), 1, 0)
        self.cleared_amt = QLabel(self.user_data["loan"]["cleared_amount"])
        self.cleared_amt.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        child_grid_2.addWidget(self.cleared_amt, 1, 1, alignment=Qt.AlignRight)

        child_grid_2.addWidget(QLabel("Current Liability:"), 2, 0)
        self.curLia = QLabel(self.user_data["loan"]["current_liability"])
        self.curLia.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        child_grid_2.addWidget(self.curLia, 2, 1, alignment=Qt.AlignRight)

        child_grid_2.addWidget(QLabel("Loan Status:"), 3, 0)
        self.loan_stat = QLabel(self.user_data["loan"]["status"])
        self.loan_stat.setObjectName("Loan")
        self.loan_stat.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        child_grid_2.addWidget(self.loan_stat, 3, 1, alignment=Qt.AlignRight)

        group_2_layout.addLayout(child_grid_1, 0, 0)
        group_2_layout.addLayout(child_grid_2, 0, 1)

        main_widget_layout.addLayout(name_lay, 0, 0, 1, 0)
        main_widget_layout.addWidget(group_1, 1, 0)
        main_widget_layout.addWidget(group_2, 1, 1)

        btn_layout = QHBoxLayout()
        cancel_btn = QPushButton("Cancel")
        self.save_btn = QPushButton("Save")
        cancel_btn.setFixedHeight(35)
        self.save_btn.setFixedHeight(35)
        self.save_btn.setDisabled(True)

        cancel_btn.clicked.connect(self.close)
        self.save_btn.clicked.connect(self._check_save)

        btn_layout.addWidget(cancel_btn)
        btn_layout.addWidget(self.save_btn)

        initial_layout.addLayout(btn_layout)

        self.setLayout(initial_layout)

    def _check_save(self):
        details = f"""The details are as follows:
        Account: {self.nam_int.text()}
        Loan Amount: {self.loan.text()}
        Current Liability: {self.curLia.text()}
        Cleared Amount: {self.cleared_amt.text()}"""

        msg = QMessageBox()
        msg.setIcon(QMessageBox.Question)
        msg.setText(
            f"Are you sure you want to record loan clearance for {self.nam_int.text()}?"
        )
        msg.setWindowTitle("Loan Issuance")
        msg.setDetailedText(details)
        msg.setStandardButtons(QMessageBox.No | QMessageBox.Yes)
        msg.setDefaultButton(QMessageBox.Yes)
        msg.buttonClicked.connect(self._confirm_save)
        msg.exec_()
        msg.show()

    def _confirm_save(self, i):
        if i.text() == "&Yes":
            msg = QMessageBox()
            msg.setWindowTitle("Loan Clearance")

            amt = self.cleared_amt.text().replace("\u20A6", "").replace(",", "")
            curLia = self.curLia.text().replace("\u20A6", "").replace(",", "")

            try:
                if self.user_data["loan"]["status"].lower() == "not cleared":
                    loan_status = "cleared" if float(curLia) == 0.0 else "pending"
                else:
                    loan_status = (
                        "cleared"
                        if float(curLia) == 0.0
                        else self.user_data["loan"]["status"].lower()
                    )

                if self.user_data["status"].lower() == "inactive":
                    acc_stat = (
                        "active"
                        if loan_status == "cleared"
                        else self.user_data["status"].lower()
                    )
                self.db.execute(
                    """UPDATE loans SET
                        cleared_amount=?,
                        current_liability=?,
                        status=? WHERE user_id=? ORDER BY id DESC LIMIT 1;""",
                    (
                        float(amt),
                        float(curLia),
                        loan_status,
                        self.user_data["id"],
                    ),
                )
                self.db.execute(
                    """UPDATE users SET
                        status=? WHERE id=?""",
                    (acc_stat, self.user_data["id"]),
                )
                if self.useSavings.isChecked():
                    self.db.execute(
                        """UPDATE savings SET
                            balance=?,
                            total=?,
                            date_updated=? WHERE user_id=?;""",
                        (
                            self.new_bal,
                            self.new_total,
                            datetime.today().now().strftime("%Y-%m-%d %H:%M:%S"),
                            self.user_data["id"],
                        ),
                    )
                    self.alter_dep_intr(user_id=self.user_data["id"], amount=amt)

                if loan_status == "cleared":
                    self.params["qtshed"].remove_job(job_id=f"{self.user_data["fullname"]} loan schedule")
                self.params["db"].conn.commit()
                msg.setIcon(QMessageBox.Information)
                msg.setText(f"Loan Clearance Successful")
                msg.buttonClicked.connect(self.hide)
            except Exception as e:
                print(e)
                msg.setIcon(QMessageBox.Critical)
                msg.setText(f"Error clearing loan, please check the form again")
            msg.setDefaultButton(QMessageBox.Ok)
            msg.exec_()
            msg.show()

    def _handle_useSav(self, state):
        old_bal = self.user_data["balance"].replace("\u20A6", "").replace(",", "")
        old_tot = self.user_data["total_balance"].replace("\u20A6", "").replace(",", "")

        old_clr_amt = (
            self.user_data["loan"]["cleared_amount"]
            .replace("\u20A6", "")
            .replace(",", "")
        )

        old_curr_liab = (
            self.user_data["loan"]["current_liability"]
            .replace("\u20A6", "")
            .replace(",", "")
        )

        number = self.clear_amt.text().replace(",", "")
        if not number == "":
            new_clr_amt = float(old_clr_amt) + float(number)
            if state:
                if float(old_tot) >= float(number):
                    self.new_bal = float(old_bal) - float(number)
                    self.new_total = float(old_tot) - float(number)
                    self.bal.setText("\u20A6{:,}".format(int(self.new_total)))
                    new_curr_liab = float(old_curr_liab) - float(number)
                else:
                    self.clear_amt.setText(old_tot)
                    new_clr_amt = float(old_clr_amt) + float(old_tot)
                    new_curr_liab = float(old_curr_liab) - float(old_tot)

                self.cleared_amt.setText("\u20A6{:,}".format(int(new_clr_amt)))
                self.curLia.setText("\u20A6{:,}".format(int(new_curr_liab)))
            else:
                self.bal.setText("\u20A6{:,}".format(int(old_tot)))

    def _calc(self, number):
        new_curr_liab, new_clr_amt, self.new_bal, self.new_total = (
            None,
            None,
            None,
            None,
        )
        if not number == "":
            number = number.replace(",", "")
            self.clear_amt.setText("{:,}".format(int(number)))

            old_bal = self.user_data["balance"].replace("\u20A6", "").replace(",", "")
            old_tot = (
                self.user_data["total_balance"].replace("\u20A6", "").replace(",", "")
            )

            old_clr_amt = (
                self.user_data["loan"]["cleared_amount"]
                .replace("\u20A6", "")
                .replace(",", "")
            )

            old_curr_liab = (
                self.user_data["loan"]["current_liability"]
                .replace("\u20A6", "")
                .replace(",", "")
            )

            new_clr_amt = float(old_clr_amt) + float(number)

            self.save_btn.setDisabled(False if len(number) >= 3 else True)

            if self.useSavings.isChecked():
                if float(old_tot) >= float(number):
                    self.new_bal = float(old_bal) - float(number)
                    self.new_total = float(old_tot) - float(number)

                    self.bal.setText("\u20A6{:,}".format(int(self.new_total)))

                    new_curr_liab = float(old_curr_liab) - float(number)
                else:
                    self.clear_amt.setText(old_bal)
                    new_clr_amt = float(old_clr_amt) + float(old_bal)
                    new_curr_liab = float(old_curr_liab) - float(old_bal)
            else:
                if float(old_curr_liab) >= float(number):
                    new_curr_liab = float(old_curr_liab) - float(number)
                else:
                    self.clear_amt.setText(old_curr_liab)
                    new_curr_liab = float(old_curr_liab) - float(old_curr_liab)
                    new_clr_amt = float(old_clr_amt) + float(old_curr_liab)

            self.cleared_amt.setText("\u20A6{:,}".format(int(new_clr_amt)))
            self.curLia.setText("\u20A6{:,}".format(int(new_curr_liab)))
        else:
            self.bal.setText(self.user_data["total_balance"])
            self.curLia.setText(self.user_data["loan"]["current_liability"])
            self.cleared_amt.setText(self.user_data["loan"]["cleared_amount"])

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
        new_amt = float(_lst[1]) - float(amount)
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

    def _get_data_db(self, user_id):
        self.db.execute(
            """SELECT * FROM users WHERE id=?;""",
            (user_id,),
        )
        user = self.db.fetchone()
        account = {
            "id": user[0],
            "fullname": f"{user[3]} {user[2]} {user[1]}",
            "account_type": user[8].capitalize(),
            "status": user[9],
        }

        self.db.execute(
            """SELECT * FROM savings WHERE user_id=?;""",
            (user_id,),
        )
        savings = self.db.fetchone()

        self.db.execute(
            """SELECT * FROM loans WHERE user_id=? ORDER BY id DESC LIMIT 1;""",
            (user_id,),
        )
        loans = self.db.fetchone()

        account["balance"] = "\u20A6{:,}".format(int(savings[1])) if savings else "0.0"
        account["total_balance"] = (
            "\u20A6{:,}".format(int(savings[3])) if savings else "0.0"
        )
        account["loan"] = {
            "amount": "\u20A6{:,}".format(int(loans[1])) if loans else "-",
            "cleared_amount": "\u20A6{:,}".format(int(loans[4])) if loans[4] else "-",
            "current_liability": "\u20A6{:,}".format(int(loans[5]))
            if loans[5]
            else "-",
            "status": loans[6].capitalize() if loans[6] else "-",
        }

        return account