

class Buffer:

    def __init__(self, text=''):
        self.text = list(text)

    def insert(self, index, char):
        self.text.insert(index, char)

    def delete(self, index):
        self.text.pop(index)

    def str(self, index=0):
        return ''.join(self.text[index:])

    def char(self, index):
        return ''.join(self.text[index])
