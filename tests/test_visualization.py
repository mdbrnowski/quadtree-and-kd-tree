import unittest
from geometry import Rectangle
from quadtree_visualization import QuadtreeVis
from kd_tree_visualization import KdTreeVis


class QuadtreeKdTreeVisualizationTest(unittest.TestCase):
    def test_visualization(self):
        points = [(0, 0), (0, 1), (1, 1), (1, 0)]
        rectangle = Rectangle(0, 0.2, 0.8, 1)
        try:
            tree = QuadtreeVis(points)
            tree.add_grid()
            tree.find(rectangle)
        except Exception as e:
            self.fail(f'Quadtree visualization raised "{e}"')
        try:
            tree = KdTreeVis(points)
            tree.find(rectangle)
        except Exception as e:
            self.fail(f'Kd tree visualization raised "{e}')


if __name__ == '__main__':
    unittest.main()
