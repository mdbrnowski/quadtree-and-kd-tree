import unittest
from geometry import Rectangle


class RectangleTest(unittest.TestCase):
    def test_correct_extrema(self):
        self.assertRaises(ValueError, Rectangle, 0, 1, 1, 0)
        self.assertRaises(ValueError, Rectangle, 0, -1, 1, 2)

    def test_equality(self):
        a = Rectangle(0, 1, 0, 1)
        b = Rectangle(0, 1, 0, 1)
        c = Rectangle(0, 1, 0, 2)

        self.assertTrue(a == b)
        self.assertFalse(a == c)

    def test_get_extrema(self):
        a = Rectangle(1, 2, 3, 4)
        self.assertEqual((1, 2, 3, 4), a.get_extrema())

    def test_and(self):
        a = Rectangle(0, 3, 0, 3)
        b = Rectangle(4, 7, 4, 7)
        c = Rectangle(2, 5, 2, 5)

        self.assertEqual(None, a & b)
        self.assertEqual(Rectangle(2, 3, 2, 3), a & c)
        self.assertEqual(Rectangle(4, 5, 4, 5), b & c)

    def test_contains_Rectangle(self):
        a = Rectangle(0, 1, 0, 1)
        b = Rectangle(0, 0.5, 0, 0.5)
        c = Rectangle(0.5, 2, 0.5, 2)
        d = Rectangle(0, 1, 0, 2)

        self.assertTrue(b in a)
        self.assertTrue(a not in b)
        self.assertTrue(a not in c)
        self.assertTrue(c not in a)
        self.assertTrue(a in d)
        self.assertTrue(d not in a)

    def test_contains_Point(self):
        a = Rectangle(0, 1, 0, 1)

        self.assertTrue((0.5, 0.5) in a)
        self.assertTrue((0, 0) in a)
        self.assertTrue((1, 1) in a)
        self.assertTrue((0, 2) not in a)
        self.assertTrue((2, 0) not in a)
        self.assertRaises(TypeError, a.__contains__, 1)


if __name__ == '__main__':
    unittest.main()
