import curses
from curses.textpad import Textbox, rectangle

class CursesWindow:

    def __init__(self, y, x, height, width, text='', color=None):
        self.y = y
        self.x = x
        self.height = height
        self.width = width
        #main_height = curses.LINES - 3
        #main_width = curses.COLS - 1
        self.cursor = (0, 0)
        #self.rows = text.splitlines(keepends=True) if \
        #    len(text.splitlines(keepends=True)) else ['']
        self.rows = text.splitlines() if len(text.splitlines()) else ['']
        self.yx2actual = {}
        self.actual2yx = {}
        self.scroll_line = 0

    def _insrow(self, y, rowstr):
        ay, an = self.yx2actual[y]
        #print(ay, an, self.yx2actual, file=open('/tmp/log', 'a+'))

        for n in range(an):
            if ay+an >= self.height:
                break
            nthstr = rowstr[self.width*n:(n+1)*self.width]
            #print(nthstr, ay, n, file=open('/tmp/log', 'a+'))
            self.window.move(ay+n, 0)
            self.window.deleteln()
            self.window.insstr(ay+n, 0, nthstr.strip())

        self.window.refresh()

    def _yx2actual(self, y, x):
        ay, an = self.yx2actual[y]
        return -self.scroll_line + ay + x // self.width, x % self.width

    def _isscroll(self, y, x):
        if y >= self.height:
            return y - self.height + 1
        return 0

    def move(self, y, x):
        y = 0 if y < 0 else y
        y = len(self.rows) - 1 if y > len(self.rows) - 1 else y

        x = len(self.rows[y]) - 1 if x > len(self.rows[y]) - 1 else x
        x = 0 if x < 0 else x

        ay, ax = self._yx2actual(y, x)
#        print(self._isscroll(ay, ax), ay, ax, file=open('/tmp/log', 'a+'))
        self.window.move(ay, ax)
        self.window.refresh()
        return ay, ax

    def scroll(self, line):
        actual_line = self._yx2actual[self.scroll_line][1]
        self.scroll_line += line
        self.window.scroll(actual_line)
        #self._insrow(4, 'abc')
        self.window.insstr(4, 0, 'abc')
        #try:
        #    self._insrow(self.height-line-1, self.rows[self.scroll_line+self.height-1])
        #except:
        #    pass
        self.window.refresh()
        return 0, 0

    def init(self):
        self.window = curses.newwin(self.height, self.width, self.y, self.x)
        self.window.scrollok(True)
        self.window.idlok(True)

        self.window.move(*self.cursor)
        self.update_ref()
        for n, row in enumerate(self.rows):
            self._insrow(n, row)

        #self.window.chgat(curses.color_pair(1))
        #self.window.border()
        #self.window.noutrefresh()

        #self.window.scroll()
        self.window.refresh()

    def insrow(self, y, x=0, newstr=''):
        try:
            self.rows[y] = self.rows[y][:x] + newstr + self.rows[y][x:]
        except:
            self.rows[y] = self.rows[y] + newstr

        self._insrow(y, self.rows[y])
        self.update_ref()


    def update_ref(self):
        start = 0
        for c, e in enumerate(self.rows):
            yxrange = 1 if len(e) == 0 else (len(e) - 1)//self.width + 1
            self.yx2actual[c] = [start, yxrange]

            for n in range(yxrange):
                self.actual2yx[start + n] = [start, n]

            start += yxrange
