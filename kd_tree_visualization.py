from __future__ import annotations
from operator import itemgetter
from bitalg.visualizer.main import Visualizer
from kd_tree import _Node
from geometry import Rectangle, Point
from tree import Tree
from quick_select import quick_select

K = 2


class KdTreeVis(Tree):
    def __init__(self, points: list[Point]):
        super().__init__(points)

        self.max_rectangle = Rectangle(
            min(points, key=itemgetter(0))[0],
            max(points, key=itemgetter(0))[0],
            min(points, key=itemgetter(1))[1],
            max(points, key=itemgetter(1))[1]
        )

        self.vis = Visualizer()
        self.vis.add_point(points, color='black', s=10)

        self.root = self.build_tree(self.points, 0, self.max_rectangle)

    def build_tree(self, points: list[Point], depth: int, rectangle: Rectangle) -> _Node:
        if len(points) == 1:
            node = _Node(None, rectangle)
            node.leaf_point = points[0]
            return node

        p1 = []
        p2 = []
        median_point = quick_select(points, 0, len(points) - 1, (len(points) - 1) // 2, depth % K)
        median = median_point[depth % K]

        equal_counter = 0
        for point in points:
            if point[depth % K] < median:
                p1.append(point)
            elif point[depth % K] > median:
                p2.append(point)
            else:
                if equal_counter % 2 == 0:
                    p1.append(point)
                else:
                    p2.append(point)
                equal_counter += 1

        min_x, max_x, min_y, max_y = rectangle.get_extrema()
        if depth % K == 0:
            self.vis.add_line_segment(((median, min_y), (median, max_y)), color='black')
            vl = self.build_tree(p1, depth + 1, Rectangle(min_x, median, min_y, max_y))
            vr = self.build_tree(p2, depth + 1, Rectangle(median, max_x, min_y, max_y))
        else:
            self.vis.add_line_segment(((min_x, median), (max_x, median)), color='black')
            vl = self.build_tree(p1, depth + 1, Rectangle(min_x, max_x, min_y, median))
            vr = self.build_tree(p2, depth + 1, Rectangle(min_x, max_x, median, max_y))

        v = _Node(depth % K, rectangle)
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

    def __find(self, node: _Node, rectangle: Rectangle, res: list[Point]):
        if rectangle & node.rectangle is None:
            return
        if len(node.leafs) == 0:
            if node.leaf_point is not None and node.leaf_point in rectangle:
                res.append(node.leaf_point)
                self.vis.add_point(node.leaf_point, s=15, color='red')
            return
        for leaf_node in node.leafs:
            self.__find(leaf_node, rectangle, res)

    def find(self, rectangle: Rectangle) -> list[Point]:
        self.vis.add_polygon([(rectangle.min_x, rectangle.min_y), (rectangle.max_x, rectangle.min_y),
                              (rectangle.max_x, rectangle.max_y), (rectangle.min_x, rectangle.max_y)],
                             color='red', alpha=0.3)
        res = []
        self.__find(self.root, rectangle, res)
        return res

    def tree_print(self, node):
        if node is not None:
            print(node)
            self.tree_print(node.left)
            self.tree_print(node.right)
