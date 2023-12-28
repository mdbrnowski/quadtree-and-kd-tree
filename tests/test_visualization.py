import unittest
from geometry import Rectangle
from quadtree_visualization import QuadtreeVisualization


class QuadtreeVisualizationTest(unittest.TestCase):
    def test_visualization(self):
        points = [(0, 0), (0, 1), (1, 1), (1, 0)]
        rectangle = Rectangle(0, 0.2, 0.8, 1)
        try:
            tree = QuadtreeVisualization(points)
            tree.add_grid()
            tree.find(rectangle)
        except Exception as e:
            self.fail(f'Quadtree visualization raised "{e}"')


if __name__ == '__main__':
    unittest.main()
