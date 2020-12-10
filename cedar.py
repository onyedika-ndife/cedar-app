import sys
from datetime import datetime
from PyQt5.QtWidgets import (
    QApplication,
)
from app import MainWindow, DB
from apscheduler.schedulers.qt import QtScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor


jobstores = {"default": SQLAlchemyJobStore(url="sqlite:///db.sqlite3")}
executors = {"default": ThreadPoolExecutor(20), "processpool": ProcessPoolExecutor(5)}
job_defaults = {"coalesce": False, "max_instances": 3}


if __name__ == "__main__":
    app = QApplication(sys.argv)
    db = DB.DataBase()
    qtsched = QtScheduler(
        jobstores=jobstores,
        executors=executors,
        job_defaults=job_defaults,
    )
    view = MainWindow.MainWindow(database=db, scheduler=qtsched)
    qtsched.start()
    # view.setWindowIcon(QIcon("./assets/icons/login.png"))
    view.show()
    view.raise_()
    sys.exit(app.exec_())