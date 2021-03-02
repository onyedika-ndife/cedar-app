import os
import shutil
from datetime import datetime

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from app import home_dir


class ADD_USER(QWidget):
    def __init__(self, params, **kwargs):
        super().__init__()
        self.params = params
        self.kwargs = kwargs
        self._view()

    def _view(self):
        initial_layout = QVBoxLayout()
        initial_layout.setContentsMargins(0, 0, 0, 0)
        label = QLabel("Register Account")
        label.setObjectName("Header")

        scrollArea = QScrollArea()
        main_widget = QWidget()
        main_widget_layout = QGridLayout()
        main_widget.setLayout(main_widget_layout)
        scrollArea.setWidget(main_widget)
        scrollArea.setWidgetResizable(True)

        group_1 = QGroupBox("Account Type")
        group_1.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        group_1_layout = QHBoxLayout()
        group_1.setLayout(group_1_layout)

        self.option_1 = QRadioButton("Member")
        self.option_1.setIcon(QIcon(self.params["ctx"].get_resource("icon/member.png")))
        self.option_1.setIconSize(QSize(30, 30))
        self.option_2 = QRadioButton("Admin / Staff")
        self.option_2.setIcon(QIcon(self.params["ctx"].get_resource("icon/admin.png")))
        self.option_2.setIconSize(QSize(30, 30))
        self.option_1.setObjectName("type")
        self.option_2.setObjectName("type")
        self.option_1.setChecked(True)
        self.option_1.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.option_2.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        group_1_layout.addWidget(self.option_1)
        group_1_layout.addWidget(self.option_2)

        group_2 = QGroupBox("Account Details")
        group_2_layout = QGridLayout()
        group_2.setLayout(group_2_layout)

        self.name = QLineEdit()
        self.acc_no = QLineEdit()
        self.shares = QLineEdit()

        self.name.textChanged.connect(self._check_for_save)
        self.name.textChanged.connect(lambda: self._capitalize(self.name, "name"))
        self.acc_no.textChanged.connect(lambda: self._capitalize(self.acc_no, "acc_no"))
        self.acc_no.textChanged.connect(self._check_for_save)
        self.shares.setValidator(QRegExpValidator(QRegExp("^[0-9]{1,},*")))
        self.shares.setClearButtonEnabled(True)
        self.shares.textChanged.connect(self._check_for_save)
        self.shares.textChanged.connect(self._calc)

        group_2_layout.addWidget(QLabel("Name"), 0, 0)
        group_2_layout.addWidget(self.name, 0, 1)
        group_2_layout.addWidget(QLabel("Account Number"), 1, 0)
        group_2_layout.addWidget(self.acc_no, 1, 1)
        group_2_layout.addWidget(QLabel("Shares"), 2, 0)
        group_2_layout.addWidget(self.shares, 2, 1)

        group_3 = QGroupBox("Personal Details")
        group_3_layout = QGridLayout()
        group_3.setLayout(group_3_layout)

        self.mob_int = QLineEdit()

        group_3_layout.addWidget(QLabel("Mobile"), 0, 0)
        group_3_layout.addWidget(self.mob_int, 0, 1)
        group_3_layout.addWidget(QLabel("Email"), 1, 0)

        self.email_int = QLineEdit()
        self.addr_int = QLineEdit()

        self.mob_int.textChanged.connect(self._check_for_save)

        self.mob_int.setValidator(QDoubleValidator())

        group_3_layout.addWidget(self.email_int, 1, 1)

        group_3_layout.addWidget(QLabel("Residential address"), 2, 0)
        group_3_layout.addWidget(self.addr_int, 2, 1)

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

        group_4_layout.addWidget(QLabel("First name"), 0, 0)
        group_4_layout.addWidget(self.next_fn_int, 0, 1)
        group_4_layout.addWidget(QLabel("Middle name"), 1, 0)
        group_4_layout.addWidget(self.next_mn_int, 1, 1)
        group_4_layout.addWidget(QLabel("Last name"), 2, 0)
        group_4_layout.addWidget(self.next_ln_int, 2, 1)
        group_4_layout.addWidget(QLabel("Mobile"), 3, 0)
        group_4_layout.addWidget(self.next_mob_int, 3, 1)
        group_4_layout.addWidget(QLabel("Residential address"), 4, 0)
        group_4_layout.addWidget(self.next_addr_int, 4, 1)
        group_4_layout.addWidget(QLabel("Relationship"), 5, 0)
        group_4_layout.addWidget(self.next_rel_int, 5, 1)

        group_5 = QGroupBox("Company")
        group_5_layout = QGridLayout()
        group_5.setLayout(group_5_layout)

        self.cn_int = QLineEdit()
        self.ct_int = QLineEdit()
        self.cadd_int = QLineEdit()
        self.ct_int.setValidator(QDoubleValidator())

        group_5_layout.addWidget(QLabel("Name"), 0, 0)
        group_5_layout.addWidget(self.cn_int, 0, 1)
        group_5_layout.addWidget(QLabel("Telephone"), 1, 0)
        group_5_layout.addWidget(self.ct_int, 1, 1)
        group_5_layout.addWidget(QLabel("Address"), 2, 0)
        group_5_layout.addWidget(self.cadd_int, 2, 1)

        pro_pic_lay = QGridLayout()
        self.blank_image = self.params["ctx"].get_resource("image/avatar.png")
        self.image_path = self.blank_image
        self.picture = QLabel()
        self.picture.setScaledContents(True)
        self.picture.setFixedSize(250, 250)

        pro_pic_lay.addWidget(self.picture, 0, 0, 1, 2)

        change_btn = QPushButton(
            QIcon(self.params["ctx"].get_resource("icon/edit_image.png")), "Change"
        )

        change_btn.clicked.connect(self._get_image)

        self.remove_btn = QPushButton(
            QIcon(self.params["ctx"].get_resource("icon/remove_image.png")),
            "Remove",
        )
        self.remove_btn.clicked.connect(self._remove_image)
        self.remove_btn.setDisabled(True)
        pro_pic_lay.addWidget(change_btn, 1, 0)
        pro_pic_lay.addWidget(self.remove_btn, 1, 1)

        main_widget_layout.addWidget(group_1, 0, 0)
        main_widget_layout.addLayout(pro_pic_lay, 0, 1, 2, 1)
        main_widget_layout.addWidget(group_2, 1, 0)
        main_widget_layout.addWidget(group_3, 2, 0, 1, 0)
        main_widget_layout.addWidget(group_4, 3, 0, 1, 0)
        main_widget_layout.addWidget(group_5, 4, 0, 1, 0)
        dor_lay = QHBoxLayout()
        dor_lbl = QLabel("Date of Registration")
        dor_lbl.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        dor_lay.addWidget(dor_lbl)
        self.dor = QDateTimeEdit(calendarPopup=True)
        self.dor.setDateTime(QDateTime.currentDateTime())
        self.dor.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        dor_lay.addWidget(self.dor)
        main_widget_layout.addLayout(dor_lay, 5, 0, 1, 0)

        btn_lay = QHBoxLayout()
        cancel_btn = QPushButton("Cancel")
        self.save_btn = QPushButton("Register")
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
            self.image_path = (
                user["details"]["Image"]
                if not user["details"]["Image"] == ""
                else self.blank_image
            )

            nok_name = user["next_of_kin"]["Name"].split(" ")

            if user["details"]["Account Type"] == "Member":
                self.option_1.setChecked(True)
            else:
                self.option_2.setChecked(True)

            self.name.setText(user["details"]["Name"])
            self.acc_no.setText(user["details"]["Account Number"])
            self.shares.setText(user["details"]["Shares"].replace("\u20A6", ""))

            if not self.image_path == self.blank_image:
                self.remove_btn.setDisabled(False)

            self.email_int.setText(user["details"]["Email"])
            self.mob_int.setText(user["details"]["Phonenumber"])
            self.addr_int.setText(user["details"]["Address"])
            if len(nok_name) == 3:
                self.next_fn_int.setText(nok_name[2])
                self.next_mn_int.setText(nok_name[1])
                self.next_ln_int.setText(nok_name[0])
            elif len(nok_name) == 2:
                self.next_fn_int.setText(nok_name[1])
                self.next_ln_int.setText(nok_name[0])

            self.next_mob_int.setText(user["next_of_kin"]["Phonenumber"])
            self.next_addr_int.setText(user["next_of_kin"]["Address"])
            self.next_rel_int.setText(user["next_of_kin"]["Relationship"])
            self.cn_int.setText(user["company"]["Name"])
            self.ct_int.setText(user["company"]["Telephone"])
            self.cadd_int.setText(user["company"]["Address"])

            dor_1 = datetime.strptime(
                user["details"]["Date Registered"], "%b %d, %Y  %H:%M"
            ).strftime("%Y-%m-%d %H:%M")
            dor_2 = datetime.strptime(dor_1, "%Y-%m-%d %H:%M").strftime(
                "%d/%m/%Y %H:%M"
            )
            self.dor.setDateTime(QDateTime.fromString(dor_2, "d/M/yyyy HH:mm"))

            self.save_btn.setText("Update")

        self.picture.setPixmap(QPixmap(self.image_path))

        self.setLayout(initial_layout)

    def _calc(self, number):
        if not number == "":
            number = number.replace(",", "")
            new_numb = "{:,}".format(int(number))
            self.shares.setText(new_numb)

    def _get_image(self):
        data_dir = os.sep.join([home_dir, "Pictures"])
        frame = QFileDialog.getOpenFileName(
            self, "Select Image", data_dir, "Image files (*.jpg, *.jpeg, *.png)"
        )
        self.image_path = frame[0]
        self.picture.setPixmap(QPixmap(self.image_path))
        self.remove_btn.setDisabled(False)

    def _remove_image(self):
        self.image_path = self.blank_image
        self.picture.setPixmap(QPixmap(self.image_path))

    def _capitalize(self, line_edit, name):
        if not line_edit.text() == "":
            name_text = line_edit.text().split(" ") if name == "name" else None
            name_text = (
                [i.capitalize() for i in name_text] if not name_text is None else None
            )
            name_text = " ".join(name_text) if not name_text is None else None
            text = name_text if name == "name" else line_edit.text().rstrip().upper()
            line_edit.setText(text)

    def _check_for_save(self):
        if (
            not self.name.text() == ""
            and not self.acc_no == ""
            and not self.shares.text() == ""
        ):
            self.save_btn.setDisabled(False)
        else:
            self.save_btn.setDisabled(True)

    def _confirm_save(self):
        name = self.name.text().split(" ")
        msg = QMessageBox()
        msg.setStyleSheet(open(self.params["ctx"].get_resource("css/style.css")).read())
        if len(name) >= 2:
            name = " ".join(name)
            self.acc_type = "member" if self.option_1.isChecked() else "staff"
            details = f"""The details are as follows:
                    
                    Name: {name}
                    Account Number: {self.acc_no.text()}
                    Shares: {self.shares.text()}
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
                        Address: {self.cadd_int.text()}
                        
                    Date of Registration: {self.dor.dateTime().toPyDateTime().strftime("%Y-%m-%d %H:%M:%S")}"""
            db = self.params["db"].conn.cursor()

            if not self.kwargs:
                db.execute(
                    """SELECT id FROM users WHERE name=?;""",
                    (self.name.text().capitalize(),),
                )

                user = db.fetchone()
                if user is None:
                    msg.setIconPixmap(
                        QPixmap(self.params["ctx"].get_resource("icon/question.png"))
                    )
                    msg.setText(f"Are you sure you want to register {name}?")
                    msg.setWindowTitle("Account Creation")
                    msg.setDetailedText(details)
                    msg.setStandardButtons(QMessageBox.No | QMessageBox.Yes)
                    msg.setDefaultButton(QMessageBox.Yes)
                    msg.buttonClicked.connect(self._handle_add_user)
                else:
                    msg.setIconPixmap(
                        QPixmap(self.params["ctx"].get_resource("icon/error.png"))
                    )
                    msg.setText(f'An account with this name "{name}" already exists!')
                    msg.setWindowTitle("Warning!")
                    msg.setDefaultButton(QMessageBox.Ok)
            else:
                msg.setIconPixmap(
                    QPixmap(self.params["ctx"].get_resource("icon/question.png"))
                )
                msg.setText(f"Are you sure you want to update {name}'s details?")
                msg.setWindowTitle("Account Update")
                msg.setDetailedText(details)
                msg.setStandardButtons(QMessageBox.No | QMessageBox.Yes)
                msg.setDefaultButton(QMessageBox.Yes)
                msg.buttonClicked.connect(self._handle_add_user)
        else:
            msg.setIconPixmap(
                QPixmap(self.params["ctx"].get_resource("icon/error.png"))
            )
            msg.setText(f"Separate Firstname and Lastname with space.")
            msg.setWindowTitle("Error")
            msg.setDefaultButton(QMessageBox.Ok)
        msg.exec_()
        msg.show()

    def _handle_add_user(self, i):
        if i.text() == "&Yes":
            db = self.params["db"].conn.cursor()
            name = self.name.text().split(" ")
            img_name = "_".join(name)

            msg = QMessageBox()
            msg.setStyleSheet(
                open(self.params["ctx"].get_resource("css/style.css")).read()
            )
            acc_img_path = os.sep.join([home_dir, "Cedar", "Account Images"])
            if not self.kwargs:
                msg.setWindowTitle("Account Creation")
                try:
                    if not os.path.exists(acc_img_path):
                        os.mkdir(acc_img_path)
                    if not self.image_path == self.blank_image:
                        dest = shutil.copy(self.image_path, acc_img_path)
                        new_dest = (
                            f"{acc_img_path}\{img_name}.png"
                            if dest.endswith(".png")
                            else f"{acc_img_path}\{img_name}.jpg"
                        )
                        os.rename(dest, new_dest)
                        save_image = new_dest
                    else:
                        save_image = ""
                    reg_date = (
                        self.dor.dateTime().toPyDateTime().strftime("%Y-%m-%d %H:%M:%S")
                    )
                    db.execute(
                        """INSERT INTO users (
                            name,
                            account_number,
                            shares,
                            phonenumber,
                            email,
                            address,
                            account_type,
                            profile_picture,
                            date_created) VALUES (?,?,?,?,?,?,?,?,?);""",
                        (
                            self.name.text().rstrip(),
                            self.acc_no.text().rstrip(),
                            float(self.shares.text().rstrip().replace(",", "")),
                            self.mob_int.text().rstrip(),
                            self.email_int.text().rstrip(),
                            self.addr_int.text().rstrip().capitalize(),
                            self.acc_type,
                            save_image,
                            reg_date,
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
                            self.next_fn_int.text().rstrip().capitalize(),
                            self.next_mn_int.text().rstrip().capitalize(),
                            self.next_ln_int.text().rstrip().capitalize(),
                            self.next_mob_int.text().rstrip(),
                            self.next_addr_int.text().rstrip().capitalize(),
                            self.next_rel_int.text().rstrip().capitalize(),
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
                            self.cn_int.text().rstrip().capitalize(),
                            self.ct_int.text().rstrip(),
                            self.cadd_int.text().rstrip().capitalize(),
                            user[0],
                        ),
                    )
                    db.execute(
                        """INSERT INTO savings(date_updated, user_id) VALUES (?,?);""",
                        (
                            reg_date,
                            user[0],
                        ),
                    )

                    self.params["db"].conn.commit()
                    msg.setIconPixmap(
                        QPixmap(self.params["ctx"].get_resource("icon/success.png"))
                    )
                    msg.setText(f"Account creation successful")
                    msg.buttonClicked.connect(self._clear_all)
                except Exception as e:
                    msg.setIconPixmap(
                        QPixmap(self.params["ctx"].get_resource("icon/error.png"))
                    )
                    msg.setText(f"Error creating account, please check the form again")
            else:
                msg.setWindowTitle("Account Update")
                save_image = ""
                if not self.image_path == self.blank_image:
                    old_image = self.kwargs["user"]["details"]["Image"]
                    if not self.image_path == old_image:
                        if not old_image == "":
                            os.remove(old_image)
                        dest = shutil.copy(self.image_path, acc_img_path)
                        new_dest = (
                            f"{acc_img_path}\{img_name}.png"
                            if dest.endswith(".png")
                            else f"{acc_img_path}\{img_name}.jpg"
                        )
                        os.rename(dest, new_dest)
                        save_image = new_dest
                    else:
                        save_image = self.image_path
                else:
                    old_image = self.kwargs["user"]["details"]["Image"]
                    if not old_image == "":
                        os.remove(old_image)
                try:
                    db.execute(
                        """UPDATE users SET
                            name=?,
                            account_number=?,
                            shares=?,
                            phonenumber=?,
                            email=?,
                            address=?,
                            account_type=?,
                            profile_picture=?
                            WHERE id=?;""",
                        (
                            self.name.text().rstrip(),
                            self.acc_no.text().rstrip(),
                            self.shares.text().rstrip(),
                            self.mob_int.text().rstrip(),
                            self.email_int.text().rstrip(),
                            self.addr_int.text().rstrip().capitalize(),
                            self.acc_type,
                            save_image,
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
                            self.next_fn_int.text().rstrip().capitalize(),
                            self.next_mn_int.text().rstrip().capitalize(),
                            self.next_ln_int.text().rstrip().capitalize(),
                            self.next_mob_int.text().rstrip(),
                            self.next_addr_int.text().rstrip().capitalize(),
                            self.next_rel_int.text().rstrip().capitalize(),
                            self.kwargs["user"]["details"]["id"],
                        ),
                    )
                    db.execute(
                        """UPDATE company SET
                            name=?,
                            telephone=?,
                            address=? WHERE user_id=?;""",
                        (
                            self.cn_int.text().rstrip().capitalize(),
                            self.ct_int.text().rstrip(),
                            self.cadd_int.text().rstrip().capitalize(),
                            self.kwargs["user"]["details"]["id"],
                        ),
                    )
                    self.params["db"].conn.commit()
                    msg.setIconPixmap(
                        QPixmap(self.params["ctx"].get_resource("icon/success.png"))
                    )
                    msg.setText(f"Account successfully updated")
                    msg.buttonClicked.connect(self._back)
                except Exception as e:
                    msg.setIconPixmap(
                        QPixmap(self.params["ctx"].get_resource("icon/error.png"))
                    )
                    msg.setText(f"Error updating account, please check the form again")
            msg.setDefaultButton(QMessageBox.Ok)
            msg.exec_()
            msg.show()

    def _back(self):
        self.params["parent"]["back_btn"].click()
        self.params["parent"]["back_btn"].click()
        self.params["parent"]["back_btn"].click()

    def _clear_all(self):
        self.picture.setPixmap(QPixmap(self.blank_image))
        self.remove_btn.setDisabled(True)
        self.dor.setDateTime(QDateTime.currentDateTime())
        self.name.clear()
        self.acc_no.clear()
        self.shares.clear()
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
