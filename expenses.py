from __future__ import annotations

import argparse
import sys
from pathlib import Path


DATA_FILE = Path(__file__).with_name("expenses.json")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="CLI utility for tracking personal expenses."
    )
    subparsers = parser.add_subparsers(dest="command")

    add_parser = subparsers.add_parser("add", help="Add a new expense.")
    add_parser.add_argument("amount")
    add_parser.add_argument("category")
    add_parser.add_argument("name")

    add_category_parser = subparsers.add_parser(
        "add-category", help="Create a new expense category."
    )
    add_category_parser.add_argument("category")

    list_parser = subparsers.add_parser("list", help="Show saved expenses.")
    list_parser.add_argument("category", nargs="?")

    total_parser = subparsers.add_parser("total", help="Show total expenses.")
    total_parser.add_argument("category", nargs="?")

    return parser


def not_implemented(command: str) -> int:
    print(f"'{command}' is not implemented yet.")
    print(f"Selected storage format: JSON ({DATA_FILE.name})")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(sys.argv[1:] if argv is None else argv)

    if not args.command:
        parser.print_help()
        return 1

    return not_implemented(args.command)


if __name__ == "__main__":
    raise SystemExit(main())
