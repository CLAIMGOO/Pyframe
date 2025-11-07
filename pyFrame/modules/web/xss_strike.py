from colorama import Fore
import re
import subprocess

def xss_strike():
    # === МЕНЮ ===
    print(Fore.CYAN + "Привет! Это проверка на XSS.")
    print("1: Тест на один параметр (reflected XSS)")
    print("2: Crawl по сайту (ищет формы)")
    print("3: Crawl + DOM XSS")
    print("4: Crawl + fuzzing (обход фильтров)")
    print("5: Crawl с 10 потоками")
    print("6: Crawl, макс 50 страниц")
    print("7: Пропустить id и token")
    print("8: Максимальный режим")
    print("9: Ввести свою команду")

    # === ВВОД ===
    try:
        choice = int(input(Fore.WHITE + "Введите номер: "))
    except ValueError:
        print(Fore.RED + "Введите число!")
        return

    url = input("Введите URL: ").strip()

    # === ПРОВЕРКА URL ===
    if not re.match(r'^https?://', url):
        print(Fore.RED + "Ошибка: URL должен начинаться с http:// или https://")
        return

    print(Fore.GREEN + f"Запуск: {url}\n")

    # === БАЗОВАЯ КОМАНДА ===
    base_cmd = ["python", "xsstrike.py", "-u", url]

    # === ДОБАВЛЕНИЕ ФЛАГОВ ===
    if choice == 1:
        cmd = base_cmd.copy()
    elif choice == 2:
        cmd = base_cmd + ["--crawl"]
    elif choice == 3:
        cmd = base_cmd + ["--crawl", "--level", "2"]
    elif choice == 4:
        cmd = base_cmd + ["--crawl", "--fuzzer"]
    elif choice == 5:
        cmd = base_cmd + ["--crawl", "--threads", "10"]
    elif choice == 6:
        cmd = base_cmd + ["--crawl", "--crawl-max", "50"]
    elif choice == 7:
        cmd = base_cmd + ["--skip", "id,token"]
    elif choice == 8:
        cmd = base_cmd + ["--crawl", "--level", "3", "--fuzzer", "--threads", "10"]
    elif choice == 9:
        custom = input(Fore.YELLOW + "Введите команду (пример: --crawl --fuzzer --level 3): ").strip()
        if not custom:
            print(Fore.RED + "Команда не введена")
            return
        cmd = base_cmd + custom.split()
    else:
        print(Fore.RED + "Неверный выбор")
        return

    # === ЗАПУСК ===
    print(Fore.CYAN + f"Команда: {' '.join(cmd)}\n")
    result = subprocess.run(cmd, capture_output=True, text=True)

    # === КАСТОМНЫЙ ВЫВОД ===
    output = result.stdout

    if "Vulnerable" in output:
        print(Fore.GREEN + "[+] XSS УЯЗВИМОСТЬ НАЙДЕНА!")
        payload_match = re.search(r"Payload: (.*)", output)
        if payload_match:
            print(Fore.YELLOW + f"Пейлоад: {payload_match.group(1)}")
    else:
        print(Fore.RED + "[-] XSS не найден")

    # === ОШИБКИ ===
    if result.returncode != 0:
        print(Fore.RED + "Ошибка XSStrike:")
        print(result.stderr)
    else:
        # Показать только ключевые строки (опционально)
        key_lines = [line for line in output.splitlines() if any(k in line for k in ["Vulnerable", "Payload", "WAF", "Crawling", "Found"])]
        if key_lines:
            print(Fore.CYAN + "\n".join(key_lines))