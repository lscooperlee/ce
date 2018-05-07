
import curses

from contextlib import contextmanager

@contextmanager
def create_main_windows():

    try:
        stdscr = curses.initscr()
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

        yield {
                "head": head_win, "main": main_win,
                "status": status_win, "bottom": bottom_win
              }
    finally:

        curses.nocbreak()
        stdscr.keypad(False)
        curses.echo()
        curses.endwin()


