import curses

class CursesScreen:

    def __init__(self, text=''):
        self.windows = {}
        self.stdscr = curses.initscr()
        self.text = text
        rows = text.split('\n')
        self.rows = rows[:-1] if rows[-1] == '' else rows

    def __enter__(self):

        curses.start_color()
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE)

        curses.noecho()
        curses.cbreak()
        curses.nl()

        head_x = 0
        head_y = 0
        head_height = 1
        head_width = curses.COLS - 1
        head_win = curses.newwin(head_height, head_width, head_y, head_x)

        main_x = 0
        main_y = 1
        main_height = curses.LINES - 3
        main_width = curses.COLS - 1
        main_win = curses.newwin(main_height, main_width, main_y, main_x)
        main_win.insstr(self.text)
        main_win.move(0, 0)

        status_x = 0
        status_y = curses.LINES - 2
        status_height = 1
        status_width = curses.COLS - 1
        status_win = curses.newwin(status_height, status_width, status_y, status_x)

        bottom_x = 0
        bottom_y = curses.LINES - 1
        bottom_height = 1
        bottom_width = curses.COLS - 1
        bottom_win = curses.newwin(bottom_height, bottom_width, bottom_y, bottom_x)

        head_win.chgat(curses.color_pair(1))
        head_win.insstr("main", curses.color_pair(1))

        status_win.chgat(curses.color_pair(1))

        head_win.refresh()
        main_win.refresh()
        status_win.refresh()
        bottom_win.refresh()

        self.windows = {
                    "main": main_win,
                    "head": head_win,
                    "status": status_win,
                    "bottom": bottom_win,
                    }

        return self

    def __exit__(self, exc_type, exc_value, traceback):

        curses.nocbreak()
        self.stdscr.keypad(False)
        curses.echo()
        curses.endwin()
        print(self.rows)

    def move_left(self):
        y, x = self.windows['main'].getyx()
        x = 0 if x == 0 else x-1
        self.windows['main'].move(y,x)

    def move_right(self):
        y, x = self.windows['main'].getyx()
        x = x+1 if x < len(self.rows[y])-1 else x
        self.windows['main'].move(y,x)

    def move_up(self):
        y, x = self.windows['main'].getyx()
        y = 0 if y == 0 else y-1
        x = x if x < len(self.rows[y])-1 else len(self.rows[y])-1
        x = x if x > 0 else 0
        self.windows['main'].move(y,x)

    def move_down(self):
        y, x = self.windows['main'].getyx()
        y = len(self.rows)-1 if y == len(self.rows)-1 else y+1
        x = x if x < len(self.rows[y])-1 else len(self.rows[y])-1
        x = x if x > 0 else 0
        self.windows['main'].move(y,x)

    def ins_char(self, char):
        if curses.ascii.isprint(char):
            y, x = self.windows['main'].getyx()
            self.windows['main'].insch(char)
            self.rows[y] = self.rows[y][:x] + chr(char) + self.rows[y][x:]
            self.windows['main'].move(y, x+1)
            self.windows['main'].refresh()

    def ins_enter(self, char):
        self.windows['main'].insch(char)
        y, x = self.windows['main'].getyx()
        newlinestr = self.rows[y][x:]
        self.rows[y] = self.rows[y][:x]
        self.rows.insert(y+1, newlinestr)
        self.windows['main'].move(y+1, 0)
        self.windows['main'].insertln()
        self.windows['main'].insstr(newlinestr)
        self.windows['main'].refresh()
