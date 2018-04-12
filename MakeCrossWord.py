import csv


"""
The plan is:
1. Read from the CSV file and choose a random word.
2. Build the crossword with that word.
3. Select the next words that work best for completing the cross word. 
4. Continue 3 and 4 until we have the crossword. 
"""

with open('dictFile.csv', 'r') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=' ')
    count = 0
    for row in spamreader:
        count+=1
        print(row)

