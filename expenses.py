from __future__ import annotations

import json
import sys
from pathlib import Path


DATA_FILE = Path(__file__).with_name("expenses.json")
DEFAULT_DATA = {"categories": [], "expenses": []}


def print_usage() -> None:
    print("Использование:")
    print("  python expenses.py add <стоимость> <категория> <название>")
    print("  python expenses.py add-category <категория>")
    print("  python expenses.py list [категория]")
    print("  python expenses.py total [категория]")


def load_data() -> dict[str, list]:
    if not DATA_FILE.exists():
        save_data(DEFAULT_DATA)
        return DEFAULT_DATA.copy()

    with DATA_FILE.open("r", encoding="utf-8") as file:
        data = json.load(file)

    categories = data.get("categories", [])
    expenses = data.get("expenses", [])
    return {
        "categories": categories,
        "expenses": expenses,
    }


def save_data(data: dict[str, list]) -> None:
    with DATA_FILE.open("w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)
        file.write("\n")


def add_category(category: str) -> int:
    normalized_category = category.strip()
    if not normalized_category:
        print("Название категории не может быть пустым.")
        return 1

    data = load_data()
    categories = data["categories"]
    if normalized_category in categories:
        print(f"Категория '{normalized_category}' уже существует.")
        return 1

    categories.append(normalized_category)
    save_data(data)
    print(f"Категория '{normalized_category}' добавлена.")
    return 0


def not_implemented(command: str) -> int:
    print(f"Команда '{command}' пока не реализована.")
    print(f"Выбранный формат хранения: JSON ({DATA_FILE.name})")
    return 0


def main(argv: list[str] | None = None) -> int:
    args = sys.argv[1:] if argv is None else argv

    if not args:
        print_usage()
        return 1

    command = args[0]

    if command in {"-h", "--help"}:
        print_usage()
        return 0

    if command == "add-category":
        if len(args) != 2:
            print("Для команды add-category нужно указать одну категорию.")
            print_usage()
            return 1
        return add_category(args[1])

    if command == "add":
        if len(args) != 4:
            print("Для команды add нужно указать стоимость, категорию и название.")
            print_usage()
            return 1
        return not_implemented(command)

    if command == "list":
        if len(args) > 2:
            print("У команды list может быть только одна категория.")
            print_usage()
            return 1
        return not_implemented(command)

    if command == "total":
        if len(args) > 2:
            print("У команды total может быть только одна категория.")
            print_usage()
            return 1
        return not_implemented(command)

    print(f"Неизвестная команда: {command}")
    print_usage()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
