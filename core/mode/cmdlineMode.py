
import curses
from curses import ascii
from .mode import Mode
from . import normalMode


class CmdlineMode(Mode):

    actions = {}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ui.windows['bottom'].keypad(True)
        self.ui.windows['bottom'].insch(0, 0, ":")
        self.ui.windows['bottom'].move(0, 1)
        self.ui.windows['bottom'].clrtoeol()
        self.ui.windows['bottom'].refresh()
        self.cmd = []

    @classmethod
    def cmd_register(self, key):
        def _register(func):
            self.actions[key] = func
            return func
        return _register

