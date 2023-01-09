import unittest
from src.Node import *
from src.HuffmanCoding import HuffmanCoding

class TestHuffmanCoding(unittest.TestCase):
    def test_make_frequency_dict(self):
        h = HuffmanCoding(None)
        text = "aaaabbbbcccc"
        frequency_dict = h.make_frequency_dict(text)
        expected_output = {'a': 4, 'b': 4, 'c': 4}
        self.assertEqual(frequency_dict, expected_output)




