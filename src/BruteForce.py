import random
from MakeCrossWord import *


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
