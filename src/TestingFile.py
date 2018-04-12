import csv

dict = {}

for i in range(3):
    temp = {}
    for j in range(3):
        temp[j] = j
    dict[i] = temp

file = open('dictfile.csv', 'w')
file.write(dict)

