from __future__ import annotations
from collections import deque
from bitalg.visualizer.main import Visualizer
from quadtree import Quadtree, _Node
from geometry import Point, Rectangle


class QuadtreeVisualization(Quadtree):
    def __init__(self, points: list[Point]):
        super().__init__(points)
        self.vis = Visualizer()
        self.vis.add_point(points, color='black', s=10)

    def find(self, rectangle: Rectangle) -> list[Point]:
        self.vis.add_polygon([(rectangle.min_x, rectangle.min_y), (rectangle.max_x, rectangle.min_y),
                              (rectangle.max_x, rectangle.max_y), (rectangle.min_x, rectangle.max_y)],
                             color='red', alpha=0.3)
        res = super().find(rectangle)
        self.vis.add_point(res, color='red', s=15)
        return res

    def add_rectangles(self, nodes: list[_Node]):
        nodes = list(filter(lambda x: x is not None, nodes))
        segments = []
        for node in nodes:
            rectangle = Rectangle(node.min_x, node.max_x, node.min_y, node.max_y)
            segments += [((rectangle.min_x, rectangle.min_y), (rectangle.max_x, rectangle.min_y)),
                         ((rectangle.max_x, rectangle.min_y), (rectangle.max_x, rectangle.max_y)),
                         ((rectangle.max_x, rectangle.max_y), (rectangle.min_x, rectangle.max_y)),
                         ((rectangle.min_x, rectangle.max_y), (rectangle.min_x, rectangle.min_y))]
        self.vis.add_line_segment(segments, color='black')

    def add_grid(self):
        q = deque()
        q.append((self.root, 0))
        current_level = 0
        nodes = []
        while len(q):
            node, level = q.popleft()
            if level > current_level:
                current_level = level
                self.add_rectangles(nodes)
                nodes = []
            nodes.append(node)
            if node.children:
                for child in node.children:
                    q.append((child, level + 1))
        self.add_rectangles(nodes)
