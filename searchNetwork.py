"""
Author: Kyle Norland
Title: Prediction Network
Summary: This program uses a network to predict
    the next camera that will capture footage of a person. It uses three neurons
    per sensor and two lists of input and output neurons to achieve this purpose.
"""

import numpy as np
import datetime
from datetime import timedelta
from collections import defaultdict
import fullCameraCheckVer2 as camCheck
#import importlib                                                #Import the lib that allows for importing files
#importlib.import_module(fullCameraCheckVer2.py)                    #Import the computer vision stuff


def checkIfLost(sensorDict):

    personLost = True                                   #Assume the person has been lost to begin
    for record in sensorDict:
        if (np.sum(sensorDict[record][0:3]) > 0):
            personLost = False
    return personLost;
                                                        #If it gets through the whole thing and hasn't been changed
                                                        #Then the person has been lost
def transmit(sensorDict):
    for sensor in sensorDict:
        if(sensorDict[sensor][2]==1):                   #If any of the lost neurons are firing
            for toNode in sensorDict[sensor][4]:        #Fire them to each of their connections
                sensorDict[toNode][0] = 1
            sensorDict[sensor][2]=0                     #Reset it to 0 so it doesn't keep transmitting.
    return sensorDict;


        

def recalculate(sensorDict, currentTime, foundList):
    #global sensorDict
    #global currentTime
    #global foundList
    endTime = currentTime + 2
    
    #Internal Check
    for sensor in sensorDict:                               #Run through and get the neurons that are triggered/active
        #Triggered sensors
        if(sensorDict[sensor][0]>0):                        #If the neuron has been triggered
            print("Checking camera " + str(sensor))
            #print(currentTime)
            #print(endTime)
            result = camCheck.checkPerson(sensor,currentTime, endTime)   #Check for a person
            if (result['personFound'] == True):                              #If a person was detected
                print("Person found at " + str(sensor))
                foundList.append(result['photoName'])
                sensorDict[sensor][0]=0
                sensorDict[sensor][1]=1                     #Change the state to active
            else:
                sensorDict[sensor][0] -=0.2                 #Decrease the weight by a little bit (Counter) #This messes up though. Not exact subtract.
                
        #Active sensors
        elif (sensorDict[sensor][1]>0):                      #If it's an active sensor
            print("Checking camera" + str(sensor))
            result = camCheck.checkPerson(sensor,currentTime, endTime)   #Check for the person
            if (result['personFound'] == True):                              #If a person was detected
                print("Person found at " + str(sensor))
                foundList.append(result['photoName'])
                sensorDict[sensor][0]=0
                sensorDict[sensor][1]=1                     #Keep the state active
            else:
                sensorDict[sensor][1] -=0.3                 #Decrement it (Just to avoid minor frame misses)
                #Record the image                           #Just in case it's just a gap
            if (sensorDict[sensor][1] <= 0):                  #If it's lost the person
                sensorDict[sensor][2] = 1                   #Trigger a transmission next turn
    return (sensorDict, foundList);

def runNetwork(triggeredWifi, currentTime, cutoffTime):
    #Dictionary approach
    #initialize dictionary
    sensorDict = defaultdict(list)
    sensorDict[2019] = [0,0,0,[],[11,13]]
    sensorDict[2039] = [0,0,0,[],[12,13,14]]
    sensorDict[2051] = [0,0,0,[],[13,14,16]]
    sensorDict[2059] = [0,0,0,[],[13,16]]
    sensorDict[2065] = [0,0,0,[],[16,17,18]]
    sensorDict[2099] = [0,0,0,[],[17,18]]
    sensorDict[2209] = [0,0,0,[],[9,11,13]]
    sensorDict[2219] = [0,0,0,[],[8,9,10]]
    sensorDict[2231] = [0,0,0,[],[8,10]]
    sensorDict[8] = [0,0,0,[2219,2231],[9]]
    sensorDict[9] = [0,0,0,[2209,2219],[8,10,11]]
    sensorDict[10] = [0,0,0,[2219,2231],[9]]
    sensorDict[11] = [0,0,0,[2019,2209], [9,12,13]]
    sensorDict[12] = [0,0,0,[2039,2051], [9,11,14,16]]
    sensorDict[13] = [0,0,0,[2019, 2039, 2051, 2059, 2209],[11,14]]
    sensorDict[14] = [0,0,0,[2039,2051], [12,13,16]]
    sensorDict[16] = [0,0,0,[2051,2059,2065],[12,14,17,18]]
    sensorDict[17] = [0,0,0,[2065,2099],[16]]
    sensorDict[18] = [0,0,0,[2065,2099],[16]]

                    
    #Set initial variables
    foundList = []                                                    #Creates a list for the found photos


    year = (int(str(currentTime)[0:4]))
    month = (int(str(currentTime)[4:6]))
    day = (int(str(currentTime)[6:8]))
    hour = (int(str(currentTime)[8:10]))                             #Convert time to date format for progression
    minute = (int(str(currentTime)[10:12]))
    second = (int(str(currentTime)[12:14]))
    timeFormat = datetime.datetime(year, month, day, hour, minute, second)

    personLost = False

    #Start with setting the triggered wifi equal to one. This should work, because 13 had me in it first.
    sensorDict[triggeredWifi][2] = 1

    #Loop until all are zeros
    while((personLost == False) and (currentTime < cutoffTime)):
        sensorDict = transmit(sensorDict)
        sensorDict, foundList = recalculate(sensorDict, currentTime, foundList)
        #Check if went correctly
        print(sensorDict[8][0:3])
        print(sensorDict[9][0:3])
        print(sensorDict[10][0:3])
        print(sensorDict[11][0:3])
        print(sensorDict[12][0:3])
        print(sensorDict[13][0:3])
        print(sensorDict[14][0:3])
        print(sensorDict[16][0:3])
        print(sensorDict[17][0:3])
        print(sensorDict[18][0:3])
        """
        for record in sensorDict:
            print(sensorDict[record][0:3])
            """
        #print("Is lost?" + str(checkIfLost(sensorDict)))
        personLost = checkIfLost(sensorDict)

        #Increment the current time to move it along
        timeFormat += datetime.timedelta(seconds=2)
        timeString = str(timeFormat.year).zfill(4) + str(timeFormat.month).zfill(2) + str(timeFormat.day).zfill(2) + str(timeFormat.hour).zfill(2) + str(timeFormat.minute).zfill(2) + str(timeFormat.second).zfill(2)
        currentTime = int(timeString)
        print(currentTime)
            

    print("The person has been lost")
    return foundList;

    #for entry in foundList:
        #print(entry)
                                 
#########################################################################################
                                       #MAIN
#########################################################################################
"""
triggeredWifi = 2039
currentTime = 20180718164252                                           #Start time is 164019
cutoffTime =  20180719164320
foundList = runNetwork(triggeredWifi, currentTime, cutoffTime)
for entry in foundList:
    print(entry)
"""
