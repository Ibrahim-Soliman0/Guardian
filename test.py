import sys
import json
import subprocess
import time, os

from PySide6.QtCore import QUrl, QObject, Slot, QTimer
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtWidgets import QApplication, QSystemTrayIcon, QMenu
from PySide6.QtGui import QIcon, QAction
import winreg


def add_to_startup():
    # Get the full path to the current executable/script
    exe_path = os.path.realpath(sys.argv[0])
    print(exe_path)
    reg_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, reg_path, 0, winreg.KEY_WRITE)
    except FileNotFoundError:
        key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, reg_path)
    winreg.SetValueEx(key, "MyApp", 0, winreg.REG_SZ, exe_path)
    winreg.CloseKey(key)
    print("Added to startup successfully!")


def remove_from_startup():
    reg_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, reg_path, 0, winreg.KEY_WRITE)
        winreg.DeleteValue(key, "MyApp")
        winreg.CloseKey(key)
        print("Removed from startup successfully!")
    except FileNotFoundError:
        print("Registry key or startup entry not found.")
    except OSError as e:
        print("Error removing startup entry:", e)


class SettingsManager(QObject):
    def __init__(self, context, parent=None):
        super(SettingsManager, self).__init__(parent)
        self.filename = "settings.json"
        self._settings = {}
        self.loadSettings()
        self.win = parent
        self.ctx = context

    def loadSettings(self):
        try:
            with open(self.filename, "r") as f:
                self._settings = json.load(f)
        except Exception as e:
            print("Error loading settings:", e)
            self._settings = {}

    def applySettings(self, changedKey=None):
        try:
            self.loadSettings()
            if changedKey is not None:
                if changedKey == "isMonitoringActive":
                    if self._settings.get("isMonitoringActive", 0) == 1:
                        self.enableMonitoring()
                    else:
                        self.disableMonitoring()
                elif changedKey == "isActiveAutoStart":
                    if self._settings.get("isActiveAutoStart", 0) == 1:
                        self.enableAutoStart()
                    else:
                        self.disableAutoStart()
                elif changedKey == "isActiveSendData":
                    if self._settings.get("isActiveSendData", 0) == 1:
                        self.enableSendData()
                    else:
                        self.disableSendData()
            else:
                if self._settings.get("isMonitoringActive", 0) == 1:
                    self.enableMonitoring()
                else:
                    self.disableMonitoring()

                if self._settings.get("isActiveAutoStart", 0) == 1:
                    self.enableAutoStart()
                else:
                    self.disableAutoStart()

                if self._settings.get("isActiveSendData", 0) == 1:
                    self.enableSendData()
                else:
                    self.disableSendData()

        except Exception as e:
            print("Error applying settings:", e)

    @Slot(str, int)
    def setSetting(self, key, value):
        self._settings[key] = value
        self.saveSettings(key)

    @Slot(str, result=object)
    def getSetting(self, key):
        print(f"getSetting called for key={key}")
        return self._settings.get(key, None)

    def saveSettings(self, changedKey=None):
        try:
            with open(self.filename, "w") as f:
                json.dump(self._settings, f, indent=4)
            print("Settings saved successfully.")
            self.applySettings(changedKey)
        except Exception as e:
            print("Error saving settings:", e)

    def enableMonitoring(self):
        print("Auto start enabled.")
        global TRAY_ICON
        if TRAY_ICON:
            TRAY_ICON.setIcon(QIcon("icons_accent/ON_Shield.svg"))



    def disableMonitoring(self):
        print("Auto start disabled.")
        global TRAY_ICON
        if TRAY_ICON:
            TRAY_ICON.setIcon(QIcon("icons_accent/OFF_Shield.svg"))


def create_tray_icon(main_window):
    tray_icon = QSystemTrayIcon(QIcon("icons_accent/OFF_Shield.svg"), main_window)
    tray_menu = QMenu()

    action_show = QAction("Show", tray_menu)
    action_show.triggered.connect(lambda: main_window.show())
    tray_menu.addAction(action_show)

    action_hide = QAction("Hide", tray_menu)
    action_hide.triggered.connect(lambda: main_window.hide())
    tray_menu.addAction(action_hide)

    action_quit = QAction("Quit", tray_menu)
    action_quit.triggered.connect(lambda: QApplication.instance().quit())
    tray_menu.addAction(action_quit)

    tray_icon.setContextMenu(tray_menu)
    tray_icon.show()

    # Store the tray icon in a global variable to prevent it from being garbage-collected.
    global TRAY_ICON
    TRAY_ICON = tray_icon


def load_main_window(engine, ctx):
    print("Loading main window...")

    try:
        with open("settings.json", "r") as f:
            userSettings = json.load(f)
    except Exception as e:
        print("Error loading settings.json:", e)
        userSettings = {}

    engine.rootContext().setContextProperty("userSettings", userSettings)

    settingsManager = SettingsManager(ctx, parent=engine)
    engine.rootContext().setContextProperty("settingsManager", settingsManager)

    main_qml_file = QUrl.fromLocalFile(r"qml\App.qml")
    engine.load(main_qml_file)

    root_objects = engine.rootObjects()
    if not root_objects:
        print("Error: Could not load App.qml")
        sys.exit(-1)
    main_window = root_objects[1]

    if userSettings.get("isActiveMinimizedInSystemTray", 0) == 1:
        main_window.hide()
        print("Starting minimized in system tray.")
    else:
        main_window.show()
        print("Starting normally.")

    create_tray_icon(main_window)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    engine = QQmlApplicationEngine()
    ctx = engine.rootContext()

    # Optionally remove or add to startup as needed
    # add_to_startup()

    # Load the splash screen QML
    splash_screen_url = QUrl.fromLocalFile(r"qml\SplashScreen.qml")
    engine.load(splash_screen_url)

    splash_objects = engine.rootObjects()
    if not splash_objects:
        print("Error: Could not load SplashScreen.qml")
        sys.exit(-1)
    splash_screen = splash_objects[0]

    # After 1 second, hide the splash screen and load the main window.
    QTimer.singleShot(1000, lambda: [
        splash_screen.setProperty("visible", False),
        load_main_window(engine, ctx)
    ])

    sys.exit(app.exec())
