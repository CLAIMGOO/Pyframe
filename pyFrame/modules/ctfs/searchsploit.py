import subprocess
import os
from colorama import Fore

def searchsploit():
    print(Fore.CYAN + "searchsploit приветствует вас!")
    search = input("вводите название: ")
    
    cmd = f"searchsploit -t {search}"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    if "No Results" in result.stdout.lower():
        print(Fore.RED + "НЕ найдено")
        return

    lines = result.stdout.splitlines()
    exploits = []
    
    print(Fore.GREEN + "Найденные эксплойты:")
    for i, line in enumerate(lines, 1):
        if "|" in line and "Exploit Title" not in line:
            title = line.split("|")[0].strip()
            path = line.split("|")[1].strip()
            print(f"{i}. {title}")
            exploits.append((title, path))
    
    if not exploits:
        print("Ничего не найдено")
        return

    try:
        choice = int(input("Введите номер эксплойта: ")) - 1
    except ValueError:
        print("Введите число!")
        return

    if 0 <= choice < len(exploits):
        selected_title, selected_path = exploits[choice]
        print(f"Выбран: {selected_title}")
        print(f"Путь: {selected_path}")
        
        edb_id = selected_path.split("/")[-1].split(".")[0]
        subprocess.run(["searchsploit", "-m", edb_id])

        current_dir = os.getcwd()
        py_file = os.path.join(current_dir, f"{edb_id}.py")
        txt_file = os.path.join(current_dir, f"{edb_id}.txt")

        if os.path.exists(py_file):
            print(f"Сохранено: {py_file}")
        elif os.path.exists(txt_file):
            print(f"Сохранено: {txt_file}")
        else:
            print("Ошибка копирования")

        if input("Перейти в папку? (y/n): ").lower() == "y":
            os.chdir(current_dir)
            print(f"Текущая папка: {os.getcwd()}")
    else:
        print("Неверный номер")