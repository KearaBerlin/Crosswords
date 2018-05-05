
from src.parseDictionary import *
# from nltk.corpus import words

file = open("wordList.csv", 'r')
text = file.read()
file.close()

FILE_NAME = 'dictFile.csv'


"""
Representing board with a 2D array.
"""
class Board:
    def __init__(self, crossword, ARRAY_WIDTH = 10):
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
        return len(self.crossword.inter)

    """
    So writing this method with the assumption that we have checked that it is valid to
    add the word at this position and the area around it. This method adds the word itself to the array and the down
    or across list, and to the intersections list. It does not update any neighboring words.
    """
    def addWordToArray(self, sX, sY, newWord, intersection, newWordIsAcross):

        for x in range(len(newWord)):
            if newWordIsAcross:
                self.boardArray[sX+x][sY] = self.Cell(newWord, None, sX + x, sY, x, 0)
            else:
                self.boardArray[sX][sY + x] = self.Cell(None, newWord, sX, sY + x, 0, x)

        # POSSIBLE ERROR: Sometimes, newWord will be placed right after an existing word, and in that case newWord
        # itself won't be added to the puzzle, but a combination of the esiting word and newWord will be added
        # instead. In that case, this line will put in a nonexistent across word into the puzzle.
        if newWordIsAcross:
            self.crossword.across[newWord] = self.getCellAt(sX, sY)
        else:
            self.crossword.down[newWord] = self.getCellAt(sX, sY)

    """
    Returns cell object at given x and y coordinate
    """
    def getCellAt(self, x, y):
        return self.boardArray[x][y]


    """
    Takes in an intersection and whether the word being theoretically added is an Across word. Returns true if the
    intersection would result in a valid new crossword, false otherwise. Calls another function which will add the new 
    word to underlying crossword.
    """
    def addIfValid(self, interCell, intersection, newWordIsAcross):
        copyArray = [[None for i in range(self.WIDTH)] for j in range(self.WIDTH)]

        # set the variables we will need that differ based on newWordIsAcross:
        # newWord is the word that we will try to add to the puzzle
        # startingX is the x-coord of the cell where newWord will start. startingY, endingY, etc are analogous
        if newWordIsAcross:
            newWord = intersection.across
            startingX = interCell.xCoord - intersection.acrossIndex
            startingY = interCell.yCoord
        else:
            newWord = intersection.down
            startingX = interCell.xCoord
            startingY = interCell.yCoord - intersection.downIndex

        # ----------------------------------------------
        # check whether would be out of bounds of the puzzle, and couldn't be shifted to fit
        # ----------------------------------------------
        # we calculate the literal horizontal width and the vertical height of the new word (in terms of puzzle cells)
        if newWordIsAcross:
            newWordWidth = len(newWord)
            newWordHeight = 1
        else:
            newWordWidth = 1
            newWordHeight = len(newWord)
        # we use the height and width to calculate the endingX and Y of the new word
        endingX = startingX + newWordWidth-1
        endingY = startingY + newWordHeight-1

        # returns a list of the form [xShift, yShift]
        shift = self.calculateShift(newWordWidth, newWordHeight, startingX, endingX, startingY, endingY)

        # if calculateShift() returns None, there is no valid way to fit the new word into the puzzle
        if shift is None:
            return False

        # otherwise, we shift the puzzle and adjust startingX etc as needed.
        if shift != [0, 0]:
            self.shiftElements(shift[0], shift[1])
            startingX += shift[0]
            endingX += shift[0]
            startingY += shift[1]
            endingY += shift[1]

        # ---------------------------------------------------------
        # loop through each cell that the new word would inhabit and check for collisions and conflicts
        # ---------------------------------------------------------
        for i in range(len(newWord)):

            # we calculate the new character to be added
            char = newWord[i]

            # we calculate the current x and y coords and the current cell we are checking
            if newWordIsAcross:
                currentX = startingX+i
                currentY = startingY
                currentCell = self.boardArray[currentX][currentY]
            else:
                currentX = startingX
                currentY = startingY+i
                currentCell = self.boardArray[currentX][currentY]

            # ------------------------------------------------------
            # Check whether the current cell would be overwritten, and whether that would cause a conflict
            # ------------------------------------------------------
            # we use a helper method to determine whether the current cell intersects invalidly with any existing word
            if not self.intersectionIsValid(char, newWord, startingX, startingY, currentX, currentY,
                                            currentCell, i, newWordIsAcross):
                return False

            # -------------------------------------------------------------
            # Check whether any adjacent cells will cause a conflict
            # -------------------------------------------------------------
            if not self.adjCellsValid(char, startingX, startingY, currentX, currentY, i, currentCell, newWordIsAcross):
                return False

        # ------------------------------------------
        # Check the cells before and after the new word for word collisions
        # ------------------------------------------
        if not self.endsAreValid(newWord, startingX, startingY, endingX, endingY, newWordIsAcross):
            return False

        # --------------------------------------------------------------------------
        # If we made it this far without returning False, the new word is valid! Add the word to the puzzle.
        # --------------------------------------------------------------------------
        self.addWordToArray(startingX, startingY, newWord, intersection, newWordIsAcross)
        return True

    """ 
    A helper method for addIfValid.
    Returns True or False to indicate whether overwriting currentCell with char will cause any conflicts.
    """
    def intersectionIsValid(self, char, newWord, startingX, startingY, currentX, currentY, currentCell, i, newWordIsAcross):
        # here, if the current cell we are checking is not None (meaning it holds a character), we find the word that
        # currentCell is part of (if any) that is perpendicular to newWord, and find the index within that perpendicular
        # word that we are currently at. We do the same for any word parallel to newWord that currentCell is part of.
        if newWordIsAcross:
            if currentCell is not None:
                perpendicularWordIndex = currentCell.indexInDownWord
                perpendicularIntersectingWord = currentCell.downWord
                parallelIntersectingWord = currentCell.acrossWord
        else:
            if currentCell is not None:
                perpendicularWordIndex = currentCell.indexInAcrossWord
                perpendicularIntersectingWord = currentCell.acrossWord
                parallelIntersectingWord = currentCell.downWord

        # if the new char being added is the same as the existing one, we know it is valid since no change occurs
        if currentCell is not None and char == currentCell.char:
            return True

        # otherwise, if there is a char in the currentCell already, check whether the perpendicular word is still valid
        if currentCell is not None and perpendicularIntersectingWord is not None:

            # we use a helper method to find the new word with only the new char changed from the existing word
            collidedWord = self.getCollidedWord(char, perpendicularWordIndex, perpendicularIntersectingWord)

            # if getCollidedWord() returns None, it means the newly formed word would not be valid anymore
            if collidedWord is None:
                return False

            # update the across and down dictionaries to contain the newly formed collidedWord instead of the old word
            # but only if the two words aren't the same (if they're the same, nothing needs to be updated)
            else:
                if newWordIsAcross:
                    if collidedWord != perpendicularIntersectingWord:
                        self.crossword.down[collidedWord] = self.crossword.down[perpendicularIntersectingWord]
                        self.crossword.down.pop(perpendicularIntersectingWord)
                        # update currentCell's down word
                        self.boardArray[startingX+i][startingY].downWord = collidedWord
                        # POSSIBLE ERROR: We also should be going through the Cells of the perpendicular intersecting
                        # word and updating their downWord to be the new, changed downWord. Currently they still
                        # refer to a word that is no longer in the puzzle and this is causing errors when we later try
                        # to use those references as keys in the across or down word dicts.
                else:
                    if collidedWord != perpendicularIntersectingWord:
                        self.crossword.across[collidedWord] = self.crossword.across[perpendicularIntersectingWord]
                        self.crossword.across.pop(perpendicularIntersectingWord)
                        # update currentCell's down word
                        self.boardArray[startingX][startingY+i].acrossWord = collidedWord
                        # POSSIBLE ERROR: Same error as above, but occurs when new word is a down word instead.

        # If there is a word that overlaps and is in the same direction as the new word, we will return False since it
        # is fairly complex to check whether this word will still be valid. (In the future, we could instead check.)
        if currentCell is not None and parallelIntersectingWord is not None:
            return False

        # if we got to this line without returning False, the intersection in this currentCell is valid.
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
        # if it is in the word list, return it
        else:
            return collidedWord

    """
    Helper method for addIfValid.
    Returns True if adding the new char to the currentCell would not cause conflicts in any neighboring cells;
    returns False otherwise.
    """
    def adjCellsValid(self, char, startingX, startingY, currentX, currentY, i, currentCell, newWordIsAcross):
        # first, we find the two adjacent cells to currentCell - either left and right (if the new word is vertical)
        # or above and below (if the new word is horizontal.) We make sure to check that these cells exist (are not
        # off the edge of the puzzle.)
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

        # if neither adjacent cell holds a character, there are no conflicts.
        if adjCellOne is None and adjCellTwo is None:
            return True

        # We use another helper method to calculate the "affix" for each adjacent cell - the character or word that
        # might cause a conflict with the new char being added. If an adjCell is None, the affix is ''
        if adjCellOne is not None:
            cellOneAffix = self.getCellAffix(adjCellOne, newWordIsAcross, True)
        else:
            cellOneAffix = ''
        if adjCellTwo is not None:
            cellTwoAffix = self.getCellAffix(adjCellTwo, newWordIsAcross, False)
        else:
            cellTwoAffix = ''

        # we add any affixes together with the new char to see what new word would be created by adding the char here,
        # and check to see if it is still a valid word
        affixedWord = cellOneAffix + char + cellTwoAffix
        if affixedWord not in self.wordList:
            return False

        # if it is valid, we go through and update the across and down word dictionaries to hold the correct words;
        # we also update the cells in each word that has now been changed to a new word.
        else:
            if newWordIsAcross:
                if adjCellOne is not None:
                    if adjCellOne.downWord is not None:
                        # update down-word dictionary to point to the cell where the old adjCellOne's word started
                        self.crossword.down[affixedWord] = self.crossword.down[adjCellOne.downWord]
                        # then remove the now-nonexistent down word
                        self.crossword.down.pop(adjCellOne.downWord)
                    else:
                        # update the down-word dict to point to adjCellOne itself
                        self.crossword.down[affixedWord] = adjCellOne
                # Since adjCellTwo's downword has been overwritten that downword is no longer in the crossword,
                # so we pop it off.
                if adjCellTwo is not None and adjCellTwo.downWord is not None and adjCellTwo.downWord in self.crossword.down.keys():
                    self.crossword.down.pop(adjCellTwo.downWord)
                # update the down words in the two adjCells and in currentCell
                if adjCellTwo is not None:
                    self.boardArray[currentX][currentY + 1].downWord = affixedWord
                if adjCellOne is not None:
                    self.boardArray[currentX][currentY - 1].downWord = affixedWord
                if currentCell is not None:
                    self.boardArray[startingX+i][startingY].downWord = affixedWord
                # POSSIBLE ERROR: We should be updating all the Cells in the down words of the two adjCells, so that
                # they no longer refer to an old word that no longer exists in the puzzle. This error is likely
                # causing the key errors we see, since we later pass in an old word that doesn't exist as a key.

            # this block follows much the same logic as above, but adjusted for if the new word is down instead
            else:
                if adjCellOne is not None:
                    if adjCellOne.acrossWord is not None:
                        self.crossword.across[affixedWord] = self.crossword.across[adjCellOne.acrossWord]
                        self.crossword.across.pop(adjCellOne.acrossWord)
                    else:
                        self.crossword.across[affixedWord] = adjCellOne
                if adjCellTwo is not None and adjCellTwo.acrossWord is not None and adjCellTwo.downWord in self.crossword.across.keys():
                    self.crossword.across.pop(adjCellTwo.acrossWord)
                if adjCellOne is not None:
                    self.boardArray[currentX-1][currentY].acrossWord = affixedWord
                if adjCellTwo is not None:
                    self.boardArray[currentX+1][currentY].acrossWord = affixedWord
                if currentCell is not None:
                    self.boardArray[startingX][startingY+i].acrossWord = affixedWord
                # POSSIBLE ERROR: Same error as above, but for the case where new word is down instead of across

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
    Helper method for addIfValid. Returns True if the two cells before and after the new word do not cause any
    conflicts that would make adding the new word invalid; returns False otherwise.
    """
    def endsAreValid(self, newWord, startingX, startingY, endingX, endingY, newWordIsAcross):
        # similarly to in adjCellsValid(), we find the two cells adjacent to the start and end of the new word
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

        # we only need to check for conflicts if one or both of the cells contains a char
        if startCell is not None or endCell is not None:

            # get the "affix" for both the cells (the char or word that we might need to combine with the newWord to
            # check whether putting them next to each other combines into a valid word or not)
            if startCell is not None:
                startAffix = self.getCellAffix(startCell, newWordIsAcross, True)
            else:
                startAffix = ""
            if endCell is not None:
                endAffix = self.getCellAffix(endCell, newWordIsAcross, False)
            else:
                endAffix = ""

            # combine the affixes with newWord to get the whole long word that would be formed by inserting newWord
            affixedWord = startAffix + newWord + endAffix

            # check whether this new long word is a valid word
            if affixedWord not in self.wordList:
                return False

            # if it is a valid word, update the entries in across and down dicts and in the affected Cells to match
            else:
                if newWordIsAcross:
                    if startCell is not None:
                        if startCell.acrossWord is not None:
                            # update the down-word dict to point to the startCell's word's begininning, if it exists
                            self.crossword.across[affixedWord] = self.crossword.across[startCell.acrossWord]
                            # also delete the old, now-non-existent down word
                            self.crossword.across.pop(startCell.acrossWord)
                    else:
                        # if startCell didn't have a down word, we update the dict to point to startCell itself instead
                        self.crossword.down[affixedWord] = startCell
                    # We update the start and end cells to hold the correct across word
                    if startCell is not None:
                        self.boardArray[startingX-1][startingY].acrossWord = affixedWord
                    if endCell is not None:
                        self.boardArray[endingX+1][endingY].acrossWord = affixedWord
                    # POSSIBLE ERROR: We should also be updating all the Cells in any word that startCell and endCell
                    # are a part of, so that those cells no longer reference a word that doesn't exist in the puzzle.
                    # This is probably causing key errors later when the old word is passed in to the across or down
                    # word dictionary.
                else:
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
                        self.boardArray[endingX][endingY + 1].downWord = affixedWord
                    # POSSIBLE ERROR: Same error as above.
        return True


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
    def shiftElements(self, xShift, yShift):
        shiftedArray = [[None for i in range(self.WIDTH)] for j in range(self.WIDTH)]
        for x in range(self.WIDTH):
            for y in range(self.WIDTH):
                if self.boardArray[x][y] is not None and 0 <= x+xShift < self.WIDTH and 0 <= y+yShift < self.WIDTH:
                    newX = x+xShift
                    newY = y+yShift
                    shiftedArray[newX][newY] = self.boardArray[x][y]
                    shiftedArray[newX][newY].setCoord(newX, newY)
                elif self.boardArray[x][y] is not None \
                        and ((0 > x+xShift or x+xShift >= self.WIDTH) or (0 > y+yShift or y + yShift >= self.WIDTH)):
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

