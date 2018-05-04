
import curses
from curses import ascii
from ..buffer import Buffer

class ModeMeta(type):
    def __init__(cls, name, bases, nmspc):
        super().__init__(name, bases, nmspc)
        cls.key_map = {"*": lambda s, c: None}

class Mode(metaclass=ModeMeta):

    def __init__(self, buffer, windows):
        self.buffer = buffer
        self.windows = windows

    def run(self):
        char = self.windows['main'].getch()
        try:
            mode = self.key_map[char](self, char)
        except KeyError:
            mode = self.key_map["*"](self, char)

        return self if mode is None else mode
