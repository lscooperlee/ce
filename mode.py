
import curses
from curses import ascii
import os

class InsertMode:

    def __init__(self, window):
        self.window = window
        self.window.keypad(True)
        self.curline = 0
        self.text = [[]]

    def _move_cursor(self, rel_y=0, rel_x=0, newline=False):
        y, x = self.window.getyx()
        if newline is True:
            self.window.move(y+1, 0)
        else:
            if y + rel_y >= 0 and y + rel_y < len(self.text):
                y = y + rel_y
            if x + rel_x >= 0 and x + rel_x < len(self.text[y]):
                x = x + rel_x
            self.window.move(y, x)

    def run(self):
        while True:
            char = self.window.getch()
#            print(char)

            if ascii.isprint(char):
                self.text[self.curline].append(char)
                self.window.echochar(char)
            else:
                if char == 27: # ESC
                    print(self.text)
                elif char == 10: #or curses.KEY_ENTER: #Enter as new line
                    self.text[self.curline].append('\n')
                    self.curline = self.curline + 1
                    self.text.append([])
                    self._move_cursor(newline=True)
                elif char == curses.KEY_RIGHT:
                    self._move_cursor(0, 1)
                elif char == curses.KEY_LEFT:
                    self._move_cursor(0, -1)
                elif char == curses.KEY_UP:
                    self._move_cursor(-1, 0)
                elif char == curses.KEY_DOWN:
                    self._move_cursor(1, 0)
                elif char == curses.KEY_BACKSPACE:
                    self.window.echochar(char)
