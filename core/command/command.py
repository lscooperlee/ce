
import curses
from curses import ascii
from ..mode import InsertMode, NormalMode, CmdlineMode


@NormalMode.register(ord(':'))
def NormalMode_colon(mode, key):
    return CmdlineMode(mode.buffer, mode.windows)

@NormalMode.register(ord('i'))
def NormalMode_colon(mode, key):
    return InsertMode(mode.buffer, mode.windows)

@NormalMode.register(ord('l'))
def NormalMode_colon(mode, key):
    y, x = mode.windows['main'].getyx()
    x = x+1 if x < len(mode.buffer.row(y)) - 1 else x
    x = x-1 if mode.buffer.row(y)[x] == '\n' else x
    mode.windows['main'].move(y, x)

@NormalMode.register(ord('h'))
def NormalMode_colon(mode, key):
    y, x = mode.windows['main'].getyx()
    x = x-1 if x > 0 else x
    mode.windows['main'].move(y, x)

@NormalMode.register(ord('j'))
def NormalMode_colon(mode, key):
    y, x = mode.windows['main'].getyx()
    y = y+1 if y < len(mode.buffer.indexes) - 2 else y
    x = len(mode.buffer.row(y)) - 1 if x > len(mode.buffer.row(y)) - 1 else x
    x = x-1 if mode.buffer.row(y)[x] == '\n' else x
    mode.windows['main'].move(y, x)

@NormalMode.register(ord('k'))
def NormalMode_colon(mode, key):
    y, x = mode.windows['main'].getyx()
    y = y-1 if y > 0 else y
    x = len(mode.buffer.row(y)) - 1 if x > len(mode.buffer.row(y)) - 1 else x
    x = x-1 if mode.buffer.row(y)[x] == '\n' else x
    mode.windows['main'].move(y, x)

@NormalMode.register(ord('h'))
def NormalMode_colon(mode, key):
    y, x = mode.windows['main'].getyx()
    x = x-1 if x > 0 else x
    mode.windows['main'].move(y, x)

@CmdlineMode.cmd_register('w')
def command_save(mode, filename=None):
    if not filename:
        filename = mode.buffer.name

    with open(filename, 'w') as fd:
        fd.write(mode.buffer.str())

@CmdlineMode.cmd_register('q')
def command_quit(mode, filename=None):
    quit()

@CmdlineMode.register("*")
def cmdlineMode_default(mode, key):
    if ascii.isprint(key):
        y, x = mode.windows['bottom'].getyx()
        mode.cmd.insert(x-1, chr(key))
        mode.windows['bottom'].insch(key)
        mode.windows['bottom'].move(y, x+1)
        mode.windows['bottom'].refresh()

@CmdlineMode.register(curses.KEY_LEFT)
def cmdlineMode_left(mode, key):
    y, x = mode.windows['bottom'].getyx()
    x = x if x == 1 else x - 1
    mode.windows['bottom'].move(y, x)
    mode.windows['bottom'].refresh()

@CmdlineMode.register(curses.KEY_RIGHT)
def cmdlineMode_right(mode, key):
    y, x = mode.windows['bottom'].getyx()
    x = x if x == len(mode.cmd) + 1 else x + 1
    mode.windows['bottom'].move(y, x)
    mode.windows['bottom'].refresh()

@CmdlineMode.register(curses.KEY_BACKSPACE)
def cmdlineMode_backspace(mode, key):
    y, x = mode.windows['bottom'].getyx()
    if x == 1:
        return

    x -= 1
    mode.cmd.pop(x-1)
    mode.windows['bottom'].delch(y, x)
    mode.windows['bottom'].refresh()

@CmdlineMode.register(27)
def cmdlineMode_esc(mode, key):
    return NormalMode(mode.buffer, mode.windows)

@CmdlineMode.register(10)
def cmdlineMode_enter(mode, key):
    mode.windows['bottom'].move(0, 1)
    mode.windows['bottom'].clrtoeol()
    mode.windows['bottom'].refresh()
    params = ''.join(mode.cmd).split()
    cmdwithend, args = params[0] + ' ', params[1:]

    cmdlist = []
    while cmdwithend != ' ':
        for i in range(1, len(cmdwithend) + 1):
            if cmdwithend[:-i] in mode.actions:
                cmdlist.append(cmdwithend[:-i])
                cmdwithend = cmdwithend[-i:]
                break
        else:
            break

    if not cmdlist:
        mode.windows['bottom'].insstr("no command")
        mode.windows['bottom'].refresh()
    else:
        for cmd in cmdlist:
            mode.actions[cmd](mode, *args)

    return NormalMode(mode.buffer, mode.windows)


@InsertMode.register("*")
def insertMode_default(mode, key):
    if ascii.isprint(key):
        y, x = mode.windows['main'].getyx()
        mode.buffer.insert(x, y, chr(key))
        mode.windows['main'].insch(key)
        mode.windows['main'].move(y, x+1)
        mode.windows['main'].refresh()

@InsertMode.register(27) #ESC
def insertMode_esc(mode, key):
    y, x = mode.windows['main'].getyx()
    return NormalMode(mode.buffer, mode.windows)

@InsertMode.register(10) #Enter
def insertMode_enter(mode, key):
    y, x = mode.windows['main'].getyx()
    mode.buffer.insert(x, y, chr(key))

    mode.windows['main'].addstr(y, x, mode.buffer.str(x, y))
    mode.windows['main'].move(y+1, 0)

@InsertMode.register(curses.KEY_UP)
def insertMode_up(mode, key):
    y, x = mode.windows['main'].getyx()
    y = y-1 if y > 0 else 0
    x = len(mode.buffer.row(y)) - 1 if x > len(mode.buffer.row(y)) - 1 else x
    mode.windows['main'].move(y, x)

@InsertMode.register(curses.KEY_DOWN)
def insertMode_down(mode, key):
    y, x = mode.windows['main'].getyx()
    y = y+1 if y < len(mode.buffer.indexes) - 2 else y
    x = len(mode.buffer.row(y)) - 1 if x > len(mode.buffer.row(y)) - 1 else x
    mode.windows['main'].move(y, x)

@InsertMode.register(curses.KEY_LEFT)
def insertMode_left(mode, key):
    y, x = mode.windows['main'].getyx()
    x = x-1 if x > 0 else 0
    mode.windows['main'].move(y, x)

@InsertMode.register(curses.KEY_RIGHT)
def insertMode_right(mode, key):
    y, x = mode.windows['main'].getyx()
    x = x+1 if x <= len(mode.buffer.row(y)) - 1 else x
    x = x-1 if mode.buffer.row(y)[x-1] == '\n' else x
    mode.windows['main'].move(y, x)

@InsertMode.register(curses.KEY_BACKSPACE)
def insertMode_backspace(mode, key):
    y, x = mode.windows['main'].getyx()
    if y == 0 and x == 0:
        return
    y, x = adjust_cursor1(mode, y, x-1)
    mode.buffer.delete(x, y)
    mode.windows['main'].addstr(y, x, mode.buffer.str(x, y))
    mode.windows['main'].clrtobot()
    mode.windows['main'].move(y, x)
