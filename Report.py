import datetime as dt
import re
from pathlib import Path
from typing import Dict

from PySide6.QtCore import QObject, Signal, Slot
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine


class AlertProcessor(QObject):
    newAlert = Signal(str, str, str, str, str)
    alertsCleared = Signal()

    def __init__(self):
        super().__init__()
        self.spawn_times = {}
        self._load_spawn_times()

    def _load_spawn_times(self):
        self.spawn_times.clear()
        date_file = Path(r"C:\Windows\System32\AntiMalware\Date.txt")
        if date_file.exists():
            try:
                for line in date_file.read_text().splitlines():
                    if not line or ":" not in line: continue
                    name, ts = line.split(":", 1)
                    name, ts = name.strip().lower(), ts.strip()
                    # Attempt to parse various known datetime formats
                    parsed_ts = None
                    for fmt in ("%Y-%m-%d %H:%M:%S.%f", "%Y-%m-%d %H:%M:%S"):
                        try:
                            # Ensure month and day are zero-padded if necessary by reconstructing
                            parts = ts.split(" ")
                            date_part = parts[0]
                            time_part = parts[1] if len(parts) > 1 else "00:00:00"
                            y, m, d = date_part.split("-")
                            m, d = m.zfill(2), d.zfill(2)
                            reconstructed_ts = f"{y}-{m}-{d} {time_part}"
                            parsed_ts = dt.datetime.strptime(reconstructed_ts, fmt)
                            break  # Successfully parsed
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
        current_line_index = 1
        while current_line_index < len(output_lines):
            line = output_lines[current_line_index]
            parts = line.split()
            if len(parts) >= 2 and parts[0].lower().endswith(".exe") and parts[1].isdigit():
                proc, path_count_str = parts[0], parts[1]
                path_count = int(path_count_str)
                ts = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                new_entries.append(f"{proc} Infostealer {path_count_str} {ts}\n")
                current_line_index += 1
                for _ in range(path_count):
                    if current_line_index < len(output_lines):
                        new_entries.append(f"{output_lines[current_line_index]}\n")
                        current_line_index += 1
                    else:
                        print(f"Warning: Expected {path_count} paths for {proc}, but found fewer in output.txt")
                        break
            else:
                print(f"Warning: Skipping unexpected line format in output.txt: {line}")
                current_line_index += 1

        with open(alerts_file_path, "w", encoding="utf-8") as f:
            f.write(f"{total_count}\n")
            if len(old_lines) > 1:
                for old in old_lines[1:]:
                    f.write(old + "\n")
            f.writelines(new_entries)

    @Slot(str)
    def log_ransomware_alert(self, ransomware_process_name: str):
        alerts_file_path = Path("alerts.txt")
        old_lines = []
        num_existing = 0

        if alerts_file_path.exists() and alerts_file_path.stat().st_size > 0:
            with open(alerts_file_path, "r", encoding="utf-8") as f:
                old_lines = [l.rstrip("\n") for l in f if l.strip()]
            if old_lines:
                try:
                    num_existing = int(old_lines[0])
                    old_lines = old_lines[1:]
                except (ValueError, IndexError):
                    num_existing = 0
                    old_lines = []

        ts = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ransomware_entry_header = f"{ransomware_process_name} Ransomware 0 {ts}"

        updated_alert_data_lines = old_lines + [ransomware_entry_header]
        total_count = num_existing + 1

        with open(alerts_file_path, "w", encoding="utf-8") as f:
            f.write(f"{total_count}\n")
            for entry_line in updated_alert_data_lines:
                f.write(entry_line + "\n")
        print(f"Logged ransomware alert for: {ransomware_process_name}")

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
                parts = lines[i].split(maxsplit=3)  # Changed from 2 to 3 to include malware_type
                if len(parts) < 4:
                    i += 1
                    continue

                process_name, malware_type, number_of_paths_str, timestamp = parts

                try:
                    number_of_paths = int(number_of_paths_str)
                except ValueError:
                    i += 1
                    continue
                paths = lines[i + 1: i + 1 + number_of_paths]
                i += number_of_paths + 1

                self.process_paths(process_name, malware_type, paths, timestamp)
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
            header = lines[i].split(maxsplit=3)
            if len(header) < 3:
                i += 1
                continue
            proc_name, malware_type, num_paths_str, timestamp = header  # Unpack with malware_type
            try:
                num_paths = int(num_paths_str)
            except ValueError:
                i += 1
                continue

            block = lines[i: i + 1 + num_paths]
            if proc_name.lower() == target_process.lower() and not removed:
                removed = True
                total -= 1  # Decrement total count as one alert block is being removed
            else:
                new_blocks.extend(block)

            i += 1 + num_paths

        if not removed:
            return

        # new_total = max(0, total - 1) # This was already handled by decrementing total inside loop
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(f"{total}\n")  # Write the decremented total
            for line in new_blocks:
                f.write(line + "\n")

        self.alertsCleared.emit()  # Signal that alerts have changed
        self.refreshAlerts()  # Repopulate the UI by re-processing the modified alerts.txt

    @Slot()
    def refreshAlerts(self):
        alerts_file = Path("alerts.txt")
        if not alerts_file.exists() or alerts_file.stat().st_size == 0:
            self.alertsCleared.emit()  # Emit even if file is empty/gone so UI can clear
            return

        with open(alerts_file, "r", encoding="utf-8") as f:
            lines = [l.rstrip("\n") for l in f if l.strip()]

        if not lines:  # If file only contained whitespace
            self.alertsCleared.emit()
            return

        try:
            _ = int(lines[0])  # Validate header count
        except (ValueError, IndexError):
            print("Warning: alerts.txt has malformed header or is empty after header.")
            self.alertsCleared.emit()  # Emit so UI can clear if data is bad
            return

        self.alertsCleared.emit()  # Emit first to clear existing UI items

        i = 1
        while i < len(lines):
            header = lines[i].split(maxsplit=3)  # Changed from 2 to 3
            if len(header) < 4:
                i += 1
                continue
            proc, malware_type, n_str, ts = header  # Unpack with malware_type
            try:
                n = int(n_str)
            except ValueError:
                i += 1
                continue
            raw_paths = lines[i + 1: i + 1 + n]

            self.process_paths(proc, malware_type, raw_paths, ts)  # Pass malware_type
            i += n

    def process_paths(self, process_name: str, malware_type: str, paths: list, timestamp: str) -> None:
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
        paths_string = ""

        if malware_type.lower() == "infostealer":
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

        if not spawn:
            self._load_spawn_times()
            spawn = self.spawn_times.get(process_key)

        elapsed = "N/A"
        if spawn:
            if ts_alert >= spawn:
                delta = ts_alert - spawn
                total_seconds = int(delta.total_seconds())

                if total_seconds < 0:
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

        self.newAlert.emit(process_name, paths_string, timestamp, elapsed, malware_type)


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
