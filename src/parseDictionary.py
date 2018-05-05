from src.MakeCrossWord import *

"""
This file contains code that will create the graph of words that we use in our algorithm to help us find words that
are likely to be able to intersect with a given existing word in our crossword. It also writes this graph and the 
word list to files so that we do not have to run the code here every time we run the algorithm - we just call readCSV()
to get the graph, or read the contents of wordList.csv to get all the quarter million words in our list.
"""

# there is no way to make a final var in python, so just don't change this value
FILE_NAME = 'dictFile.csv'


"""
Method that will check how many potential intersections
there are between words. We thought we wanted to use this to create a graph, but we found a better way.
"""
def numIntersections(word1, word2):
    wordDict = {}
    count = 0
    for x in range(len(word1)):
        if word1[x] in wordDict.keys():
            wordDict[word1[x]] += 1
        else:
            wordDict[word1[x]] = 1

    for y in range(len(word2)):
        if word2[y] in wordDict.keys():
            count += wordDict[word2[y]]
    return count


"""
Creates a graph where the keys are all the letters of the alphabet, and the values are lists of words that 
contain that letter.
"""
def createGraph(wordlist):
    wordGraph = {}
    for x in ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']:
        wordGraph[x] = []

    for word in wordlist:
        word = word.upper()
        if len(word)>=2 and len(word) <= 8:
            charsInWord = set()  # It's faster to look things up in sets than it is in lists.
            for letter in word:
                if letter not in charsInWord:
                    charsInWord.add(letter)
                    wordGraph[letter].append(word)

    return wordGraph


"""
The purpose of this is so that we don't need to create a graph on a 
quarter million words every time we run the program. Writes the graph to a file that can be read out instead.
"""
def makeCSV(graph):
    file = open(FILE_NAME, 'w')
    file.write(str(graph))

    file.close()

"""
Read a CSV representation of a graph into a graph stored as a map.
"""
def readCSV():
    file = open(FILE_NAME, 'r')
    graph = eval(file.read())
    file.close()

    return graph

"""
Takes a list of words and writes it into a file so we don't have to access the API to get our word list every time
"""
# def wordListCSV():
#     file = open('wordList.csv', 'w')
#     wList = words.words()
#
#     newList = []
#     for word in wList:
#         if len(word) >= 2 and len(word) <= 8:
#             newList.append(word)
#     file.write(str(newList))

"""
Code below will create the graph and write it into a CSV file.
"""
# wlist = words.words()
# shortened = wlist[0:10000]  # shortened version of the list of a quarter million words.
# graph = createGraph(wlist)
# makeCSV(graph)

"""
Code below will write the list of words into a csv
"""
# wordListCSV()


# index = random.randint(0,len(graph.keys()))
#
# keyList = list(graph.keys())
# letterList = graph[keyList[19]]
#
# index = random.randint(0,len(letterList))

#print(letterList[index])

# print(graph['P'][0])
# word0 = 'POINTY'
#
# for x in range(len(wlist)-1):
#     if '' == wlist[x]:
#         print(wlist[x])





