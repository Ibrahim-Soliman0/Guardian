import sys
import json
import os
from pathlib import Path
from PySide6.QtCore import Qt, QUrl, QTimer
from PySide6.QtNetwork import QLocalServer
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QWidget
from PySide6.QtGui import QIcon, QAction, QColor
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebEngineCore import QWebEngineSettings
from SettingsManager import SettingsManager, AlertHandler
from Database import SQL
from Report import AlertProcessor

sql = SQL()


class EnhancedSplashScreen(QWidget):
    def __init__(self, svg_path, parent=None):
        super().__init__(parent)

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)

        self.setAttribute(Qt.WA_TranslucentBackground)

        self.web_view = QWebEngineView(self)

        self.web_view.settings().setAttribute(QWebEngineSettings.WebGLEnabled, True)
        self.web_view.settings().setAttribute(QWebEngineSettings.Accelerated2dCanvasEnabled, True)

        self.web_view.setZoomFactor(1)

        self.web_view.page().setBackgroundColor(QColor(0, 0, 0, 0))

        svg_path = Path(svg_path).resolve()

        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0">
            <style>
                body {{
                    margin: 0;
                    padding: 0;
                    background-color: transparent;
                    overflow: hidden;
                    width: 100vw;
                    height: 100vh;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                }}
                .svg-container {{
                    width: 100%;
                    height: 100%;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                }}
                /* Force high-quality rendering */
                svg {{
                    width: 100%;
                    height: 100%;
                    shape-rendering: geometricPrecision;
                    text-rendering: geometricPrecision;
                    image-rendering: optimizeQuality;
                    -webkit-transform: translateZ(0);
                    transform: translateZ(0);
                }}
            </style>
        </head>
        <body>
            <div class="svg-container">
                <object data="file://{svg_path}" type="image/svg+xml" width="100%" height="100%"></object>
            </div>
        </body>
        </html>
        """

        temp_dir = os.path.dirname(svg_path) if os.path.dirname(svg_path) else "."
        self.temp_html_path = os.path.join(temp_dir, "temp_splash_hq.html")
        with open(self.temp_html_path, "w") as f:
            f.write(html_content)

        self.web_view.load(QUrl.fromLocalFile(self.temp_html_path))

        self.resize(300, 300)
        self.web_view.resize(300, 300)

        # Center on screen
        screen_geometry = QApplication.primaryScreen().geometry()
        x = (screen_geometry.width() - self.width()) // 2
        y = (screen_geometry.height() - self.height()) // 2
        self.move(x, y)

    def cleanup(self):
        try:
            if hasattr(self, 'temp_html_path') and os.path.exists(self.temp_html_path):
                os.remove(self.temp_html_path)
        except Exception as e:
            print(f"Error removing temporary file: {e}")

def write_data_file_from_db(output_path):
    try:
        rows_pos = sql.get_freq_gt_zero()
        normals = [(d, f) for d, f, t in rows_pos if t == 'normal']
        mals    = [(d, f) for d, f, t in rows_pos if t == 'malicious']

        rows_zero = sql.get_freq_eq_zero()
        normals0 = [d for d, t in rows_zero if t == 'normal']
        mals0    = [d for d, t in rows_zero if t == 'malicious']

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(f"{len(normals)} {len(mals)}\n")
            for name, freq in normals:
                f.write(f"{name} {freq}\n")
            for name, freq in mals:
                f.write(f"{name} {freq}\n")

            f.write(f"{len(normals0)} {len(mals0)}\n")
            for name in normals0:
                f.write(f"{name}\n")
            for name in mals0:
                f.write(f"{name}\n")

        print(f"Exported detection_data → {output_path}")

    except Exception as e:
        print("Failed to export detection_data:", e)

def write_weights_file_from_db(records):
    with open(r"C:\Windows\System32\AntiMalware\weights.txt", 'w') as f:
        for _id, weight in records:
            f.write(f"{str(weight).lower()}\n")

def update_data(userSettings):
    pass
    #if int(userSettings.get("AutoUpdate", 0)) == 1:
    #    db_version = sql.get_version()
    #    if db_version > int(userSettings.get("Version", 0)):
    #        #userSettings['Version'] = db_version
    #        #with open('settings.json', 'w') as f:
    #        #    json.dump(userSettings, f, indent=4)
    #        write_data_file_from_db("Data.txt")
    #        write_weights_file_from_db(sql.get_weight_data())

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

    action_quit = QAction(QIcon("icons_accent/exit.png"), "Exit", tray_menu)
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
    settingsManager.applySettings("isMonitoringActive")
    main_qml_file = QUrl.fromLocalFile(r"qml\App.qml")
    engine.load(main_qml_file)
    root_objects = engine.rootObjects()
    if not root_objects:
        print("Error: Could not load App.qml")
        sys.exit(-1)

    main_window = root_objects[-1]
    if int(userSettings.get("isActiveMinimizedInSystemTray", 0)) == 1:
        main_window.hide()
        print("Starting minimized in system tray.")
    else:
        main_window.show()
        print("Starting normally.")

    update_data(userSettings)

    create_tray_icon(main_window, settingsManager)
    return main_window

def setup_local_server():
    global localServer
    localServer = QLocalServer()
    QLocalServer.removeServer("AlertTriggerServer")
    if not localServer.listen("AlertTriggerServer"):
        print("Unable to start local server")
        return
    localServer.newConnection.connect(handle_new_connection)
    print("Local server listening on 'AlertTriggerServer'.")

def handle_new_connection():
    socket = localServer.nextPendingConnection()
    socket.readyRead.connect(lambda: process_socket_message(socket))


def process_socket_message(socket):
    message = socket.readAll().data().decode().strip()
    malware_type = "Unknown"

    if message.startswith("trigger_alert:"):
        try:
            parts = message.split(":", 1)
            if len(parts) > 1 and parts[1]:
                malware_type = parts[1]
            print(f"Received trigger_alert message with type: {malware_type}")

            if hasattr(alertHandler, "triggerAlertWithType"):
                alertHandler.triggerAlertWithType(malware_type)
            elif hasattr(alertHandler, "triggerAlert"):
                print("AlertHandler.triggerAlertWithType not found. Falling back to triggerAlert().")
                alertHandler.triggerAlert()
            else:
                print("AlertHandler has neither triggerAlertWithType nor triggerAlert.")

        except Exception as e:
            print(f"Error processing message '{message}': {e}")
            if hasattr(alertHandler, "triggerAlert"):
                alertHandler.triggerAlert()

    else:
        print(f"Received unknown message: {message}")

    socket.disconnectFromServer()

if __name__ == "__main__":
    sql = SQL()
    app = QApplication(sys.argv)
    engine = QQmlApplicationEngine()
    ctx = engine.rootContext()

    alertHandler = AlertHandler()
    engine.rootContext().setContextProperty("alertHandler", alertHandler)

    alert_processor = AlertProcessor()
    engine.rootContext().setContextProperty("alertProcessor", alert_processor)

    alert_qml_url = QUrl.fromLocalFile(r"qml\Alert.qml")
    engine.load(alert_qml_url)
    alert_objects = engine.rootObjects()
    if not alert_objects:
        print("Error: Could not load Alert.qml")
        sys.exit(-1)
    alert_window = alert_objects[0]
    alert_window.setProperty("visible", False)

    script_dir = os.path.dirname(os.path.abspath(__file__))

    svg_path = "icons_accent/SplashScreen.svg"

    splash_screen = EnhancedSplashScreen(svg_path)
    splash_screen.show()

    def start_main():
        splash_screen.hide()
        splash_screen.cleanup()
        main_window = load_main_window(engine, ctx)
        alert_window.setProperty("mainWindow", main_window)
        setup_local_server()

    QTimer.singleShot(3000, start_main)

    sys.exit(app.exec())
