import curses
from curses.textpad import Textbox, rectangle

class CursesScreen:

    def __init__(self, windows={}):
        self.windows = dict(windows)
        self.stdscr = curses.initscr()

    def __enter__(self):

        curses.start_color()
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE)

        curses.noecho()
        curses.cbreak()
        curses.nl()

        self.init()

        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.stdscr.keypad(False)
        curses.nocbreak()
        curses.echo()
        curses.endwin()

    def init(self):
        for win in self.windows.values():
            win.init()
        curses.doupdate()

    def add_window(self, window, name):
        self.windows[name] = window
        self.init()


