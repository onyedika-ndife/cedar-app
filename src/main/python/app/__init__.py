import os
from PyQt5.QtCore import QRunnable, QObject, pyqtSignal

home_dir = os.path.expanduser("~")
data_dir = os.sep.join([home_dir, "Cedar", "Database"])
db_file = os.sep.join([data_dir, "db.sqlite3"])
data_dir_2 = os.sep.join([home_dir, "Cedar", "Backup"])
# backup_db_file = os.sep.join([data_dir_2, "db.sqlite3"])


class Worker(QRunnable):
    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()

        # Store constructor arguments (re-used for processing)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()
        self.kwargs["result"] = self.signals.result

    def run(self):
        # Retrieve args/kwargs here; and fire processing using them
        result = self.fn(*self.args, **self.kwargs)
        self.signals.result.emit(result)


class WorkerSignals(QObject):
    result = pyqtSignal(list)
