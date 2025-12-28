# kote-md-task-parser
Утилита для поиска невыполненных задач в Markdown файлах.

Ищет в папке и подпапках md-файлы, определяет невыполненные задачи через `- [ ]` в тексте. Генерирует в корне `DIRECTORY` файл `Backlog.md`, в котором будут:
```
[[Название файла]]
- [ ] Задача. Строка X
```
## Настройка
Переименуйте `settings.py.example` в `settings.py`.
```
# Путь к вашим заметкам
DIRECTORY = "C:/Users/username/Documents/notes"

# Путь к вашим заметкам
EXCEPT_FILES = [ "README.md" ]

# Файл результатов создается автоматически
RESULTS_FILE = os.path.join(DIRECTORY, "Backlog.md")
```
## Пример использования
`uv run main.py`