import time

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from app import (
    Worker,
    WorkerSignals,
    deposit_form,
    ldw_list,
    ldw_user,
    loan_clear,
    loan_form,
    setting,
    user_add,
    user_list,
    withdrawal_form,
    home_dir,
    import_data,
)


class MainWindow(QMainWindow):
    def __init__(self, database, scheduler, ctx):
        super().__init__()
        self.setMinimumSize(840, 580)
        self.move(255, 100)
        self.setWindowTitle("Cedar App")
        self.setStyleSheet(open(ctx.get_resource("css/style.css")).read())

        self.main_widget = QStackedWidget()

        self.params = {
            "parent": {
                "self": self,
                "widget": self.main_widget,
            },
            "db": database,
            "qtsched": scheduler,
            "ctx": ctx,
        }
        self.setCentralWidget(self.main_widget)
        self.threadpool = QThreadPool()

        self._view()

    def _sidebar(self):
        next_layout = QHBoxLayout()
        self.next_widget = QWidget()
        self.next_widget.setLayout(next_layout)
        side_layout = QVBoxLayout()
        side_widget = QWidget()
        side_widget.setLayout(side_layout)
        back_btn = QPushButton(
            QIcon(self.params["ctx"].get_resource("icon/back.png")), None
        )
        back_btn.setFixedSize(35, 35)
        back_btn.setIconSize(QSize(25, 25))
        back_btn.setToolTip("Back")

        self.params["parent"]["back_btn"] = back_btn

        setting_btn = QPushButton(
            QIcon(self.params["ctx"].get_resource("icon/settings.png")), None
        )
        setting_btn.setFixedSize(35, 35)
        setting_btn.setIconSize(QSize(25, 25))
        setting_btn.setToolTip("Settings")

        setting_btn.clicked.connect(self._handle_setting)

        side_layout.addWidget(back_btn, alignment=Qt.AlignTop)
        side_layout.addWidget(setting_btn, alignment=Qt.AlignBottom)
        side_layout.setContentsMargins(0, 0, 0, 0)
        next_layout.addWidget(side_widget)
        self.next_stacked = QStackedWidget()
        back_btn.clicked.connect(self._back)
        next_layout.addWidget(self.next_stacked)

    def _view(self):
        self.initial_widget = QWidget()
        initial_layout = QVBoxLayout()
        top_layout = QHBoxLayout()

        setting_btn = QPushButton(
            QIcon(self.params["ctx"].get_resource("icon/settings.png")), "Settings"
        )
        setting_btn.setIconSize(QSize(20, 20))
        self.params["parent"]["setting_btn"] = setting_btn
        setting_btn.clicked.connect(self._handle_setting)

        imp_data_btn = QPushButton(
            QIcon(self.params["ctx"].get_resource("icon/settings.png")), "Import Data"
        )
        imp_data_btn.setIconSize(QSize(20, 20))
        imp_data_btn.clicked.connect(self._handle_imp_data)

        top_layout.addWidget(imp_data_btn, alignment=Qt.AlignLeft)
        top_layout.addWidget(setting_btn, alignment=Qt.AlignRight)

        initial_layout.addLayout(top_layout)

        group_box_layout = QGridLayout()
        initial_layout.addLayout(group_box_layout)

        au_btn = QPushButton(
            QIcon(self.params["ctx"].get_resource("icon/create_account.png")),
            "Register Member",
        )
        ul_btn = QPushButton(
            QIcon(self.params["ctx"].get_resource("icon/account_list.png")),
            "List of Members",
        )
        au_btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        au_btn.setIconSize(QSize(50, 50))
        au_btn.setObjectName("home")
        ul_btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        ul_btn.setObjectName("home")
        ul_btn.setIconSize(QSize(50, 50))

        group_box_layout.addWidget(au_btn, 0, 0)
        group_box_layout.addWidget(ul_btn, 0, 1)

        loan_lay = QHBoxLayout()

        loan_form_btn = QPushButton(
            QIcon(self.params["ctx"].get_resource("icon/request_loan.png")),
            "Request Loan",
        )
        loan_list_btn = QPushButton(
            QIcon(self.params["ctx"].get_resource("icon/loan.png")),
            "Issued Loans",
        )
        loan_clear_btn = QPushButton(
            QIcon(self.params["ctx"].get_resource("icon/cleared_loan.png")),
            "Repay Loan",
        )
        loan_form_btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        loan_form_btn.setObjectName("home")
        loan_form_btn.setIconSize(QSize(50, 50))
        loan_list_btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        loan_list_btn.setObjectName("home")
        loan_list_btn.setIconSize(QSize(50, 50))
        loan_clear_btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        loan_clear_btn.setObjectName("home")
        loan_clear_btn.setIconSize(QSize(50, 50))

        loan_lay.addWidget(loan_form_btn)
        loan_lay.addWidget(loan_list_btn)
        loan_lay.addWidget(loan_clear_btn)

        group_box_layout.addLayout(loan_lay, 1, 0, 1, 0)

        deposit_btn = QPushButton(
            QIcon(self.params["ctx"].get_resource("icon/deposit.png")), "Deposit"
        )
        deposit_list_btn = QPushButton(
            QIcon(self.params["ctx"].get_resource("icon/deposit_list.png")),
            "Deposit History",
        )
        deposit_btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        deposit_list_btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        deposit_btn.setObjectName("home")
        deposit_btn.setIconSize(QSize(50, 50))
        deposit_list_btn.setObjectName("home")
        deposit_list_btn.setIconSize(QSize(50, 50))

        group_box_layout.addWidget(deposit_btn, 2, 0)
        group_box_layout.addWidget(deposit_list_btn, 2, 1)

        withdraw_btn = QPushButton(
            QIcon(self.params["ctx"].get_resource("icon/withdraw.png")),
            "Withdraw",
        )
        withdraw_list_btn = QPushButton(
            QIcon(self.params["ctx"].get_resource("icon/withdraw_list.png")),
            "Withdrawal History",
        )
        withdraw_btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        withdraw_list_btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        withdraw_btn.setObjectName("home")
        withdraw_btn.setIconSize(QSize(50, 50))
        withdraw_list_btn.setObjectName("home")
        withdraw_list_btn.setIconSize(QSize(50, 50))

        group_box_layout.addWidget(withdraw_btn, 3, 0)
        group_box_layout.addWidget(withdraw_list_btn, 3, 1)

        self.initial_widget.setLayout(initial_layout)
        self.main_widget.addWidget(self.initial_widget)

        au_btn.clicked.connect(self._handle_aub)
        ul_btn.clicked.connect(self._handle_ul)
        loan_form_btn.clicked.connect(self._handle_reqloan)
        loan_list_btn.clicked.connect(lambda: self._handle_ldw_list(context="loans"))
        loan_clear_btn.clicked.connect(
            lambda: self._handle_ldw_list(context="clear_loans")
        )
        deposit_list_btn.clicked.connect(
            lambda: self._handle_ldw_list(context="deposits")
        )
        withdraw_list_btn.clicked.connect(
            lambda: self._handle_ldw_list(context="withdrawals")
        )
        deposit_btn.clicked.connect(self._handle_df)
        withdraw_btn.clicked.connect(self._handle_wf)

        self._check_setting()

    def _handle_aub(self):
        self._sidebar()
        self.params["next"] = {"widget": self.next_stacked}
        view = user_add.ADD_USER(self.params)
        self.next_stacked.addWidget(view)
        self.main_widget.addWidget(self.next_widget)
        self.main_widget.setCurrentWidget(self.next_widget)

    def _handle_ul(self):
        self._sidebar()
        self.params["next"] = {"widget": self.next_stacked}
        view = user_list.USER_LIST(self.params)
        self.next_stacked.addWidget(view)
        self.main_widget.addWidget(self.next_widget)
        self.main_widget.setCurrentWidget(self.next_widget)

    def _handle_reqloan(self):
        self._sidebar()
        self.params["next"] = {"widget": self.next_stacked}
        view = loan_form.LOAN_FORM(self.params)
        self.next_stacked.addWidget(view)
        self.main_widget.addWidget(self.next_widget)
        self.main_widget.setCurrentWidget(self.next_widget)

    def _handle_ldw_list(self, context):
        self._sidebar()
        self.params["next"] = {"widget": self.next_stacked}
        view = ldw_list.LDW_LIST(self.params, context)
        self.next_stacked.addWidget(view)
        self.main_widget.addWidget(self.next_widget)
        self.main_widget.setCurrentWidget(self.next_widget)

    def _handle_df(self):
        view = deposit_form.DEPOSIT_FORM(self.params)
        view.exec_()

    def _handle_wf(self):
        self._sidebar()
        self.params["next"] = {"widget": self.next_stacked}
        view = withdrawal_form.WITHDRAWAL_FORM(self.params)
        self.next_stacked.addWidget(view)
        self.main_widget.addWidget(self.next_widget)
        self.main_widget.setCurrentWidget(self.next_widget)

    def _handle_setting(self):
        view = setting.SETTING(self.params)
        view.show()

    def _handle_imp_data(self):
        view = import_data.IMPORT(self.params)
        view.exec_()

    def execute_check_fn(self, data, check):
        return data

    def _check_set_data(self, account_type):
        account_type = "member" if account_type == 0 else "staff"
        db = self.params["db"].conn.cursor()

        db.execute("""SELECT * FROM settings WHERE account_type=?;""", (account_type,))
        data = db.fetchone()

        return data

    def _check_setting(self):
        # Pass the function to execute
        db = self.params["db"].conn.cursor()

        db.execute("""SELECT * FROM settings;""")
        data = db.fetchall()

        worker = CHECK_SETTING_WORKER(
            self.execute_check_fn, data
        )  # Any other args, kwargs are passed to the run function

        worker.signals.result.connect(self._one_time_check)

        # Execute
        self.threadpool.start(worker)

    @pyqtSlot(list)
    def _one_time_check(self, data):
        if not len(data) > 0:
            msg = QMessageBox()
            msg.setStyleSheet(
                open(self.params["ctx"].get_resource("css/style.css")).read()
            )
            msg.setIconPixmap(
                QPixmap(self.params["ctx"].get_resource("icon/high_priority.png"))
            )
            msg.setText(f"Input rates for Cedar App")
            msg.setWindowTitle("Notice")
            msg.setDefaultButton(QMessageBox.Ok)
            msg.buttonClicked.connect(self._handle_setting)
            msg.exec_()

    def _back(self):
        if not self.params["parent"]["widget"].currentIndex() == 0:
            if self.params["next"]["widget"].currentIndex() >= 1:
                current = self.params["next"]["widget"].widget(
                    self.params["next"]["widget"].currentIndex()
                )
                self.params["next"]["widget"].setCurrentIndex(
                    self.params["next"]["widget"].currentIndex() - 1
                )
                self.params["next"]["widget"].removeWidget(current)
            else:
                self.params["parent"]["widget"].setCurrentIndex(0)
                if self.params["parent"]["widget"].count() > 1:
                    self.params["parent"]["widget"].removeWidget(self.next_widget)


class CHECK_SETTING_WORKER(QRunnable):
    def __init__(self, fn, *args, **kwargs):
        super(CHECK_SETTING_WORKER, self).__init__()
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()
        self.kwargs["check"] = self.signals.result

    def run(self):
        check = self.fn(*self.args, **self.kwargs)
        time.sleep(1.0)
        self.signals.result.emit(check)
