from __future__ import annotations
from operator import itemgetter
from geometry import Point, Rectangle
from tree import Tree


class _Node:
    def __init__(self, min_x: float, max_x: float, min_y: float, max_y: float):
        self.rectangle = Rectangle(min_x, max_x, min_y, max_y)
        self.min_x = min_x
        self.max_x = max_x
        self.min_y = min_y
        self.max_y = max_y
        self.mid_x = (min_x + max_x) / 2
        self.mid_y = (min_y + max_y) / 2
        self.children = None
        self.leaf_point = None


class Quadtree(Tree):
    def __init__(self, points: list[Point]):
        super().__init__(points)
        self.root = _Node(
            min(points, key=itemgetter(0))[0],
            max(points, key=itemgetter(0))[0],
            min(points, key=itemgetter(1))[1],
            max(points, key=itemgetter(1))[1]
        )
        self.__construct_subtree(self.root, self.points)

    def __construct_subtree(self, node: _Node, points: list[Point]):
        if len(points) == 1:
            node.leaf_point = points[0]
        if len(points) <= 1:
            return

        children_nodes = [
            _Node(node.mid_x, node.max_x, node.mid_y, node.max_y),
            _Node(node.min_x, node.mid_x, node.mid_y, node.max_y),
            _Node(node.min_x, node.mid_x, node.min_y, node.mid_y),
            _Node(node.mid_x, node.max_x, node.min_y, node.mid_y)
        ]

        # todo: check if it's not better to just append and iterate only once
        children_points = [
            list(filter(lambda p: p[0] > node.mid_x and p[1] >= node.mid_y, points)),
            list(filter(lambda p: p[0] <= node.mid_x and p[1] > node.mid_y, points)),
            list(filter(lambda p: p[0] < node.mid_x and p[1] <= node.mid_y, points)),
            list(filter(lambda p: p[0] >= node.mid_x and p[1] < node.mid_y, points)),
        ]

        node.children = children_nodes
        for child_node, child_points in zip(children_nodes, children_points):
            self.__construct_subtree(child_node, child_points)

    def __find(self, node: _Node, rectangle: Rectangle, res: list[Point]):
        if rectangle & node.rectangle is None:
            return
        if node.children is None:
            if node.leaf_point is not None and node.leaf_point in rectangle:
                res.append(node.leaf_point)
            return
        for child_node in node.children:
            self.__find(child_node, rectangle, res)

    def find(self, rectangle: Rectangle) -> list[Point]:
        res = []
        self.__find(self.root, rectangle, res)
        return res
