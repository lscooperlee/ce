import os
import sys

from core.mode import InsertMode
from core.buffer import Buffer
from core.ui.screen import create_main_windows


def run():

    os.environ["ESCDELAY"] = "0"
    try:
        with open(sys.argv[1], 'a+') as fd:
            fd.seek(0)
            buffer = Buffer(fd.read())
            buffer.name=sys.argv[1]
    except:
        buffer = Buffer()

    with create_main_windows() as windows:
        windows['main'].insstr(buffer.str())
        windows['main'].move(0, 0)
        windows['main'].refresh()
        mode = InsertMode(buffer, windows)
        while True:
            mode = mode.run()



if __name__ == "__main__":
    run()
