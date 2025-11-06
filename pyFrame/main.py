import colorama

print(colorama.Fore.YELLOW + "здравствуй дорогой хакер, видимо ты зашел сюда для легкого использования утилит для пентеста, выбирай что хочешь делать:")
print(colorama.Fore.GREEN + "1. Автоматическое сканирование nmap")
print(colorama.Fore.GREEN + "2. автоматическая инъекция sqlmap")
print(colorama.Fore.RED + "3. определить тип хэша(временно не работает)")
print(colorama.Fore.GREEN + "4. крякнуть хэш")
print(colorama.Fore.GREEN + "5. найти эксплоит searchsploit")
print(colorama.Fore.RED + "в стадии разработки 6. угнать wifi сеть (только для linux, aircrack-ng должен быть установлен,)")
print(colorama.Fore.RED + "в стадии разработки 7. проверить сайт на xss(xss striker должен быть установлен)")
print(colorama.Fore.RED + "в стадии разработки 8. выйти из программы")

choice = input(colorama.Fore.WHITE + "введите что вы хотите сделать: ")

command_to_run = ""

if choice > "8" or choice < "1":
    print(colorama.Fore.RED + "Неверный ввод")
    exit()

if choice == "1":
    from modules.scanners.research import auto_nmap
    auto_nmap()
elif choice == "2":
    from modules.web.sqlmap import sqlmap
    sqlmap()
elif choice == "3":
    from modules.crypto.identify import identify
    identify()
elif choice == "4":
    from modules.crypto.crack import crack
    crack()
elif choice == "5":
    from modules.ctfs.searchsploit import find_sploit
    find_sploit() 