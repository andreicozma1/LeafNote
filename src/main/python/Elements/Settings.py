from PyQt5.QtCore import QSettings
class Settings(QSettings):
    def __init__(self):
        super(Settings, self).__init__()
