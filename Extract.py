import math
import string
import logging
import io
import csv

#logging
logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
def log(message):
    print(message)


inputFile = 'dumpstateTemp.txt'
#inputFile = input("Please enter the filename IN THIS FOLDER you would like to Extract")
outputFile = 'OutputCSV.txt'

#extract important data chunk
isCopying = False
fileIndex = 0
i: int = 0
state = 0

with open(inputFile) as file:
    for line in file:

        states = ['', '[MARS]','[CONFIG LIST]']
        #           1   

        data = []
        starti = 0
        endi = 0

        #enter state 1 [MARS]
        if (line.strip() == states[1]):
            state = 1
            i = fileIndex
            starti = fileIndex
            endi = fileIndex + 34
            print(f"Changed State to: {state} becasuse of {states[state]}\nExtracting from line {starti} to line {endi}...")



        #extract MARS (state 1)
        if(state == 1): 
            #when done, set state to inactive
            if(i == endi):  
                state = 0

            data = line.split()
            

        #output if the state is active (not 0)
        if(state!=0):
            with open(outputFile, 'w') as csvfile:
                print(f"writing {data}")
                writer = csv.writer(csvfile)
                writer.writerow(data)

        #iterate fileIndex
        fileIndex += 1


    file.close()    
