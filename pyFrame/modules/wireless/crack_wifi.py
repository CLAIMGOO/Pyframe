#КОД НА СТАДИИ РАЗРАБОТКИ
#КОД НА СТАДИИ РАЗРАБОТКИ
#КОД НА СТАДИИ РАЗРАБОТКИ
#КОД НА СТАДИИ РАЗРАБОТКИ
#КОД НА СТАДИИ РАЗРАБОТКИ
#КОД НА СТАДИИ РАЗРАБОТКИ
#КОД НА СТАДИИ РАЗРАБОТКИ
#КОД НА СТАДИИ РАЗРАБОТКИ
#КОД НА СТАДИИ РАЗРАБОТКИ
#КОД НА СТАДИИ РАЗРАБОТКИ
#КОД НА СТАДИИ РАЗРАБОТКИ
#КОД НА СТАДИИ РАЗРАБОТКИ
#КОД НА СТАДИИ РАЗРАБОТКИ
#КОД НА СТАДИИ РАЗРАБОТКИ
#КОД НА СТАДИИ РАЗРАБОТКИ
#КОД НА СТАДИИ РАЗРАБОТКИ
#!/usr/bin/env python3
import subprocess
import getpass
import colorama
from colorama import Fore, init

init(autoreset=True)

# === 1. Предупреждение ===
print(Fore.RED + "ВНИМАНИЕ:")
print(Fore.YELLOW + "- aircrack-ng должен быть установлен")
print(Fore.YELLOW + "- WiFi-карта должна поддерживать monitor mode и packet injection")
print(Fore.WHITE + "Если вы всё поняли, продолжайте")
input(Fore.YELLOW + "[Нажмите Enter для продолжения]")

print(Fore.YELLOW + "=== Кряк сети ===")

# === 2. Выбор интерфейса ===
print("\nСетевые интерфейсы:")
print("=================")

result = subprocess.run(["iwconfig"], capture_output=True, text=True)
lines = result.stdout.splitlines()

found_interfaces = []
for line in lines:
    line = line.strip()
    if not line:
        continue
    if line[0].isalnum() and "IEEE" in line:
        interface_name = line.split()[0]
        print(Fore.GREEN + f"Интерфейс: {interface_name}")
        found_interfaces.append(interface_name)

if not found_interfaces:
    print(Fore.RED + "[-] WiFi-интерфейсы не найдены")
    exit()

interface = input(Fore.WHITE + "Введите интерфейс для мониторинга (например, wlan0): ").strip()

# === 3. Убить конфликтующие процессы? ===
print("\nВы хотите убить конфликтующие процессы?")
print("1: Да (рекомендуется)")
print("2: Нет")
choice = input("Выбор: ").strip()

if choice == "1":
    print(Fore.YELLOW + "[+] Для airmon-ng check kill нужен sudo")
    passwd = getpass.getpass(Fore.WHITE + "Введите пароль sudo: ")

    # Правильно: echo + sudo -S
    kill_cmd = f"echo '{passwd}' | sudo -S airmon-ng check kill"
    result = subprocess.run(kill_cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(Fore.RED + "[-] Ошибка sudo или airmon-ng")
        print(result.stderr)
        exit()
    print(Fore.GREEN + "[+] Конфликты устранены")
else:
    print(Fore.YELLOW + "[!] Пропускаем kill — возможны ошибки")

# === 4. Включить monitor mode ===
print(Fore.YELLOW + f"\n[+] Включаем monitor mode на {interface}...")
start_cmd = f"echo '{passwd}' | sudo -S airmon-ng start {interface}"
result = subprocess.run(start_cmd, shell=True, capture_output=True, text=True)

if result.returncode != 0:
    print(Fore.RED + "[-] Не удалось включить monitor mode")
    print(result.stderr)
    exit()

# Парсим имя интерфейса 
mon_interface = None
for line in result.stdout.splitlines():
        try:
            mon_interface = line.split("[")[-1].split("]")[0]
            print(Fore.GREEN + f"[+] Monitor interface: {mon_interface}")
        except:
            pass
        break

if not mon_interface:
    print(Fore.RED + "[-] Не удалось определить mon-интерфейс")
    exit()

print(Fore.CYAN + f"\n[+] Готово! Используйте {mon_interface} для сканирования.")