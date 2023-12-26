from abc import ABC, abstractmethod
from geometry import Point, Rectangle


class Tree(ABC):
    @abstractmethod
    def __init__(self, points: list[Point]):
        self.points = list(set(points))

    @abstractmethod
    def find(self, rectangle: Rectangle) -> list[Point]:
        pass
