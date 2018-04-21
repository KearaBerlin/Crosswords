import unittest
from src.MakeCrossWord import *
from src.parseDictionary import *


class TestMethods(unittest.TestCase):

    def test_board_constructor(self):
        crossword = CrosswordRepresentation([], ["HELLO"], [])
        board = Board(crossword)
        self.assertEqual(board.WIDTH, 30)  # test the default width is right
        # test that rows and cols are empty or not as appropriate
        self.assertFalse(board.colIsEmpty(0))
        self.assertTrue(board.colIsEmpty(15))
        self.assertFalse(board.rowIsEmpty(0))
        self.assertTrue(board.rowIsEmpty(1))
        self.assertTrue(board.rowIsEmpty(5))

if __name__ == '__main__':
    unittest.main()

