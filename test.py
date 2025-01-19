import sys

from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine


app = QGuiApplication(sys.argv)

engine = QQmlApplicationEngine()
engine.quit.connect(app.quit)

try:
    engine.load(r'qml\Screen01.ui.qml')
except Exception as e:
    print(e)

sys.exit(app.exec())