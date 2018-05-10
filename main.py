import os
import sys

from core.command import command
from core.mode import NormalMode
from core.buffer import Buffer
from core.ui.ui import create_main_windows
from core.ui.screen import CursesScreen


def run():

    os.environ["ESCDELAY"] = "0"

    try:
        with open(sys.argv[1], 'a+') as fd:
            fd.seek(0)
            buffer = Buffer(fd.read())
            buffer.name=sys.argv[1]
    except:
        buffer = Buffer()


    with CursesScreen(buffer.str()) as screen:
        mode = NormalMode(buffer, screen)
        while True:
            mode = mode.run()

    print("buffer: ", buffer.str())



if __name__ == "__main__":
    run()
