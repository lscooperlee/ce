
import curses
from curses import ascii
from .mode import Mode
from .normalMode import NormalMode

class InsertMode(Mode):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ui.windows['main'].keypad(True)

