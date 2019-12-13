import unittest
from src.parser import add_two

class TestVMTranslator(unittest.TestCase):
    def test(self):
        self.assertEqual(add_two(3), 5)
