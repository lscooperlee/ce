import unittest

from core.buffer import Buffer

class TestBuffer(unittest.TestCase):

    def test_index(self):
        buf = Buffer('abcde\nfg\n\n\nh')
        self.assertEqual(buf.index(0, 0), 0)
        self.assertEqual(buf.index(1, 0), 1)
        self.assertEqual(buf.index(0, 1), 6)
        self.assertEqual(buf.index(0, 4), 11)
        #self.assertEqual(buf.index(19, 91), 11)

    def test_char(self):
        buf = Buffer('abcde\nfg\n\n\nh')
        self.assertEqual(buf.char(0, 0), 'a')
        self.assertEqual(buf.char(1, 0), 'b')
        self.assertEqual(buf.char(0, 1), 'f')
        self.assertEqual(buf.char(0, 4), 'h')

    def test_str(self):
        buf = Buffer('abcde\nfg\n\n\nh')
        self.assertEqual(buf.str(1, 1), 'g\n\n\nh')

    def test_row(self):
        buf = Buffer('abcde\nfg\n\n\nh')
        self.assertEqual(buf.row(1), 'fg\n')
        self.assertEqual(buf.row(0), 'abcde\n')
        self.assertEqual(buf.row(2), '\n')
        self.assertEqual(buf.row(3), '\n')
        self.assertEqual(buf.row(4), 'h')

    def test_delete(self):
        buf = Buffer('abcde\nfg\n\n\nh')
        buf.delete(0, 0)
        self.assertEqual(buf.str(), 'bcde\nfg\n\n\nh')
        buf.delete(1, 1)
        self.assertEqual(buf.str(), 'bcde\nf\n\n\nh')
        buf.delete(1, 2)
        self.assertEqual(buf.str(), 'bcde\nf\n\nh')

    def test_insert(self):
        buf = Buffer('abcde\nfg\n\n\nh')
        buf.insert(0, 0, 'i')
        self.assertEqual(buf.str(), 'iabcde\nfg\n\n\nh')
        buf.insert(1, 1, 'm')
        self.assertEqual(buf.str(), 'iabcde\nfmg\n\n\nh')
        buf.insert(0, 2, 'l')
        self.assertEqual(buf.str(), 'iabcde\nfmg\nl\n\nh')

if __name__ == "__main__":
    unittest.main()
