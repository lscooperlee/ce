import unittest

from core.ui.screen import CursesScreen

class TestMode(unittest.TestCase):

    def test_index(self):
        with CursesScreen('abcde\nfg\n\n\nh') as screen:
            self.assertEqual(screen.index(0, 0), 0)
            self.assertEqual(screen.index(0, 1), 1)
            self.assertEqual(screen.index(1, 0), 6)
            self.assertEqual(screen.index(4, 0), 11)


if __name__ == "__main__":
    unittest.main()
