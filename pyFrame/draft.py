#!/usr/bin/env python3
import subprocess
import getpass
from colorama import init; init()

choice = int(input("Проверить airmon-ng? (1/0): "))
passwd = getpass.getpass("Пароль sudo: ")
interface = input("Интерфейс (wlan0): ").strip()

if choice == 1:
    cmd = f"echo '{passwd}' | sudo -S airmon-ng"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    print("Ошибка!" if result.returncode or "error" in result.stderr.lower() else result.stdout or "OK")

cmd = f"echo '{passwd}' | sudo -S airmon-ng start {interface}"
result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
if result.returncode:
    print(f"Ошибка: {result.stderr}")
else:
    for line in result.stdout.splitlines():
        if "monitor mode" in line.lower():
            mon = line.split("[")[-1].split("]")[0]
            print(f"Monitor: {mon}")