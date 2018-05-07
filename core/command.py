
def command_save(mode, filename=None):
    if not filename:
        filename = mode.buffer.name

    with open(filename, 'w') as fd:
        fd.write(mode.buffer.str())

def command_quit(mode, filename=None):
    quit()
