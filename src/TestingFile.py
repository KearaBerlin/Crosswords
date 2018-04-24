import unittest
from src.MakeCrossWord import *
from src.parseDictionary import *

width = 30

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

    def test_shiftElements(self):
        crossword = CrosswordRepresentation([],['HELLO'],[])
        board = Board(crossword)

        for y in range(width):
            board.boardArray[0][y] = 'a'

        self.assertTrue(board.shiftElements(3,0))
        self.assertTrue(board.shiftElements(width-2,0))




if __name__ == '__main__':
    unittest.main()

