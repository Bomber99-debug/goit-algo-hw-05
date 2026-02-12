from functools import wraps
from typing import Dict, Callable


def input_error(func):
    @wraps(func)
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Please provide both name and phone."
        except KeyError as e:
            return f"Contact '{e.args[0]}' not found."
        except IndexError:
            return "Missing arguments."

    return inner


# Розбирає ввід користувача на команду та аргументи
@input_error
def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


# Додає новий контакт у словник contacts
@input_error
def add_contact(args: list, contacts: dict) -> str:
    try:
        name, phone = args
        contacts[name] = phone
        return "Contact added."
    except ValueError as e:
        return "Name and phone number not recognized"


# Змінює телефон існуючого контакту або додає новий
@input_error
def change_contact(args: list, contacts: dict) -> str:
    try:
        name, phone = args
        contacts[name] = phone
        return "Contact updated."
    except:
        return "Name and phone number not recognized"


# Показує номер телефону конкретного контакту
@input_error
def show_phone(args: list, contacts: dict) -> str:
    name = args[0]
    if name in contacts:
        return f"{name}: {contacts[name]}"
    else:
        return "Contact not found"


# Показує всі контакти в телефонній книзі
def show_all(args: list, contacts: dict) -> str:
    if contacts:
        return '\n'.join(f"{k}: {v}" for k, v in contacts.items())
    else:
        return "Phone book is empty"


# Основна функція, що запускає бота
def main():
    # Словник команд і відповідних функцій
    COMANDS: Dict[str, Callable] = {
        'add': add_contact,
        'change': change_contact,
        'phone': show_phone,
        'all': show_all
    }

    # Початкові контакти для тесту
    contacts: Dict[str, str] = {
        "Alexander": "+380501234567",
        "Maria": "+380631112233",
        "Igor": "+380671234890",
        "Anna": "+380931223344",
        "Victor": "+380991112222",
        "Olena": "+380671234111",
        "Sergey": "+380501112233",
        "Katerina": "+380631234567",
        "Michael": "+380971112345",
        "Tatyana": "+380931234567"
    }

    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        if not user_input:
            print("Please enter a command.")
            continue
        command, *args = parse_input(user_input)

        # Вихід з програми
        if command in ["close", "exit"]:
            print("Good bye!")
            break
        # Привітання
        elif command == "hello":
            print("How can I help you?")
        # Виконання однієї з команд
        elif command in COMANDS:
            print(COMANDS[command](args, contacts))
        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()
