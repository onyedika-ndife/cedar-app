import sys

from apscheduler.executors.pool import ProcessPoolExecutor, ThreadPoolExecutor
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.qt import QtScheduler
from fbs_runtime.application_context.PyQt5 import ApplicationContext
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from app import db_file
from app.database import DataBase
from app.main_window import MainWindow

jobstores = {"default": SQLAlchemyJobStore(url=f"sqlite:///{db_file}")}
executors = {"default": ThreadPoolExecutor(20), "processpool": ProcessPoolExecutor(5)}
job_defaults = {"coalesce": False, "max_instances": 3}


if __name__ == "__main__":
    appctxt = ApplicationContext()  # 1. Instantiate ApplicationContext
    db = DataBase()

    qtsched = QtScheduler(
        jobstores=jobstores,
        executors=executors,
        job_defaults=job_defaults,
    )
    view = MainWindow(database=db, scheduler=qtsched, ctx=appctxt)
    qtsched.start()

    view.show()
    view.raise_()
    exit_code = appctxt.app.exec_()  # 2. Invoke appctxt.app.exec_()
    sys.exit(exit_code)
