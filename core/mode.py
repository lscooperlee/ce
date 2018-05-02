
import curses
from curses import ascii

class InsertMode:

    def __init__(self):
        self.text = []
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

def yx2idx(self, y, x):
    try:
        idx = [i for i, n in enumerate(self.text) if n == '\n'][y-1] + x + 1
    except:
        idx = x
    return idx

def insert_default(self, key):
    if ascii.isprint(key):
        y, x = self.windows['main'].getyx()
        idx = yx2idx(self, y, x)
        self.text.insert(idx, chr(key))
        self.windows['main'].echochar(key)
insert_mode.key_map["*"] = insert_default

def insert_esc(self, key):
    print(self.text)
insert_mode.key_map[27] = insert_esc #ESC

def flatten_text(self, y, x):
    idx = 0
    for t in self.text[:y]:
        idx += len(t)
    idx += x

    tmp = []
    for t in self.text:
        tmp+=t
    return tmp, idx - 1

def deflatten_text(self, flattened, index):
    tmp = [[]]
    y, x = 0, 0
    for t in flattened:
        if t == '\n':
            tmp.append([])
        tmp[len(tmp) - 1].append(t)

def insert_enter(self, key):
    y, x = self.windows['main'].getyx()
    idx = yx2idx(self, y, x)
    self.text.insert(idx, chr(key))

    self.windows['main'].addstr(y+1, 0, ''.join(self.text[idx:]))

    self.windows['main'].move(y+1, 0)

insert_mode.key_map[10] = insert_enter #Enter

def adjust_cursor(self, y, x):
    retidx = [0]+[i for i, n in enumerate(self.text) if n == '\n']

    maxy = len(retidx)

    if y < 0:
        y = 0

    if y >= maxy:
        y = maxy - 1

    try:
        textx = self.text[retidx[y]:retidx[y+1]]
        maxx = len(textx) - 1
    except:
        textx = self.text[retidx[y]:]
        maxx = len(textx)

    #print(textx, y, x, retidx)

    if x >= maxx:
        x = maxx - 1

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
    flattend, idx = flatten_text(self, y, x)
    if y == 0 and x == 0:
        return
    elif x == 0:
        y, x = adjust_cursor(self, y-1, 1000)
    else:
        y, x = adjust_cursor(self, y, x-1)

    #self.text[y].pop(x)
    try:
        flattend.pop(idx)
    except IndexError:
        pass
    self.text = [[y for y in x] + ['\n'] for x in ''.join(flattend).split('\n')]
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
