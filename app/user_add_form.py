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
    QDateEdit,
)
from PyQt5.QtCore import Qt, QSize, QDate


class ADD_USER(QWidget):
    def __init__(self, params, **kwargs):
        super().__init__()
        self.params = params
        self.kwargs = kwargs
        self._view()

    def _view(self):
        self.params["parent"]["self"].setWindowTitle("Registration - Cedar App")

        initial_layout = QVBoxLayout()
        initial_layout.setContentsMargins(0, 0, 0, 0)
        label = QLabel("Register Account")
        # label.setFixedHeight(30)
        label.setObjectName("Header")

        scrollArea = QScrollArea()
        main_widget = QWidget()
        main_widget_layout = QVBoxLayout()
        main_widget.setLayout(main_widget_layout)
        scrollArea.setWidget(main_widget)
        scrollArea.setWidgetResizable(True)

        group_1 = QGroupBox("Account Type")
        group_1_layout = QHBoxLayout()
        group_1.setLayout(group_1_layout)

        self.option_1 = QRadioButton("Member")
        self.option_2 = QRadioButton("Admin / Staff")
        self.option_1.setObjectName("type")
        self.option_2.setObjectName("type")
        self.option_1.setChecked(True)
        self.option_1.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.option_2.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        group_1_layout.addWidget(self.option_1)
        group_1_layout.addWidget(self.option_2)

        group_2 = QGroupBox("Name")
        group_2_layout = QGridLayout()
        group_2.setLayout(group_2_layout)

        self.fn_int = QLineEdit()
        self.mn_int = QLineEdit()
        self.ln_int = QLineEdit()

        self.fn_int.textChanged.connect(self._check_for_save)
        self.mn_int.textChanged.connect(self._check_for_save)
        self.ln_int.textChanged.connect(self._check_for_save)

        group_2_layout.addWidget(QLabel("First Name:"), 0, 0)
        group_2_layout.addWidget(self.fn_int, 0, 1)
        group_2_layout.addWidget(QLabel("Middle Name:"), 1, 0)
        group_2_layout.addWidget(self.mn_int, 1, 1)
        group_2_layout.addWidget(QLabel("Last Name:"), 2, 0)
        group_2_layout.addWidget(self.ln_int, 2, 1)

        group_3 = QGroupBox("Personal Details")
        group_3_layout = QGridLayout()
        group_3.setLayout(group_3_layout)

        group_3_layout.addWidget(QLabel("Date of birth:"), 0, 0)

        self.dob_int = QDateEdit(calendarPopup=True)

        group_3_layout.addWidget(self.dob_int, 0, 1)
        group_3_layout.addWidget(QLabel("Email:"), 1, 0)

        self.email_int = QLineEdit()
        self.mob_int = QLineEdit()
        self.addr_int = QLineEdit()

        self.mob_int.textChanged.connect(self._check_for_save)

        self.mob_int.setValidator(QDoubleValidator())

        group_3_layout.addWidget(self.email_int, 1, 1)
        group_3_layout.addWidget(QLabel("Mobile:"), 2, 0)
        group_3_layout.addWidget(self.mob_int, 2, 1)
        group_3_layout.addWidget(QLabel("Residential address:"), 3, 0)
        group_3_layout.addWidget(self.addr_int, 3, 1)

        group_4 = QGroupBox("Next of Kin")
        group_4_layout = QGridLayout()
        group_4.setLayout(group_4_layout)

        self.next_fn_int = QLineEdit()
        self.next_mn_int = QLineEdit()
        self.next_ln_int = QLineEdit()
        self.next_mob_int = QLineEdit()
        self.next_addr_int = QLineEdit()
        self.next_rel_int = QLineEdit()

        self.next_mob_int.setValidator(QDoubleValidator())

        group_4_layout.addWidget(QLabel("First Name:"), 0, 0)
        group_4_layout.addWidget(self.next_fn_int, 0, 1)
        group_4_layout.addWidget(QLabel("Middle Name:"), 1, 0)
        group_4_layout.addWidget(self.next_mn_int, 1, 1)
        group_4_layout.addWidget(QLabel("Last Name:"), 2, 0)
        group_4_layout.addWidget(self.next_ln_int, 2, 1)
        group_4_layout.addWidget(QLabel("Mobile:"), 3, 0)
        group_4_layout.addWidget(self.next_mob_int, 3, 1)
        group_4_layout.addWidget(QLabel("Residential address:"), 4, 0)
        group_4_layout.addWidget(self.next_addr_int, 4, 1)
        group_4_layout.addWidget(QLabel("Relationship:"), 5, 0)
        group_4_layout.addWidget(self.next_rel_int, 5, 1)

        group_5 = QGroupBox("Company")
        group_5_layout = QGridLayout()
        group_5.setLayout(group_5_layout)

        self.cn_int = QLineEdit()
        self.ct_int = QLineEdit()
        self.cadd_int = QLineEdit()
        self.ct_int.setValidator(QDoubleValidator())

        group_5_layout.addWidget(QLabel("Name:"), 0, 0)
        group_5_layout.addWidget(self.cn_int, 0, 1)
        group_5_layout.addWidget(QLabel("Telephone:"), 1, 0)
        group_5_layout.addWidget(self.ct_int, 1, 1)
        group_5_layout.addWidget(QLabel("Address:"), 2, 0)
        group_5_layout.addWidget(self.cadd_int, 2, 1)

        main_widget_layout.addWidget(group_1)
        main_widget_layout.addWidget(group_2)
        main_widget_layout.addWidget(group_3)
        main_widget_layout.addWidget(group_4)
        main_widget_layout.addWidget(group_5)

        btn_lay = QHBoxLayout()
        cancel_btn = QPushButton("Cancel")
        self.save_btn = QPushButton("Save")
        cancel_btn.setFixedHeight(35)
        self.save_btn.setFixedHeight(35)
        self.save_btn.setDisabled(True)

        cancel_btn.clicked.connect(self.params["parent"]["self"]._back)
        self.save_btn.clicked.connect(self._confirm_save)

        btn_lay.addWidget(cancel_btn)
        btn_lay.addWidget(self.save_btn)

        initial_layout.addWidget(label)
        initial_layout.addWidget(scrollArea)
        initial_layout.addLayout(btn_lay)

        if self.kwargs:
            user = self.kwargs["user"]
            name = user["details"]["Name"].split(" ")
            nok_name = user["next_of_kin"]["Name"].split(" ")
            dob = datetime.strptime(
                user["details"]["Date of Birth"], "%b %d, %Y"
            ).strftime("%d/%m/%Y")
            if user["details"]["Member or Staff"] == "Member":
                self.option_1.setChecked(True)
            else:
                self.option_2.setChecked(True)

            self.fn_int.setText(name[2])
            self.mn_int.setText(name[1])
            self.ln_int.setText(name[0])
            self.dob_int.setDate(QDate.fromString(dob, "d/M/yyyy"))
            self.email_int.setText(user["details"]["Email"])
            self.mob_int.setText(user["details"]["Phonenumber"])
            self.addr_int.setText(user["details"]["Address"])
            self.next_fn_int.setText(nok_name[2])
            self.next_mn_int.setText(nok_name[1])
            self.next_ln_int.setText(nok_name[0])
            self.next_mob_int.setText(user["next_of_kin"]["Phonenumber"])
            self.next_addr_int.setText(user["next_of_kin"]["Address"])
            self.next_rel_int.setText(user["next_of_kin"]["Relationship"])
            self.cn_int.setText(user["company"]["Name"])
            self.ct_int.setText(user["company"]["Telephone"])
            self.cadd_int.setText(user["company"]["Address"])

            self.save_btn.setText("Update")

        self.setLayout(initial_layout)

    def _check_for_save(self):
        if (
            not self.fn_int.text() == ""
            and not self.mn_int.text() == ""
            and not self.ln_int.text() == ""
            and not self.mob_int.text() == ""
        ):
            self.save_btn.setDisabled(False)

    def _confirm_save(self):
        name = f"{self.ln_int.text()} {self.mn_int.text()} {self.fn_int.text()}"
        self.dob = self.dob_int.date().toString(Qt.ISODate)
        self.acc_type = "member" if self.option_1.isChecked() else "staff"
        details = f"""The details are as follows:
                
                First Name: {self.fn_int.text()}
                Middle Name: {self.mn_int.text()}
                Last Name: {self.ln_int.text()}
                Date of birth: {self.dob}
                Phonenumber: {self.mob_int.text()}
                Email: {self.email_int.text()}
                Address: {self.addr_int.text()}
                Account Type: {self.acc_type}
                Next of Kin:
                    First Name: {self.next_fn_int.text()}
                    Middle Name: {self.next_mn_int.text()}
                    Last Name: {self.next_ln_int.text()}
                    Phonenumber: {self.next_mob_int.text()}
                    Address: {self.next_addr_int.text()}
                    Relationship: {self.next_rel_int.text()}
                Company:
                    Name: {self.cn_int.text()}
                    Telephone: {self.ct_int.text()}
                    Address: {self.cadd_int.text()}"""
        db = self.params["db"].conn.cursor()
        msg = QMessageBox()
        if not self.kwargs:
            db.execute(
                """SELECT id FROM users WHERE first_name=? AND middle_name=? AND last_name=?;""",
                (
                    self.fn_int.text().capitalize(),
                    self.mn_int.text().capitalize(),
                    self.ln_int.text().capitalize(),
                ),
            )

            user = db.fetchone()
            if user is None:
                msg.setIcon(QMessageBox.Question)
                msg.setText(f"Are you sure you want to register {name}?")
                msg.setWindowTitle("Account Creation")
                msg.setDetailedText(details)
                msg.setStandardButtons(QMessageBox.No | QMessageBox.Yes)
                msg.setDefaultButton(QMessageBox.Yes)
                msg.buttonClicked.connect(self._handle_add_user)
            else:
                msg.setIcon(QMessageBox.Critical)
                msg.setText(f'An account with this name "{name}" already exists!')
                msg.setWindowTitle("Warning!")
                msg.setDefaultButton(QMessageBox.Ok)
        else:
            msg.setIcon(QMessageBox.Question)
            msg.setText(f"Are you sure you want to update {name}'s details?")
            msg.setWindowTitle("Account Update")
            msg.setDetailedText(details)
            msg.setStandardButtons(QMessageBox.No | QMessageBox.Yes)
            msg.setDefaultButton(QMessageBox.Yes)
            msg.buttonClicked.connect(self._handle_add_user)
        msg.exec_()
        msg.show()

    def _handle_add_user(self, i):
        if i.text() == "&Yes":
            db = self.params["db"].conn.cursor()
            msg = QMessageBox()
            if not self.kwargs:
                msg.setWindowTitle("Account Creation")
                try:
                    db.execute(
                        """INSERT INTO users (
                            first_name,
                            middle_name,
                            last_name,
                            dob,
                            phonenumber,
                            email,
                            address,
                            account_type,
                            date_created) VALUES (?,?,?,?,?,?,?,?,?);""",
                        (
                            self.fn_int.text().capitalize(),
                            self.mn_int.text().capitalize(),
                            self.ln_int.text().capitalize(),
                            self.dob,
                            self.mob_int.text(),
                            self.email_int.text(),
                            self.addr_int.text().capitalize(),
                            self.acc_type,
                            datetime.today().now().strftime("%Y-%m-%d %H:%M:%S"),
                        ),
                    )
                    db.execute(
                        """
                        SELECT * FROM users ORDER BY id DESC LIMIT 1;
                        """
                    )
                    user = db.fetchone()
                    db.execute(
                        """INSERT INTO next_of_kin (
                            first_name,
                            middle_name,
                            last_name,
                            phonenumber,
                            address,
                            relationship,
                            user_id) VALUES (?,?,?,?,?,?,?);""",
                        (
                            self.next_fn_int.text().capitalize(),
                            self.next_mn_int.text().capitalize(),
                            self.next_ln_int.text().capitalize(),
                            self.next_mob_int.text(),
                            self.next_addr_int.text().capitalize(),
                            self.next_rel_int.text().capitalize(),
                            user[0],
                        ),
                    )
                    db.execute(
                        """INSERT INTO company (
                            name,
                            telephone,
                            address,
                            user_id) VALUES (?,?,?,?);""",
                        (
                            self.cn_int.text().capitalize(),
                            self.ct_int.text(),
                            self.cadd_int.text().capitalize(),
                            user[0],
                        ),
                    )
                    db.execute(
                        """INSERT INTO savings(date_updated, user_id) VALUES (?,?);""",
                        (datetime.today().now().strftime("%Y-%m-%d %H:%M:%S"), user[0]),
                    )
                    self.params["db"].conn.commit()
                    msg.setIcon(QMessageBox.Information)
                    msg.setText(f"Account creation successful")
                    msg.buttonClicked.connect(self._clear_all)
                except Exception as e:
                    msg.setIcon(QMessageBox.Critical)
                    msg.setText(f"Error creating account, please check the form again")
            else:
                msg.setWindowTitle("Account Update")
                try:
                    db.execute(
                        """UPDATE users SET
                            first_name=?,
                            middle_name=?,
                            last_name=?,
                            dob=?,
                            phonenumber=?,
                            email=?,
                            address=?,
                            account_type=? 
                            WHERE id=?;""",
                        (
                            self.fn_int.text(),
                            self.mn_int.text(),
                            self.ln_int.text(),
                            self.dob,
                            self.mob_int.text(),
                            self.email_int.text(),
                            self.addr_int.text(),
                            self.acc_type,
                            self.kwargs["user"]["details"]["id"],
                        ),
                    )
                    db.execute(
                        """UPDATE next_of_kin SET
                            first_name=?,
                            middle_name=?,
                            last_name=?,
                            phonenumber=?,
                            address=?,
                            relationship=? WHERE user_id=?;""",
                        (
                            self.next_fn_int.text(),
                            self.next_mn_int.text(),
                            self.next_ln_int.text(),
                            self.next_mob_int.text(),
                            self.next_addr_int.text(),
                            self.next_rel_int.text(),
                            self.kwargs["user"]["details"]["id"],
                        ),
                    )
                    db.execute(
                        """UPDATE company SET
                            name=?,
                            telephone=?,
                            address=? WHERE user_id=?;""",
                        (
                            self.cn_int.text(),
                            self.ct_int.text(),
                            self.cadd_int.text(),
                            self.kwargs["user"]["details"]["id"],
                        ),
                    )
                    self.params["db"].conn.commit()
                    msg.setIcon(QMessageBox.Information)
                    msg.setText(f"Account update successful")
                    msg.buttonClicked.connect(
                        lambda: self.params["parent"]["back_btn"].click()
                    )
                except Exception as e:
                    msg.setIcon(QMessageBox.Critical)
                    msg.setText(f"Error updating account, please check the form again")
            msg.setDefaultButton(QMessageBox.Ok)
            msg.exec_()
            msg.show()

    def _clear_all(self):
        self.fn_int.clear()
        self.mn_int.clear()
        self.ln_int.clear()
        self.dob_int.clear()
        self.email_int.clear()
        self.mob_int.clear()
        self.addr_int.clear()
        self.next_fn_int.clear()
        self.next_mn_int.clear()
        self.next_ln_int.clear()
        self.next_mob_int.clear()
        self.next_addr_int.clear()
        self.next_rel_int.clear()
        self.cn_int.clear()
        self.ct_int.clear()
        self.cadd_int.clear()