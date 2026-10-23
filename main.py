import argparse
import math
import sys
from pathlib import Path

from exceptions import GraphError
from graph import Graph

METRO_PATH = Path(__file__).parent / "metro.json"


def parse_args() -> argparse.Namespace:
    # --from/--to нужны и без подкоманды, и после неё, поэтому они вынесены
    # в общий парсер; SUPPRESS не даёт подкоманде затереть уже введённые значения
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument(
        "--from", dest="start", default=argparse.SUPPRESS, help="станция отправления"
    )
    common.add_argument(
        "--to", dest="end", default=argparse.SUPPRESS, help="станция назначения"
    )

    parser = argparse.ArgumentParser(
        description="Кратчайший путь между станциями московского метро",
        epilog="без подкоманды выводятся и время, и маршрут",
        parents=[common],
    )
    subparsers = parser.add_subparsers(dest="command", title="подкоманды")
    subparsers.add_parser("time", parents=[common], help="вывести только время")
    subparsers.add_parser("path", parents=[common], help="вывести только маршрут")

    args = parser.parse_args()
    missing = [
        option
        for option, dest in (("--from", "start"), ("--to", "end"))
        if not hasattr(args, dest)
    ]
    if missing:
        parser.error(f"обязательные аргументы: {', '.join(missing)}")
    return args


def main() -> None:
    args = parse_args()
    try:
        graph = Graph.from_json(METRO_PATH)
        time = graph.shortest_time(args.start, args.end)
        path = graph.shortest_path(args.start, args.end)
    except GraphError as e:
        print(f"Ошибка: {e}", file=sys.stderr)
        sys.exit(1)

    if time == math.inf:
        print(f"Пути от «{args.start}» до «{args.end}» нет")
        sys.exit(1)

    if args.command in (None, "time"):
        print(time)
    if args.command in (None, "path"):
        print("\n".join(path))


if __name__ == "__main__":
    main()
