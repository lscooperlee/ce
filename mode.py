
import curses
from curses import ascii
import os

class InsertMode:

    def __init__(self, window):
        self.window = window

    def run(self):
        print(ascii.BS)
        print(curses.KEY_BACKSPACE)
        print(os.environ['TERM'])

        while True:
            #c = self.window.getkey()
            c = self.window.getch()
            if ascii.isprint(c):
                self.window.echochar(c)
            else:
                print('iii')
                print(c)
