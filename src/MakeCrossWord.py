
from src.parseDictionary import *
from nltk.corpus import words
from src.BruteForce import *
from src.CrosswordRepresentation import CrosswordRepresentation
from src.Intersection import Intersection

file = open("wordList.csv", 'r')
text = file.read()
file.close()

wordList = ["HELLO", "NEW", "SWARM", "LOPS"]  # eval(text)  # words.words()

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
            self.addWordToArray(0, 0, self.startingWord, None, True)

    """
    Method that will let us view what the crossword looks like in the terminal by printing the crossword row by row.
    """
    def terminalRepresentationOfCrossword(self, usedCells = True):
        row = []
        for y in range(len(self.boardArray)):
            for x in range(len(self.boardArray)):
                cell = self.boardArray[x][y]
                if cell is not None and cell.char is not None:
                    row.append(cell.char)
                else:
                    row += ['_']
            print(row)
            row = []

    def wordCount(self):
        return len(self.crossword.across) + len(self.crossword.down)

    def numIntersections(self):
        return len(self.crossword.intersections)

    """
    So writing this method with the assumption that we have checked that it is valid to
    add the word at this position and the area around it. This method adds the word itself to the array and the down
    or across list, and to the intersections list. It does not update any neighboring words.
    """
    def addWordToArray(self, sX, sY, newWord, intersection, newWordIsAcross):
        if intersection is not None:
            self.crossword.inter.append(intersection)
        if newWordIsAcross:
            self.crossword.across.append(newWord)
        else:
            self.crossword.down.append(newWord)

        for x in range(len(newWord)):
            if newWordIsAcross:
                self.boardArray[sX+x][sY] = self.Cell(newWord, None, sX + x, sY, x, 0)
            else:
                self.boardArray[sX][sY + x] = self.Cell(None, newWord, sX, sY + x, 0, x)

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
    def addIfValid(self, interCell, intersection, newWordIsAcross):
        copyArray = [[None for i in range(self.WIDTH)] for j in range(self.WIDTH)]

        # set the variables we will need that differ based on newWordIsAcross
        if newWordIsAcross:
            newWord = intersection.across
            existingWord = intersection.down
            startingX = interCell.x - intersection.acrossIndex
            startingY = interCell.y
        else:
            newWord = intersection.down
            existingWord = intersection.across
            startingX = interCell.x
            startingY = interCell.y - intersection.downIndex

        # ----------------------------------------------
        # 1. check whether would be out of bounds of the puzzle, and couldn't be shifted to fit
        # ----------------------------------------------
        if newWordIsAcross:
            newWordWidth = len(newWord)
            newWordHeight = 1
        else:
            newWordWidth = 1
            newWordHeight = len(newWord)
        endingX = startingX + newWordWidth
        endingY = startingY + newWordHeight

        shift = self.getShift(newWordWidth, newWordHeight, startingX, endingX, startingY, endingY)

        if shift is None:
            return False
        if shift != [0, 0]:
            self.shiftElements(shift[0], shift[1])

        # ---------------------------------------------------------
        # 2. loop through each cell that the new word would inhabit
        # ---------------------------------------------------------
        for i in range(len(newWord)):
            if newWordIsAcross:
                currentCell = self.boardArray[startingX+i][startingY]
                perpendicularWordIndex = currentCell.indexInDownWord
                perpendicularIntersectingWord = currentCell.downWord
                parallelIntersectingWord = currentCell.acrossWord
                parallelWordIndex = currentCell.indexInAcrossWord
            else:
                currentCell = self.boardArray[startingX][startingY+i]
                perpendicularWordIndex = currentCell.indexInAcrossWord
                perpendicularIntersectingWord = currentCell.acrossWord
                parallelIntersectingWord = currentCell.downWord
                parallelWordIndex = currentCell.indexInDownWord

            char = newWord[i]

            # ------------------------------------------------------
            # 3. check whether this cell is part of an existing word
            # ------------------------------------------------------
            # check the perpendicular word, if any
            if perpendicularIntersectingWord is not None:
                if not self.collidedWordIsValid(char, perpendicularWordIndex, perpendicularIntersectingWord):
                    return False
            # If there is a word that overlaps and is in the same direction as the new word, for now we will just
            # return False.
            if parallelIntersectingWord is not None:
                return False

            # -------------------------------------------------------------
            # 4. Check whether the word containing new char and any affixes from above and/or below is a valid word
            # -------------------------------------------------------------
            if newWordIsAcross:
                adjCellOne = self.boardArray[currentCell.x][currentCell.y + 1]
                adjCellTwo = self.boardArray[currentCell.x][currentCell.y - 1]
            else:
                adjCellOne = self.boardArray[currentCell.x+1][currentCell.y]
                adjCellTwo = self.boardArray[currentCell.x-1][currentCell.y]

            affixedWord = self.getCellAffix(adjCellOne, True) + char + self.getCellAffix(adjCellTwo, True)
            if not affixedWord in self.wordList:
                return False

        # ------------------------------------------
        # 5. Check the cells before and after the new word for word collisions
        # ------------------------------------------
        if newWordIsAcross:
            startCell = self.boardArray[startingX - 1][startingY]
            endCell = self.boardArray[startingX + 1][startingY]
        else:
            startCell = self.boardArray[startingX][startingY - 1]
            endCell = self.boardArray[startingX][startingY + 1]

        affixedWord = self.getCellAffix(startCell, newWordIsAcross) + newWord + self.getCellAffix(endCell, newWordIsAcross)
        if affixedWord not in wordList:
            return False

        # --------------------------------------------------------------------------
        # 6. If we made it this far without returning False, the new word is valid!
        # --------------------------------------------------------------------------
        # TODO how do we actually add the word now that it is valid? Maybe this can be done in addWordToArray() method.
        self.addWordToArray(startingX, startingY, newWord, newWordIsAcross)
        return True

    """
    Helper method for addIfValid. Returns whether a new word with a certain character changed is still a valid word.
    This is only meant to check words that are perpendicular to the new word being added. Client code should check
    the validity of any word that is parallel to the added word, since that will involve multiple new cells 
    simultaneously.
    """
    def collidedWordIsValid(self, char, perpendicularWordIndex, perpendicularWord):
        # case 1: adding char as index 0
        if perpendicularWordIndex == 0:
            collidedWord = char + perpendicularWord[perpendicularWordIndex+1:]
        # case 2: adding char as last index
        elif perpendicularWordIndex == len(perpendicularWord)-1:
            collidedWord = perpendicularWord[:len(perpendicularWord)-1] + char
        # case 3: adding char somewhere in the middle
        else:
            collidedWord = perpendicularWord[:perpendicularWordIndex] + char \
                           + perpendicularWord[perpendicularWordIndex+1:]

        # check whether this word is in our word list
        if collidedWord not in wordList:
            return False
        else:
            return True


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
                ret = str(adjCell.acrossWord[adjCell.indexInAcrossWord])
                return ret
            elif hasDown:
                # whether it has both or only down, only return the whole word above
                return str(adjCell.downWord)
        else:
            # this is a very similar idea to above, but now adjCell is just to the right or left of new character.
            if hasDown and not hasAcross:
                ret = str(adjCell.downWord[adjCell.indexInDownWord])
                return ret
            elif hasAcross:
                return str(adjCell.acrossWord)

    """
    Helper method for addIfValid. Computes and returns a length-2 array in the form [x, y] of the needed amount to 
    shift the puzzle to fit the new word.
    If there is no way to fit the word, returns None. Returns [0, 0] if the puzzle does not need to be shifted.
    """
    def calculateShift(self, newWordWidth, newWordHeight, startingX, endingX, startingY, endingY):
        # if the word is too long to fit in the puzzle at all, forget about it
        if newWordWidth > self.WIDTH or newWordHeight > self.WIDTH:
            return None

        xShift = 0
        yShift = 0

        if startingX < 0:
            # check if there are enough empty columns to shift the puzzle
            if self.getEmptyColsToRight() >= abs(startingX):
                xShift = abs(startingX)
            else:
                return None
        if endingX > self.WIDTH - 1:
            # same check, but for the right instead of left side of the puzzle.
            if self.getEmptyColsToLeft() >= abs(self.WIDTH - 1 - endingX):
                xShift = self.WIDTH - 1 - endingX
            else:
                return None
        if startingY < 0:
            # check the top of the puzzle
            if self.getEmptyRowsBelow() >= abs(startingY):
                yShift = abs(startingY)
            else:
                return None
        if endingY > self.WIDTH - 1:
            # check the bottom of the puzzle
            if self.getEmptyRowsAbove() >= abs(self.WIDTH - 1 - endingY):
                yShift = self.WIDTH - 1 - endingY
            else:
                return None

        return [xShift, yShift]


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

    def getEmptyRowsAbove(self):
        row = 0
        count = 0
        while row < self.WIDTH and self.rowIsEmpty(row):
            row += 1
            count += 1
        return count

    def getEmptyRowsBelow(self):
        row = self.WIDTH - 1
        count = 0
        while row >= 0 and self.rowIsEmpty(row):
            count += 1
            row -= 1
        return count

    def getEmptyColsToLeft(self):
        col = 0
        count = 0
        while col < self.WIDTH and self.colIsEmpty(col):
            col += 1
            count += 1
        return count

    def getEmptyColsToRight(self):
        col = self.WIDTH - 1
        count = 0
        while col >= 0 and self.colIsEmpty(col):
            col -= 1
            count += 1
        return count

    class Cell:
        def __init__(self, acrossWord, downWord, x, y, indexInAcrossWord, indexInDownWord):
            self.acrossWord = acrossWord
            self.downWord = downWord
            self.xCoord = x
            self.yCoord = y
            self.indexInAcrossWord = indexInAcrossWord
            self.indexInDownWord = indexInDownWord
            if self.acrossWord is not None:
                self.char = self.acrossWord[self.indexInAcrossWord]
            elif self.downWord is not None:
                self.char = self.downWord[self.indexInDownWord]

        """
        Setter method for the coordinates of the cell.
        Will use this when we shift the array or certain cells.
        """
        def setCoord(self, newX, newY):
            self.xCoord = newX
            self.yCoord = newY



# Commented code below is just an example of how we would use the Intersection class.
# listA = ["attack", "sleep", "awake"]
# listD = ["apple", "koala"]
# inter1 = Intersection("attack", "apple", 3, 0)
# inter2 = Intersection("attack", "koala", 5, 0)
# inter3 = Intersection("sleep", "apple", 4, 2)
# inter4 = Intersection("awake","apple", 4, 4)
#
# interTotal = [inter1,inter2, inter3, inter4]




# graph = readCSV()  # from parseDictionary.py
# print(graph['A'])
# bF = BruteForceCrossword()
# cw = bF.bruteForce(graph)
# print(cw.across, cw.down)

