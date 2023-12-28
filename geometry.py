from __future__ import annotations

Point = tuple[float, float]


class Rectangle:
    def __init__(self, min_x: float, max_x: float, min_y: float, max_y: float):
        if min_x >= max_x or min_y >= max_y:
            raise ValueError('Incorrect rectangle extrema.')
        self.min_x = min_x
        self.max_x = max_x
        self.min_y = min_y
        self.max_y = max_y

    def get_extrema(self) -> tuple[float, float, float, float]:
        return self.min_x, self.max_x, self.min_y, self.max_y

    def __eq__(self, other: Rectangle) -> bool:
        if not isinstance(other, Rectangle):
            return False
        return self.get_extrema() == other.get_extrema()

    def __and__(self, other: Rectangle) -> Rectangle | None:
        if not isinstance(other, Rectangle):
            raise TypeError(f"'&' not supported between instances of 'Rectangle' and '{type(other).__name__}'")
        min_x = max(self.min_x, other.min_x)
        max_x = min(self.max_x, other.max_x)
        min_y = max(self.min_y, other.min_y)
        max_y = min(self.max_y, other.max_y)
        if min_x < max_x and min_y < max_y:
            return Rectangle(min_x, max_x, min_y, max_y)
        else:
            return None

    def __contains__(self, item: Rectangle | Point) -> bool:
        if isinstance(item, Rectangle):
            return self & item == item
        else:
            try:
                return self.min_x <= item[0] <= self.max_x and self.min_y <= item[1] <= self.max_y
            except (ValueError, TypeError):
                raise TypeError(f"'in' not supported between instances of '{type(item).__name__}' and 'Rectangle'")
