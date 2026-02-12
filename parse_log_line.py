from sys import argv
from pathlib import Path
from typing import List, Optional
from collections import Counter


def parse_log_line(line: str) -> Optional[dict[str, str]]:
    """
    Розбирає один рядок лог-файлу.
    Очікує формат: <дата> <час> <рівень> <повідомлення>
    Повертає словник з ключами: log_date, log_time, log_level, log_message.
    Якщо рядок некоректний, повертає None.
    """
    try:
        log_date, log_time, log_level, *log_message = line.split()
    except ValueError:
        print(f"Invalid log line: {line.strip()}")
        return None

    return {'log_date': log_date,
            'log_time': log_time,
            'log_level': log_level,
            'log_message': ' '.join(log_message)
            }


def load_logs(file_path: Path, encoding: str = "utf-8") -> list[dict[str, str]]:
    """
    Завантажує всі рядки з лог-файлу та парсить їх за допомогою parse_log_line.
    Повертає список словників, де кожен словник — один лог.
    """
    log_entries: List[dict[str, str]] = []

    try:
        with file_path.open(encoding=encoding) as file:
            for line in file:
                log_entry = parse_log_line(line)
                if log_entry:
                    log_entries.append(log_entry)
    except (FileNotFoundError, PermissionError, OSError) as e:
        print(f"Error opening file {file_path}: {e}")

    return log_entries


def filter_logs_by_level(logs: list[dict[str, str]], level: str) -> list[str]:
    """
    Фільтрує логи за вказаним рівнем (INFO, DEBUG, ERROR, WARNING).
    Повертає список форматованих рядків: '<дата> <час> - <повідомлення>'.
    """
    try:
        return list(
            f"{log['log_date']} {log['log_time']} - {log['log_message']}"
            for log in logs
            if log['log_level'] == level.upper()
        )
    except KeyError as e:
        print(f"Missing expected key in log: {e}")
        return []


def count_logs_by_level(logs: list[dict[str, str]]) -> dict[str, int]:
    """
    Підраховує кількість логів для кожного рівня.
    Повертає словник у форматі {рівень: кількість}.
    """
    try:
        return dict(Counter(log['log_level'] for log in logs))
    except KeyError as e:
        print(f"Missing expected key in log: {e}")
        return []


def display_log_counts(counts: dict):
    """
    Форматує та повертає таблицю з підрахунком логів за рівнем.
    Використовує українські заголовки: 'Рівень логування' та 'Кількість'.
    """
    headers = ["Рівень логування", "Кількість"]
    col1_width = max(len(headers[0]), *(len(k) for k in counts))
    col2_width = max(len(headers[1]), *(len(str(v)) for v in counts.values()))
    border = "+" + '-' * (col1_width + 2) + "+" + '-' * (col2_width + 2) + '+'
    head = f'{border}\n| {headers[0]} | {headers[1]} |\n{border}\n'
    body = ''
    for k, v in counts.items():
        body += f"| {k:<{col1_width}} | {v:<{col2_width}} |\n"

    return head + body + border


def main():
    """
    Головна функція скрипту.
    - Читає аргументи командного рядка: шлях до файлу та опціонально рівень логів для фільтру.
    - Завантажує та підраховує логи.
    - Виводить таблицю підрахунків та деталі логів для вказаного рівня.
    """
    valid_levels = ['INFO', 'DEBUG', 'ERROR', 'WARNING']
    file_path = Path('files/logs.txt').absolute()  # Шлях до файлу за замовчуванням
    filter_level = None

    # Якщо переданий аргумент командного рядка, використовуємо його як шлях до файлу
    if len(argv) >= 2:
        file_path = Path(argv[1]).absolute()

    # Якщо переданий другий аргумент, використовуємо його як рівень логів для фільтру
    if len(argv) == 3:
        filter_level = argv[2]

    if file_path.is_file():
        logs = load_logs(file_path)  # Завантажуємо всі логи з файлу
        counts = count_logs_by_level(logs)  # Підраховуємо кількість логів за рівнем
        result = display_log_counts(counts)  # Форматуємо таблицю
        print(result)

        # Фільтруємо та виводимо логи для конкретного рівня
        if filter_level:
            if filter_level in valid_levels:
                result_options = filter_logs_by_level(logs, filter_level)
                print(f"\nДеталі логів для рівня '{filter_level.upper()}':")
                for log_line in result_options:
                    print(log_line)
            else:
                print("Error not found")  # Некоректний рівень логів
    else:
        print(f"The specified path is not a valid file: {file_path}")  # Файл не знайдено


if __name__ == '__main__':
    main()  # Виконання скрипту
