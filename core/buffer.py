

class Buffer:

    def __init__(self, text=''):
        self.text = list(text)
        self.indexes = self.make_indexes()

    def make_indexes(self):
        return [0] + \
            [i + 1 for i, n in enumerate(self.text) if n == '\n'] + \
            [len(self.text)]

    def index(self, x, y):
        idx = self.indexes[y] + x
        return idx

    def coordinate(self, index):
        return 0, 0

    def insert(self, x, y, char):
        self.text.insert(self.index(x, y), char)
        self.indexes = self.make_indexes()

    def delete(self, x, y):
        self.text.pop(self.index(x, y))
        self.indexes = self.make_indexes()

    def str(self, x=0, y=0):
        return ''.join(self.text[self.index(x, y):])

    def char(self, x, y):
        return ''.join(self.text[self.index(x, y)])

    def row(self, y=0):
        return ''.join(self.text[self.indexes[y]: self.indexes[y+1]])
