import heapq
import json
import math
from os import PathLike
from typing import Self

from exceptions import (
    EdgeAlreadyExistsError,
    EdgeNotFoundError,
    NonPositiveWeightError,
    StationAlreadyExistsError,
    StationNotFoundError,
)


class Graph:
    def __init__(self) -> None:
        self._adj: dict[str, dict[str, float]] = {}

    def add_station(self, station: str) -> None:
        if self.has_station(station):
            raise StationAlreadyExistsError(station)
        self._adj[station] = {}

    def add_edge(self, from_station: str, to_station: str, weight: float) -> None:
        if weight <= 0:
            raise NonPositiveWeightError(weight)
        self._check_station(from_station)
        self._check_station(to_station)
        if to_station in self._adj[from_station]:
            raise EdgeAlreadyExistsError(from_station, to_station)
        # метро двунаправленное — добавляем ребро в обе стороны
        self._adj[from_station][to_station] = weight
        self._adj[to_station][from_station] = weight

    def neighbors(self, station: str) -> list[tuple[str, float]]:
        self._check_station(station)
        return list(self._adj[station].items())

    def remove_station(self, station: str) -> None:
        self._check_station(station)
        for neighbor in self._adj[station]:
            del self._adj[neighbor][station]
        del self._adj[station]

    def remove_edge(self, from_station: str, to_station: str) -> None:
        self._check_station(from_station)
        self._check_station(to_station)
        if to_station not in self._adj[from_station]:
            raise EdgeNotFoundError(from_station, to_station)
        del self._adj[from_station][to_station]
        del self._adj[to_station][from_station]

    def has_station(self, station: str) -> bool:
        return station in self._adj

    def _check_station(self, station: str) -> None:
        if not self.has_station(station):
            raise StationNotFoundError(station)

    def stations(self) -> list[str]:
        return list(self._adj)

    def shortest_time(self, start: str, end: str) -> float:
        """Наименьшее время от start до end (inf, если пути нет)."""
        time, _ = self._dijkstra(start, end)
        return time

    def shortest_path(self, start: str, end: str) -> list[str]:
        """Станции кратчайшего пути от start до end ([], если пути нет)."""
        _, path = self._dijkstra(start, end)
        return path

    def _dijkstra(self, start: str, end: str) -> tuple[float, list[str]]:
        """Дейкстра от start до end.

        Возвращает (время, [станции пути]) или (inf, []), если пути нет.
        """
        self._check_station(start)
        self._check_station(end)

        dist: dict[str, float] = {start: 0}
        prev: dict[str, str | None] = {start: None}
        heap: list[tuple[float, str]] = [(0, start)]

        while heap:
            d, u = heapq.heappop(heap)
            if u == end:
                break
            if d > dist[u]:
                continue
            for v, w in self._adj[u].items():
                nd = d + w
                if nd < dist.get(v, math.inf):
                    dist[v] = nd
                    prev[v] = u
                    heapq.heappush(heap, (nd, v))

        if end not in dist:
            return math.inf, []

        path: list[str] = []
        cur: str | None = end
        while cur is not None:
            path.append(cur)
            cur = prev[cur]
        path.reverse()
        return dist[end], path

    @classmethod
    def from_json(cls, path: str | PathLike[str]) -> Self:
        graph = cls()
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        for station in data.get("stations", []):
            graph.add_station(station)
        for edge in data.get("edges", []):
            graph.add_edge(edge["from"], edge["to"], edge["weight"])
        return graph
