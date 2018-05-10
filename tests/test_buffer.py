import unittest

from core.buffer import Buffer

class TestBuffer(unittest.TestCase):

    def test_char(self):
        buf = Buffer('abcde\nfg\n\n\nh')
        self.assertEqual(buf.char(0), 'a')
        self.assertEqual(buf.char(1), 'b')
        self.assertEqual(buf.char(6), 'f')
        self.assertEqual(buf.char(11), 'h')

    def test_str(self):
        buf = Buffer('abcde\nfg\n\n\nh')
        self.assertEqual(buf.str(7), 'g\n\n\nh')

    def test_delete(self):
        buf = Buffer('abcde\nfg\n\n\nh')
        buf.delete(0)
        self.assertEqual(buf.str(), 'bcde\nfg\n\n\nh')
        buf.delete(6)
        self.assertEqual(buf.str(), 'bcde\nf\n\n\nh')
        buf.delete(7)
        self.assertEqual(buf.str(), 'bcde\nf\n\nh')

    def test_insert(self):
        buf = Buffer('abcde\nfg\n\n\nh')
        buf.insert(0, 'i')
        self.assertEqual(buf.str(), 'iabcde\nfg\n\n\nh')
        buf.insert(7, 'm')
        self.assertEqual(buf.str(), 'iabcde\nmfg\n\n\nh')
        buf.insert(8, 'l')
        self.assertEqual(buf.str(), 'iabcde\nmlfg\n\n\nh')

if __name__ == "__main__":
    unittest.main()
