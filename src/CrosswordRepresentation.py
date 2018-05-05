""""
This class holds two dictionaries with keys being words in the puzzle and values being the Cell where that word
begins. There is a dictionary for across words and another for down words. The dictionaries also serve as lists
of the across and down words currently in the puzzle.
"""
class CrosswordRepresentation:

    """
    Parameters: ListD of Down words, ListA of Across words.
    listD and listA are dictionaries where the keys are the words that are across or down and the value is the cell
    object of the first letter of the word in the Board.
    """
    def __init__(self, dictA, dictD):
        self.across = dictA
        self.down = dictD

    """
    Scores the density of the current crossword. This will be used to find a better neighbor
    than the brute force algorithm. We did not get to complete this method, but it would have likely been
    useful for creating a more optimal algorithm.
    """
    def density(self):

        # ----------------
        # 1. Track how words are in the crossword
        # 2. Count how many intersections are in the crossword
        # 3.

        # Python code that generates a crossword: http://bryanhelmig.com/python-crossword-puzzle-generator/
        return


