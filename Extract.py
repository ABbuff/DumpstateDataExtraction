import string
import os
import csv
from datetime import datetime
from datetime import date
import re

#debugging
debug = False
print()


def extract(inputFile: string, outputFile: string):
    specialTitle = False
    fileIndex = 1

    with open(outputFile,'w',newline='', encoding="utf8") as writefile,open(inputFile,newline='', encoding="utf8") as readfile:
        writer = csv.writer(writefile)
        
        
        state = 0
        processNum = 0
        starti = 0
        for line in readfile:

        #PRELIMINARY----------------------------------------------------------
            states = ['',                                               #0  just read line
                    '[MARS]',                                           #1
                    '[CONFIG LIST]',                                    #2
                    'Process usage summary',                            #3
                    '[Batterystats Collector]',                         #4
                    'Daily Summary',                                    #5
                    '[PowerAnomaly Battery Dump]',                      #6
                    'Anomaly List For DeviceCare',                      #7
                    '[TCPU dump]',                                      #8
                    '[UCPU dump]',                                      #9
                    '------ NETWORK DEV INFO (/proc/net/dev) ------',   #10
                    '------ MEMORY INFO (/proc/meminfo) ------',        #11
                    '------ VIRTUAL MEMORY STATS (/proc/vmstat) ------',#12
                    '** MEMINFO in pid[com.x3AM.Innovations.Flare.Mobile.App] **'#13


                    ]
            
            data = ['']
        #/////////////////////////////////////////////////////////////////////

        #SET STATE------------------------------------------------------------   
            #enter state 1 ([MARS])
            if (line.strip() == states[1]):
                state = 1
                starti = fileIndex
                print(f"--Changed State to: {state} becasuse of {states[state]}\nExtracting from line {starti}...")

            #enter state 2 ([CONFIG LIST])
            elif (line.strip() == states[2]):
                state = 2
                starti = fileIndex
                #handle special title
                specialTitle = True
                writer.writerows([[states[state]], ['Boot Number', 'Date/Time']])
                print(f"--Changed State to: {state} w/ special title becasuse of {states[state]}\nExtracting from line {starti}...")

            #enter state 3 (Process usage summary)
            elif (line.strip()[:21] == states[3]):        #[:21] take the first 21 characters
                state = 3
                processNum = 0
                starti = fileIndex
                #handle special title
                specialTitle = True
                writer.writerow([line])
                print(f"--Changed State to: {state} w/ special title becasuse of {states[state]}\nExtracting from line {starti}...")

            #enter state 4 ([Batterystats Collector])
            elif (line.strip() == states[4]):
                state = 4
                processNum = 0
                starti = fileIndex
                #handle special title
                specialTitle = True
                writer.writerow([line])
                print(f"--Changed State to: {state} w/ special title becasuse of {states[state]}\nExtracting from line {starti}...")

            #enter state 5 (Daily Summary)
            elif (line.strip() == states[5]):
                state = 5
                processNum = 0
                starti = fileIndex
                #handle special title
                specialTitle = True
                writer.writerow([])
                writer.writerow([line])
                print(f"--Changed State to: {state} w/ special title becasuse of {states[state]}\nExtracting from line {starti}...")

            #enter state 6 ([PowerAnomaly Battery Dump])
            elif (line.strip() == states[6]):
                state = 6
                processNum = 0
                starti = fileIndex
                #handle special title
                specialTitle = True
                writer.writerow([line])
                print(f"--Changed State to: {state} w/ special title becasuse of {states[state]}\nExtracting from line {starti}...")

            #enter state 7 (Anomaly List For DeviceCare)
            elif (line.strip() == states[7]):
                state = 7
                processNum = 0
                starti = fileIndex
                #handle special title
                specialTitle = True
                writer.writerow([])
                writer.writerow([line])
                print(f"--Changed State to: {state} w/ special title becasuse of {states[state]}\nExtracting from line {starti}...")

            #enter state 8 ([TCPU dump])
            elif (line.strip() == states[8]):
                state = 8
                processNum = 0
                starti = fileIndex
                #handle special title
                specialTitle = True
                writer.writerow([])
                writer.writerow([line])
                print(f"--Changed State to: {state} w/ special title becasuse of {states[state]}\nExtracting from line {starti}...")

            #enter state 9 ([UCPU dump])
            elif (line.strip() == states[9]):
                state = 9
                processNum = 0
                starti = fileIndex
                #handle special title
                specialTitle = True
                writer.writerow([])
                writer.writerow([line])
                print(f"--Changed State to: {state} w/ special title becasuse of {states[state]}\nExtracting from line {starti}...")

            #enter state 10 (------ NETWORK DEV INFO (/proc/net/dev) ------ )
            elif (line.strip() == states[10]):
                state = 10
                starti = fileIndex
                #handle special title
                specialTitle = True
                writer.writerow([line])
                print(f"--Changed State to: {state} w/ special title becasuse of {states[state]}\nExtracting from line {starti}...")

            #enter state 11 (------ MEMORY INFO (/proc/meminfo) ------ )
            elif(line.strip() == states[11]):
                state = 11
                processNum = 0
                starti = fileIndex
                #handle special title
                specialTitle = True
                writer.writerow([line])
                print(f"--Changed State to: {state} w/ special title becasuse of {states[state]}\nExtracting from line {starti}...")

            #enter state 12 (------ VIRTUAL MEMORY STATS (/proc/vmstat) ------)
            elif(line.strip() == states[12]):
                state = 12
                processNum = 0
                starti = fileIndex
                #handle special title
                specialTitle = True
                writer.writerow([line])
                print(f"--Changed State to: {state} w/ special title becasuse of {states[state]}\nExtracting from line {starti}...")
            
            '''
            #enter state 13 (** MEMINFO in pid[com.x3AM.Innovations.Flare.Mobile.App] **)
            elif(line.strip()[:17] == states[13][:17]  and  re.search('[com.x3AM.Innovations.Flare.Mobile.App]', line)==True):
                state = 13
                processNum = 0
                starti = fileIndex
                #handle special title
                specialTitle = True
                writer.writerow([line])
                print(f"--Changed State to: {state} w/ special title becasuse of {states[state]}\nExtracting from line {starti}...")
            '''
                
            #debug info
            #print(f"fileIndex: {fileIndex} | i: {i} | state: {state}")

        #/////////////////////////////////////////////////////////////////////

        #PERFORM STATE ACTIONS----------------------------------------------------
            #extract MARS                               (state 1)
            if(state == 1): 
                #when done, set state to inactive
                if(line.strip() == ''):  
                    state = 0
                    print(f"--Reverted State to {state} at {fileIndex}--\n")
                    writer.writerow([])
                
                data = line.split()
                    
            #extract CONFIG LIST                        (state 2)
            if(state == 2):
                #when done, set state to inactive
                if(line.strip() == ''):  
                    state = 0
                    print(f"--Reverted State to {state} at {fileIndex}--\n")
                    writer.writerow([''])

                #close special title
                if(fileIndex!=starti  and  specialTitle):
                    specialTitle = False 
                    if(debug):
                        print(f"Ended specialTitle at line {fileIndex}")

                if(not specialTitle and state!=0):
                    raw = line.split()
                    data[0] = (raw[0])
                    data.append(f"{raw[1]} {raw[2]} ")

            #extract power usage summary                (state 3)
            if(state == 3):
                #finish at end flag
                if(line.strip() == 'SSRM MEMORY DUMP **********'):
                    state = 0
                    print(f"--Reverted State to {state} at {fileIndex}--\n")
                    writer.writerow([])
                    
                #close special title
                if(fileIndex!=starti  and  specialTitle):
                    specialTitle = False 
                    if(debug):
                        print(f"Ended specialTitle at line {fileIndex}")

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

            #extract Batterystats                       (state 4)
            if(state == 4):
                trimmed = line.strip()
                #finish will finish when state is changed at 'set state' level
            
                #close special title
                if(fileIndex!=starti  and  specialTitle):
                    specialTitle = False 
                    if(debug):
                        print(f"Ended specialTitle at line {fileIndex}")

                #mark new usage title
                if(line.strip() == '' and state==4):
                    processNum = 0

                #set process
                if(trimmed != ''  and  line[0] == 'S'  and  state==4):
                    processNum = 3
                if(trimmed != ''  and  line[2] == 'U'  and  state==4):
                    processNum = 2
                if(trimmed != ''  and  processNum == 2  and  line[2] == ' '):
                    processNum = 2
                if(trimmed != ''  and  processNum != 2  and  line[0] == ' '  and  state==4):
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

            #extract Daily Summary                      (state 5)
            if(state == 5):
                #finish at end flag
                if(line.strip() == ''):
                    state = 0
                    print(f"--Reverted State to {state} at {fileIndex}--\n")
                    writer.writerow([])
                    
                #close special title
                if(fileIndex>starti+1  and  specialTitle  and  specialTitle):
                    specialTitle = False 
                    if(debug):
                        print(f"Ended specialTitle at line {fileIndex}")
                        
                #parse data
                data = line.split('|')
                for elem in data:
                    elem = elem.strip()

            #extract PowerAnomaly Battery Dump          (state 6)
            if(state == 6):
                #close special title
                if(fileIndex>starti  and  specialTitle  and  state == 6):
                    specialTitle = False 
                    if(debug):
                        print(f"Ended specialTitle at line {fileIndex}")

                #finish at next title
                if(line[:3] == '[Ba'):
                    state = 0
                    print(f"--Reverted State to {state} at {fileIndex}--\n")
                    writer.writerow([])

                if(state == 6):
                    data = line.strip()
                
            #extract Anomaly List For DeviceCare        (state 7)
            if(state == 7):
                #finish parsing after second null line
                if(line.strip() == ''  and  processNum == 2):
                    state = 0
                    print(f"--Reverted State to {state} at {fileIndex}--\n")
                    writer.writerow([])

                #next process after null line
                if(line.strip() == ''  and  state == 7):
                    processNum = 1
                    print(f"Process Number has been changed to {processNum} at line {fileIndex}")
                
                #close special title
                if(fileIndex>starti  and  specialTitle):
                    specialTitle = False 
                    if(debug):
                        print(f"Ended specialTitle at line {fileIndex}")

                #parse data by default
                if(processNum == 0  and  state == 7):
                    data = line.split('|')
                    newData = []
                    for elem in data:
                        elem = elem.strip()
                        newData.append(elem)
                    data = newData

                #collect stats
                elif(processNum == 2  and  state == 7):
                    data = line.split(':')
                    #print(f"{data[0]} : {data[1]}")

                #collect stats timestamp
                elif(line.strip() != ''  and  processNum == 1):
                    raw = line.split()
                    data[0] = f"{raw[2]} {raw[3]}"
                    data.append(f"{raw[5]} {raw[6]}")
                    processNum = 2
                    print(f"Process Number has been changed to {processNum} at line {fileIndex}")
            
            #extract [TCPU dump]                        (state 8)
            if(state == 8):
                #finish at end flag
                if(line.strip() == ''):
                    state = 0
                    print(f"--Reverted State to {state} at {fileIndex}--\n")
                    writer.writerow([])
                    
                #close special title
                if(fileIndex>starti+1  and  specialTitle):
                    specialTitle = False 
                    if(debug):
                        print(f"Ended specialTitle at line {fileIndex}")
                        
                #parse data
                data = line.split('|')
                for elem in data:
                    elem = elem.strip()

            #extract [UCPU dump]                        (state 9)
            if(state == 9):
                #finish at end flag
                if(line.strip() == ''):
                    state = 0
                    print(f"--Reverted State to {state} at {fileIndex}--\n")
                    writer.writerow([])
                    
                #close special title
                if(fileIndex>starti+1  and  specialTitle  and  specialTitle):
                    specialTitle = False 
                    if(debug):
                        print(f"Ended specialTitle at line {fileIndex}")
                        
                #parse data
                data = line.split('|')
                for elem in data:
                    elem = elem.strip()

            #extract NETWORK DEV INFO                   (state 10)
            if(state == 10): 
                #when done, set state to inactive
                if(line.strip()!=''  and  line.split()[0] == '------'  and  not specialTitle):  
                    state = 0
                    print(f"--Reverted State to {state} at {fileIndex}--\n")
                    writer.writerow([])
                
                #close special title
                if(fileIndex>starti+1  and  specialTitle):
                    specialTitle = False 
                    if(debug):
                        print(f"Ended specialTitle at line {fileIndex}")

                #collect data
                if(state == 10  and  not specialTitle):
                    line = line.strip()
                    data = line.split()

                    keep = False
                    for elem in data:
                        if(elem.isnumeric()  and  int(elem)>10000):
                                keep = True
                    
                    if(not keep):
                        data = []
                        
            #extract MEMORY INFO                        (state 11)
            if(state == 11):
                #when done, set state to inactive
                if(line.strip()!=''  and  line.split()[0] == '------'  and  not specialTitle):  
                    state = 0
                    print(f"--Reverted State to {state} at {fileIndex}--\n")
                    writer.writerow([])
                
                #close special title
                if(fileIndex>starti+1  and  specialTitle):
                    specialTitle = False 
                    if(debug):
                        print(f"Ended specialTitle at line {fileIndex}")

                if(line.strip()!=''  and  not specialTitle and state==11):
                    raw = line.split(':')
                    data[0] = raw[0].strip()
                    data.append(raw[1].strip())

            #extract VIRTUAL MEMORY STATS               (state 12)
            if(state == 12):
                #when done, set state to inactive
                if(line.strip()!=''  and  line.split()[0] == '------'  and  not specialTitle):  
                    state = 0
                    print(f"--Reverted State to {state} at {fileIndex}--\n")
                    writer.writerow([])
                
                #close special title
                if(fileIndex>starti  and  specialTitle):
                    specialTitle = False 
                    if(debug):
                        print(f"Ended specialTitle at line {fileIndex}")

                if(line.strip()!=''  and  not specialTitle and state==11):
                    raw = line.split()
                    data[0] = raw[0].strip()
                    data.append(raw[1].strip())

            '''
            #extract MEMINFO in pid                     (state 13)
            if(state == 13):
                #when done, set state to inactive
                if(line.strip()!=''  and  line.split()[0] == '*'  and  not specialTitle):  
                    state = 0
                    print(f"--Reverted State to {state} at {fileIndex}--\n")
                    writer.writerow([])
                
                #close special title
                if(fileIndex>starti  and  specialTitle):
                    specialTitle = False 
                    if(debug):
                        print(f"Ended specialTitle at line {fileIndex}")

                #collect data
                if(processNum == 2  and  line.strip()!=''  and  not specialTitle  and  state==13):
                    data = line.split()
                    for elem in data:
                        elem = elem.strip()
                        
                #collect title
                if(processNum == 1):
                    data[0] = line
                    processNum = 2
                if(line.strip()==''  and  not specialTitle  and  state==13):
                    processNum = 1
            '''

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
                    elif(debug):
                        print(f"Did not write line {fileIndex} to CSV because data was empty")
            if(specialTitle  and  debug):
                print(f"Did not write line {fileIndex} to CSV because of Special Title")

            fileIndex += 1


#   main
inputFiles = os.listdir('INPUT')
fileCount = 1
for file in inputFiles:
    outfile = f"{file.split('.')[0]}-output_{fileCount}.csv"
    print(f'RUNNING EXTRACT ON [{file}] AND WRITING TO [{outfile}]...')
    print()
    extract(f'INPUT\{file}', outfile)
    print("Exited properly\n")
    fileCount+=1
