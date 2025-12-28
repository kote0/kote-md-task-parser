import os
from settings import DIRECTORY, EXCEPT_FILES, RESULTS_FILE
from task_finder import process_md_files

# Проверяем директорию
if not os.path.isdir(DIRECTORY):
    print(f"Директория {DIRECTORY} не существует!")
    exit()

# Очищаем старый файл результатов
if os.path.exists(RESULTS_FILE):
    os.remove(RESULTS_FILE)

# Создаем новый файл с заголовком
with open(RESULTS_FILE, "w", encoding="utf-8") as f:
    f.write("# Невыполненные задачи\n\n")

# Запускаем поиск
print("Поиск невыполненных задач...")
process_md_files(
    directory=DIRECTORY,
    except_files=EXCEPT_FILES,
    results_path=RESULTS_FILE
)

print("Готово!")