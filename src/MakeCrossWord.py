import random
from src.parseDictionary import *
from nltk.corpus import words

wordList = words.words()

FILE_NAME = 'dictFile.csv'

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
                self.boardArray[sX+x][sY] = self.Cell(word, None, sX+x, sY, x)
            else:
                self.boardArray[sX][sY + x] = self.Cell(None, word, sX, sY + x, x)

    """
    Returns cell object at given x and y coordinate
    """
    def getCellAt(self, x, y):
        return self.boardArray[x][y]

    # TODO this needs to be finished. Also, we need to update all the cells whose word changed to be the new word...
    # and maybe we need to also change the underlying CrosswordRepresentation somehow?? adding a new intersection
    # and a new word, mostly
    """
    Takes in an intersection and whether the word being theoretically added is an Across word. Returns true if the
    intersection would result in a valid new crossword, false otherwise. Does not add the new word to underlying
    crossword.
    """
    def addIfValid(self,interCell, intersection, newWordIsAcross):
        copyArray = [[None for i in range(self.WIDTH)] for j in range(self.WIDTH)]
        if newWordIsAcross:
            newWord = intersection.across
            existingWord = intersection.down
            interX = interCell.x
            interY = interCell.y

            startingX = interCell.x - intersection.acrossIndex
            startingY = interCell.y

            # ----------------------------------------------
            # TODO 1. check whether would be out of bounds of the puzzle
            # ----------------------------------------------

            # loop through each cell that the new word would inhabit
            for i in range(len(newWord)):
                currentCell = self.boardArray[startingX+i][startingY]
                perpendicularWordIndex = currentCell.indexWithinWord
                char = newWord[i]

                # ------------------------------------------------------
                # 2. check whether this cell is part of an existing word
                # ------------------------------------------------------
                collidedWordIsValid = collidedWordIsValid(char, perpendicularWordIndex, currentCell.acrossWord)
                if not collidedWordIsValid:
                    return False

                # -------------------------------------------------------------
                # 3. Check whether the cells above and below are part of a word
                # -------------------------------------------------------------
                if currentCell.y == 0:
                    aboveFilled = False
                else:
                    cellAbove = self.boardArray[currentCell.x][currentCell.y + 1]
                    aboveFilled = cellAbove is not None

                if currentCell.y == (self.WIDTH -1):
                    belowFilled = False
                else:
                    cellBelow = self.boardArray[currentCell.x][currentCell.y - 1]
                    belowFilled = cellBelow is not None

                # if only one cell is part of a word, check whether it's still a valid
                # word once we add on the new char at the beginning/end
                # TODO I am not sure we meant acrossWord -- but will be fixed when we account for rest of edge cases
                if aboveFilled and not belowFilled:
                    if not wordList.contains(cellAbove.acrossWord + char):
                        return False
                elif belowFilled and not aboveFilled:
                    if not wordList.contains(char + cellBelow.acrossWord):
                        return False

                # TODO again, same as above Todo
                # if both cells are part of a word, we will check whether that whole long word is valid.
                elif aboveFilled and belowFilled:
                    collidedWord = aboveFilled.acrossWord + char + belowFilled.acrossWord
                    if not wordList.contains(collidedWord):
                        return False

            # ------------------------------------------
            # 4. Check the cells before and after the new word for word collisions
            # ------------------------------------------
            if startingX == 0:
                leftFilled = False
            else:
                leftCell = self.boardArray[startingX - 1][startingY]
                leftFilled = leftCell is not None
            if startingX == self.WIDTH - 1:
                rightFilled = False
            else:
                rightCell = self.boardArray[startingX + 1][startingY]
                rightFilled = rightCell is not None

            # if only one cell is filled, check whether that collision is valid
            if leftFilled and not rightFilled:
                if not wordList.contains(leftCell.acrossWord + newWord):
                    return False
            elif rightFilled and not leftFilled:
                if not wordList.contains(newWord + rightCell.acrossWord):
                    return False

            # if both cells are filled, check whether that whole long word will work
            elif rightFilled and leftFilled:
                if not wordList.contains(leftCell.acrossWord + newWord + rightCell.acrossWord):
                    return False

            # If we made it this far without returning False, the new word is valid!
            # TODO how do we actually add the word now that it is valid?

        else:
            newWord = intersection.down
            existingWord = intersection.across

        return 1

    """
    Helper method for addIfValid. Returns whether a new word with a certain character changed is still a valid word
    """
    def collidedWordIsValid(self, char, perpendicularWordIndex, perpendicularWord):
        # case 1: adding char as index 0
        if perpendicularWordIndex == 0:
            collidedWord = char + perpendicularWord[perpendicularWordIndex+1:]
        # case 2: adding char as last index
        elif perpendicularWordIndex == len(perpendicularWord):
            collidedWord = perpendicularWord[:len(perpendicularWord)-1] + char
        # case 3: adding char somewhere in the middle
        else:
            collidedWord = perpendicularWord[:perpendicularWordIndex-1] + char \
                           + perpendicularWord[perpendicularWordIndex+1:]

        # check whether this word is in our word list
        if not wordList.contains(collidedWord):
            return False


    """
    Helper method for addIfValid. Takes in a Cell adjacent to a Cell that would be part of the new word being added.
    Returns the character(s) that should be added to the character in that new cell, to get a word that can be checked
    whether it is in the quarter million word list. The client code should know whether the returned chars go after or
    before the new char, and should also perform the check in the word list etc. This method simply returns an affix.
    adjCell - a Cell representing the Cell that is directly adjacent to the new character being added
    newIsAcross - a boolean stating whether the new word being added is across or down
    Returns a str
    """
    def getCellAffix(self, adjCell, newIsAcross):
        # check whether the adjCell has an acrossWord, downWord, or both
        hasAcross = adjCell.acrossWord is not None
        hasDown = adjCell.downWord is not None

        if newIsAcross:
            # whether or not the cell is above or below the new character, we will always either return a character
            # in the adjCell or the word that adjCell is part of.

            if hasAcross and not hasDown:
                # return only the char above
                return str(adjCell.acrossWord[adjCell.indexWithinWord])
            elif hasDown:
                # whether it has both or only down, only return the whole word above
                return str(adjCell.downWord)
        else:
            # this is a very similar idea to above, but now adjCell is just to the right or left of new character.
            if hasDown and not hasAcross:
                return str(adjCell.downWord[adjCell.indexWithinWord])
            elif hasAcross:
                return str(adjCell.acrossWord)

    """
    Shifts everything in the array by copying things over in another array.
    Will shift things over x to the right and y down.
    If either are negative then it's just the opposite direction.
    
    Also checks if the shift is valid
    """
    def shiftElements(self,xShift,yShift):
        shiftedArray = [[None for i in range(self.WIDTH)] for j in range(self.WIDTH)]
        for x in range(self.WIDTH):
            for y in range(self.WIDTH):
                if self.boardArray[x][y] is not None and 0 <= x+xShift < self.WIDTH and 0 <= y+yShift < self.WIDTH:
                    shiftedArray[x+xShift][y+yShift] = self.boardArray[x][y]
                elif self.boardArray[x][y] is not None and (0 > x+xShift or x+xShift > self.WIDTH) and (0 > y+yShift or y + yShift > self.WIDTH):
                    return False
        self.boardArray = shiftedArray
        return True


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
        def __init__(self, acrossWord, downWord, x, y, indexWithinWord):
            self.acrossWord = acrossWord
            self.downWord = downWord
            self.xCoord = x
            self.yCoord = y
            self.indexWithinWord = indexWithinWord

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
    def __init__(self,listD, listA, intersections):
        self.across = listA
        self.down = listD
        self.inter = intersections

    """
    Scores the density of the current crossword. This will be used to find a better neighbor
    than the brute force algorithm.
    """
    def density(self):
        return 0

"""
Represents two words and which index in the word will intersect with the other word.
"""
class Intersection:

    def __init__(self, acrossWord, downWord,acrossWordIndex, downWordIndex, ):
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
    board = Board(crossword)

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
            if addNeighbor(currentWord, currentWordIsAcross, neighborWord, board):
                currentWord = neighborWord
                break

        # every other word will be across
        currentWordIsAcross = not currentWordIsAcross
    return board


"""
Used by the brute force crossword algorithm to add a neighbor word to the crossword if any intersections with the
current word are valid. (Adds the word at the first valid intersection found.)
If a word is added, returns True; otherwise, returns False.
"""
def addNeighbor(currentWord, currentWordIsAcross, neighborWord, board):

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
                if board.addIfValid(intersection, not currentWordIsAcross):
                    return True

    return False


# graph = readCSV()  # from parseDictionary.py
# print(graph['A'])
# cw = bruteForce(graph)
# print(cw.across, cw.down)

