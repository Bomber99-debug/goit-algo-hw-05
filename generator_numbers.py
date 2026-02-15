from typing import Callable, Generator


def generator_numbers(text: str) -> list[str]:
    return text.split()


def sum_profit(text: str, fun: Callable[[str], list[str]]) -> float:
    # Підсумовує всі числові значення, отримані з генератора
    summ = 0
    for value in fun(text)[1:-1]:
        try:
            summ += float(value[1])  # Додає число, якщо його можна перетворити у float
        except ValueError:
            continue  # Ігнорує токени, які не є числами
    return summ


text = "Загальний дохід працівника складається з декількох частин: 1000.01 як основний дохід, доповнений додатковими надходженнями 27.45 і 324.00 доларів."

if __name__ == "__main__":
    total_income = sum_profit(text, generator_numbers)
    print(f"Загальний дохід: {total_income}")  # Виводить сумарний дохід