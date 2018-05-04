
import curses
from curses import ascii
from .mode import Mode
from . import normalMode


class CmdlineMode(Mode):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.windows['bottom'].keypad(True)
        self.windows['bottom'].echochar(":")
        self.cmd = []


def cmdlineMode_default(self, key):
    if ascii.isprint(key):
        y, x = self.windows['bottom'].getyx()
        self.cmd.insert(x-1, chr(key))
        self.windows['bottom'].insch(key)
        self.windows['bottom'].move(y, x+1)
        self.windows['bottom'].refresh()
CmdlineMode.key_map["*"] = cmdlineMode_default

def cmdlineMode_left(self, key):
    y, x = self.windows['bottom'].getyx()
    x = x if x == 1 else x - 1
    self.windows['bottom'].move(y, x)
    self.windows['bottom'].refresh()
CmdlineMode.key_map[curses.KEY_LEFT] = cmdlineMode_left

def cmdlineMode_right(self, key):
    y, x = self.windows['bottom'].getyx()
    x = x if x == len(self.cmd) + 1 else x + 1
    self.windows['bottom'].move(y, x)
    self.windows['bottom'].refresh()
CmdlineMode.key_map[curses.KEY_RIGHT] = cmdlineMode_right

def cmdlineMode_backspace(self, key):
    y, x = self.windows['bottom'].getyx()
    if x == 1:
        return

    x -= 1
    self.cmd.pop(x-1)
    self.windows['bottom'].delch(y, x)
    self.windows['bottom'].refresh()
CmdlineMode.key_map[curses.KEY_BACKSPACE] = cmdlineMode_backspace

def cmdlineMode_enter(self, key):
    self.windows['main'].addstr(0, 0, ''.join(self.cmd))
CmdlineMode.key_map[10] = cmdlineMode_enter #Enter

def cmdlineMode_esc(self, key):
    return normalMode.NormalMode(self.buffer, self.windows)
CmdlineMode.key_map[27] = cmdlineMode_esc #ESC
