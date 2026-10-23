import math

import pytest

from exceptions import (
    EdgeAlreadyExistsError,
    EdgeNotFoundError,
    NonPositiveWeightError,
    StationAlreadyExistsError,
    StationNotFoundError,
)
from graph import Graph


@pytest.fixture
def graph() -> Graph:
    g = Graph()
    for station in ["A", "B", "C", "D", "X"]:
        g.add_station(station)
    g.add_edge("A", "B", 4)
    g.add_edge("A", "C", 1)
    g.add_edge("C", "B", 2)
    g.add_edge("B", "D", 5)
    return g


def test_add_station_new_station_is_added() -> None:
    g = Graph()
    g.add_station("Курская")
    assert g.has_station("Курская")
    assert g.neighbors("Курская") == []


def test_add_station_duplicate_raises() -> None:
    g = Graph()
    g.add_station("Курская")
    with pytest.raises(StationAlreadyExistsError):
        g.add_station("Курская")


def test_add_edge_is_bidirectional(graph: Graph) -> None:
    graph.add_station("E")
    graph.add_edge("D", "E", 3)
    assert ("E", 3) in graph.neighbors("D")
    assert ("D", 3) in graph.neighbors("E")


@pytest.mark.parametrize("weight", [0, -1, -10.5])
def test_add_edge_non_positive_weight_raises(graph: Graph, weight: float) -> None:
    start, end = "D", "X"
    with pytest.raises(NonPositiveWeightError):
        graph.add_edge(start, end, weight)


def test_add_edge_duplicate_in_reverse_direction_raises(graph: Graph) -> None:
    start, end = "B", "A"
    with pytest.raises(EdgeAlreadyExistsError):
        graph.add_edge(start, end, 7)


def test_remove_station_removes_links_from_neighbors(graph: Graph) -> None:
    station = "B"
    graph.remove_station(station)
    assert not graph.has_station("B")
    assert graph.neighbors("A") == [("C", 1)]
    assert graph.neighbors("D") == []


def test_remove_station_missing_raises(graph: Graph) -> None:
    missing = "Нет такой"
    with pytest.raises(StationNotFoundError):
        graph.remove_station(missing)


def test_remove_edge_removes_both_directions(graph: Graph) -> None:
    start, end = "A", "B"
    graph.remove_edge(start, end)
    assert "B" not in dict(graph.neighbors("A"))
    assert "A" not in dict(graph.neighbors("B"))
    assert graph.has_station("A") and graph.has_station("B")


def test_remove_edge_missing_raises(graph: Graph) -> None:
    start, end = "A", "D"
    with pytest.raises(EdgeNotFoundError):
        graph.remove_edge(start, end)


def test_neighbors_returns_pairs_with_weights(graph: Graph) -> None:
    station = "B"
    result = graph.neighbors(station)
    assert sorted(result) == [("A", 4), ("C", 2), ("D", 5)]


def test_neighbors_missing_station_raises(graph: Graph) -> None:
    missing = "Z"
    with pytest.raises(StationNotFoundError):
        graph.neighbors(missing)


@pytest.mark.parametrize(
    "start, end, expected",
    [
        ("A", "B", 3),
        ("A", "D", 8),
        ("D", "C", 7),
        ("A", "A", 0),
    ],
)
def test_shortest_time_finds_minimum(
    graph: Graph, start: str, end: str, expected: float
) -> None:
    result = graph.shortest_time(start, end)
    assert result == expected


def test_shortest_time_no_path_returns_inf(graph: Graph) -> None:
    start, end = "A", "X"
    result = graph.shortest_time(start, end)
    assert result == math.inf


def test_shortest_path_returns_stations_in_order(graph: Graph) -> None:
    start, end = "A", "D"
    result = graph.shortest_path(start, end)
    assert result == ["A", "C", "B", "D"]


def test_shortest_path_no_path_returns_empty(graph: Graph) -> None:
    start, end = "D", "X"
    result = graph.shortest_path(start, end)
    assert result == []


def test_shortest_path_missing_station_raises(graph: Graph) -> None:
    start, end = "A", "Z"
    with pytest.raises(StationNotFoundError):
        graph.shortest_path(start, end)
