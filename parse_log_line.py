from sys import argv
from pathlib import Path


def parse_log_line(line: str) -> dict:
    pass


def load_logs(file_path: str) -> list:
    pass


def filter_logs_by_level(logs: list, level: str) -> list:
    pass


def count_logs_by_level(logs: list) -> dict:
    pass


def display_log_counts(counts: dict):
    pass


def main():
    file_path = Path('files/logs.txt').absolute()
    load_option  = None

    if len(argv) >= 2:
        file_path = Path(argv[1]).absolute()

    if len(argv) == 3:
        load_option  = argv[3]

    if file_path.is_file():
        pass

    else:
        print(f"The specified path is not a valid file: {file_path}")

if __name__ == '__main__':
    main()