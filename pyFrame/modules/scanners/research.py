import subprocess
import colorama
import re
import getpass
from colorama import Fore, Style

colorama.init()

def auto_nmap():
    ip_address = input("введите ip адрес приложения: ")
    
    # ПРОВЕРКА IP
    if not re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", ip_address):
        print(Fore.RED + "Вы ввели не правильный ip адрес, в нем должны быть только цифры и точки!")
        return  # выход из функции

    # Меню
    print(Fore.YELLOW + "Выберите что вы хотите сделать:")
    print(Fore.CYAN + "1. Полное сканирование nmap с обнаружением версий и ОС")
    print(Fore.CYAN + "2. Сканирование nmap с обнаружением версий")
    print(Fore.CYAN + "3. Сканирование nmap с обнаружением версий и уязвимостей")
    print(Fore.CYAN + "4. Проверка пинга")
    print(Fore.CYAN + "5. Быстрое сканирование портов с помощью rustscan")

    # Выбор
    choice = input(Fore.WHITE + "Введите что вы хотите сделать: ")
    passwd = ""
    command_to_run = ""

    # --- ЛОГИКА ---
    if choice in ["1", "2", "3"]:
        print(Fore.YELLOW + "Для выполнения этой команды требуются права суперпользователя (sudo).")
        passwd = getpass.getpass("Введите пароль для sudo (ввод скрыт): ")
        
        if choice == "1":
            command_to_run = f"echo '{passwd}' | sudo -S nmap -A -T4 -p- {ip_address}"
        elif choice == "2":
            command_to_run = f"echo '{passwd}' | sudo -S nmap -sV -T4 -p- {ip_address}"
        elif choice == "3":
            command_to_run = f"echo '{passwd}' | sudo -S nmap -sV --script=vuln -T4 -p- {ip_address}"
    
    elif choice == "4":
        command_to_run = f"ping -c 4 {ip_address}"
    elif choice == "5":
        command_to_run = f"rustscan -a {ip_address} --ulimit 5000"
    else:
        print(Fore.RED + "Неверный ввод")
        return

    # --- Уведомление ---
    if passwd:
        print(Fore.YELLOW + f"Выполняется команда для {ip_address} (с sudo)...")
    else:
        print(Fore.YELLOW + f"Выполняется команда: {command_to_run}")

    # --- Запуск ---
    result = subprocess.run(command_to_run, shell=True, capture_output=True, text=True)

    # --- Ошибки ---
    if result.returncode != 0:
        print(Fore.RED + "ОШИБКА ЗАПУСКА:")
        print(result.stderr)
        return

    # --- Анализ и вывод ---
    lines = result.stdout.split('\n')
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if "open" in line:
            print(Fore.GREEN + "[+] ОТКРЫТ ПОРТ: " + line)
        elif "PING" in line or "bytes from" in line:
            print(Fore.CYAN + "[+] ПИНГУЕТ: " + line)
        else:
            print(Fore.WHITE + line)