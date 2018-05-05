# TODO fill in this class description comment
"""
Write stuff:
"""
class CrosswordRepresentation:

    """
    Parameters: ListD of Down words, ListA of Across words. Intersections of words
    We will represent the intersection of words by having a coordinate representing
    which index of listD and listA intersect.
    listD and listA are dictionaires where the keys are the words that are across or down and the value is the cell
    object of the first letter of the word.
    """
    def __init__(self, dictA, dictD):
        self.across = dictA
        self.down = dictD

    """
    Scores the density of the current crossword. This will be used to find a better neighbor
    than the brute force algorithm.
    """
    def density(self):

        # ----------------
        # 1. Track how words are in the crossword
        # 2. Count how many intersections are in the crossword
        # 3.

        # Python code that generates a crossword: http://bryanhelmig.com/python-crossword-puzzle-generator/
        return


