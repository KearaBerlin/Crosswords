from PyDictionary import PyDictionary
from nltk.corpus import words
import csv

dictionary=PyDictionary() # will use this at some point to look up the meaning of words.


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
                if y!=x and len(y)>=4 and intersections >= 1:
                    valueList.append([y, intersections])
            wordGraph[x] = valueList


    return wordGraph



"""
Method that will transfer the graph from createGraph() to a CSV file.
The purpose of this is so that we don't need to create a graph on a 
quarter million words everytime we run the program. 

The CSV file will be written with each row representing a value and it's keys as strings
"""
def makeCSV(graph):
    file = open('dictFile.csv', 'w')
    for k in graph.keys():

        # form the string encoding the value at this key
        listString = ""
        for tuple in graph[k]:
            listString += tuple[0] + ":" + str(tuple[1]) + ", "

        # encode the whole entry, including key
        stringToWrite = k + ' : ' + listString + '\n'
        file.write(stringToWrite)

    file.close()



"""
Method that will also write the graph to a CSV but as the data type Dictionary 
rather than string. 

Currently not working yet...
"""
def makeDictCSV(graph):
    file = open('dictFile.csv', 'w')
    wr = csv.DictWriter(file, fieldnames='fieldnames')

    for k in graph.keys():
        # form the string encoding the value at this key
        listString = []
        value = []
        stringToWrite = {}
        for tuple in graph[k]:
            value += [tuple]
        # encode the whole entry, including key
        stringToWrite = {k: value}
        # wr.writerow(stringToWrite)
        # wr.writerow('\n')
        print({k: value})
        wr.writerow({k: value})

    file.close()



wlist = words.words()
shortened = wlist[0:1000] # shortened version of the list of a quarter million words.

graphFile = createGraph(shortened)
makeCSV(graphFile)







