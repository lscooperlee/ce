
import curses
from curses import ascii
from ..mode import InsertMode, NormalMode, CmdlineMode


@NormalMode.register(ord(':'))
def NormalMode_colon(mode, key):
    return CmdlineMode(mode.buffer, mode.ui)

@NormalMode.register(ord('i'))
def NormalMode_colon(mode, key):
    return InsertMode(mode.buffer, mode.ui)

@NormalMode.register(ord('a'))
def NormalMode_colon(mode, key):
    mode.ui.move_right(True)
    return InsertMode(mode.buffer, mode.ui)

@NormalMode.register(ord('l'))
def NormalMode_colon(mode, key):
    mode.ui.move_right()

@NormalMode.register(ord('h'))
def NormalMode_colon(mode, key):
    mode.ui.move_left()

@NormalMode.register(ord('j'))
def NormalMode_colon(mode, key):
    mode.ui.move_down()

@NormalMode.register(ord('k'))
def NormalMode_colon(mode, key):
    mode.ui.move_up()

@NormalMode.register(ord('h'))
def NormalMode_colon(mode, key):
    y, x = mode.ui.windows['main'].getyx()
    x = x-1 if x > 0 else x
    mode.ui.windows['main'].move(y, x)

@CmdlineMode.cmd_register('w')
def command_save(mode, filename=None):
    if not filename:
        filename = mode.buffer.name

    print(mode.buffer.text, end='')
    with open(filename, 'w') as fd:
        fd.write(mode.buffer.str())

@CmdlineMode.cmd_register('q')
def command_quit(mode, filename=None):
    quit()

@CmdlineMode.register("*")
def cmdlineMode_default(mode, key):
    if curses.ascii.isprint(key):
        index = mode.ui.bottom_char(key)
        mode.cmd.insert(index-1, chr(key))

@CmdlineMode.register(curses.KEY_LEFT)
def cmdlineMode_left(mode, key):
    y, x = mode.ui.windows['bottom'].getyx()
    x = x if x == 1 else x - 1
    mode.ui.windows['bottom'].move(y, x)
    mode.ui.windows['bottom'].refresh()

@CmdlineMode.register(curses.KEY_RIGHT)
def cmdlineMode_right(mode, key):
    y, x = mode.ui.windows['bottom'].getyx()
    x = x if x == len(mode.cmd) + 1 else x + 1
    mode.ui.windows['bottom'].move(y, x)
    mode.ui.windows['bottom'].refresh()

@CmdlineMode.register(curses.KEY_BACKSPACE)
def cmdlineMode_backspace(mode, key):
    y, x = mode.ui.windows['bottom'].getyx()
    if x == 1:
        return

    x -= 1
    mode.cmd.pop(x-1)
    mode.ui.windows['bottom'].delch(y, x)
    mode.ui.windows['bottom'].refresh()

@CmdlineMode.register(27)
def cmdlineMode_esc(mode, key):
    return NormalMode(mode.buffer, mode.ui.windows)

@CmdlineMode.register(10)
def cmdlineMode_enter(mode, key):
    mode.ui.windows['bottom'].move(0, 1)
    mode.ui.windows['bottom'].clrtoeol()
    mode.ui.windows['bottom'].refresh()
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
        mode.ui.windows['bottom'].insstr("no command")
        mode.ui.windows['bottom'].refresh()
    else:
        for cmd in cmdlist:
            mode.actions[cmd](mode, *args)

    return NormalMode(mode.buffer, mode.ui)


@InsertMode.register("*")
def insertMode_default(mode, key):
    if curses.ascii.isprint(key):
        index = mode.ui.ins_char(key)
        mode.buffer.insert(index, chr(key))

@InsertMode.register(27) #ESC
def insertMode_esc(mode, key):
    mode.ui.ins_esc(key)
    return NormalMode(mode.buffer, mode.ui)

@InsertMode.register(10) #Enter
def insertMode_enter(mode, key):
    index=mode.ui.ins_enter(key)
    mode.buffer.insert(index, '\n')

@InsertMode.register(curses.KEY_UP)
def insertMode_up(mode, key):
    mode.ui.move_up(True)

@InsertMode.register(curses.KEY_DOWN)
def insertMode_down(mode, key):
    mode.ui.move_down(True)

@InsertMode.register(curses.KEY_LEFT)
def insertMode_left(mode, key):
    mode.ui.move_left(True)

@InsertMode.register(curses.KEY_RIGHT)
def insertMode_right(mode, key):
    mode.ui.move_right(True)

@InsertMode.register(curses.KEY_BACKSPACE)
def insertMode_backspace(mode, key):
    index=mode.ui.ins_backspace(key)
    mode.buffer.delete(index)
