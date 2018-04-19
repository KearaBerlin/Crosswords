from PyDictionary import PyDictionary
from nltk.corpus import words
from src.MakeCrossWord import *

# there is no way to make a final var in python, so just don't change this value
FILE_NAME = 'dictFile.csv'

dictionary = PyDictionary()  # will use this at some point to look up the meaning of words.


"""
Method that will check how many potential intersections
there are between words
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
Method that will create a graph with each word being a key and the value being
the words that have an intersection of some kind with it and the number of intersections.
Will use method numIntersections() above to compute the number of intersections.
"""
def createGraph(wordlist):
    wordGraph = {}

    for x in wordlist:
        x = x.upper()
        if len(x)>=4:
            wordGraph[x] = []
            valueList = []

            for y in wordlist:
                y = y.upper()
                intersections = numIntersections(x,y)
                if y != x and len(y) >= 4 and intersections >= 1:
                    valueList.append([y, intersections])
            wordGraph[x] = valueList

    return wordGraph



"""
The purpose of this is so that we don't need to create a graph on a 
quarter million words every time we run the program. 
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

    # eval() will literally execute the Python represented by the string.
    # It is VERY insecure but we don't mind for this little app
    graph = eval(file.read())
    file.close()

    return graph


# wlist = words.words()
# shortened = wlist[0:100]  # shortened version of the list of a quarter million words.

# words for Keara to use to test since we don't have the words in a big file yet.
shortened = ['able', 'apple', 'ant', 'bear', 'brown', 'cat', 'crustacean', 'dog', 'dandruff', 'eatery', 'felt', 'fire',
             'good', 'hello', 'ibis', 'interesting', 'jewel', 'koala', 'lump', 'lime', 'moo', 'nantucket', 'opal',
             'oh', 'prime', 'quick', 'rhythm', 'so', 'spire', 'team', 'understanding', 'velociraptor', 'water', 'xylophone', 'zebra']

graph = createGraph(shortened)
makeCSV(graph)

graphFromCSV = readCSV()









