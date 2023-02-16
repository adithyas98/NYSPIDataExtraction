#!/usr/bin/env python3
import os
import re
from redcapAPI import RedCapAPI
import csv
from mat4py import loadmat
import itertools
import numpy as np
debug = True #Set to false when not debugging

def readData(file):
    '''
    This function will read and extract the data from the .mat file
    Inputs:
        - file: the mat file to be read
    Outputs:
        - labels and the respective data points associated with the .mat file
    '''
    data = []
    labels = []
 
    dataFile = loadmat(file)
    #print(dataFile)
    print(dataFile.keys())
    keys = list(dataFile.keys())
    print(dataFile[keys[0]].keys())
    print(dataFile[keys[1]].keys())
    ID = list(re.findall('\d{3}$',file.split('.')[0])[0])
    subjectID = "ecr_0{}_00{}{}".format(ID[0],ID[1],ID[2])
    #Add the recordID to the labels and the Data 
    data.append(subjectID)
    labels.append('recordid')
    if debug:
        print(subjectID)
    #first create a list of the keys

    keysLevelOne = list(dataFile.keys())
    dataLists = []#Create an empty array to hold data
    listLabels = []#Create list labels to keep track of the order
    #Now we can extract the data
    keylength = 0
    print(keysLevelOne)
    for k1 in keysLevelOne:
        keys = dataFile[k1].keys()
        keylength += len(keys)
        print(keys)
        for k in keys:
            #we want to pre populate the list so that we add our data to it
            listLabels.append(k)
            dataLists.append([])
        for i,k in enumerate(keys):
            #Here we will iterate through the keys and extract the data
            #An issue is that for some reason some of the data lists contain
            #   other lists inside them. So we need a generalizable way of handling
            #   this problem

            #We will first check to see if the list contains other lists in it

            if any(isinstance(el, list) for el in dataFile[k1]):
                #Then we need to convert it to one single list and append 
                dataLists[i] = list(itertools.chain(*dataFile[k1][k]))
            else:
                #append like normal
                dataLists[i] = dataFile[k1][k]
        assert keylength == len(dataLists)#Just make sure we don't run into any issues
        print("assertion Passed")
        #We want to add empty values if we have different number of data points
        i =  listLabels.index('Audio')#The Audio Labels is the one that seems to have all the info we want
        if debug:
            print(listLabels)
            print(type(dataLists[i]))
            print(dataLists[i])
        #Now extract the data from the sub dictionary in datalists[0]
        keys = dataLists[i].keys()
        for k in keys:
            d = dataLists[i][k]
            if type(d) != list:
                #This means we have nothing to really average
                mean = d
                sd = 0
            elif any(isinstance(el, list) for el in d):
                #Then we need to convert it to one single list and append 
                d = list(itertools.chain(*d))
                mean = np.mean(d)
                sd = np.std(d)
            else:
                #append like normal
                mean = np.mean(d)
                sd = np.std(d)
            #Now we can append these values with the appropriate label
            #Mean
            data.append(mean)
            labels.append('mthresh_{}_avg'.format(k.lower()))
            #stdev
            data.append(sd)
            labels.append('mthresh_{}_stdev'.format(k.lower()))
    assert len(labels) == len(data)

    return labels,data

if __name__ == "__main__":
    baseDir = "/Users/adish/Documents/NYPSI Research/RedCapEncryptionProject/NYSPI-ExpTher-2021/test/MTHresh"
    #baseDir = "/mnt/h/RedCapDataExtractionScripts/NYSPIDataExtraction/test/CS"
    os.chdir(baseDir)#change the directory
    errorFiles = []
    rc = RedCapAPI()
    dataDicts = []
    for f in os.listdir():
        if f.endswith('.mat'):
            print(f)
            labels,data = readData(f)
            if len(labels) != len(data):
                #Then we want to append the error files to a list
                errorFiles.append(f)
            else:
                #if there aren't any issues continue normally
                #we want to make them into dictionaries
                dataDicts.append(rc.toDict(labels,data))
    header = dataDicts[0].keys()
    rc.addCSVHeader(header,"CSCombinedData")
    for d in dataDicts:
        h = d.keys()
        rc.toCSV(d,"CSCombinedData",h)
    print("Problem Files:\n")
    print(errorFiles)
 
