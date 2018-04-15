import random




"""
Representing board with a 2D array.
"""
class Board:

    def __init__(self, array, crossword):
        self.boardArray = array
        # fill array with valid/current words

    """
    Returns cell object at given x and y coordinate
    """
    def getCellAt(self, x, y):
        return self.boardArray[x][y]

    class Cell:
        def __init__(self, word, index):
            self.word = word
            self.index = index


"""
Write stuff:
"""
class CrosswordRepresentation:

    """
    Parameters: ListD of Down words, ListA of Across words. Intersections of words
    We will represent the intersection of words by having a coordinate representing
    which index of listD and listA intersect.
    """
    def __init__(self,listD, listA, intersections):
        self.across = listA
        self.down = listD
        self.inter = intersections




    # def wouldBeValid(self, intersection):
    #
    #
    # # def makeBoard(self):
    # #
    #






class Intersection:

    def __init__(self, acrossWord, acrossWordIndex, downWord, downWordIndex):
        self.across = acrossWord
        self.down = downWord
        self.acrossIndex = acrossWordIndex
        self.downIndex = downWordIndex

# Commented code below is just an example of how we would use the Intersection class.
# listA = ["attack", "sleep", "awake"]
# listD = ["apple", "koala"]
# inter1 = Intersection("attack", "apple", 3, 0)
# inter2 = Intersection("attack", "koala", 5, 0)
# inter3 = Intersection("sleep", "apple", 4, 2)
# inter4 = Intersection("awake","apple", 4, 4)
#
# interTotal = [inter1,inter2, inter3, inter4]


"""
Brute force algorithm to pick words for the crossword
1. Pick random word
2. Examine neighbors 
"""
def bruteForce(graph):
    keys = graph.keys()
    randomIndex = random.random(0,len(keys))
    startWord = keys[randomIndex]

    crossword = CrosswordRepresentation([],[startWord], [])

