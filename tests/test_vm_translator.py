import unittest
from VMTranslator import add_one

def fun(x):
    return x + 1

class TestVMTranslator(unittest.TestCase):
    def test(self):
        self.assertEqual(add_one(3), 4)
