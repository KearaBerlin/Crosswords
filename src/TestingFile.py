import unittest
from src.MakeCrossWord import *
from src.parseDictionary import *
from src.BruteForce import *


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
        test_array = []
        # for x in range(

    def test_get_cell_affix_empty(self):
        board = Board(CrosswordRepresentation([], ["HELLO"], []))
        self.assertEqual(board.getCellAffix(board.Cell(None, None, 5, 5, 0, 0), True),
                         "")
        self.assertEqual(board.getCellAffix(board.Cell(None, None, 5, 5, 0, 0), False),
                         "")

    def test_get_cell_affix_across(self):
        board = Board(CrosswordRepresentation([], ["HELLO"], []))
        self.assertEqual(board.getCellAffix(board.Cell("HELLO", None, 5, 5, 0, 0), True),
                         "HELLO")
        self.assertEqual(board.getCellAffix(board.Cell(None, "HELLO", 5, 5, 0, 0), True),
                         "H")
        self.assertEqual(board.getCellAffix(board.Cell(None, "HELLO", 5, 5, 0, 4), True),
                         "O")
        self.assertEqual(board.getCellAffix(board.Cell("OVAL", "PEAR", 5, 5, 0, 2), True),
                         "PEAR")

if __name__ == '__main__':
    unittest.main()

