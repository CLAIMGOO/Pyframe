import hashlib
print("=== Кряк хеша ===")
print("Поддерживаемые методы: md5, sha1, sha256")
print("Используйте хороший словарь для повышения шансов на успех")
print("=================")

# --- Ввод ---
target = input("Введите хеш (строка): ").strip().lower()
method = input("Метод (md5/sha1/sha256): ").strip().lower()
wordlist_path = input("Путь к словарю: ").strip()

# --- Подсчёт строк ---
with open(wordlist_path, encoding='latin-1') as f:
    total_lines = sum(1 for _ in f)

# --- Кряк ---
with open(wordlist_path, encoding='latin-1') as f:
    for current_line, line in enumerate(f, 1):
        word = line.strip()
        if not word:
            continue
        # ... остальное без изменений

        # Хеширование
        if method == "md5":
            h = hashlib.md5(word.encode()).hexdigest()
        elif method == "sha1":
            h = hashlib.sha1(word.encode()).hexdigest()
        elif method == "sha256":
            h = hashlib.sha256(word.encode()).hexdigest()
        else:
            print("Метод не поддерживается")
            exit()

        # Сравнение
        if h == target:
            print(f"\n[+] НАЙДЕНО: {word}")
            print(f"    Хеш: {h}")
            print(f"    Прогресс: {current_line/total_lines*100:.2f}%")
            exit()

        # Прогресс (каждые 1000 строк)
        if current_line % 1000 == 0:
            print(f"Прогресс: {current_line/total_lines*100:.2f}%", end="\r")

print("\n[-] Слово не найдено в словаре.")