import re
import os
import glob


def find_uncompleted_tasks(text: str) -> list[tuple[str, int]]:
    """
    Находит все невыполненные задачи в тексте.
    
    Возвращает список кортежей (task_text, line_number)
    
    Args:
        text (str): Текст для поиска задач
        
    Returns:
        list[tuple[str, int]]: Список невыполненных задач с номерами строк
    """
    lines = text.split('\n')
    uncompleted_tasks = []
    
    for line_num, line in enumerate(lines, start=1):
        # Ищем паттерн "- [ ]" в начале строки (с возможными отступами)
        match = re.match(r'^(\s*)- \[ \] (.+)$', line)
        if match:
            task_text = match.group(2).strip()
            uncompleted_tasks.append((task_text, line_num))
    
    return uncompleted_tasks


def process_tasks(
    text: str,
    file_name_with_ext: str,
    file_path: str,
    except_files: list[str],
    results_path: str
) -> None:
    """
    Обрабатывает задачи в тексте и записывает результаты в файл.
    
    Args:
        text (str): Текст файла
        file_name (str): Имя файла с расширением
        file_path (str): Относительный путь к файлу
        except_files (list[str]): Список файлов для исключения
        results_path (str): Путь к файлу для записи результатов
    """
    # Проверяем, нужно ли пропустить файл
    if file_name_with_ext in except_files:
        return
    
    file_name = os.path.splitext(file_name_with_ext)[0]

    # Ищем невыполненные задачи
    tasks = find_uncompleted_tasks(text)
    
    # Если задач нет - выходим
    if not tasks:
        return
    
    # Формируем содержимое для записи
    result_content = [f"[[{file_name}]]\n"]
    
    for task_text, line_num in tasks:
        result_content.append(f"- [ ] {task_text}. Строка {line_num}\n")
    
    # Записываем результаты в файл
    with open(results_path, "a", encoding="utf-8") as f:
        f.writelines(result_content)
    
    print(f"Обработан файл: {file_path}")


def process_md_files(
    directory: str,
    except_files: list[str],
    results_path: str
) -> None:
    """
    Находит все .md файлы в директории и её подпапках,
    читает их содержимое и вызывает функцию обработки для каждого файла.
    
    Args:
        directory (str): Путь к директории для поиска
        except_files (list[str]): Список файлов для исключения
        results_path (str): Путь к файлу для записи результатов
    """
    
    # Находим все .md файлы рекурсивно
    md_files = glob.glob(os.path.join(directory, '**', '*.md'), recursive=True)
    
    print(f"Найдено {len(md_files)} .md файлов в директории {directory}")
    
    # Обрабатываем каждый файл
    processed_count = 0
    skipped_count = 0
    
    for file_path in md_files:
        try:
            # Получаем информацию о файле
            file_name_with_ext = os.path.basename(file_path)
            relative_path = os.path.relpath(file_path, directory)
            
            # Читаем содержимое файла
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            # Вызываем функцию обработки
            process_tasks(
                content,
                file_name_with_ext,
                relative_path,
                except_files,
                results_path
            )
            
            processed_count += 1
            
        except UnicodeDecodeError:
            print(f"Ошибка кодировки в файле: {file_path}")
            skipped_count += 1
        except Exception as e:
            print(f"Ошибка при обработке файла {file_path}: {e}")
            skipped_count += 1
    
    # Выводим статистику
    print(f"\nСтатистика обработки:")
    print(f"  Успешно обработано: {processed_count}")
    print(f"  Пропущено с ошибками: {skipped_count}")
    print(f"  Всего файлов: {len(md_files)}")