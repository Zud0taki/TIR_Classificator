# import necessary libraries
from PyQt5.QtCore import QObject, pyqtSignal


# define and initialize the QObject GUITrigger
class GUITrigger(QObject):
    def __init__(self):
        self.trigger = pyqtSignal()
        self.logstring = "Hello World!"

    def executeTrigger(self):
        self.trigger.emit()