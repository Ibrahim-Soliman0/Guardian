import shutil
import sys, os, subprocess
import frida
import psutil
import time
import threading
import queue
import tempfile
import re
import stat
import datetime
from multiprocessing import Pool, freeze_support, set_start_method
from PySide6.QtCore import QCoreApplication, QTimer
from PySide6.QtNetwork import QLocalSocket
from Database import SQL
from Report import AlertProcessor

import json

MAX_THREADS = 30
MAX_PROCESSES = 3

tries = 0

active_hooks = set()
last_access_time = {}
process_sessions = {}
lock = threading.Lock()
parsinglock = threading.Lock()
write_queue = queue.Queue()
sql = SQL()
alert_processor = AlertProcessor()


log_file_path = r"C:\Windows\System32\AntiMalware\input.txt"

log_file = open(log_file_path, "w", encoding="utf-8")

with open("settings.json", "r") as f:
    userSettings = json.load(f)

system_process_list = [
    "brave.exe", "chrome.exe", "firefox.exe", "svchost.exe", "consent.exe",
    "frida-helper-x86.exe", "frida-helper-x86_64.exe", "dllhost.exe",
    "ctfmon.exe", "conhost.exe", "runtimebroker.exe", "wmiprvse.exe",
    "taskmgr.exe", "werfault.exe", "explorer.exe", "taskhostw.exe",
    "searchprotocolhost.exe", "Ransomware.exe", "parser.exe", "tiworker.exe"
]

hook_script = """
var fileNames = [];
var maxBatchSize = 10;
var processName = Process.enumerateModules()[0].name;
var getFinalPathNameByHandle = Module.getExportByName("kernel32.dll", "GetFinalPathNameByHandleW");
var sentFileNames = new Set();


Interceptor.attach(Module.getExportByName("kernel32.dll", "GetFileAttributesExW"), {
    onEnter: function (args) {
        var ptr = args[0];
        if (ptr.isNull()) return;
        this.fileName = Memory.readUtf16String(args[0]);

        fileNames.push(`${processName} >> ${this.fileName}`);

        if (fileNames.length >= maxBatchSize) {
            send(fileNames.join("\\n"));
            fileNames = [];
        }
    }
});

Interceptor.attach(Module.getExportByName("kernel32.dll", "CreateFileW"), {
    onEnter: function (args) {
        var ptr = args[0];
        if (ptr.isNull()) return;
        this.fileName = Memory.readUtf16String(args[0]);

        fileNames.push(`${processName} >> ${this.fileName}`);

        if (fileNames.length >= maxBatchSize) {
            send(fileNames.join("\\n"));
            fileNames = [];
        }
    }
});

Interceptor.attach(Module.getExportByName("kernel32.dll", "FindFirstFileExW"), {
    onEnter: function (args) {
        var ptr = args[0];
        if (ptr.isNull()) return;
        this.fileName = Memory.readUtf16String(args[0]);

        fileNames.push(`${processName} >> ${this.fileName}`);

        if (fileNames.length >= maxBatchSize) {
            send(fileNames.join("\\n"));
            fileNames = [];
        }
    }
});

Interceptor.attach(Module.getExportByName("kernel32.dll", "ReadFile"), {
    onEnter: function (args) {
        this.fileHandle = args[0];
    },
    onLeave: function (retval) {
        if (retval.toInt32() === 0) {
            return;
        }

        if (!this.fileHandle.isNull()) {
            var buffer = Memory.alloc(1024);
            var length = new NativeFunction(getFinalPathNameByHandle, "uint32", ["pointer", "pointer", "uint32", "uint32"])(
                this.fileHandle,
                buffer,
                1024,
                0
            );

            if (length > 0) {
                var fileName = Memory.readUtf16String(buffer);

                if (!sentFileNames.has(fileName)) {
                    sentFileNames.add(fileName);
                    send(`${processName} >> (ReadFile) ${fileName}`);
                }
            }
        }
    }
});

Interceptor.attach(Module.getExportByName("kernel32.dll", "CopyFileA"), {
    onEnter: function (args) {
        var ptr = args[0];
        if (ptr.isNull()) return;
        this.fileName = Memory.readAnsiString(args[0]);


        fileNames.push(`${processName} >> (CopyFile) ${this.fileName}`);

        if (fileNames.length >= maxBatchSize) {
            send(fileNames.join("\\n"));
            fileNames = [];
        }
    }
});

Interceptor.attach(Module.getExportByName("kernel32.dll", "MoveFileW"), {
    onEnter: function (args) {
        var newFileNamePtr = args[1];

        if (!newFileNamePtr.isNull()) {
            var newFileName = Memory.readUtf16String(newFileNamePtr);

            fileNames.push(`${processName} >> ${newFileName}`);

            if (fileNames.length >= maxBatchSize) {
                send(fileNames.join("\\n"));
                fileNames = [];
            }
        }
    }
});

rpc.exports = {
    flush: function () {
        if (fileNames.length > 0) {
            send(fileNames.join("\\n"));
            fileNames = [];
        }
    }
};
"""

def get_or_create_process(proc_name):
    if sql.process_exists(proc_name):
        return sql.get_process_id(proc_name)
    return sql.insert_process(proc_name)

def insert_out_file(file="output.txt"):
    default_type_name = "InfoStealer"

    type_mapping = {}

    with open(file, "r", encoding="utf-8") as f:
        lines = [L.strip() for L in f if L.strip()]

    idx = 0
    total_runs = int(lines[idx])
    idx += 1

    for _ in range(total_runs):
        exe_name, cnt_s = lines[idx].split(maxsplit=1)
        cnt = int(cnt_s)
        idx += 1

        paths = lines[idx: idx + cnt]
        idx += cnt

        proc_id = get_or_create_process(exe_name)

        type_name = type_mapping.get(exe_name, default_type_name)
        type_id = sql.get_malware_type_id(type_name)

        for p in paths:
            sql.insert_process_path(proc_id, type_id, p)


def getProcessByName(process_name):
    for proc in psutil.process_iter(['name']):
        try:
            if proc.info['name'] and proc.info['name'].lower() == process_name.lower():
                return proc
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue
    return None

def parseInfoFile():
    pattern = re.compile(r"^(\S+\.exe)\s+\d+$", re.IGNORECASE)

    processes = []

    with open(r"C:\Windows\System32\AntiMalware\output.txt", "r") as f:
        for line in f:
            line = line.strip()
            match = pattern.match(line)
            if match:
                processes.append(match.group(1))

    if processes:
        print(processes)
        terminateAndRemove(str(processes[0]), "infostealer")

    open(r"C:\Windows\System32\AntiMalware\output.txt", "w")
    open(r"C:\Windows\System32\AntiMalware\ransom.txt", "w")


def parseRansomFile():
    with open(r"C:\Windows\System32\AntiMalware\ransom.txt", "r") as f:
        lines = f.readlines()
        if len(lines) >= 2:
            second_line = lines[1].strip()
            print(second_line)
            terminateAndRemove(str(second_line), "Ransomware")

        open(r"C:\Windows\System32\AntiMalware\ransom.txt", "w")
        open(r"C:\Windows\System32\AntiMalware\output.txt", "w")

def terminateAndRemove(name, type):
    alert_processor.copy_to_alerts()

    proc = getProcessByName(name)
    if not proc:
        print("Process not found")
        open(r"C:\Windows\System32\AntiMalware\input.txt", "w")
        socket = QLocalSocket()
        socket.connectToServer("AlertTriggerServer")
        if socket.waitForConnected(1000):
            socket.write(f"trigger_alert:{type}".encode())
            socket.flush()
            socket.disconnectFromServer()
            print("Sent trigger_alert")
        else:
            print("Could not connect to AlertTriggerServer")

        if not sql.process_exists(name):
            sql.insert_process(name)

        insert_out_file(r"C:\Windows\System32\AntiMalware\output.txt")

        QTimer.singleShot(500, app.quit)
        return

    try:
        exe_path = proc.exe()
        print(f"Process executable path: {exe_path}")

        proc.kill()
        try:
            proc.wait(timeout=5)
        except psutil.TimeoutExpired:
            print("Process did not terminate within timeout.")

        print("Process killed")

        time.sleep(1)

        open(r"C:\Windows\System32\AntiMalware\input.txt", "w")

        if os.path.exists(exe_path):
            try:
                os.chmod(exe_path, stat.S_IWRITE)
            except Exception as e:
                print(f"Could not change file permissions: {e}")

            try:
                os.remove(exe_path)
                print(f"Removed executable: {exe_path}")
            except Exception as e:
                print(f"Error removing file: {e}")
        else:
            print("Executable file not found.")

        socket = QLocalSocket()
        socket.connectToServer("AlertTriggerServer")
        if socket.waitForConnected(1000):
            socket.write(f"trigger_alert:{type}".encode())
            socket.flush()
            socket.disconnectFromServer()
            print("Sent trigger_alert")
        else:
            print("Could not connect to AlertTriggerServer")

        if not sql.process_exists(name):
            sql.insert_process(name)

        insert_out_file(r"C:\Windows\System32\AntiMalware\output.txt")

        QTimer.singleShot(500, app.quit)

    except Exception as e:
        print(f"An error occurred: {e}")

def restart_script():
    print("Restarting Frida script...")
    try:
        delete_frida_Temp()

        python = sys.executable
        os.execv(python, [python] + sys.argv)
    except Exception as e:
        print(f"Failed to restart script: {e}")
        sys.exit(1)


def delete_frida_Temp():
    temp_dir = tempfile.gettempdir()

    try:
        for item in os.listdir(temp_dir):
            item_path = os.path.join(temp_dir, item)
            if os.path.isdir(item_path) and item.startswith("frida"):
                print(f"Deleting directory: {item_path}")
                shutil.rmtree(item_path)
    except Exception as e:
        print(f"Error while deleting directories: {e}")

def monitor_and_log(interval=0.05, logfile=r"C:\Windows\System32\AntiMalware\Date.txt"):
    entries = {}
    if os.path.exists(logfile):
        with open(logfile, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    name, ts = line.strip().split(':', 1)
                    entries[name] = ts
                except ValueError:
                    continue

    for new_pids in monitor_processes(interval):
        updated = False
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        for pid in new_pids:
            try:
                proc = psutil.Process(pid)
                name = proc.name()
                entries[name] = timestamp
                updated = True
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        if updated:
            with open(logfile, 'w', encoding='utf-8') as f:
                for pname, pts in entries.items():
                    f.write(f"{pname}:{pts}\n")

def start_process_logger():
    thread = threading.Thread(target=monitor_and_log, daemon=True)
    thread.start()


def monitor_processes(interval=0.05):
    seen_processes = {proc.pid for proc in psutil.process_iter(attrs=['pid', 'name'])}
    while True:
        time.sleep(interval)
        current_processes = {proc.pid for proc in psutil.process_iter(attrs=['pid', 'name'])}
        new_pids = current_processes - seen_processes
        seen_processes = current_processes

        if new_pids:
            yield new_pids


def on_message(message, data):
    global log_file
    if message["type"] == "send":
        log_message = f"{message['payload']}\n"
        print(log_message.strip())
        with lock:
            log_file.write(log_message)
            log_file.flush()
            for process_name in active_hooks:
                last_access_time[process_name] = time.time()
    else:
        error_message = f"[!] {message}\n"
        print(error_message.strip())


def get_high_memory_pid(process_name):
    max_memory = 0
    high_memory_pid = None
    for proc in psutil.process_iter(['name', 'memory_info']):
        if proc.info['name'] == process_name:
            try:
                memory_usage = proc.info['memory_info'].rss
                if memory_usage > max_memory:
                    max_memory = memory_usage
                    high_memory_pid = proc.pid
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
    return high_memory_pid


def detach_with_timeout(session, timeout=0.5):
    detach_done = threading.Event()

    def detach():
        try:
            if not session.is_detached:
                session.detach()
        except Exception as e:
            print(f"Error detaching session: {e}")
        finally:
            detach_done.set()

    detach_thread = threading.Thread(target=detach)
    detach_thread.start()
    detach_done.wait(timeout)
    if not detach_done.is_set():
        print("Detach timed out, proceeding without detaching.")
    else:
        print("Detached successfully.")


def hook_process(pid, process_name):
    global tries
    try:
        if pid is None:
            return

        session = frida.attach(pid, persist_timeout=10)

        with lock:
            process_sessions[process_name] = session
            last_access_time[process_name] = time.time()

        print(f"Hooked to process: {process_name} (PID: {pid})")
        script = session.create_script(hook_script)
        script.on("message", on_message)
        script.load()
        active_hooks.add(process_name)
        print(active_hooks)
        while True:
            if psutil.pid_exists(pid):
                time.sleep(0.1)
                continue
            else:
                break
        detach_with_timeout(session)
        with lock:
            try:
                active_hooks.remove(process_name)
            except:
                pass
            last_access_time.pop(process_name, None)
            process_sessions.pop(process_name, None)
        print("Process Finished")
    except frida.ProcessNotFoundError:
        print(f"Process {pid} not found.")
        with lock:
            try:
                active_hooks.remove(process_name)
            except:
                pass
            last_access_time.pop(process_name, None)
            process_sessions.pop(process_name, None)
    except frida.ProcessNotRespondingError:
        print(f"Process {pid} not responding.")
        with lock:
            try:
                active_hooks.remove(process_name)
            except:
                pass
            last_access_time.pop(process_name, None)
            process_sessions.pop(process_name, None)

    except Exception as e:
        if "refused to load frida-agent" in str(e):
            tries += 1
            if tries <= 3:
                time.sleep(0.5)
                hook_process(pid, process_name)
            else:
                tries = 0
        elif "timeout was reached" in str(e):
            print(e)
            restart_script()


def check_inactivity(interval=5, timeout=60):
    while True:
        time.sleep(interval)
        with lock:
            current_time = time.time()
            inactive_processes = [
                name for name, last_time in last_access_time.items()
                if current_time - last_time > timeout
            ]
            for process_name in inactive_processes:
                print(f"Removing inactive process: {process_name}")
                session = process_sessions.pop(process_name, None)
                if session:
                    detach_with_timeout(session)
                try:
                    active_hooks.remove(process_name)
                except:
                    pass
                last_access_time.pop(process_name, None)


def hook_in_process(pid, process_name):
    hook_process(pid, process_name)

def parse_and_calc():
    while True:
        if os.path.getsize(log_file_path) / (1024 * 1024) >= int(userSettings.get("MaximumLogFileSize", 0)):
            open(r"C:\Windows\System32\AntiMalware\input.txt", "w")
        time.sleep(int(userSettings.get("InfoInterval", 0)))
        with parsinglock:
            print("Parse")
            p = subprocess.Popen(r"C:\Windows\System32\AntiMalware\parser.exe")
            p.wait()
            print("Make Calcs")
            p = subprocess.Popen(r"C:\Windows\System32\AntiMalware\infodetection.exe")
            p.wait()
            print("Done")
            parseInfoFile()

def ransom():
    while True:
        time.sleep(int(userSettings.get("RansomInterval", 0)))
        with parsinglock:
            print("Ransom")
            p = subprocess.Popen(r"C:\Windows\System32\AntiMalware\parser.exe")
            p.wait()
            print("Make Calcs")
            p = subprocess.Popen(r"C:\Windows\System32\AntiMalware\Ransomware.exe")
            p.wait()
            parseRansomFile()

def process_hook_manager():
    global active_hooks
    thread_pool = queue.Queue(maxsize=MAX_THREADS)
    pool = Pool(processes=MAX_PROCESSES)
    threading.Thread(target=check_inactivity, daemon=True).start()
    start_process_logger()
    for new_pids in monitor_processes():
        for pid in new_pids:
            try:
                proc = psutil.Process(pid)
                process_name = proc.name()
                if process_name in active_hooks:
                    continue

                if process_name.lower() in system_process_list:
                    continue

                if thread_pool.full():
                    pool.apply_async(hook_in_process, args=(get_high_memory_pid(process_name), process_name))
                else:
                    thread = threading.Thread(target=hook_process,
                                              args=(get_high_memory_pid(process_name), process_name))
                    thread_pool.put(thread)
                    thread.start()

                while not thread_pool.empty():
                    t = thread_pool.get()
                    if not t.is_alive():
                        t.join()
            except psutil.AccessDenied:
                print(f"Access denied for PID {pid}")
            except psutil.NoSuchProcess:
                continue
            except Exception as e:
                print(f"Error managing process {pid}: {e}")


if __name__ == "__main__":
    app = QCoreApplication(sys.argv)
    freeze_support()
    set_start_method("spawn")
    try:
        delete_frida_Temp()
    except:
        pass
    threading.Thread(target=parse_and_calc, daemon=True).start()
    threading.Thread(target=ransom, daemon=True).start()

    try:
        print("Starting process monitor...")
        process_hook_manager()
    except KeyboardInterrupt:
        print("Monitoring stopped.")
        sys.exit(1)
