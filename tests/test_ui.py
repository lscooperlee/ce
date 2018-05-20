import unittest
import time

from core.ui.screen import CursesScreen
from core.ui.window import CursesWindow

class TestMode(unittest.TestCase):

    def test_constructor(self):
        main = CursesWindow(0, 0, 5, 10,
                              '1\n'
                              '1234567890abc\n'
                              '1234567890abcdefg\n'
                              '1234567890abcdefghijklmn\n')
        bottom = CursesWindow(5, 0, 1, 10, '##########')
        screen = CursesScreen({'main': main, 'bottom': bottom})

        with screen as s:
            time.sleep(100)

if __name__ == "__main__":
    unittest.main()
