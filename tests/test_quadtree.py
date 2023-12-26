import unittest
from numpy.random import seed, uniform
from quadtree import Quadtree
from geometry import Rectangle


class QuadtreeTest(unittest.TestCase):
    def test_construction(self):
        points = [(0, 0), (0, 1), (1, 1), (1, 0)]
        try:
            Quadtree(points)
        except Exception as e:
            self.fail(f'Quadtree constructor raised "{e}"')

    def test_find_trivial(self):
        points = [(0, 0), (0, 1), (1, 1), (1, 0)]
        tree = Quadtree(points)
        rectangle = Rectangle(0, 0.2, 0.8, 1e18)
        self.assertEqual([(0, 1)], tree.find(rectangle))

    def test_find_random_small_rect(self):
        points = list(zip(uniform(-1, 1, 5000),
                          uniform(-1, 1, 5000)))
        tree = Quadtree(points)

        for _ in range(100):
            xs = uniform(-1, 1, 2)
            ys = uniform(-1, 1, 2)
            rectangle = Rectangle(min(xs), max(xs), min(ys), max(ys))
            self.assertEqual(set(filter(lambda p: p in rectangle, points)), set(tree.find(rectangle)))

    def test_find_random_normal_rect(self):
        points = list(zip(uniform(-1000, 1000, 5000),
                          uniform(-1000, 1000, 5000)))
        tree = Quadtree(points)

        for _ in range(100):
            xs = uniform(-1000, 1000, 2)
            ys = uniform(-1000, 1000, 2)
            rectangle = Rectangle(min(xs), max(xs), min(ys), max(ys))
            self.assertEqual(set(filter(lambda p: p in rectangle, points)), set(tree.find(rectangle)))

    def test_find_random_huge_rect(self):
        points = list(zip(uniform(-1e18, 1e18, 5000),
                          uniform(-1e18, 1e18, 5000)))
        tree = Quadtree(points)

        for _ in range(100):
            xs = uniform(-1e18, 1e18, 2)
            ys = uniform(-1e18, 1e18, 2)
            rectangle = Rectangle(min(xs), max(xs), min(ys), max(ys))
            self.assertEqual(set(filter(lambda p: p in rectangle, points)), set(tree.find(rectangle)))

    def test_find_two_identical_points(self):
        points = [(0, 0), (0, 1), (1, 0), (0, 0)]
        tree = Quadtree(points)
        rectangle = Rectangle(-0.1, 0.1, -1, 0.9)
        self.assertEqual([(0, 0)], tree.find(rectangle))


if __name__ == '__main__':
    seed(0)
    unittest.main()
