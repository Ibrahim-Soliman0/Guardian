import sys
import json
import os, subprocess
from PySide6.QtCore import QUrl, QTimer
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtWidgets import QApplication, QSystemTrayIcon, QMenu
from PySide6.QtGui import QIcon, QAction
from SettingsManager import SettingsManager


def create_tray_icon(main_window, settingsManager):
    tray_icon = QSystemTrayIcon(QIcon("icons_accent/OFF_Shield.svg"), main_window)
    if settingsManager.getSetting("isMonitoringActive") == 1:
        tray_icon.setIcon(QIcon("icons_accent/ON_Shield.svg"))
    else:
        tray_icon.setIcon(QIcon("icons_accent/OFF_Shield.svg"))
    tray_menu = QMenu()

    def getText():
        return "Disable Monitoring" if settingsManager.getSetting("isMonitoringActive") == 1 else "Enable Monitoring"

    action_toggle_monitoring = QAction(getText(), tray_menu)
    action_toggle_monitoring.setCheckable(True)
    action_toggle_monitoring.setChecked(bool(settingsManager.getSetting("isMonitoringActive")))

    def toggle_monitoring(checked):
        settingsManager.setSetting("isMonitoringActive", 1 if checked else 0)
        action_toggle_monitoring.setText(getText())

    action_toggle_monitoring.triggered.connect(toggle_monitoring)
    tray_menu.addAction(action_toggle_monitoring)

    action_quit = QAction(QIcon("icons_accent/exit.png"), "Quit", tray_menu)
    action_quit.triggered.connect(lambda: QApplication.instance().quit())
    tray_menu.addAction(action_quit)

    tray_icon.setContextMenu(tray_menu)
    tray_icon.activated.connect(lambda reason: main_window.show() if reason == QSystemTrayIcon.Trigger else None)
    tray_icon.show()

    def updateTrayAction(key, value):
        if key == "isMonitoringActive":
            action_toggle_monitoring.setChecked(bool(value))
            action_toggle_monitoring.setText("Disable Monitoring" if value == 1 else "Enable Monitoring")

    settingsManager.settingsChanged.connect(updateTrayAction)

    settingsManager.trayIcon = tray_icon


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
    if int(userSettings.get("isActiveMinimizedInSystemTray", 0)) == 1:
        main_window.hide()
        print("Starting minimized in system tray.")
    else:
        main_window.show()
        print("Starting normally.")
    create_tray_icon(main_window, settingsManager)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    engine = QQmlApplicationEngine()
    ctx = engine.rootContext()
    splash_screen_url = QUrl.fromLocalFile(r"qml\SplashScreen.qml")
    engine.load(splash_screen_url)
    splash_objects = engine.rootObjects()
    if not splash_objects:
        print("Error: Could not load SplashScreen.qml")
        sys.exit(-1)
    splash_screen = splash_objects[0]
    QTimer.singleShot(1000, lambda: [
        splash_screen.setProperty("visible", False),
        load_main_window(engine, ctx)
    ])
    sys.exit(app.exec())
