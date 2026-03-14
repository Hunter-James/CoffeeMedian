import argparse
import csv
import sys
from typing import List, Dict

from tabulate import tabulate
from reports import REPORT_REGISTRY


def read_csv_files(file_paths: List[str]) -> List[Dict[str, str]]:
    data = []
    for path in file_paths:
        try:
            with open(path, mode="r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                data.extend(list(reader))
        except FileNotFoundError:
            print(f"Ошибка: Файл '{path}' не найден.", file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            print(f"Ошибка при чтении файла '{path}': {e}", file=sys.stderr)
            sys.exit(1)
    return data


def main():
    parser = argparse.ArgumentParser(description="Генератор отчетов об успеваемости и тратах студентов.")
    parser.add_argument(
        "--files",
        nargs="+",
        required=True,
        help="Пути к CSV файлам с данными"
    )
    parser.add_argument(
        "--report",
        required=True,
        help="Название отчета для генерации"
    )

    args = parser.parse_args()

    # Проверка наличия отчета в реестре
    if args.report not in REPORT_REGISTRY:
        available_reports = ", ".join(REPORT_REGISTRY.keys())
        print(f"Ошибка: Отчет '{args.report}' не найден. Доступные отчеты: {available_reports}", file=sys.stderr)
        sys.exit(1)

    # Чтение данных
    raw_data = read_csv_files(args.files)
    if not raw_data:
        print("Внимание: Данные не найдены, отчет пуст.")
        sys.exit(0)

    # Генерация отчета
    report_strategy = REPORT_REGISTRY[args.report]
    report_data = report_strategy.generate(raw_data)

    # Форматирование и вывод через tabulate
    table_rows = [[row[header] for header in report_strategy.headers] for row in report_data]

    # tablefmt="psql" делает рамки
    print(tabulate(table_rows, headers=report_strategy.headers, tablefmt="psql"))


if __name__ == "__main__":
    main()