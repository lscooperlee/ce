
import curses
from curses import ascii
from .mode import Mode
from . import cmdlineMode


class NormalMode(Mode):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
