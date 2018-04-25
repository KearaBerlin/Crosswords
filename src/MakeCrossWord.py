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

        # initialize array with None
        self.boardArray = [[None for i in range(self.WIDTH)] for j in range(self.WIDTH)]

        if len(crossword.across) != 0:
            self.startingWord = crossword.across[0]  # First word will always be the first index of the across list.
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
                # 3. Check whether the word containing new char and any affixes from above and/or below is a valid word
                # -------------------------------------------------------------
                cellAbove = self.boardArray[currentCell.x][currentCell.y + 1]
                cellBelow = self.boardArray[currentCell.x][currentCell.y - 1]

                if not wordList.contains(self.getCellAffix(cellAbove, True) + char + self.getCellAffix(cellBelow, True)):
                    return False

            # ------------------------------------------
            # 4. Check the cells before and after the new word for word collisions
            # ------------------------------------------
            leftCell = self.boardArray[startingX - 1][startingY]
            rightCell = self.boardArray[startingX + 1][startingY]

            if not wordList.contains(self.getCellAffix(leftCell, False) + newWord + self.getCellAffix(rightCell, False)):
                return False

            # If we made it this far without returning False, the new word is valid!
            # TODO how do we actually add the word now that it is valid?
            return True

        # TODO fill this in, or find a way to make across and down both the same code.
        else:
            newWord = intersection.down
            existingWord = intersection.across

            return True

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
    Returns a str - can be empty if there was no chars or word in adjCell
    """
    def getCellAffix(self, adjCell, newIsAcross):
        # check whether the adjCell has an acrossWord, downWord, or both
        hasAcross = adjCell.acrossWord is not None
        hasDown = adjCell.downWord is not None

        if (not hasAcross) and (not hasDown):
            return str("")

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
                elif self.boardArray[x][y] is not None and ((0 > x+xShift or x+xShift >= self.WIDTH) or (0 > y+yShift or y + yShift >= self.WIDTH)):
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

"""
Method that will let us view what the crossword looks like in the terminal by printing the crossword row by row.
"""
def terminalRepresentationOfCrossword(board):
    row = []
    for y in range(len(board.boardArray)):
        for x in range(len(board.boardArray)):
            cell = board.boardArray[x][y]
            if cell is not None:
                index = cell.indexWithinWord
                row += [cell.acrossWord[index]]
            else:
                row += ['_']
        print(row)
        row = []


crossword = CrosswordRepresentation([],["HELLO"],[])
board = Board(crossword)


terminalRepresentationOfCrossword(board)

# graph = readCSV()  # from parseDictionary.py
# print(graph['A'])
# cw = bruteForce(graph)
# print(cw.across, cw.down)

