from PySide6.QtCore import QObject, Slot, Signal
from PySide6.QtGui import QIcon
import json, os, sys
import winreg

class AlertHandler(QObject):
    showAlert = Signal()

    @Slot()
    def triggerAlert(self):
        self.showAlert.emit()



class SettingsManager(QObject):
    # Signal to indicate a setting has changed (key, new value)
    settingsChanged = Signal(str, object)

    def __init__(self, context, trayIcon=None, parent=None):
        super(SettingsManager, self).__init__(parent)
        self.filename = "settings.json"
        self._settings = {}
        self.loadSettings()
        self.ctx = context
        self.trayIcon = trayIcon  # Reference to the tray icon

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
                        self.addToStartup()
                    else:
                        self.removeFromStartup()
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

                if self._settings.get("isActiveMinimizedInSystemTray", 0) == 1:
                    self.enableMinimizeToTray()
                else:
                    self.disableMinimizeToTray()

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
        return self._settings.get(key, None)

    def saveSettings(self, changedKey=None):
        try:
            with open(self.filename, "w") as f:
                json.dump(self._settings, f, indent=4)
            print("Settings saved successfully.")
            self.ctx.setContextProperty("userSettings", self._settings)
            if changedKey:
                self.settingsChanged.emit(changedKey, self._settings[changedKey])
            self.applySettings(changedKey)
        except Exception as e:
            print("Error saving settings:", e)

    def enableMonitoring(self):
        print("Monitoring enabled.")
        if self.trayIcon:
            self.trayIcon.setIcon(QIcon("icons_accent/ON_Shield.svg"))

    def disableMonitoring(self):
        print("Monitoring disabled.")
        if self.trayIcon:
            self.trayIcon.setIcon(QIcon("icons_accent/OFF_Shield.svg"))

    def addToStartup(self):
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

    def removeFromStartup(self):
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

    def enableSendData(self):
        print("Send data enabled.")

    def disableSendData(self):
        print("Send data disabled.")
