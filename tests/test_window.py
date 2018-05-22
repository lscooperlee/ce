import unittest
import time

from core.ui.window import CursesWindow
from core.ui.screen import CursesScreen

class TestMode(unittest.TestCase):

    def test_update_ref(self):
        window = CursesWindow(0, 0, 10, 10,
                              '1\n'
                              '1234567890123\n'
                              '1234567890\n'
                              '12345678901234567890\n'
                              '123456789012345678\n')
        window.update_ref()

        expected_yx2actual = {0: [0, 1],
                              1: [1, 2],
                              2: [3, 1],
                              3: [4, 2],
                              4: [6, 2]}
        self.assertEqual(window.yx2actual, expected_yx2actual)
        expected_actual2yx = {0: [0, 0],
                              1: [1, 0],
                              2: [1, 1],
                              3: [3, 0],
                              4: [4, 0],
                              5: [4, 1],
                              6: [6, 0],
                              7: [6, 1]}
        self.assertEqual(window.actual2yx, expected_actual2yx)

    @unittest.skip
    def test_move(self):
        window = CursesWindow(0, 0, 10, 10,
                              '1\n'
                              '1234567890123\n'
                              '1234567890\n'
                              '1234567890abcdefghij\n'
                              '1234567890abcdefgh\n')
        window.update_ref()
        self.assertEqual(window._yx2actual(0, 0), (0, 0))
        self.assertEqual(window._yx2actual(0, 1), (0, 1))
        self.assertEqual(window._yx2actual(0, 12), (1, 2))
        self.assertEqual(window._yx2actual(1, 2), (1, 2))
        self.assertEqual(window._yx2actual(3, 15), (5, 5))
        self.assertEqual(window._yx2actual(4, 12), (7, 2))

        screen = CursesScreen({'main': window})

        with screen as s:
            win = s.windows['main']
            y, x = win.move(0, 0)
            time.sleep(1)
            self.assertEqual(win.window.inch(y, x), ord('1'))
            y, x = win.move(0, 1)
            time.sleep(1)
            self.assertEqual(win.window.inch(y, x), ord('1'))
            y, x = win.move(0, 12)
            time.sleep(1)
            self.assertEqual(win.window.inch(y, x), ord('1'))
            y, x = win.move(1, 2)
            time.sleep(1)
#            self.assertEqual(win.window.inch(y, x), ord('3'))
            y, x = win.move(3, 15)
            time.sleep(1)
#            self.assertEqual(win.window.inch(y, x), ord('f'))
            y, x = win.move(4, 12)
            time.sleep(1)
#            self.assertEqual(win.window.inch(y, x), ord('c'))

    @unittest.skip
    def test_scroll(self):
        window = CursesWindow(0, 0, 5, 10,
                              '1\n'
                              '1234567890123\n'
                              '1234567890\n'
                              '1234567890abcdefghij\n'
                              '1234567890abcdefgh\n')
        window.update_ref()
        self.assertEqual(window._yx2actual(0, 0), (0, 0))
        self.assertEqual(window._yx2actual(0, 1), (0, 1))
        self.assertEqual(window._yx2actual(0, 12), (1, 2))
        self.assertEqual(window._yx2actual(1, 2), (1, 2))
        self.assertEqual(window._yx2actual(3, 15), (5, 5))
        self.assertEqual(window._yx2actual(4, 12), (7, 2))

        screen = CursesScreen({'main': window})

        with screen as s:
            win = s.windows['main']
            time.sleep(1)
            y, x = win.scroll(0)
            time.sleep(1)
            y, x = win.scroll(1)
            time.sleep(1)
            return
            y, x = win.scroll(2)
            time.sleep(1)
            y, x = win.scroll(3)
            time.sleep(1)
            y, x = win.scroll(-4)
            time.sleep(1)
            y, x = win.scroll(-2)
            time.sleep(1)

    def test_insrow(self):
        window = CursesWindow(0, 0, 4, 10,
                              '1234\n1234567890123\n123456789012345678\n')
        screen = CursesScreen({'main': window})

        with screen as s:
            win = s.windows['main']
            time.sleep(1)
            win.insrow(1, 0, 'abcde')
            time.sleep(1)
            win.insrow(2, 5, 'abcde')
            time.sleep(1)


if __name__ == "__main__":
    unittest.main()
