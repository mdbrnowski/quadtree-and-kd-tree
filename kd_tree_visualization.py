from __future__ import annotations
from bitalg.visualizer.main import Visualizer
from operator import itemgetter
from kd_tree import Node, Point
from geometry import Rectangle
from tree import Tree

K = 2
Point = tuple(float() for _ in range(K))

class KdTreeVis(Tree):
    def __init__(self, points: list[Point]):
        self.points = points

        self.sorted_points = []
        for i in range(K):
            self.sorted_points.append(sorted(points, key=itemgetter(i)))

        rectangle = Rectangle(
            min(points, key=itemgetter(0))[0],
            max(points, key=itemgetter(0))[0],
            min(points, key=itemgetter(1))[1],
            max(points, key=itemgetter(1))[1]
        )

        self.vis = Visualizer()
        self.vis.add_point(self.points, s=10, color="black")

        self.root = self.build_tree(self.sorted_points, 0, rectangle)
        # self.vis.show()
        # self.vis.show_gif()
        # self.root = self.build_tree(self.sorted_points, 0, Rectangle(0, 10, 0, 10))

    def build_tree(self, points: list[list[Point]], depth: int, rectangle: Rectangle):
        if len(points[depth % K]) == 1:
            node = Node(None, None, rectangle)
            node.leaf_point = points[depth % K][0]
            return node

        if len(points[depth % K]) == 0:
            # print("WRONG")
            return None

        # Dodaj losowość, żeby zrównoważyć
        p1 = [[] for _ in range(K)]
        p2 = [[] for _ in range(K)]
        median = len(points[depth % K]) // 2

        for i in range(K):
            for point in points[i]:
                # print(point, points[depth % K][median])
                if point[depth % K] < points[depth % K][median][depth % K]:
                    p1[i].append(point)
                else:
                    p2[i].append(point)
        # return None

        # tutaj do zmiany, żeby działało dla K > 2
        min_x, max_x, min_y, max_y = rectangle.get_extrema()
        vl, vr = None, None
        if depth % K == 0:
            val = points[depth % K][median][0]
            self.vis.add_line_segment(((val, min_y), (val, max_y)))

            vl = self.build_tree(p1, depth + 1, Rectangle(min_x, val, min_y, max_y))
            vr = self.build_tree(p2, depth + 1, Rectangle(val, max_x, min_y, max_y))
        else:
            val = points[depth % K][median][1]
            self.vis.add_line_segment(((min_x, val), (max_x, val)))

            vl = self.build_tree(p1, depth + 1, Rectangle(min_x, max_x, min_y, val))
            vr = self.build_tree(p2, depth + 1, Rectangle(min_x, max_x, val, max_y))

        v = Node(depth % K, points[depth % K][median], rectangle)
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


    def points_from_rectangle(self, rectangle: Rectangle):
        min_x, max_x, min_y, max_y = rectangle.get_extrema()
        return (min_x, min_y), (max_x, min_y), (max_x, max_y), (min_x, max_y)

    def __find(self, node: Node, rectangle: Rectangle, res: list[Point]):
        if rectangle & node.rectangle is None:
            return
        if len(node.leafs) == 0:
            if node.leaf_point is not None and node.leaf_point in rectangle:
                self.vis.add_point(node.leaf_point, s=10, color="red")
                res.append(node.leaf_point)
            return
        for leaf_node in node.leafs:
            self.__find(leaf_node, rectangle, res)

    def find(self, rectangle: Rectangle) -> list[Point]:

        self.vis.add_polygon(self.points_from_rectangle(rectangle), alpha=0.5, color="red")
        res = []
        self.__find(self.root, rectangle, res)
        return res

