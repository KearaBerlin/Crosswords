import unittest
from src.MakeCrossWord import *
from src.parseDictionary import *
from src.BruteForce import *
from src.Intersection import Intersection

width = 30

class TestMethods(unittest.TestCase):

    helloBoard = Board(CrosswordRepresentation({"HELLO":None}, {}, []))

    # def test_board_constructor(self):
    #     crossword = CrosswordRepresentation(["HELLO"], [], [])
    #     board = Board(crossword)
    #     self.assertEqual(board.WIDTH, 30)  # test the default width is right
    #     # test that rows and cols are empty or not as appropriate
    #     self.assertFalse(board.colIsEmpty(0))
    #     self.assertTrue(board.colIsEmpty(15))
    #     self.assertFalse(board.rowIsEmpty(0))
    #     self.assertTrue(board.rowIsEmpty(1))
    #     self.assertTrue(board.rowIsEmpty(5))
    #
    #
    # """
    # Test for the shiftElements method. If the assert is true then there is a shift in the opposite direction of the
    # shift in the assert. This allows me to keep using the same array and not have to keep track of the changes from
    # each call of shiftElements since shiftElements updates the array and doesn't return an array.
    # """
    # def test_shiftElements(self):
    #     crossword = CrosswordRepresentation([],[],[])
    #     board = Board(crossword)
    #
    #     for y in range(width):
    #         board.boardArray[0][y] = 'a'
    #
    #     self.assertTrue(board.shiftElements(3,0))
    #     board.shiftElements(-3,0)
    #
    #     self.assertTrue(board.shiftElements(width-2,0))
    #     board.shiftElements(-(width-2),0)
    #     # board.terminalRepresentationOfCrossword()
    #
    #     self.assertFalse(board.shiftElements(width,0))
    #     self.assertFalse(board.shiftElements(-1, 0))
    #
    #     for y in range(width):
    #         board.boardArray[0][y] = None
    #         board.boardArray[y][2] = 'a'
    #
    #     self.assertTrue(board.shiftElements(0, 2))
    #     board.shiftElements(0, -2)
    #
    #     self.assertTrue(board.shiftElements(0, width-4))
    #     board.shiftElements(0, -(width-4))
    #
    #     self.assertFalse(board.shiftElements(0, width))
    #     self.assertFalse(board.shiftElements(0, -3))
    #
    # """
    # Comment out the assertEqual statements if you want to significantly decrease the run time.
    # """
    # def test_fillInWords(self):
    #     crossword = CrosswordRepresentation([], [], [])
    #     board = Board(crossword)
    #     cell0 = board.Cell('TAKE', 'TIME', 5, 5, 0, 0)
    #     cell1 = board.Cell('ATE', 'MATE', 5, 8, 1, 2)
    #     bf = BruteForceCrossword()
    #     self.assertGreaterEqual(len(bf.fillInWords(cell0, cell1)), 15)
    #     # self.assertEqual(bf.fillInWords(cell0, cell1), bf.fillInWords(cell1, cell0))
    #
    #     cell2 = board.Cell('TAKE', 'TIME', 6, 6, 0, 0)
    #     cell3 = board.Cell('ATE', 'MATE', 9, 6, 1, 2)
    #     # self.assertEqual(bf.fillInWords(cell2, cell3), bf.fillInWords(cell0, cell1))


    def test_addIfValid(self):
        crossword = CrosswordRepresentation({"HELLO": None}, {}, [])
        board = Board(crossword)

        # This is a valid add
        interCell0 = board.getCellAt(0, 0)
        inter0 = Intersection("HELLO", "HELP", 0, 0)
        self.assertTrue(board.addIfValid(interCell0, inter0, False))
        board.terminalRepresentationOfCrossword()
        print("====================================")

        # This is a valid add
        interCell1 = board.getCellAt(0, 3)
        inter1 = Intersection("PARTY", "HELP", 0, 3)
        self.assertTrue(board.addIfValid(interCell1, inter1, True))
        board.terminalRepresentationOfCrossword()
        print("====================================")

        # A valid add -- Tests for adding a word out of bounds, requires shift down
        interCell2 = board.getCellAt(2, 0)
        inter2 = Intersection("HELLO", "HELL", 2, 2)
        self.assertTrue(board.addIfValid(interCell2, inter2, False))
        board.terminalRepresentationOfCrossword()
        print("====================================")

        interCell3 = board.getCellAt(2, 3)
        inter3 = Intersection("LONDON", "HELL", 0, 3)
        self.assertTrue(board.addIfValid(interCell3, inter3, True))
        board.terminalRepresentationOfCrossword()
        print("====================================")

        # This one should fail because the word is too long
        interCell4 = board.getCellAt(2, 5)
        inter4 = Intersection("PARTY", "ROOSTER", 2, 0)
        self.assertFalse(board.addIfValid(interCell4, inter4, False))
        board.terminalRepresentationOfCrossword()
        print("====================================")

        # This should also fail since it has a "parallel intersecting word"
        interCell5 = board.getCellAt(3, 2)
        inter5 = Intersection("LO", "LOUT", 0, 0)
        self.assertFalse(board.addIfValid(interCell5, inter5, False))
        board.terminalRepresentationOfCrossword()
        print("====================================")



    # def test_get_cell_affix_empty(self):
    #     board = self.helloBoard
    #     self.assertEqual(board.getCellAffix(board.Cell(None, None, 5, 5, 0, 0), True, True),
    #                      "")
    #     self.assertEqual(board.getCellAffix(board.Cell(None, None, 5, 5, 0, 0), False, True),
    #                      "")
    #
    # def test_get_cell_affix_across(self):
    #     board = self.helloBoard
    #     self.assertEqual(board.getCellAffix(board.Cell(None, "HELLO", 5, 5, 0, 4), True),
    #                      "HELLO")
    #     self.assertEqual(board.getCellAffix(board.Cell("HELLO", None, 5, 5, 0, 0), True),
    #                      "H")
    #     self.assertEqual(board.getCellAffix(board.Cell("HELLO", None, 5, 5, 4, 0), True),
    #                      "O")
    #     self.assertEqual(board.getCellAffix(board.Cell("MOOR", "PEAR", 5, 5, 3, 3), True),
    #                      "PEAR")
    #
    # def test_get_cell_affix_down(self):
    #     board = self.helloBoard
    #     self.assertEqual(board.getCellAffix(board.Cell(None, "HELLO", 5, 5, 0, 4), False),
    #                      "O")
    #     self.assertEqual(board.getCellAffix(board.Cell("HELLO", None, 5, 5, 0, 0), False),
    #                      "HELLO")
    #     self.assertEqual(board.getCellAffix(board.Cell(None, "HELLO", 5, 5, 0, 0), False),
    #                      "H")
    #     self.assertEqual(board.getCellAffix(board.Cell("PEEP", "PEAR", 5, 5, 0, 0), False),
    #                      "PEEP")
    #
    # def test_collidedWordIsValid(self):
    #     board = self.helloBoard
    #     self.assertTrue(board.getCollidedWord('N', 0, 'PEW') is not None)
    #     self.assertTrue(board.getCollidedWord('W', 1, 'SMARM') is not None)
    #     self.assertTrue(board.getCollidedWord('S', 3, 'LOPE') is not None)
    #     self.assertFalse(board.getCollidedWord('A', 0, 'MAP') is not None)
    #     self.assertTrue(board.getCollidedWord('H', 0, 'HELLO') is not None)
    #
    # def test_add_word_to_array(self):
    #     board = self.helloBoard
    #     board.shiftElements(0, 3)
    #     existing = "HELLO"
    #     new = "WORLD"
    #     intersection = Intersection(existing, new, 2, 3)
    #     afterBoard = Board(CrosswordRepresentation([existing], [new], [intersection]))
    #     afterBoard.boardArray = []
    #     board.addWordToArray(0, 3, new, intersection, False)
    #
    #     board.terminalRepresentationOfCrossword()
    #     print("--------------------------------------------------------------------")
    #     afterBoard.terminalRepresentationOfCrossword()
    #     # self.assertEquals(board, afterBoard)

if __name__ == '__main__':
    unittest.main()

