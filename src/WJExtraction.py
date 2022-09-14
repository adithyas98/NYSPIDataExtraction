#!/usr/bin/env python3
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
        if 'CLUSTER/Test'.lower() in line.lower():
            #We want to mark the position
            dataLine = i
    #Now we can start reading the data in from this point on
    dataEntries = []
    for line in lines[dataLine+2:]:
        if 'Woodcock-Johnson IV Tests'.lower() in line.lower():
            #We are done reading the data and we can stop
            break
        if len(line.strip()) != 0:
            dataEntries.append(line.split('\n'))
            #The best way to do it would be to find the data points based on split and regex
            if debug:
                print(dataEntries[0])
    #Now we need to gather the clusters (The tests run) and the data points
    clusters = []
    for d in dataEntries:
        cluster = re.findall(r'[a-zA-Z]{2,}',d[0])
        clusters.append('_'.join(cluster))

    if debug:
        print(clusters)

    #Now we can try to extract the data points
    data = [file.split('.')[0]]
    for d in dataEntries:
        #extracts = re.findall("[><\-\(]?\d{1,}.{0,2}\d{1,}\)?",d[0])
        extracts = re.findall("[><\-\(]?\d{0,}[-]?\d{1,}\)?",d[0])
        print("Before:",extracts)
        for i,e in enumerate(extracts):
            #We want to iterate through and modify particular ones
            if i==1 and ("-" in e):
                #Then we need to conver to a decimal 
                date = re.findall("\d{1,}",e)
                extracts[1] = float(date[0]) + float(date[1])/12
                print("Dash",extracts)
            elif i == 5:
                #The confidence interval will be in the following format
                #   (XX - YY)
                #We want to separate it such that we only get the numbers
                confInt = re.findall("\d{1,}",e)
                #Now we want to place this in the correct place
                extracts[5] = confInt[0]
                if len(confInt) > 1:
                    extracts.append(confInt[1])
                else:
                    #This means that the range is the same number so we will 
                    #   add the value we found
                    extracts.append(confInt[0])
                print("Conf Int",extracts)
            if not e.isnumeric():
                #We want to only extract the numbers
                digits = re.findall("\d{1,}",e)
                extracts[i] = digits[0]
                print("non-digit", extracts)
        if debug:
            print(extracts,len(extracts) == 7)
        data.extend(extracts)
    if debug:
        print(data)
    
    #Now create the labels
    scoreNames = ['W','AE','RPI_num','RPI_denom','SS','SS_68%_LowBound','SS_68%_UpBound']
    labels = ['record_id']
    print("clusters:",len(clusters))
    for c in clusters:
        for s in scoreNames:
            labels.append("WJ_{}_{}".format(c,s))
            
    if debug:
        print(labels)
        print(data)
    return labels,data















if __name__ == "__main__":
    #baseDir = "/Users/adish/Documents/NYPSI and NKI Research/RedCapEncryptionProject/NYSPI-ExpTher-2021/test/Woodcock Johnson"
    baseDir = "/mnt/h/RedCapDataExtractionScripts/NYSPIDataExtraction/test/Woodcock Johnson"
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
            labels,data = readData(f)
            if len(labels) != len(data):
                #Then we want to append the error files to a list
                print('labels:{},data:{}'.format(len(labels),len(data)))
                errorFiles.append(f)
            else:
                #if there aren't any issues continue normally
                #we want to make them into dictionaries
                dataDicts.append(rc.toDict(labels,data))
    print(len(dataDicts))
    header = dataDicts[0].keys()
    rc.addCSVHeader(header,"WJCombinedData")
    for d in dataDicts:
        h = d.keys()
        rc.toCSV(d,"WJCombinedData",h)
    print("Problem Files:\n")
    print(errorFiles)
 
