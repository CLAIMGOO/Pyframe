import colorama
import time
import shlex
import re
import subprocess
from colorama import Fore, Style, init

print(Fore.YELLOW + "введите url адрес целевого приложения (например: http://example.com или 192.168.1.1)")

target = input(Fore.WHITE + "цель: ")
while target.strip() == "":
    print(Fore.RED + "Вы не ввели цель. Пожалуйста, введите URL адрес целевого приложения.")
    target = input(Fore.WHITE + "цель: ")

# проверка на url

if re.match(r'^https?://', target):
    print(Fore.GREEN + f"Вы ввели URL: {target}")
else:
    print(Fore.RED + "Вы ввели не правильный URL, он должен начинаться с http:// или https://")
    
    exit()
    
print(Fore.YELLOW + "Выберите что вы хотите сделать:")
print(Fore.CYAN + "1. агрессивная инъекция sqlmap (рекомендуется для опытных пользователей)")
print(Fore.CYAN + "2. автоматическая инъекция sqlmap (рекомендуется для новичков)")
print(Fore.CYAN + "3. скрытное тестирование на sql инъекции (используется tamper скрипты и risk = 1, level = 1)")
choice1 = input(Fore.WHITE + "введите что вы хотите сделать: ")


print(Fore.WHITE + "что желаете видеть в выводе?")
print(Fore.CYAN + "1. полный вывод sqlmap (агрессивный режим)")
print(Fore.CYAN + "2. только ошибки, предупреждения и найденные базы данных (автоматический режим)")
print(Fore.CYAN + "3. только ошибки")

choice2 = input(Fore.WHITE + "введите что вы хотите сделать: ")

if choice1 == "1":
    command_to_run = f"sqlmap -u {target} --batch --random-agent --threads=10 --risk=3 --level=5 --dbs"
    
elif choice1 == "2":
    command_to_run = f"sqlmap -u {target} --batch --random-agent --threads=10 --dbs"
elif choice1 == "3":
    command_to_run = f"sqlmap -u {target} --batch --random-agent --threads=10 --risk=1 --level=1 --tamper=between,randomcase --dbs"
else:
    print(Fore.RED + "Неверный ввод")
    exit()
    
print(Fore.YELLOW + "Запуск команды sqlmap...")


if choice2 == "1":
    import re

if choice2 == "1":
    result = subprocess.run(shlex.split(command_to_run), capture_output=True, text=True)
    output = result.stdout

    # Фильтрация и форматирование вывода sqlmap
    pattern = r"Payload: (.+?)\nResult: (.+?)\n"
    matches = re.findall(pattern, output, re.DOTALL)

    for match in matches:
        payload = match[0].strip()
        result = match[1].strip()
        print(f"Payload: {payload}\nResult: {result}\n")
        
    pattern = r"\[ERROR\].+?\n"
    matches = re.findall(pattern, output, re.DOTALL)

    for match in matches:
        print(match.strip())

elif choice2 == "2":
    result = subprocess.run(shlex.split(command_to_run), capture_output=True, text=True)
    output = result.stdout

    # Вывод только ошибок, предупреждений и найденных баз данных
    pattern = r"\[ERROR\].+?\n|\[WARNING\].+?\n|Database: .+?\n"
    matches = re.findall(pattern, output, re.DOTALL)

    for match in matches:
        print(match.strip())

elif choice2 == "3":
    # Запускаем sqlmap и получаем вывод
    result = subprocess.run(
        shlex.split(command_to_run),
        capture_output=True,
        text=True
    )
    output = result.stdout

    # Выводим только строки с [ERROR]
    pattern = r"\[ERROR\].+?\n"
    matches = re.findall(pattern, output, re.DOTALL)

    for match in matches:
        print(match.strip())

    if pattern := r"\[CRITICAL\].+?\n":
        matches = re.findall(pattern, output, re.DOTALL)
        for match in matches:
            print(match.strip())
            print(Fore.RED + "Критическая ошибка при выполнении sqlmap. Завершение работы, возможно указан неверный url?.")
    else:
        print(Fore.RED + "Неверный ввод")
        exit()
print(Fore.GREEN + "Команда sqlmap выполнена.")
print(Fore.GREEN + "понравилось использовать утилиту? заходи еще!")