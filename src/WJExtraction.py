#!/usr/bin/env python
import os
import re
from redcapAPI import RedCapAPI
import csv
from mat4py import loadmat
import itertools
import pypandoc
debug = True #Set to false when not debugging




def readData(file):
    '''
    This method will read in the data from the woodcock johnson task
    the file input is in the format of a word document.
    Input:
        - Word document containing woodcock Johnson forms
    output:
        - data points and labels
    '''
    #Extract the data into a list
    lines = []
    with open(file,'r') as f:
        lines = f.readlines()
    dataLine = 0#hold the position of where the data starts
    for i,line in enumerate(lines):
        if 'CLUSTER/Test' in line:
            #We want to mark the position
            dataLine = i
    #Now we can start reading the data in from this point on
    data = []
    for line in lines[dataLine+2:]:
        if 'Woodcock-Johnson IV Tests' in line:
            #We are done reading the data and we can stop
            break
        if len(line.strip()) != 0:
            dataEntries = line.split()[1:]
            #TODO: Need to find a way to only get number entries, maybe with regex and space characters, with split
            #The best way to do it would be to find the data points based on split and regex
            print(dataEntries)
            
    return None,None















if __name__ == "__main__":
    baseDir = "/Users/adish/Documents/NYPSI and NKI Research/RedCapEncryptionProject/NYSPI-ExpTher-2021/test/Woodcock Johnson"
    os.chdir(baseDir)#change the directory
    errorFiles = []
    rc = RedCapAPI()
    dataDicts = []
    for f in os.listdir():
        if f.endswith('.docx'):
           #We want to first convert it to a txt
           output = pypandoc.convert_file(f,'plain',outputfile='{}.txt'.format(f.split('.')[0]))
           assert output == ""
        if f.endswith('.txt'):
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
 
