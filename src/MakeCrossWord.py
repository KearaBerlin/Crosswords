
from src.parseDictionary import *
# from nltk.corpus import words
from src.BruteForce import *
from src.CrosswordRepresentation import CrosswordRepresentation
from src.Intersection import Intersection

file = open("wordList.csv", 'r')
text = file.read()
file.close()

testWordList = ["HELLO", "HELP", "NEW", "SWARM", "LOPS"]  # eval(text)  # words.words()

FILE_NAME = 'dictFile.csv'


"""
Representing board with a 2D array.
"""
class Board:
    def __init__(self, crossword, ARRAY_WIDTH = 30):
        self.WIDTH = ARRAY_WIDTH
        self.crossword = crossword
        self.wordList = text
        # initialize array with None
        self.boardArray = [[None for i in range(self.WIDTH)] for j in range(self.WIDTH)]

        if len(crossword.across.keys()) != 0:

            self.startingWord = list(crossword.across.keys())[0]  # First word will always be the first index of the across list.
            # puts the starting word the top left corner of the array (0,0) to (0,len(word)-1)
            self.addWordToArray(0, 0, self.startingWord, None, True)
            self.crossword.across[self.startingWord] = self.getCellAt(0,0)

    """
    Method that will let us view what the crossword looks like in the terminal by printing the crossword row by row.
    """
    def terminalRepresentationOfCrossword(self, usedCells = True):
        row = []
        for y in range(len(self.boardArray)):
            for x in range(len(self.boardArray)):
                cell = self.boardArray[x][y]
                if cell is not None and type(cell) is self.Cell:
                    row.append(cell.char)
                else:
                    row += ['_']
            print(row)
            row = []

    def wordCount(self):
        return len(self.crossword.across.keys()) + len(self.crossword.down.keys())

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

        for x in range(len(newWord)):
            if newWordIsAcross:
                self.boardArray[sX+x][sY] = self.Cell(newWord, None, sX + x, sY, x, 0)
            else:
                self.boardArray[sX][sY + x] = self.Cell(None, newWord, sX, sY + x, 0, x)

        if newWordIsAcross:
            self.crossword.across[newWord] = self.getCellAt(sX,sY)
        else:
            self.crossword.down[newWord] = self.getCellAt(sX,sY)

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
            startingX = interCell.xCoord - intersection.acrossIndex
            startingY = interCell.yCoord
        else:
            newWord = intersection.down
            existingWord = intersection.across
            startingX = interCell.xCoord
            startingY = interCell.yCoord - intersection.downIndex

        # ----------------------------------------------
        # 1. check whether would be out of bounds of the puzzle, and couldn't be shifted to fit
        # ----------------------------------------------
        if newWordIsAcross:
            newWordWidth = len(newWord)
            newWordHeight = 1
        else:
            newWordWidth = 1
            newWordHeight = len(newWord)
        endingX = startingX + newWordWidth-1
        endingY = startingY + newWordHeight-1

        shift = self.calculateShift(newWordWidth, newWordHeight, startingX, endingX, startingY, endingY)

        if shift is None:
            return False
        if shift != [0, 0]:
            self.shiftElements(shift[0], shift[1])
            startingX += shift[0]
            endingX += shift[0]
            startingY += shift[1]
            endingY += shift[1]

        # ---------------------------------------------------------
        # 2. loop through each cell that the new word would inhabit
        # ---------------------------------------------------------
        for i in range(len(newWord)):
            if newWordIsAcross:
                currentX = startingX+i
                currentY = startingY
                currentCell = self.boardArray[currentX][currentY]
                if currentCell is not None:
                    perpendicularWordIndex = currentCell.indexInDownWord
                    perpendicularIntersectingWord = currentCell.downWord
                    parallelIntersectingWord = currentCell.acrossWord
                    parallelWordIndex = currentCell.indexInAcrossWord
            else:
                currentX = startingX
                currentY = startingY+i
                currentCell = self.boardArray[currentX][currentY]
                if currentCell is not None:
                    perpendicularWordIndex = currentCell.indexInAcrossWord
                    perpendicularIntersectingWord = currentCell.acrossWord
                    parallelIntersectingWord = currentCell.downWord
                    parallelWordIndex = currentCell.indexInDownWord

            char = newWord[i]
            if currentCell is not None and char == currentCell.char:
                continue

            # ------------------------------------------------------
            # 3. check whether this cell is part of an existing word
            # ------------------------------------------------------
            # check the perpendicular word, if any
            if currentCell is not None and perpendicularIntersectingWord is not None:
                collidedWord = self.getCollidedWord(char, perpendicularWordIndex, perpendicularIntersectingWord)
                if collidedWord is None:
                    return False
                else:  # so this was originally elif but that didn't make sense
                    # update the collided word so it has the right listing in across or down and in intersections.
                    if newWordIsAcross:
                        # update the crossword's down word list
                        if collidedWord != perpendicularIntersectingWord:
                            self.crossword.down[collidedWord] = self.crossword.down[perpendicularIntersectingWord]
                            self.crossword.down.pop(perpendicularIntersectingWord)
                            # update this cell's down word
                            self.boardArray[startingX+i][startingY].downWord = collidedWord
                            # now update the crossword's intersections list by iterating through the list
                            newIntersection = Intersection(newWord, collidedWord, i, perpendicularWordIndex)
                            if len(self.crossword.inter) == 0:
                                self.crossword.inter.append(newIntersection)
                            else:
                                for j in range(len(self.crossword.inter)-1):
                                    if self.crossword.inter[j].indexInAcrossWord == i:
                                        self.crossword.inter[j] = newIntersection
                                    break
                    else:
                        if collidedWord != perpendicularIntersectingWord:
                            self.crossword.across[collidedWord] = self.crossword.across[perpendicularIntersectingWord]
                            self.crossword.across.pop(perpendicularIntersectingWord)

                            self.boardArray[startingX][startingY+i].acrossWord = collidedWord
                            newIntersection = Intersection(collidedWord, newWord, perpendicularWordIndex, i)
                            if len(self.crossword.inter) == 0:
                                self.crossword.inter.append(newIntersection)
                            else:
                                for j in range(len(self.crossword.inter)-1):
                                    if self.crossword.inter[j].indexInDownWord == i:
                                        self.crossword.inter[j] = newIntersection
                                    break

            # If there is a word that overlaps and is in the same direction as the new word, for now we will just
            # return False.
            if currentCell is not None and parallelIntersectingWord is not None:
                return False

            # -------------------------------------------------------------
            # 4. Check whether the word containing new char and any affixes from adjacent cells is a valid word
            # -------------------------------------------------------------
            adjCellOne = None
            adjCellTwo = None
            if newWordIsAcross:
                if currentY + 1 <= self.WIDTH - 1:
                    adjCellTwo = self.boardArray[currentX][currentY + 1]
                if currentY - 1 >= 0:
                    adjCellOne = self.boardArray[currentX][currentY - 1]
            else:
                if currentX+1 <= self.WIDTH - 1:
                    adjCellTwo = self.boardArray[currentX+1][currentY]
                if currentX-1 >= 0:
                    adjCellOne = self.boardArray[currentX-1][currentY]

            if adjCellOne is None and adjCellTwo is None:
                continue  # Because this step was the last one in the loop, and no affixes were found.

            if adjCellOne is not None:
                cellOneAffix = self.getCellAffix(adjCellOne, newWordIsAcross, True)
            else:
                cellOneAffix = ''
            if adjCellTwo is not None:
                cellTwoAffix = self.getCellAffix(adjCellTwo, newWordIsAcross, False)
            else:
                cellTwoAffix = ''
            affixedWord = cellOneAffix + char + cellTwoAffix
            if affixedWord not in self.wordList:
                return False
            else:
                # we will need to delete both neighboring words and add the one new total word to all the lists.
                if newWordIsAcross:
                    # delete any old down words from crossword's down word dictionary
                    if adjCellOne is not None and adjCellOne.downWord is not None:
                        # update crossword down dict first if needed
                        self.crossword.down[affixedWord] = self.crossword.down[adjCellOne.downWord]
                        self.crossword.down.pop(adjCellOne.downWord)
                    if adjCellTwo is not None and adjCellTwo.downWord is not None:
                        self.crossword.down.pop(adjCellTwo.downWord)
                    # update the down words in the three cells
                    if adjCellTwo is not None:
                        self.boardArray[currentCell.xCoord][currentCell.yCoord + 1].downWord = affixedWord
                    if adjCellOne is not None:
                        self.boardArray[currentCell.xCoord][currentCell.yCoord - 1].downWord = affixedWord
                    self.boardArray[startingX+i][startingY].downWord = affixedWord
                    # udpate the crosswords down word dict if we didn't already
                    if adjCellOne is not None and adjCellOne.downWord is None:
                        self.crossword.down[affixedWord] = adjCellOne
                else:
                    if adjCellOne is not None and adjCellOne.acrossWord is not None:
                        self.crossword.across[affixedWord] = self.crossword.across[adjCellOne.acrossWord]
                        self.crossword.across.pop(adjCellOne.acrossWord)
                    if adjCellTwo is not None and adjCellTwo.acrossWord is not None:
                        self.crossword.across.pop(adjCellTwo.acrossWord)
                    if adjCellOne is not None:
                        self.boardArray[currentCell.xCoord-1][currentCell.yCoord].acrossWord = affixedWord
                    if adjCellTwo is not None:
                        self.boardArray[currentCell.xCoord+1][currentCell.yCoord].acrossWord = affixedWord
                        self.boardArray[startingX][startingY+i].acrossWord = affixedWord
                    if adjCellOne is not None and adjCellOne.acrossWord is None:
                        self.crossword.across[affixedWord] = adjCellOne

        # ------------------------------------------
        # 5. Check the cells before and after the new word for word collisions
        # ------------------------------------------
        startCell = None
        endCell = None
        if newWordIsAcross:
            if startingX-1 >= 0:
                startCell = self.boardArray[startingX - 1][startingY]
            if endingX+1 <= self.WIDTH-1:
                endCell = self.boardArray[endingX + 1][endingY]
        else:
            if startingY-1 >= 0:
                startCell = self.boardArray[startingX][startingY - 1]
            if endingY+1 <= self.WIDTH-1:
                endCell = self.boardArray[endingY][endingY + 1]

        if startCell is not None or endCell is not None:

            if startCell is not None:
                startAffix = self.getCellAffix(startCell, newWordIsAcross, True)
            else:
                startAffix = ""
            if endCell is not None:
                endAffix = self.getCellAffix(endCell, newWordIsAcross, False)
            else:
                endAffix = ""
            affixedWord = startAffix + newWord + endAffix

            if affixedWord not in self.wordList:
                return False
            else:
                if newWordIsAcross:
                    if startCell is not None and startCell.acrossWord is not None:
                        self.crossword.across[affixedWord] = self.crossword.across[startCell.acrossWord]
                        self.crossword.across.pop(startCell.acrossWord)
                    else:
                        self.crossword.down[affixedWord] = startCell
                    if startCell is not None:
                        self.boardArray[startingX+1][startingY].acrossWord = affixedWord
                    if endCell is not None:
                        self.boardArray[startingX-1][startingY].acrossWord = affixedWord
                else:
                    # we remove any old down words from the crossword down dict
                    if startCell is not None and startCell.downWord is not None:
                        # update the crossword down dict first
                        self.crossword.down[affixedWord] = self.crossword.down[startCell.downWord]
                        self.crossword.down.pop(startCell.downWord)
                    if endCell is not None and endCell.downWord is not None:
                        self.crossword.down.pop(endCell.downWord)
                    # add the new down word to crossword down dict if we didn't already
                    if startCell is not None and startCell.downWord is None:
                        self.crossword.down[affixedWord] = startCell
                    # update the two cells (all the new cells will be updated in another method, addWordToArray() )
                    if startCell is not None:
                        self.boardArray[startingX][startingY - 1].downWord = affixedWord
                    if endCell is not None:
                        self.boardArray[startingX][startingY + 1].downWord = affixedWord

        # --------------------------------------------------------------------------
        # 6. If we made it this far without returning False, the new word is valid!
        # --------------------------------------------------------------------------
        self.addWordToArray(startingX, startingY, newWord, intersection, newWordIsAcross)
        return True

    """
    Helper method for addIfValid. Returns (if there is a valid one) the new word with a certain character changed. If
     that new word is not a valid word, this method returns None.
    This is only meant to check words that are perpendicular to the new word being added. Client code should check
    the validity of any word that is parallel to the added word, since that will involve multiple new cells 
    simultaneously. (We decided to ignore them, in fact).
    """
    def getCollidedWord(self, char, perpendicularWordIndex, perpendicularWord):
        # case 1: adding char as index 0
        if perpendicularWordIndex == 0:
            collidedWord = char + perpendicularWord[1:]
        # case 2: adding char as last index
        elif perpendicularWordIndex == len(perpendicularWord)-1:
            collidedWord = perpendicularWord[:len(perpendicularWord)-1] + char
        # case 3: adding char somewhere in the middle
        else:
            collidedWord = perpendicularWord[:perpendicularWordIndex] + char \
                           + perpendicularWord[perpendicularWordIndex+1:]

        # check whether this word is in our word list
        if collidedWord not in self.wordList:
            return None
        else:
            return collidedWord


    """
    Helper method for addIfValid. Takes in a Cell adjacent to a Cell that would be part of the new word being added.
    Returns the character(s) that should be added to the character in that new cell, to get a word that can be checked
    whether it is in the quarter million word list. The client code should know whether the returned chars go after or
    before the new char, and should also perform the check in the word list etc. This method simply returns an affix.
    adjCell - a Cell representing the Cell that is directly adjacent to the new character being added
    newIsAcross - a boolean stating whether the new word being added is across or down
    Returns a str - can be empty if there was no chars or word in adjCell
    """
    def getCellAffix(self, adjCell, newIsAcross, newIsToLeft):
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
                # whether it has both or only down, only return the part of the word that is above (minus the new char)
                word = adjCell.downWord
                if newIsToLeft:
                    return str(word[:adjCell.indexInDownWord+1])
                else:
                    return str(word[adjCell.indexInDownWord:])
        else:
            # this is a very similar idea to above, but now adjCell is just to the right or left of new character.
            if hasDown and not hasAcross:
                ret = str(adjCell.downWord[adjCell.indexInDownWord])
                return ret
            elif hasAcross:
                word = adjCell.acrossWord
                if newIsToLeft:
                    return str(word[:adjCell.indexInAcrossWord+1])  # Do we need the +1 - is syntax inclusive:exclusive?
                else:
                    return str(word[adjCell.indexInAcrossWord:])

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

