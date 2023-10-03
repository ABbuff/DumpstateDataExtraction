import math
import string
import logging
import io
import csv

#debugging
debug = False
print()

inputFile = 'dumpstateTemp.txt'
#inputFile = input("Please enter the filename IN THIS FOLDER you would like to Extract")
outputFile = 'OutputCSV.csv'

#extract important data chunk
specialTitle = False
fileIndex = 0


with open(outputFile,'w',newline='') as writefile,open(inputFile,newline='') as readfile:
    writer = csv.writer(writefile)
    
    
    i = 0
    state = 0
    processNum = 0
    starti = 0
    for line in readfile:

    #PRELIMINARY----------------------------------------------------------
        states = ['',                                   #0  just read line
                  '[MARS]',                             #1
                  '[CONFIG LIST]',                      #2
                  'Process usage summary',              #3
                  '[Batterystats Collector]',           #4
                  'Daily Summary'                       #5
                  ]
        
        data = ['']
    #/////////////////////////////////////////////////////////////////////

    #SET STATE------------------------------------------------------------   
        #enter state 1 [MARS]
        if (line.strip() == states[1]):
            state = 1
            i = fileIndex
            starti = fileIndex
            print(f"--Changed State to: {state} becasuse of {states[state]}\nExtracting from line {starti}...")

        #enter state 2 [CONFIG LIST]
        if (line.strip() == states[2]):
            state = 2
            i = fileIndex
            starti = fileIndex
            #handle special title
            specialTitle = True
            writer.writerows([[states[state]], ['Boot Number', 'Date/Time']])
            print(f"--Changed State to: {state} w/ special title becasuse of {states[state]}\nExtracting from line {starti}...")

        #enter state 3 (Process usage summary)
        if (line.strip()[:21] == states[3]):        #[:21] take the first 21 characters
            state = 3
            processNum = 0
            i = fileIndex
            starti = fileIndex
            #handle special title
            specialTitle = True
            writer.writerow([line])
            print(f"--Changed State to: {state} w/ special title becasuse of {states[state]}\nExtracting from line {starti}...")

        #enter state 4 [Batterystats Collector]
        if (line.strip() == states[4]):
            state = 4
            processNum = 0
            i = fileIndex
            starti = fileIndex
            #handle special title
            specialTitle = True
            writer.writerow([line])
            print(f"--Changed State to: {state} w/ special title becasuse of {states[state]}\nExtracting from line {starti}...")

        #enter state 5 (Daily Summary)
        if (line.strip() == states[5]):
            state = 5
            processNum = 0
            i = fileIndex
            starti = fileIndex
            #handle special title
            specialTitle = True
            writer.writerow([])
            writer.writerow([line])
            print(f"--Changed State to: {state} w/ special title becasuse of {states[state]}\nExtracting from line {starti}...")


        #debug info
        if(debug):
            print(f"fileIndex: {fileIndex} | i: {i} | state: {state}")
    #/////////////////////////////////////////////////////////////////////

    #PERFORM STATE ACTIONS----------------------------------------------------
        #extract MARS (state 1)
        if(state == 1): 
            #when done, set state to inactive
            if(line.strip() == ''):  
                state = 0
                print("--Reverted State to 0--\n")
                writer.writerow([])
                
            #if not done, iterate i and build data
            i+=1
            data = line.split()
                
        #extract CONFIG LIST (state 2)
        if(state == 2):
            #when done, set state to inactive
            if(line.strip() == ''):  
                state = 0
                print("--Reverted State to 0--\n")
                writer.writerow([''])

            #close special title
            if(i!=starti):
                specialTitle = False 
                if(debug):
                    print("Ended specialTitle")

            if(not specialTitle and state!=0):
                raw = line.split()
                data[0] = (raw[0])
                data.append(f"{raw[1]} {raw[2]} ")

            i+=1

        #extract power usage summary (state 3)
        if(state == 3):
            #finish at end flag
            if(line.strip() == 'SSRM MEMORY DUMP **********'):
                state = 0
                print("--Reverted State to 0--\n")
                writer.writerow([])
                
            #close special title
            if(i!=starti):
                specialTitle = False 
                if(debug):
                    print("Ended specialTitle")

            #take usage title
            if(processNum!=1  and  line[0] == '['  and  state!=0):
                processNum = 1
            
            #collect data for usage title
            if(processNum == 1 and state!=0):
                data = line.split('|')
                for elem in data:
                    elem = elem.strip()

            #mark new usage title
            if(line.strip() == '' and state!=0):
                processNum = 0

            i+=1

        #extract Batterystats (state 4)
        if(state == 4):
            #finish will finish when state is changed at 'set state' level
           
            #close special title
            if(i!=starti):
                specialTitle = False 
                if(debug):
                    print("Ended specialTitle")

            #mark new usage title
            if(line.strip() == '' and state==4):
                processNum = 0

            #set process
            if(line.strip() != ''  and  line[0] == 'S'  and  state==4):
                processNum = 3
            if(line.strip() != ''  and  line[2] == 'U'  and  state==4):
                processNum = 2
            elif(line.strip() != ''  and  line[0] == ' '  and  state==4):
                processNum = 1
            
            #collect prelim data for usage (process 1)
            if(processNum == 1 and state==4):
                data = line.split(":")
                for elem in data:
                    elem = elem.strip()

            #collect data for usage title (process 2)
            if(processNum == 2 and state==4):
                data = line.split('|')
                for elem in data:
                    elem = elem.strip()

            #collect title
            if(processNum == 3  and  state==4):
                raw = line.split()
                data[0] = f"{raw[2]} {raw[3]}"
                data.append(f"{raw[5]} {raw[6]}")
            i+=1

        #extract Daily Summary (state 5)
        if(state == 5):
            #finish at end flag
            if(line.strip() == ''):
                state = 0
                print("--Reverted State to 0--\n")
                writer.writerow([])
                
            #close special title
            if(i>starti+1):
                specialTitle = False 
                if(debug):
                    print("Ended specialTitle")
                    
            #parse data
            data = line.split('|')
            for elem in data:
                elem = elem.strip()

            i+=1



    #/////////////////////////////////////////////////////////////////////


        #output if the state is active (not 0)
        if(state!=0 and (not specialTitle)):
                #print(f"writing {data}")
                isEmpty = True
                for elem in data:
                    if(elem.strip() != ''):
                        isEmpty = False
                        break
                if(not isEmpty):
                    writer.writerow(data)

        fileIndex += 1


