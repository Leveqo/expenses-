import json
import sys


DATA_FILE = "expenses.json"

def load_data():
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {"categories": [], "expenses": []}
    except json.JSONDecodeError:
        print("Ошибка: файл с данными поврежден.")
        data = {"categories": [], "expenses": []}

    if "categories" not in data:
        data["categories"] = []
    if "expenses" not in data:
        data["expenses"] = []

    return data

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)

def show_help():
    print("Использование:")
    print("  python expenses.py add <стоимость> <категория> <название>")
    print("  python expenses.py add-category <категория>")
    print("  python expenses.py list [категория]")
    print("  python expenses.py total [категория]")

def add_category(category):
    data = load_data()
    category = category.strip()

    if category == "":
        print("Название категории не может быть пустым.")
        return

    if category in data["categories"]:
        print("Такая категория уже есть.")
        return

    data["categories"].append(category)
    save_data(data)
    print("Категория добавлена.")


def add_expense(amount_text, category, name):
    data = load_data()
    amount_text = amount_text.replace(",", ".").strip()
    category = category.strip()
    name = name.strip()

    if amount_text == "" or category == "" or name == "":
        print("Все поля должны быть заполнены.")
        return

    if category not in data["categories"]:
        print("Такой категории нет.")
        return

    try:
        amount = float(amount_text)
    except ValueError:
        print("Стоимость должна быть числом.")
        return

    if amount <= 0:
        print("Стоимость должна быть больше нуля.")
        return

    expense = {
        "amount": amount,
        "category": category,
        "name": name,
    }
    data["expenses"].append(expense)
    save_data(data)
    print("Расход добавлен.")

def print_expense(number, expense):
    amount = expense["amount"]
    if amount == int(amount):
        amount = int(amount)

    print(
        str(number)
        + ". "
        + expense["name"]
        + " - "
        + str(amount)
        + " ("
        + expense["category"]
        + ")"
    )

def show_expenses(category):
    data = load_data()
    found = False
    number = 1

    if category != "" and category not in data["categories"]:
        print("Такой категории нет.")
        return

    for expense in data["expenses"]:
        if category == "" or expense["category"] == category:
            print_expense(number, expense)
            found = True
            number += 1

    if not found:
        print("Расходов пока нет.")

def show_total(category):
    data = load_data()
    total = 0

    if category != "" and category not in data["categories"]:
        print("Такой категории нет.")
        return

    for expense in data["expenses"]:
        if category == "" or expense["category"] == category:
            total += expense["amount"]

    if total == int(total):
        total = int(total)

    if category == "":
        print("Общая сумма расходов:", total)
    else:
        print("Сумма расходов в категории", category + ":", total)

def main():
    args = sys.argv[1:]

    if len(args) == 0:
        show_help()
        return

    command = args[0]

    if command == "add-category":
        if len(args) != 2:
            print("Нужно указать категорию.")
            show_help()
            return
        add_category(args[1])
    elif command == "add":
        if len(args) != 4:
            print("Нужно указать стоимость, категорию и название.")
            show_help()
            return
        add_expense(args[1], args[2], args[3])
    elif command == "list":
        if len(args) == 1:
            show_expenses("")
        elif len(args) == 2:
            show_expenses(args[1])
        else:
            print("У команды list может быть только одна категория.")
            show_help()
    elif command == "total":
        if len(args) == 1:
            show_total("")
        elif len(args) == 2:
            show_total(args[1])
        else:
            print("У команды total может быть только одна категория.")
            show_help()
    else:
        print("Неизвестная команда.")
        show_help()

main()