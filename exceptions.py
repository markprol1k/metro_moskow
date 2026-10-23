class GraphError(Exception):
    """Базовое исключение для ошибок графа."""


class StationAlreadyExistsError(GraphError):
    def __init__(self, station: str) -> None:
        self.station = station
        super().__init__(f"Станция уже существует: {station}")


class EdgeAlreadyExistsError(GraphError):
    def __init__(self, from_station: str, to_station: str) -> None:
        self.from_station = from_station
        self.to_station = to_station
        super().__init__(f"Ребро уже существует: {from_station} — {to_station}")


class StationNotFoundError(GraphError):
    def __init__(self, station: str) -> None:
        self.station = station
        super().__init__(f"Нет станции: {station}")


class EdgeNotFoundError(GraphError):
    def __init__(self, from_station: str, to_station: str) -> None:
        self.from_station = from_station
        self.to_station = to_station
        super().__init__(f"Нет ребра: {from_station} — {to_station}")


class NonPositiveWeightError(GraphError):
    def __init__(self, weight: float) -> None:
        self.weight = weight
        super().__init__(f"Вес ребра должен быть положительным, получено: {weight}")
