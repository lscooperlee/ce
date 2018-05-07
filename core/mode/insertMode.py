
import curses
from curses import ascii
from .mode import Mode
from .normalMode import NormalMode

class InsertMode(Mode):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.windows['main'].keypad(True)

def insertMode_up(self, key):
    y, x = self.windows['main'].getyx()
    y = y-1 if y > 0 else 0
    x = len(self.buffer.row(y)) - 1 if x > len(self.buffer.row(y)) - 1 else x
    self.windows['main'].move(y, x)
InsertMode.key_map[curses.KEY_UP] = insertMode_up

def insertMode_down(self, key):
    y, x = self.windows['main'].getyx()
    y = y+1 if y < len(self.buffer.indexes) - 2 else y
    x = len(self.buffer.row(y)) - 1 if x > len(self.buffer.row(y)) - 1 else x
    self.windows['main'].move(y, x)
InsertMode.key_map[curses.KEY_DOWN] = insertMode_down

def insertMode_left(self, key):
    y, x = self.windows['main'].getyx()
    x = x-1 if x > 0 else 0
    self.windows['main'].move(y, x)
InsertMode.key_map[curses.KEY_LEFT] = insertMode_left

def insertMode_right(self, key):
    y, x = self.windows['main'].getyx()
    x = x+1 if x <= len(self.buffer.row(y)) - 1 else x
    x = x-1 if self.buffer.row(y)[x-1] == '\n' else x
    self.windows['main'].move(y, x)
InsertMode.key_map[curses.KEY_RIGHT] = insertMode_right

def insertMode_backspace(self, key):
    y, x = self.windows['main'].getyx()
    if y == 0 and x == 0:
        return
    y, x = adjust_cursor1(self, y, x-1)
    self.buffer.delete(x, y)
    self.windows['main'].addstr(y, x, self.buffer.str(x, y))
    self.windows['main'].clrtobot()
    self.windows['main'].move(y, x)
InsertMode.key_map[curses.KEY_BACKSPACE] = insertMode_backspace
