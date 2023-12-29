from __future__ import annotations
from bitalg.visualizer.main import Visualizer
from operator import itemgetter
from kd_tree import _Node, Point
from geometry import Rectangle
from tree import Tree

K = 2


class KdTreeVis(Tree):
    def __init__(self, points: list[Point]):
        super().__init__(points)

        self.sorted_points = []
        for i in range(K):
            self.sorted_points.append(sorted(self.points, key=itemgetter(i)))

        self.max_rectangle = Rectangle(
            min(points, key=itemgetter(0))[0],
            max(points, key=itemgetter(0))[0],
            min(points, key=itemgetter(1))[1],
            max(points, key=itemgetter(1))[1]
        )

        self.vis = Visualizer()
        self.vis.add_point(self.points, s=10, color="black")

        self.root = self.build_tree(self.sorted_points, 0, self.max_rectangle)

    def build_tree(self, points: list[list[Point]], depth: int, rectangle: Rectangle) -> _Node:
        if len(points[depth % K]) == 1:
            node = _Node(None, None, rectangle)
            node.leaf_point = points[depth % K][0]
            return node

        p1 = [[] for _ in range(K)]
        p2 = [[] for _ in range(K)]

        median_id = (len(points[depth % K]) - 1) // 2
        median = points[depth % K][median_id][depth % K]
        if len(points[depth % K]) % 2 == 0:
            median = (median + points[depth % K][median_id + 1][depth % K]) / 2

        for i in range(K):
            for point in points[i]:
                if point[depth % K] < median:
                    p1[i].append(point)
                elif point[depth % K] > median:
                    p2[i].append(point)
                else:
                    if depth % 2 == 0:
                        p1[i].append(point)
                    else:
                        p2[i].append(point)

        min_x, max_x, min_y, max_y = rectangle.get_extrema()
        if depth % K == 0:
            val = points[depth % K][median_id][0]
            self.vis.add_line_segment(((val, min_y), (val, max_y)))

            vl = self.build_tree(p1, depth + 1, Rectangle(min_x, val, min_y, max_y))
            vr = self.build_tree(p2, depth + 1, Rectangle(val, max_x, min_y, max_y))
        else:
            val = points[depth % K][median_id][1]
            self.vis.add_line_segment(((min_x, val), (max_x, val)))

            vl = self.build_tree(p1, depth + 1, Rectangle(min_x, max_x, min_y, val))
            vr = self.build_tree(p2, depth + 1, Rectangle(min_x, max_x, val, max_y))

        v = _Node(depth % K, points[depth % K][median_id], rectangle)
        v.left = vl
        v.right = vr
        if vl.leaf_point is not None:
            v.leafs.append(vl)
        else:
            v.leafs += vl.leafs

        if vr.leaf_point is not None:
            v.leafs.append(vr)
        else:
            v.leafs += vr.leafs

        return v

    def points_from_rectangle(self, rectangle: Rectangle) -> tuple[tuple[float, float],
    tuple[float, float],
    tuple[float, float],
    tuple[float, float]]:
        min_x, max_x, min_y, max_y = rectangle.get_extrema()
        return (min_x, min_y), (max_x, min_y), (max_x, max_y), (min_x, max_y)

    def __find(self, node: _Node, rectangle: Rectangle, res: list[Point]):
        if rectangle & node.rectangle is None:
            return
        if len(node.leafs) == 0:
            if node.leaf_point is not None and node.leaf_point in rectangle:
                res.append(node.leaf_point)
                self.vis.add_point(node.leaf_point, s=10, color="red")
            return
        for leaf_node in node.leafs:
            self.__find(leaf_node, rectangle, res)

    def find(self, rectangle: Rectangle) -> list[Point]:
        self.vis.add_polygon(self.points_from_rectangle(rectangle), alpha=0.5, color="red")
        res = []
        self.__find(self.root, rectangle, res)
        return res
