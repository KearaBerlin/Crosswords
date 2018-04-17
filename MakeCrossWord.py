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
    def __init__(self,listD, listA, intersections):
        self.across = listA
        self.down = listD
        self.inter = intersections

    # TODO this needs to actually get written
    """
    Takes in an intersection and whether the word being theoretically added is an Across word. Returns true if the 
    intersection would result in a valid new crossword, false otherwise. Does not add the new word to underlying
    crossword.
    """
    def wouldBeValid(self, intersection, newWordIsAcross):
        return None

    # TODO this has not been written yet either
    """
    This method takes in an intersection and whether the word being added is an Across word, and adds the word to the
    crossword.
    """
    def addWord(self, intersection, newWordIsAcross):
        todo = -1


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
    randomIndex = random.random(0,len(keys))
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
                break

        # every other word will be across
        currentWordIsAcross = not currentWordIsAcross


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
                if crossword.wouldBeValid(intersection, not currentWordIsAcross):
                    crossword.addWord(intersection, not currentWordIsAcross)
                    return True

    return False


