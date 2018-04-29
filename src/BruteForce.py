import random
from MakeCrossWord import *
import math


class BruteForceCrossword:
    def __init__(self):
        self.name = "Brute Force"

    """
    Brute force algorithm to pick words for the crossword
    1. Pick random word
    2. Examine neighbors
    """
    def bruteForce(self, graph):

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
                if self.addNeighbor(currentWord, currentWordIsAcross, neighborWord, board):
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
    def addNeighbor(self, currentWord, currentWordIsAcross, neighborWord, board):

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
    This method will take in cells and parse our alphabet graph and return a list of words that can form a word given
    the parameters of the cells. 
    
    So if there's a space that looks like T_T, this will return a list of words such as TOTAL that could be put in 
    there.
    """

    def fillInWords(self, cell0, cell1, cell3 = None, cell4 = None):
        graph = readCSV()
        validWordList = []
        acrossWord = True
        list0 = graph[cell0.acrossWord[cell0.indexInAcrossWord]] # list of words that will be parsed for valid words

        x0 = cell0.xCoord
        y0 = cell0.yCoord
        x1 = cell1.xCoord
        y1 = cell1.xCoord

        # --------------
        # This makes sure that the cell0 variable holds the cell with the smallest x coord or y coord.
        # --------------
        if x0 == x1:
            acrossWord = False
            distance = math.fabs(y0 - y1)
            if y0 > y1: # making sure cell0 is the first cell in the pattern
                cell = cell1
                cell1 = cell0
                cell0 = cell
        else:
            distance = math.fabs(x0-x1)
            if x0 > x1:
                cell = cell1
                cell1 = cell0
                cell0 = cell


        for word in list0:
            valid = False # If valid is true then a word is added to the validWordList.
            parameter = [cell0.acrossWord[cell0.indexInAcrossWord]]  # this makes the first index of the parameter the first letter (cell0's letter)

            if acrossWord:

                for x in range(distance-2):
                    parameter.append(None)
                parameter.append(cell1.acrossWord[cell1.indexInAcrossWord]) # this
                for letterIndex in range(len(word)):
                    if word[letterIndex] == parameter[0] and letterIndex+distance < len(word):
                        if word[letterIndex + distance] == parameter[-1]:
                            valid = True
                            # break
            else:  # code for if we are getting words for a down position in the crossword
                for x in range(distance-2):
                    parameter.append(None)
                parameter.append(cell1.acrossWord[cell1.indexInAcrossWord])


            if valid is True:
                validWordList.append(word)







        return validWordList