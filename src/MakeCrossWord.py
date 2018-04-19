import random
from src.parseDictionary import *


"""
Representing board with a 2D array.
"""
class Board:
    def __init__(self, crossword, ARRAY_WIDTH = 30):
        self.WIDTH = ARRAY_WIDTH
        self.crossword = crossword
        self.startingWord = crossword.across[0] # First word will always be the first index of the across list.

        # initialize array with None
        self.boardArray = [[None for i in range(self.WIDTH)] for j in range(self.WIDTH)]

        # puts the starting word the top left corner of the array (0,0) to (0,len(word)-1)
        self.addWordToArray(0, 0, self.startingWord, True)

    """
   So writing this method with the assumption that we have checked that it is valid to 
   add the word at this position and the area around it.
   """
    def addWordToArray(self, sX, sY, word, isAcross):
        for x in range(len(word)):
            if isAcross:
                self.boardArray[sX+x][sY] = self.Cell(word, sX+x)
            else:
                self.boardArray[sX][sY + x] = self.Cell(word, sX,sY + x)

    """
    Returns cell object at given x and y coordinate
    """
    def getCellAt(self, x, y):
        return self.boardArray[x][y]

    """
    Shifts everything in the array by copying things over in another array. 
    Will shift things over x to the right and y down. 
    If either are negative then it's just the opposite direction.
    
    Not sure if I should assume that we have checked that a shift is valid or not...
    """
    def shiftElements(self,x,y):
        shiftedArray = []

        return 0

    """
    Returns true or false
    """
    def colIsEmpty(self, col):
        if col < self.WIDTH:
            for x in range(self.WIDTH):
                if self.boardArray[col][x] is not None:  # If is not None then there's an element in the column.
                    return False
            return True
        else:
            return False

    """
    Returns true or false
    """
    def rowIsEmpty(self, row):
        if row < self.WIDTH:
            for x in range(self.WIDTH):
                if self.boardArray[x][row] is not None:  # If is not None then there's an element in the column
                    return False
            return True
        else:
            return False


    class Cell:
        def __init__(self, word, x,y):
            self.word = word
            self.xCoord = x
            self.yCoord = y


        """
        Setter method for the coordinates of the cell.
        Will use this when we shift the array or certain cells.
        """
        def setCoord(self, newX, newY):
            self.xCoord = newX
            self.yCoord = newY


# TODO fill in this class description comment
"""
Write stuff:
"""
class CrosswordRepresentation:

    """
    Parameters: ListD of Down words, ListA of Across words. Intersections of words
    We will represent the intersection of words by having a coordinate representing
    which index of listD and listA intersect.
    """
    def __init__(self,listD, listA, intersections,):
        self.across = listA
        self.down = listD
        self.inter = intersections


    # TODO this needs to actually get written
    """
    Takes in an intersection and whether the word being theoretically added is an Across word. Returns true if the 
    intersection would result in a valid new crossword, false otherwise. Does not add the new word to underlying
    crossword.
    
    """
    def addIfValid(self, intersection, newWordIsAcross):

        return 1




    """
    Scores the density of the current crossword. This will be used to find a better neighbor
    than the brute force algorithm.
    """
    def density(self):
        return 0


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

    # get a random word to start with
    keys = graph.keys()
    randomIndex = random.randint(0,len(keys)-1)
    keys = list(keys)
    startWord = keys[randomIndex]

    # initialize a crossword that contains that start word
    crossword = CrosswordRepresentation([],[startWord], [])

    # this outer loop continues until we have the desired number of words in our crossword
    currentWord = startWord
    currentWordIsAcross = True
    for i in range(10):

        # this loops through the current word's neighbors until we find a neighbor we can insert into the crossword
        neighbors = graph[currentWord]
        found = False
        for neighborTuple in neighbors:
            neighborWord = neighborTuple[0]

            # call a method that adds the neighbor word in a valid intersection if it finds one
            if addNeighbor(currentWord, currentWordIsAcross, neighborWord, crossword):
                currentWord = neighborWord
                break

        # every other word will be across
        currentWordIsAcross = not currentWordIsAcross
    return crossword


"""
Used by the brute force crossword algorithm to add a neighbor word to the crossword if any intersections with the 
current word are valid. (Adds the word at the first valid intersection found.)
If a word is added, returns True; otherwise, returns False.
"""
def addNeighbor(currentWord, currentWordIsAcross, neighborWord, crossword):

    for current_i in range(len(currentWord)):
        for neighbor_i in range(len(neighborWord)):
            if currentWord[current_i] == neighborWord[neighbor_i]:

                # generate an intersection object
                if currentWordIsAcross:
                    intersection = Intersection(currentWord, current_i,
                                                neighborWord, neighbor_i)
                else:
                    intersection = Intersection(neighborWord, neighbor_i,
                                                currentWord, current_i)

                # if this is a valid intersection, add it to crossword and break out of the second loop
                if crossword.addIfValid(intersection, not currentWordIsAcross):
                    return True

    return False


graph = readCSV()  # from MakeCrossWord.py
#print(graph)
cw = bruteForce(graph)
print(cw.across, cw.down)

