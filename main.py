import argparse
import math
import sys
from pathlib import Path

from exceptions import GraphError
from graph import Graph

DEFAULT_METRO = Path(__file__).parent / "metro.json"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Кратчайший путь между станциями московского метро"
    )
    parser.add_argument(
        "--from", dest="start", required=True, help="станция отправления"
    )
    parser.add_argument("--to", dest="end", required=True, help="станция назначения")
    parser.add_argument(
        "--metro", default=DEFAULT_METRO, help="путь к JSON со схемой метро"
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    try:
        graph = Graph.from_json(args.metro)
        time = graph.shortest_time(args.start, args.end)
        path = graph.shortest_path(args.start, args.end)
    except GraphError as e:
        print(f"Ошибка: {e}", file=sys.stderr)
        sys.exit(1)

    if time == math.inf:
        print(f"Пути от «{args.start}» до «{args.end}» нет")
        sys.exit(1)

    print(f"Время в пути: {time} мин")
    print("\n".join(path))


if __name__ == "__main__":
    main()
