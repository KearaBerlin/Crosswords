import unittest
from src.MakeCrossWord import *
from src.parseDictionary import *
from src.BruteForce import *

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


    """
    Test for the shiftElements method. If the assert is true then there is a shift in the opposite direction of the 
    shift in the assert. This allows me to keep using the same array and not have to keep track of the changes from
    each call of shiftElements since shiftElements updates the array and doesn't return an array. 
    """
    def test_shiftElements(self):
        crossword = CrosswordRepresentation([],[],[])
        board = Board(crossword)

        for y in range(width):
            board.boardArray[0][y] = 'a'

        self.assertTrue(board.shiftElements(3,0))
        board.shiftElements(-3,0)

        self.assertTrue(board.shiftElements(width-2,0))
        board.shiftElements(-(width-2),0)

        self.assertFalse(board.shiftElements(width,0))
        self.assertFalse(board.shiftElements(-1, 0))

        for y in range(width):
            board.boardArray[0][y] = None
            board.boardArray[y][2] = 'a'

        self.assertTrue(board.shiftElements(0, 2))
        board.shiftElements(0, -2)

        self.assertTrue(board.shiftElements(0, width-4))
        board.shiftElements(0, -(width-4))

        self.assertFalse(board.shiftElements(0, width))
        self.assertFalse(board.shiftElements(0, -3))


    def test_get_cell_affix_empty(self):
        board = Board(CrosswordRepresentation([], ["HELLO"], []))
        self.assertEqual(board.getCellAffix(board.Cell(None, None, 5, 5, 0, 0), True),
                         "")
        self.assertEqual(board.getCellAffix(board.Cell(None, None, 5, 5, 0, 0), False),
                         "")

    def test_get_cell_affix_across(self):
        board = Board(CrosswordRepresentation([], ["HELLO"], []))
        self.assertEqual(board.getCellAffix(board.Cell(None, "HELLO", 5, 5, 0, 4), True),
                         "HELLO")
        self.assertEqual(board.getCellAffix(board.Cell("HELLO", None, 5, 5, 0, 0), True),
                         "H")
        self.assertEqual(board.getCellAffix(board.Cell("HELLO", None, 5, 5, 4, 0), True),
                         "O")
        self.assertEqual(board.getCellAffix(board.Cell("MOOR", "PEAR", 5, 5, 3, 3), True),
                         "PEAR")

    def test_get_cell_affix_down(self):
        board = Board(CrosswordRepresentation([], ["HELLO"], []))
        self.assertEqual(board.getCellAffix(board.Cell(None, "HELLO", 5, 5, 0, 4), False),
                         "O")
        self.assertEqual(board.getCellAffix(board.Cell("HELLO", None, 5, 5, 0, 0), False),
                         "HELLO")
        self.assertEqual(board.getCellAffix(board.Cell(None, "HELLO", 5, 5, 0, 0), False),
                         "H")
        self.assertEqual(board.getCellAffix(board.Cell("PEEP", "PEAR", 5, 5, 0, 0), False),
                         "PEEP")

if __name__ == '__main__':
    unittest.main()

