import datetime as dt
import re
from pathlib import Path
from typing import Dict

from PySide6.QtCore import QObject, Signal, Slot
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine


class AlertProcessor(QObject):
    newAlert = Signal(str, str, str, str)
    alertsCleared = Signal()

    def __init__(self):
        super().__init__()
        self.spawn_times = {}
        self._load_spawn_times()  # Call the new method

    def _load_spawn_times(self):
        self.spawn_times.clear()
        date_file = Path(r"C:\Windows\System32\AntiMalware\Date.txt")
        if date_file.exists():
            try:
                for line in date_file.read_text().splitlines():
                    if not line or ":" not in line: continue
                    name, ts = line.split(":", 1)
                    name, ts = name.strip().lower(), ts.strip()
                    parsed_ts = None
                    for fmt in ("%Y-%m-%d %H:%M:%S.%f", "%Y-%m-%d %H:%M:%S"):
                        try:
                            parts = ts.split(" ")
                            date_part = parts[0]
                            time_part = parts[1] if len(parts) > 1 else "00:00:00"
                            y, m, d = date_part.split("-")
                            m, d = m.zfill(2), d.zfill(2)
                            reconstructed_ts = f"{y}-{m}-{d} {time_part}"
                            parsed_ts = dt.datetime.strptime(reconstructed_ts, fmt)
                            break
                        except ValueError:
                            continue
                    if parsed_ts:
                        self.spawn_times[name] = parsed_ts
                    else:
                        print(f"Warning: Could not parse timestamp '{ts}' for process '{name}'")
            except Exception as e:
                print(f"Error reading or parsing Date.txt: {e}")

    @Slot()
    def initialize(self):
        # self.copy_to_alerts()
        self.process_file()
        self._initialized = True

    def copy_to_alerts(self):
        output_file_path = Path(r"C:\Windows\System32\AntiMalware\output.txt")
        if not output_file_path.exists() or output_file_path.stat().st_size == 0:
            return

        with open(output_file_path, "r", encoding="utf-8") as file:
            output_lines = [line.strip() for line in file if line.strip()]

        alerts_file_path = Path("alerts.txt")
        old_lines = []
        if alerts_file_path.exists():
            with open(alerts_file_path, "r", encoding="utf-8") as f:
                old_lines = [l.rstrip("\n") for l in f if l.strip()]

        try:
            num_output = int(output_lines[0])
        except (ValueError, IndexError):
            num_output = 0

        try:
            num_existing = int(old_lines[0])
        except (ValueError, IndexError):
            num_existing = 0

        total_count = num_output + num_existing

        new_entries = []
        for line in output_lines[1:]:
            parts = line.split()
            if len(parts) >= 2 and parts[0].lower().endswith(".exe") and parts[1].isdigit():
                proc, cnt = parts[0], parts[1]
                ts = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                new_entries.append(f"{proc} {cnt} {ts}\n")
            else:
                new_entries.append(f"{line}\n")

        with open(alerts_file_path, "w", encoding="utf-8") as f:
            f.write(f"{total_count}\n")
            if len(old_lines) > 1:
                for old in old_lines[1:]:
                    f.write(old + "\n")
            f.writelines(new_entries)

    @Slot()
    def process_file(self):
        try:
            file_path = Path("alerts.txt")
            if not file_path.exists() or file_path.stat().st_size == 0:
                return
            with open(file_path, "r", encoding="utf-8") as file:
                lines = [line.strip() for line in file if line.strip()]

            if not lines:
                return
            i = 1
            total_lines = len(lines)

            while i < total_lines:
                parts = lines[i].split(maxsplit=2)
                if len(parts) < 3:
                    i += 1
                    continue

                process_name, number_of_paths, timestamp = parts

                try:
                    number_of_paths = int(number_of_paths)
                except ValueError:
                    i += 1
                    continue
                paths = lines[i + 1: i + 1 + number_of_paths]
                i += number_of_paths + 1

                self.process_paths(process_name, paths, timestamp)

        except Exception as e:
            print(f"Error processing file: {str(e)}")

    @Slot()
    def clear_alerts(self):
        try:
            with open("alerts.txt", "w", encoding="utf-8") as file:
                file.write("")
            self.alertsCleared.emit()
        except Exception as e:
            print(f"Error clearing alerts: {str(e)}")

    @Slot(str)
    def clearProcess(self, target_process: str):
        file_path = Path("alerts.txt")
        if not file_path.exists():
            return

        with open(file_path, "r", encoding="utf-8") as f:
            lines = [l.rstrip("\n") for l in f if l.strip()]

        if not lines:
            return

        try:
            total = int(lines[0])
        except ValueError:
            return

        new_blocks = []
        i = 1
        removed = False
        while i < len(lines):
            header = lines[i].split(maxsplit=2)
            if len(header) < 3:
                i += 1
                continue

            proc_name, num_paths_str, timestamp = header
            try:
                num_paths = int(num_paths_str)
            except ValueError:
                i += 1
                continue

            block = lines[i: i + 1 + num_paths]
            if proc_name.lower() == target_process.lower() and not removed:
                removed = True
            else:
                new_blocks.extend(block)

            i += 1 + num_paths

        if not removed:
            return

        new_total = max(0, total - 1)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(f"{new_total}\n")
            for line in new_blocks:
                f.write(line + "\n")

        self.alertsCleared.emit()

        j = 0
        while j < len(new_blocks):
            proc_name, num_paths_str, timestamp = new_blocks[j].split(maxsplit=2)
            num_paths = int(num_paths_str)

            raw_paths = new_blocks[j + 1: j + 1 + num_paths]

            self.process_paths(proc_name, raw_paths, timestamp)

            j += 1 + num_paths

    @Slot()
    def refreshAlerts(self):
        alerts_file = Path("alerts.txt")
        if not alerts_file.exists():
            return

        with open(alerts_file, "r", encoding="utf-8") as f:
            lines = [l.rstrip("\n") for l in f if l.strip()]

        try:
            _ = int(lines[0])
        except:
            return

        self.alertsCleared.emit()

        i = 1
        while i < len(lines):
            header = lines[i].split(maxsplit=2)
            if len(header) < 3:
                i += 1
                continue
            proc, n_str, ts = header
            try:
                n = int(n_str)
            except:
                i += 1
                continue
            raw_paths = lines[i + 1: i + 1 + n]

            self.process_paths(proc, raw_paths, ts)
            i += n + 1

    def process_paths(self, process_name: str, paths: list, timestamp: str) -> None:
        info_stealer_keywords = {
            "Credentials or Login Information": [
                "login",
                "password",
                "credentials",
                "AutoFill",
                "Chrome",
                "Firefox",
                "Edge",
                "Brave",
                "Safari",
                "Opera",
                "LastPass",
                "Bitwarden",
                "1Password",
                "Dashlane",
                "KeePass",
            ],
            "Payment Information (Banking & Crypto)": [
                "bank",
                "credit",
                "debit",
                "card",
                "account",
                "finance",
                "wallet",
                "crypto",
                "PayPal",
                "Stripe",
                "Venmo",
                "Zelle",
                "Coinbase",
                "Metamask",
                "Binance",
                "Kraken",
                "CashApp",
                "Revolut",
                "Wise",
            ],
            "Authentication or API Keys": [
                "token",
                "API",
                "Key",
                "access",
                "Auth",
                "cookie",
                "AWS",
                "GitHub",
                "OAuth",
                "Secret",
                "SSH",
                "GCP",
                "Azure",
                "JWT",
                "PrivateKey",
                "id_rsa",
                "Bearer",
            ],
            "Email & Messaging Data": [
                "email",
                "outlook",
                "thunderbird",
                "telegram",
                "whatsapp",
                "messenger",
                "chat",
                "yahoo",
                "gmail",
                "protonmail",
                "zoho",
                "imap",
                "smtp",
            ],
            "Cloud Storage & Sync": [
                "drive",
                "dropbox",
                "onedrive",
                "icloud",
                "box",
                "mega",
                "nextcloud",
                "pcloud",
                "sync",
            ],
            "Gaming Accounts & Data": [
                "steam",
                "epic",
                "riot",
                "blizzard",
                "ubisoft",
                "game",
                "launcher",
                "rockstar",
                "bethesda",
                "twitch",
                "origin",
                "battlenet",
                "gog",
            ],
            "Browser or Desktop Application Data": [
                "browser",
                "extension",
                "plugin",
                "Data",
                "Cookies",
                "History",
                "Profile",
                "Discord",
                "Slack",
                "Zoom",
                "Teams",
                "Skype",
                "Vivaldi",
                "Tor",
                "Brave",
                "OperaGX",
            ],
            "Configuration or Backup Files": [
                ".env",
                ".ini",
                ".yaml",
                ".config",
                "backup",
                ".bak",
                ".backup",
                ".xml",
                ".plist",
                ".reg",
                ".cfg",
            ],
            "Database/Text/Sensitive Documents": [
                ".txt",
                ".csv",
                ".dat",
                ".json",
                ".docx",
                ".pdf",
                ".log",
                ".sql",
                ".xlsx",
                ".md",
                ".pptx",
                ".rtf",
            ],
        }

        processed_paths = []

        for path in paths:
            for category, keywords in info_stealer_keywords.items():
                matches = sum(
                    1
                    for keyword in keywords
                    if re.search(
                        rf"(^|[/\\])([^/\\]*{re.escape(keyword)}[^/\\]*)",
                        path,
                        re.IGNORECASE,
                    )
                )
                if matches >= 2:
                    processed_paths.append(f"{path.strip()} - {category}")
                    break

        paths_string = "\n".join(processed_paths)

        ts_alert = dt.datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
        process_key = process_name.lower()
        spawn = self.spawn_times.get(process_key)

        if not spawn:  # If not found, try reloading and get again
            # print(f"DEBUG: Spawn time for {process_key} not found, reloading Date.txt...") # Optional debug
            self._load_spawn_times()
            spawn = self.spawn_times.get(process_key)

        elapsed = "N/A"
        if spawn:
            if ts_alert >= spawn:
                delta = ts_alert - spawn
                total_seconds = int(delta.total_seconds())

                if total_seconds < 0:  # Should ideally not happen if ts_alert >= spawn
                    elapsed = "N/A (Alert before spawn)"
                else:
                    days, remainder_seconds = divmod(total_seconds, 86400)
                    hrs, remainder_seconds = divmod(remainder_seconds, 3600)
                    mins, secs = divmod(remainder_seconds, 60)

                    if days > 0:
                        elapsed = f"{days}d {hrs}h {mins}m {secs}s"
                    elif hrs > 0:
                        elapsed = f"{hrs}h {mins}m {secs}s"
                    else:
                        elapsed = f"{mins}m {secs}s"
            else:
                elapsed = "N/A (Alert before spawn)"
        else:
            elapsed = "N/A (Spawn time unknown)"

        self.newAlert.emit(process_name, paths_string, timestamp, elapsed)


def main():
    app = QGuiApplication()
    engine = QQmlApplicationEngine()

    alert_processor = AlertProcessor()
    alert_processor.copy_to_alerts()
    engine.rootContext().setContextProperty("alertProcessor", alert_processor)

    engine.load("qml/Test.qml")

    if not engine.rootObjects():
        return -1

    return app.exec()


if __name__ == "__main__":
    main()
