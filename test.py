import subprocess
import sys

from PySide6.QtCore import QTimer, QUrl, QObject, Slot
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtWidgets import QApplication


class MainApp(QObject):

    def __init__(self, context, parent=None):
        super(MainApp, self).__init__(parent)
        self.win = parent
        self.ctx = context

    @Slot(str)
    def foo(self, aword):
        print(f'from qml: {aword} was received')
        if aword == 1:
            subprocess.Popen(["python", "Opened_Files.py"], shell=True)


def load_main_window(engine, ctx):
    print("Loading main window...")
    # Load the main QML file
    main_qml_file = QUrl.fromLocalFile(r"qml\Screen01.ui.qml")
    engine.load(main_qml_file)

    # Ensure the main window is loaded
    root_objects = engine.rootObjects()
    if not root_objects:
        print("Error: Could not load Screen01.ui.qml")
        sys.exit(-1)

    main_window = root_objects[-1]  # Load the last object (main window)
    py_mainapp = MainApp(ctx, main_window)
    ctx.setContextProperty("py_mainapp", py_mainapp)

    # Show the main window
    main_window.setProperty("visible", True)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    engine = QQmlApplicationEngine()
    ctx = engine.rootContext()

    # Load the splash screen QML
    splash_screen_url = QUrl.fromLocalFile(r"qml\SplashScreen.qml")
    engine.load(splash_screen_url)

    # Ensure the splash screen is loaded
    splash_objects = engine.rootObjects()
    if not splash_objects:
        print("Error: Could not load SplashScreen.qml")
        sys.exit(-1)

    splash_screen = splash_objects[0]

    # Set a timer to load the main window after 3 seconds
    QTimer.singleShot(3000, lambda: [splash_screen.setProperty("visible", False), load_main_window(engine, ctx)])

    sys.exit(app.exec())
