import random
from src.MakeCrossWord import Board
from src.CrosswordRepresentation import CrosswordRepresentation
from src.parseDictionary import readCSV
import math
from collections import deque
from Intersection import *

"""
This file contains a class that holds the method that is our crossword generation algorithm. It also holds several
helper methods for that algorithm and for potential future algorithms that would be more optimal than the one we have
now. The executable code used to run the algorithm is down at the bottom of this file.
"""


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
        keys = list(graph.keys())
        randomIndex0 = random.randint(0, len(keys)-1)
        randomLetter = keys[randomIndex0]  # Gives us a list of words from graph[some random letter]
        wordList = graph[randomLetter]
        randomIndex1 = random.randint(0, len(wordList)-1)
        startWord = wordList[randomIndex1]

        Q = deque([])  # initialize a queue that will store each word that has been added to the crossword
        Q.append(startWord)
        allWords = []
        allWords.append(startWord)
        # initialize a crossword that contains that start word
        crossword = CrosswordRepresentation({startWord: None}, {})
        board = Board(crossword)

        # this outer loop continues until we have the desired number of words in our crossword
        currentWordIsAcross = True
        while len(Q) > 0:  # while Q is not empty
            currentWord = Q.popleft()  # removes the first element in the Queue.

            # updates currentWordIsAcross depending on whether or not
            # the current word is in the across or down dictionary keys.
            if currentWord in board.crossword.across.keys():
                currentWordIsAcross = True
            elif currentWord in board.crossword.down.keys():
                currentWordIsAcross = False

            # loops through each letter in the current word and try's to add a word on each letter.
            for x in range(0,len(currentWord),2):
                neighbors = graph[currentWord[x]] # list of all words that have the letter of currentWord[x] in them.
                for neighbor in neighbors: # Searches through all the neighbors for a potentially valid word to add.
                    newWord = neighbor
                    if currentWordIsAcross and newWord not in Q and newWord not in allWords:
                        intersection = Intersection(currentWord, newWord, x, newWord.find(currentWord[x]))
                        # print("Current word: " + currentWord + ", list: " + str(board.crossword.across))
                        firstCell = board.crossword.across[currentWord]
                        interCell = board.getCellAt(firstCell.xCoord+x, firstCell.yCoord)
                        if interCell is not None and board.addIfValid(interCell, intersection, False):
                            Q.append(newWord)
                            allWords.append(newWord)
                            board.terminalRepresentationOfCrossword()  # prints the crossword in the terminal as it is.
                            print("--------------")
                            break  # We don't want to keep looping through all the neighbors if we found a valid one.
                    elif not currentWordIsAcross and newWord not in Q and newWord not in allWords:
                        intersection = Intersection(newWord, currentWord, newWord.find(currentWord[x]), x)
                        # print("Current word: "+currentWord+", list: "+str(board.crossword.down))
                        firstCell = board.crossword.down[currentWord]
                        interCell = board.getCellAt(firstCell.xCoord, firstCell.yCoord+x)
                        if interCell is not None and board.addIfValid(interCell, intersection, True):
                            Q.append(newWord)
                            allWords.append(newWord)
                            board.terminalRepresentationOfCrossword()  # prints the crossword in the terminal as it is.
                            print("--------------")
                            break
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
    the parameters of the cells. We could use it when writing a more optimal algorithm.
    If there's a space that looks like T_T, this will return a list of words such as TOTAL that could be put in 
    there.
    Currently only works for the input of two cells. 
    """

    def fillInWords(self, cell0, cell1, cell3 = None, cell4 = None):
        graph = readCSV()
        validWordList = []
        # acrossWord = True
        list0 = graph[cell0.char] # list of words that will be parsed for valid words

        x0 = cell0.xCoord
        y0 = cell0.yCoord
        x1 = cell1.xCoord
        y1 = cell1.yCoord

        # --------------
        # This makes sure that the cell0 variable holds the cell with the smallest x coord or y coord.
        # --------------
        if x0 == x1:
            distance = int(math.fabs(y0 - y1))
            if y0 > y1:  # making sure cell0 is the first cell in the pattern
                cell = cell1
                cell1 = cell0
                cell0 = cell
        else:
            distance = int(math.fabs(x0-x1))
            if x0 > x1:
                cell = cell1
                cell1 = cell0
                cell0 = cell

        for word in list0:
            valid = False # If valid is true then a word is added to the validWordList.
            parameter = [cell0.char]  # this makes the first index of the parameter the first letter (cell0's letter)
            for x in range(distance-1):
                parameter.append('_')
            parameter.append(cell1.char) # this makes the parameter look like this [cell0 letter, None, None, cell1 letter]
            for letterIndex in range(len(word)):
                if word[letterIndex] == parameter[0] and letterIndex+distance < len(word):
                    if word[letterIndex + distance] == parameter[-1]:
                        valid = True
                        break  # this probably isn't need but could reduce time complexity by stopping the loop once a match to the parameter is found.

            if valid is True:
                validWordList.append(word)

        return validWordList


# -----------------------------------------------
# EXECUTABLE CODE TO RUN THE ALGORITHM
# -----------------------------------------------
bruteForce = BruteForceCrossword()
cw = bruteForce.bruteForce(readCSV())
cw.terminalRepresentationOfCrossword()