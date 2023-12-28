from __future__ import annotations
from operator import itemgetter
from geometry import Rectangle
from tree import Tree


# todo: wiekszość kodu działa dla dowolnego K, ale trzeba by jeszcze zmodyfikować klasę Rectangle
K = 2
Point = tuple(float() for _ in range(K))

class Node:
    def __init__(self, dim : int, line : float, rectangle : Rectangle):
        self.dim = dim
        self.line = line
        self.rectangle = rectangle
        self.left = None
        self.right = None
        self.leafs = []
        self.leaf_point = None

    def __str__(self):
        return f'Node({repr(self.dim)}, {self.line}, {self.leaf_point})'


class KdTree(Tree):
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
        self.root = self.build_tree(self.sorted_points, 0, rectangle)

    def build_tree(self, points: list[list[Point]], depth: int, rectangle : Rectangle):
        if len(points[depth % K]) == 1:
            node = Node(None, None, rectangle)
            node.leaf_point = points[depth % K][0]
            return node

        if len(points[depth % K]) == 0:
            return None

        # todo: dodaj losowość, żeby zrównoważyć
        p1 = [[] for _ in range(K)]
        p2 = [[] for _ in range(K)]
        median = len(points[depth % K]) // 2

        for i in range(K):
            for point in points[i]:
                if point[depth % K] < points[depth % K][median][depth % K]:
                    p1[i].append(point)
                else:
                    p2[i].append(point)

        min_x, max_x, min_y, max_y = rectangle.get_extrema()
        if depth % K == 0:
            val = points[depth % K][median][0]
            vl = self.build_tree(p1, depth + 1, Rectangle(min_x, val, min_y, max_y))
            vr = self.build_tree(p2, depth + 1, Rectangle(val, max_x, min_y, max_y))
        else:
            val = points[depth % K][median][1]
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

    def __find(self, node : Node, rectangle : Rectangle, res : list[Point]):
        if rectangle & node.rectangle is None:
            return
        if len(node.leafs) == 0:
            if node.leaf_point is not None and node.leaf_point in rectangle:
                res.append(node.leaf_point)
            return
        for leaf_node in node.leafs:
            self.__find(leaf_node, rectangle, res)

    def find(self, rectangle: Rectangle) -> list[Point]:
        res = []
        self.__find(self.root, rectangle, res)
        return res

    def tree_print(self, node):
        if node is not None:
            print(node)
            self.tree_print(node.left)
            self.tree_print(node.right)
