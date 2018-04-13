from PyDictionary import PyDictionary
from nltk.corpus import words
import csv

# there is no way to make a final var in python, so just don't change this value
FILE_NAME = 'dictFile.csv'

dictionary=PyDictionary()  # will use this at some point to look up the meaning of words.


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

        if len(x)>=4:
            wordGraph[x] = []
            valueList = []

            for y in wordlist:
                intersections = numIntersections(x,y)
                if y != x and len(y) >= 4 and intersections >= 1:
                    valueList.append([y, intersections])
            wordGraph[x] = valueList

    return wordGraph



"""
Method that will transfer the graph from createGraph() to a CSV file.
The purpose of this is so that we don't need to create a graph on a 
quarter million words every time we run the program. 
"""
def makeCSV(graph):
    file = open(FILE_NAME, 'w')
    file.write(str(graph))
    # for k in graph.keys():
    #
    #     # form the string encoding the value at this key
    #     listString = ""
    #     for tuple in graph[k]:
    #         listString += tuple[0] + ":" + str(tuple[1]) + ", "
    #
    #     # encode the whole entry, including key
    #     # NOTE: I deleted the + '\n' but that made everything work, so I think it automatically adds a newline
    #     # and our newline was redundant.
    #     stringToWrite = k + ' : ' + listString + '\n'
    #     file.write(stringToWrite)

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

    # #read all lines into content w/o newline chars
    # content = file.readlines()
    #
    # print(len(content))
    #
    # # read each line into a key-value pair in the map
    # for newLine in content:
    #     newLine = newLine.strip('\n')
    #
    #     # we aren't at the end of the file yet, so get the key word on this line
    #     keyEnd = newLine.find(" : ", 1)
    #     key = newLine[0:keyEnd]
    #
    #     # get all the neighbor nodes and parse them into a list of length-2-lists
    #     neighbors = newLine[keyEnd+3:].split(", ")[-1]
    #     tuples = []
    #     for neighbor in neighbors:
    #         vals = neighbor.split(":")
    #         tuple = [vals[0], vals[1]]
    #         tuples.append(tuple)
    #
    #     # add the key and its list of lists to the map
    #     graph[key] = tuples

    return graph

wlist = words.words()
shortened = wlist[0:1000]  # shortened version of the list of a quarter million words.

# words for Keara to use to test since we don't have the words in a big file yet.
# shortened = ['able', 'apple', 'ant', 'bear', 'brown', 'cat', 'crustacean', 'dog', 'dandruff', 'eatery', 'felt', 'fire',
#              'good', 'hello', 'ibis', 'interesting', 'jewel', 'koala', 'lump', 'lime', 'moo', 'nantucket', 'opal',
#              'oh', 'prime', 'quick', 'rhythm', 'so', 'spire', 'team', 'understanding', 'velociraptor', 'water', 'xylophone', 'zebra']

graph = createGraph(shortened)
makeCSV(graph)

graphFromCSV = readCSV()








