
import curses
from curses import ascii

class InsertMode:

    def __init__(self):
        self.text = [[]]
        self.key_map = {"*": lambda s, c: None}

    def run(self, windows):
        self.windows = windows
        self.windows['main'].keypad(True)
    #    while True:
        if True:
            char = self.windows['main'].getch()
            try:
                self.key_map[char](self, char)
            except KeyError:
                self.key_map["*"](self, char)

        return self

insert_mode = InsertMode()

def insert_default(self, key):
    if ascii.isprint(key):
        y, x = self.windows['main'].getyx()
        self.text[y].insert(x, chr(key))
        self.windows['main'].echochar(key)
insert_mode.key_map["*"] = insert_default

def insert_esc(self, key):
    print(self.text)
insert_mode.key_map[27] = insert_esc #ESC

def insert_enter(self, key):
    y, x = self.windows['main'].getyx()

    thisline = self.text[y][:x] + ['\n']
    nextline = self.text[y][x:]
    self.text[y] = thisline
    self.text.insert(y+1, nextline)

    for i in range(y, len(self.text)):
    #    self.windows['main'].clrtoeol()
        self.windows['main'].addstr(i, 0, ''.join(self.text[i]))

    self.windows['main'].move(y+1, 0)

insert_mode.key_map[10] = insert_enter #Enter

def adjust_cursor(self, y, x):
    if y < 0:
        y = 0

    if y >= len(self.text):
        y = len(self.text) - 1

    if x >= len(self.text[y]):
        x = len(self.text[y]) - 1
        if y == len(self.text) - 1:
            x = len(self.text[y])

    if x < 0:
        x = 0

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
    y, x = adjust_cursor(self, y, x-1)

    try:
        self.text[y].pop(x)
    except IndexError:
        pass
    self.windows['main'].delch(y, x)
    self.windows['main'].move(y, x)

insert_mode.key_map[curses.KEY_BACKSPACE] = insert_backspace



class CommandMode:

    def __init__(self):
        self.key_map = {"*": lambda s, c: None}

    def run(self, windows):
        self.windows = windows
        self.windows['main'].keypad(True)
        while True:
            char = self.windows['main'].getch()
            try:
                self.key_map[char](self, char)
            except KeyError:
                self.key_map["*"](self, char)

command_mode = CommandMode()
