#!/usr/bin/env python
import os
import re
from redcapAPI import RedCapAPI
import csv
from mat4py import loadmat
import itertools
debug = True #Set to false when not debugging


def readData(file):
    '''
    This function will read and extract the data from the .mat file
    Inputs:
        - file: the mat file to be read
    Outputs:
        - labels and the respective data points associated with the .mat file
    '''
    dataFile = loadmat(file)
    ID = list(re.findall('\d{3}$',file.split('.')[0])[0])
    subjectID = "ecr_0{}_00{}{}".format(ID[0],ID[1],ID[2])
    if debug:
        print(subjectID)
    #first create a list of the keys

    keys = dataFile.keys()
    dataLists = []#Create an empty array to hold data
    #Now we can extract the data
    for k in keys:
        #we want to pre populate the list so that we add our data to it
        dataLists.append([])
    for i,k in enumerate(keys):
        #Here we will iterate through the keys and extract the data
        #An issue is that for some reason some of the data lists contain
        #   other lists inside them. So we need a generalizable way of handling
        #   this problem

        #We will first check to see if the list contains other lists in it

        if any(isinstance(el, list) for el in dataFile[k]):
            #Then we need to convert it to one single list and append 
            dataLists[i] = list(itertools.chain(*dataFile[k]))
        else:
            #append like normal
            dataLists[i] = dataFile[k]
    assert len(keys) == len(dataLists)#Just make sure we don't run into any issues
    #Make sure we have the same amount of data
    assert len(dataLists[0]) == len(dataLists[1]) and len(dataLists[1]) == len(dataLists[2])
    #calculate the averages
    averages = []
    for dataset in dataLists:
        averages.append(sum(dataset)/len(dataset))

    #Make the labels
    
    labels = ['record_id']#init the labels list
    for k in keys:
        for i in range(len(dataLists[0])):
            labels.append("CS_{}_{}".format(k,i))

    #create keys for averages
    for k in keys:
        labels.append("CS_{}_avg".format(k))



    #Merge all data to one list
    data = [subjectID]#init the data list
    for d in dataLists:
        data.extend(d)
    
    #Append the averages
    for avg in averages:
        data.append(avg)

    print(labels,data)
    return labels,data













if __name__ == "__main__":
    baseDir = "/Users/adish/Documents/NYPSI and NKI Research/RedCapEncryptionProject/NYSPI-ExpTher-2021/test/CS"
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
    
