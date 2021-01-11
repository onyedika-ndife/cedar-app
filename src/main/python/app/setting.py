from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from datetime import datetime


class SETTING(QDialog):
    def __init__(self, params):
        super().__init__()
        self.params = params
        self.db = self.params["db"].conn.cursor()

        self.setFixedSize(350, 250)
        self.setWindowTitle("Cedar Settings")
        self.setStyleSheet(
            open(self.params["ctx"].get_resource("css/style.css")).read()
        )
        self.setWindowIcon(QIcon(self.params["ctx"].get_resource("icon/settings.png")))
        self.setWindowFlags(Qt.WindowStaysOnTopHint)

        self._view()

    def _view(self):
        data = self._check_set_data(0)
        initial_layout = QVBoxLayout()
        tab_widget = QTabWidget()
        initial_layout.addWidget(tab_widget)

        member_wid = QWidget()
        staff_wid = QWidget()

        btn_layout1 = QHBoxLayout()
        btn_layout2 = QHBoxLayout()
        btn_layout1.setContentsMargins(0, 0, 0, 0)
        btn_layout2.setContentsMargins(0, 0, 0, 0)

        # FOR Member
        gridLay = QGridLayout()

        self.inter_rate_mem = QLineEdit()
        self.inter_rate_mem.setReadOnly(True)
        self.inter_rate_mem.setValidator(QIntValidator())
        self.loan_rate_mem = QLineEdit()
        self.loan_rate_mem.setValidator(QIntValidator())
        self.loan_rate_mem.setReadOnly(True)

        gridLay.addWidget(QLabel("Interest Rate:"), 0, 0)
        gridLay.addWidget(self.inter_rate_mem, 0, 1)
        gridLay.addWidget(QLabel("%"), 0, 2)

        gridLay.addWidget(QLabel("Loan Rate:"), 1, 0)
        gridLay.addWidget(self.loan_rate_mem, 1, 1)
        gridLay.addWidget(QLabel("%"), 1, 2)

        gridLay.addWidget(QLabel("Loan Duration:"), 2, 0)
        loan_dura_gridLay = QHBoxLayout()
        self.loan_dura_mem_int = QLineEdit()
        self.loan_dura_mem_int.setValidator(QIntValidator())
        self.loan_dura_mem_opt = QComboBox()
        self.loan_dura_mem_opt.addItems(["Month(s)", "Year(s)"])
        loan_dura_gridLay.addWidget(self.loan_dura_mem_int)
        loan_dura_gridLay.addWidget(self.loan_dura_mem_opt)

        gridLay.addLayout(loan_dura_gridLay, 2, 1, 1, 2)

        gridLay.addWidget(QLabel("Interest Starts After:"), 3, 0)
        intr_start_gridLay = QHBoxLayout()
        self.intr_start_mem_int = QLineEdit()
        self.intr_start_mem_int.setValidator(QIntValidator())
        self.intr_start_mem_opt = QComboBox()
        self.intr_start_mem_opt.addItems(["Month(s)", "Year(s)"])
        intr_start_gridLay.addWidget(self.intr_start_mem_int)
        intr_start_gridLay.addWidget(self.intr_start_mem_opt)

        gridLay.addLayout(intr_start_gridLay, 3, 1, 1, 2)

        member_wid.setLayout(gridLay)

        self.save_edit_btn1 = QPushButton(None)
        self.cancel_btn1 = QPushButton("Cancel")
        self.cancel_btn1.clicked.connect(lambda: self.hide())

        self.cancel_btn1.setFixedHeight(35)
        self.save_edit_btn1.setFixedHeight(35)

        btn_layout1.addWidget(self.cancel_btn1)
        btn_layout1.addWidget(self.save_edit_btn1)

        gridLay.addLayout(btn_layout1, 4, 0, 1, 0)

        if not data is None:
            dur = data[4].split(" ")
            intr_start = data[5].split(" ")
            self.inter_rate_mem.setText(str(data[2]))
            self.loan_rate_mem.setText(str(data[3]))
            self.loan_dura_mem_int.setText(dur[0])
            self.loan_dura_mem_opt.setCurrentText(dur[1])
            self.intr_start_mem_int.setText(intr_start[0])
            self.intr_start_mem_opt.setCurrentText(intr_start[1])

            self.inter_rate_mem.setReadOnly(True)
            self.loan_rate_mem.setReadOnly(True)
            self.loan_dura_mem_int.setReadOnly(True)
            self.loan_dura_mem_opt.setDisabled(True)
            self.intr_start_mem_int.setReadOnly(True)
            self.intr_start_mem_opt.setDisabled(True)

            self.save_edit_btn1.setText("Edit")
        else:
            self.inter_rate_mem.setReadOnly(False)
            self.loan_rate_mem.setReadOnly(False)
            self.loan_dura_mem_int.setReadOnly(False)
            self.loan_dura_mem_opt.setDisabled(False)
            self.intr_start_mem_int.setReadOnly(False)
            self.intr_start_mem_opt.setDisabled(False)

            self.save_edit_btn1.setText("Save")

        tab_widget.tabBarClicked.connect(self._check_set_data)

        # FOR Staff
        gridLay = QGridLayout()
        self.inter_rate_sta = QLineEdit()
        self.inter_rate_sta.setValidator(QIntValidator())
        self.loan_rate_sta = QLineEdit()
        self.loan_rate_sta.setValidator(QIntValidator())
        self.loan_dura_sta = QLineEdit()
        self.loan_dura_sta.setValidator(QIntValidator())
        gridLay.addWidget(QLabel("Interest Rate:"), 0, 0)
        gridLay.addWidget(QLabel("Loan Rate:"), 1, 0)
        gridLay.addWidget(QLabel("Loan Duration:"), 2, 0)
        gridLay.addWidget(QLabel("%"), 0, 2)
        gridLay.addWidget(QLabel("%"), 1, 2)

        gridLay.addWidget(self.inter_rate_sta, 0, 1)
        gridLay.addWidget(self.loan_rate_sta, 1, 1)

        loan_dura_sta_lay = QHBoxLayout()
        self.loan_dura_sta_int = QLineEdit()
        self.loan_dura_sta_opt = QComboBox()
        self.loan_dura_sta_opt.addItems(["Month(s)", "Year(s)"])
        loan_dura_sta_lay.addWidget(self.loan_dura_sta_int)
        loan_dura_sta_lay.addWidget(self.loan_dura_sta_opt)

        gridLay.addLayout(loan_dura_sta_lay, 2, 1, 1, 2)

        gridLay.addWidget(QLabel("Interest Starts After:"), 3, 0)
        intr_start_gridLay = QHBoxLayout()
        self.intr_start_sta_int = QLineEdit()
        self.intr_start_sta_int.setValidator(QIntValidator())
        self.intr_start_sta_opt = QComboBox()
        self.intr_start_sta_opt.addItems(["Month(s)", "Year(s)"])
        intr_start_gridLay.addWidget(self.intr_start_sta_int)
        intr_start_gridLay.addWidget(self.intr_start_sta_opt)

        gridLay.addLayout(intr_start_gridLay, 3, 1, 1, 2)

        self.save_edit_btn2 = QPushButton(None)
        self.cancel_btn2 = QPushButton("Cancel")
        self.cancel_btn2.clicked.connect(lambda: self.hide())

        self.cancel_btn2.setFixedHeight(35)
        self.save_edit_btn2.setFixedHeight(35)

        btn_layout2.addWidget(self.cancel_btn2)
        btn_layout2.addWidget(self.save_edit_btn2)

        gridLay.addLayout(btn_layout2, 4, 0, 1, 0)

        staff_wid.setLayout(gridLay)

        self.save_edit_btn1.clicked.connect(
            lambda: self._handle_setSaveEdit(
                {"text": self.save_edit_btn1.text(), "type": "member"}
            )
        )
        self.save_edit_btn2.clicked.connect(
            lambda: self._handle_setSaveEdit(
                {"text": self.save_edit_btn2.text(), "type": "staff"}
            )
        )

        tab_widget.addTab(member_wid, "MEMBER")
        tab_widget.addTab(staff_wid, "STAFF")

        self.setLayout(initial_layout)

    def _check_set_data(self, account_type):
        account_type = "member" if account_type == 0 else "staff"
        db = self.params["db"].conn.cursor()

        db.execute("""SELECT * FROM settings WHERE account_type=?;""", (account_type,))
        data = db.fetchone()

        if account_type == "staff":
            if not data is None:
                dur = data[4].split(" ")
                intr_start = data[5].split(" ")
                self.inter_rate_sta.setText(str(data[2]))
                self.loan_rate_sta.setText(str(data[3]))
                self.loan_dura_sta_int.setText(dur[0])
                self.loan_dura_sta_opt.setCurrentText(dur[1])
                self.intr_start_sta_int.setText(intr_start[0])
                self.intr_start_sta_opt.setCurrentText(intr_start[1])

                self.inter_rate_sta.setReadOnly(True)
                self.loan_rate_sta.setReadOnly(True)
                self.loan_dura_sta_int.setReadOnly(True)
                self.loan_dura_sta_opt.setDisabled(True)
                self.intr_start_sta_int.setReadOnly(True)
                self.intr_start_sta_opt.setDisabled(True)

                self.save_edit_btn2.setText("Edit")
            else:
                self.inter_rate_sta.setReadOnly(False)
                self.loan_rate_sta.setReadOnly(False)
                self.loan_dura_sta_int.setReadOnly(False)
                self.loan_dura_sta_opt.setDisabled(False)
                self.intr_start_sta_int.setReadOnly(False)
                self.intr_start_sta_opt.setDisabled(False)

                self.save_edit_btn2.setText("Save")

        return data

    def _handle_setSaveEdit(self, params):
        interest_rate, loan_rate, loan_duration = None, None, None

        if params["text"].lower() == "edit":
            if params["type"] == "member":
                self.inter_rate_mem.setReadOnly(False)
                self.loan_rate_mem.setReadOnly(False)
                self.loan_dura_mem_int.setReadOnly(False)
                self.loan_dura_mem_opt.setDisabled(False)
                self.intr_start_mem_int.setReadOnly(False)
                self.intr_start_mem_opt.setDisabled(False)

                self.save_edit_btn1.setText("Save")
            elif params["type"] == "staff":
                self.inter_rate_sta.setReadOnly(False)
                self.loan_rate_sta.setReadOnly(False)
                self.loan_dura_sta_int.setReadOnly(False)
                self.loan_dura_sta_opt.setDisabled(False)
                self.intr_start_sta_int.setReadOnly(False)
                self.intr_start_sta_opt.setDisabled(False)
                self.save_edit_btn2.setText("Save")
        elif params["text"].lower() == "save":
            if params["type"] == "member":
                self.inter_rate_mem.setReadOnly(True)
                self.loan_rate_mem.setReadOnly(True)
                self.loan_dura_mem_int.setReadOnly(True)
                self.loan_dura_mem_opt.setDisabled(True)
                self.inter_rate_mem.setReadOnly(True)
                self.intr_start_mem_int.setReadOnly(True)
                self.intr_start_mem_opt.setDisabled(True)
                self.save_edit_btn1.setText("Edit")

                interest_rate = self.inter_rate_mem.text()
                loan_rate = self.loan_rate_mem.text()
                loan_duration = f"{self.loan_dura_mem_int.text()} {self.loan_dura_mem_opt.currentText()}"
                interest_start = f"{self.intr_start_mem_int.text()} {self.intr_start_mem_opt.currentText()}"

            elif params["type"] == "staff":
                self.inter_rate_sta.setReadOnly(True)
                self.loan_rate_sta.setReadOnly(True)
                self.loan_dura_sta_int.setReadOnly(True)
                self.loan_dura_sta_opt.setDisabled(True)
                self.inter_rate_sta.setReadOnly(True)
                self.intr_start_sta_int.setReadOnly(True)
                self.intr_start_sta_opt.setDisabled(True)
                self.save_edit_btn2.setText("Edit")

                interest_rate = self.inter_rate_sta.text()
                loan_rate = self.loan_rate_sta.text()
                loan_duration = f"{self.loan_dura_sta_int.text()} {self.loan_dura_sta_opt.currentText()}"
                interest_start = f"{self.intr_start_sta_int.text()} {self.intr_start_sta_opt.currentText()}"

            data = self._check_set_data(0 if params["type"] == "member" else 1)

            if not data is None:
                self.db.execute(
                    """UPDATE settings 
                    SET interest_rate=?, 
                    loan_rate=?,
                    loan_duration=?,
                    interest_start=?,
                    date_updated=?
                    WHERE account_type=?;""",
                    (
                        interest_rate,
                        loan_rate,
                        loan_duration,
                        interest_start,
                        datetime.today().date(),
                        params["type"],
                    ),
                )
            else:
                self.db.execute(
                    """INSERT INTO settings (
                        account_type,
                        interest_rate,
                        loan_rate,
                        loan_duration,
                        interest_start,
                        date_added,
                        date_updated) 
                        VALUES(?,?,?,?,?,?,?);""",
                    (
                        params["type"],
                        interest_rate,
                        loan_rate,
                        loan_duration,
                        interest_start,
                        datetime.today().date(),
                        datetime.today().date(),
                    ),
                )
            self.params["db"].conn.commit()

            data = self._check_set_data(0 if params["type"] == "member" else 1)
            duration = data[4].split(" ")
            intr_start = data[5].split(" ")
            if params["type"] == "member":
                self.inter_rate_mem.setText(str(data[2]))
                self.loan_rate_mem.setText(str(data[3]))
                self.loan_dura_mem_int.setText(duration[0])
                self.loan_dura_mem_opt.setCurrentText(duration[1])
                self.intr_start_mem_int.setText(intr_start[0])
                self.intr_start_mem_opt.setCurrentText(intr_start[1])

                self.inter_rate_mem.setReadOnly(True)
                self.loan_rate_mem.setReadOnly(True)
                self.loan_dura_mem_int.setReadOnly(True)
                self.loan_dura_mem_opt.setDisabled(True)
                self.intr_start_mem_int.setReadOnly(True)
                self.intr_start_mem_opt.setDisabled(True)

                self.save_edit_btn1.setText("Edit")
            elif params["type"] == "staff":
                self.inter_rate_sta.setText(str(data[2]))
                self.loan_rate_sta.setText(str(data[3]))
                self.loan_dura_sta_int.setText(duration[0])
                self.loan_dura_sta_opt.setCurrentText(duration[1])
                self.intr_start_sta_int.setText(intr_start[0])
                self.intr_start_sta_opt.setCurrentText(intr_start[1])

                self.inter_rate_sta.setReadOnly(True)
                self.loan_rate_sta.setReadOnly(True)
                self.loan_dura_sta_int.setReadOnly(True)
                self.loan_dura_sta_opt.setDisabled(True)
                self.intr_start_sta_int.setReadOnly(True)
                self.intr_start_sta_opt.setDisabled(True)

                self.save_edit_btn2.setText("Edit")
