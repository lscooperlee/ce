
import curses
from curses import ascii
from .mode import Mode
from . import cmdlineMode


class NormalMode(Mode):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

def NormalMode_colon(self, key):
    return cmdlineMode.CmdlineMode(self.buffer, self.windows)
NormalMode.key_map[ord(':')] = NormalMode_colon

def NormalMode_colon(self, key):
    return cmdlineMode.CmdlineMode(self.buffer, self.windows)
NormalMode.key_map[ord(':')] = NormalMode_colon
