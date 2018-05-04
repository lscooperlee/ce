
import curses
from curses import ascii
from .buffer import Buffer

class InsertMode:

    def __init__(self):
        self.buffer = Buffer()
        self.key_map = {"*": lambda s, c: None}

    def run(self, windows):
        self.windows = windows
        self.windows['main'].keypad(True)

        char = self.windows['main'].getch()
        try:
            mode = self.key_map[char](self, char)
        except KeyError:
            mode = self.key_map["*"](self, char)

        return self if mode is None else mode

insert_mode = InsertMode()

def insert_default(self, key):
    if ascii.isprint(key):
        y, x = self.windows['main'].getyx()
        self.buffer.insert(x, y, chr(key))
        self.windows['main'].echochar(key)
insert_mode.key_map["*"] = insert_default

def insert_esc(self, key):
#    self.windows['bottom'].insstr(self.buffer.str())
#    self.windows['bottom'].refresh()
#    #print(self.buffer.str())
    return CommandMode()
insert_mode.key_map[27] = insert_esc #ESC

def insert_enter(self, key):
    y, x = self.windows['main'].getyx()
    self.buffer.insert(x, y, chr(key))

    self.windows['main'].addstr(y, x, self.buffer.str(x, y))
    self.windows['main'].move(y+1, 0)

insert_mode.key_map[10] = insert_enter #Enter

def adjust_cursor(self, y, x):
    maxy = len(self.buffer.indexes) - 1

    if y < 0:
        y = 0

    if y >= maxy:
        y = maxy - 1

    maxx = len(self.buffer.row(y)) + 1
    if x >= maxx:
        x = maxx - 1

    if x < 0:
        x = 0

    return y, x

def adjust_cursor1(self, y, x):

    maxx = len(self.buffer.row(y)) + 1
    if x >= maxx:
        y += 1
        x = 0

    if x < 0:
        y -= 1
        x = len(self.buffer.row(y)) - 1

    maxy = len(self.buffer.indexes) - 1

    if y < 0:
        y = 0

    if y >= maxy:
        y = maxy - 1

    return y, x

def insert_up(self, key):
    y, x = self.windows['main'].getyx()
    y, x = adjust_cursor(self, y-1, x)
    self.windows['main'].move(y, x)
insert_mode.key_map[curses.KEY_UP] = insert_up

def insert_down(self, key):
    y, x = self.windows['main'].getyx()
    y, x = adjust_cursor(self, y+1, x)
    self.windows['main'].move(y, x)
insert_mode.key_map[curses.KEY_DOWN] = insert_down

def insert_left(self, key):
    y, x = self.windows['main'].getyx()
    y, x = adjust_cursor(self, y, x-1)
    self.windows['main'].move(y, x)
insert_mode.key_map[curses.KEY_LEFT] = insert_left

def insert_right(self, key):
    y, x = self.windows['main'].getyx()
    y, x = adjust_cursor(self, y, x+1)
    self.windows['main'].move(y, x)
insert_mode.key_map[curses.KEY_RIGHT] = insert_right

def insert_backspace(self, key):
    y, x = self.windows['main'].getyx()
    if y == 0 and x == 0:
        return
    y, x = adjust_cursor1(self, y, x-1)
    self.buffer.delete(x, y)
    self.windows['main'].addstr(y, x, self.buffer.str(x, y))
    self.windows['main'].clrtobot()
    self.windows['main'].move(y, x)
insert_mode.key_map[curses.KEY_BACKSPACE] = insert_backspace

class CommandMode:

    def __init__(self):
        self.key_map = {"*": lambda s, c: None}

    def run(self, windows):
        self.windows = windows
        self.windows['main'].keypad(True)

        char = self.windows['main'].getch()
        try:
            mode = self.key_map[char](self, char)
        except KeyError:
            mode = self.key_map["*"](self, char)

        return self if mode is None else mode

command_mode = CommandMode()
