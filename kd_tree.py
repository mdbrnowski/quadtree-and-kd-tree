from __future__ import annotations
from operator import itemgetter
from geometry import Rectangle
from tree import Tree
from random import randint

K = 2
Point = tuple(float() for _ in range(K))


class _Node:
    def __init__(self, dim: int | None, line: float | None, rectangle: Rectangle):
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
        super().__init__(points)

        self.max_rectangle = Rectangle(
            min(points, key=itemgetter(0))[0],
            max(points, key=itemgetter(0))[0],
            min(points, key=itemgetter(1))[1],
            max(points, key=itemgetter(1))[1]
        )

        self.root = self.build_tree(self.points, 0, self.max_rectangle)

    def build_tree(self, points: list[Point], depth: int, rectangle: Rectangle) -> _Node:
        if len(points) == 1:
            node = _Node(None, None, rectangle)
            node.leaf_point = points[0]
            return node

        p1 = []
        p2 = []
        median_point = self.quick_select(points, 0, len(points) - 1, (len(points) - 1) // 2, depth % K)
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
            vl = self.build_tree(p1, depth + 1, Rectangle(min_x, median, min_y, max_y))
            vr = self.build_tree(p2, depth + 1, Rectangle(median, max_x, min_y, max_y))
        else:
            vl = self.build_tree(p1, depth + 1, Rectangle(min_x, max_x, min_y, median))
            vr = self.build_tree(p2, depth + 1, Rectangle(min_x, max_x, median, max_y))

        v = _Node(depth % K, median_point, rectangle)
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

    def partition(self, points, l, r, depth) -> int:
        pivot = points[r][depth % K]
        i = l - 1
        for j in range(l, r):
            if points[j][depth % K] < pivot:
                i += 1
                points[j], points[i] = points[i], points[j]
        i += 1
        points[i], points[r] = points[r], points[i]
        return i

    def rand_partition(self, points, l, r, depth) -> int:
        rand_num = randint(l, r)
        points[rand_num], points[r] = points[r], points[rand_num]
        return self.partition(points, l, r, depth)

    def quick_select(self, points, l, r, k, depth) -> Point:
        pivot = self.rand_partition(points, l, r, depth)
        if pivot == k:
            return points[pivot]
        if pivot > k:
            return self.quick_select(points, l, pivot - 1, k, depth)
        return self.quick_select(points, pivot + 1, r, k, depth)

    def __find(self, node: _Node, rectangle: Rectangle, res: list[Point]):
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
