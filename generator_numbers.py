from typing import Callable, Generator


def generator_numbers(text: str) -> Generator[str, None, None]:
    # Розбиває текст на токени та повертає їх по одному
    for i in text.split():
        yield i.strip()


def sum_profit(text: str, fun: Callable[[str], Generator[str, None, None]]) -> float:
    # Підсумовує всі числові значення, отримані з генератора
    summ = 0
    for value in fun(text):
        try:
            summ += float(value)  # Додає число, якщо його можна перетворити у float
        except ValueError:
            continue  # Ігнорує токени, які не є числами
    return summ


text = "Загальний дохід працівника складається з декількох частин: 1000.01 як основний дохід, доповнений додатковими надходженнями 27.45 і 324.00 доларів."

if __name__ == "__main__":
    total_income = sum_profit(text, generator_numbers)
    print(f"Загальний дохід: {total_income}")  # Виводить сумарний дохід