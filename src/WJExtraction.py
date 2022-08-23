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
    dataLine = None#hold the position of where the data starts
    for i,line in enumerate(lines):
        if 'CLUSTER/TEST'.lower() in line.lower():
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
    if debug:
        print(len(dataEntries))
    for d in dataEntries:
        cluster = re.findall(r'[a-zA-Z]{2,}',d[0])
        clusters.append('_'.join(cluster))

    if debug:
        print(clusters)

    #Now we can try to extract the data points
    data = [file]
    for d in dataEntries:
        extracts = re.findall("[><\-\(]?\d{1,}.{0,2}\d{1,}\)?",d[0])
        # combine the last two elements
        data.extend(extracts[0:-2])
        data.append(''.join(extracts[-2:]))
    if debug:
        print("Printing Data")
        print(data)
    
    '''Outdated, Need to use the wj_row<num>_col<num> format
    #Now create the labels
    scoreNames = ['W','AE','RPI','SS']
    labels = ['record_id']
    for c in clusters:
        for s in scoreNames:
            labels.append("WJ_{}_{}".format(c,s))
    '''
    #We need to create labels in the following format
    #wj_row<num>_col<num>
    #however, the numbering is messed up in redcap so we need to take that into account
    
    labels = ['record_id','wj_row1_colu0','wj_row1_colu1','wj_row1_colu2','wj_row1_colu3']
    #we want to go ahead and extend the first row since it doesn't follow any pattern
    columns = ['4','1','2','3']
    #Now we will use the cluseters/tests list to figure out what row we are on
    for row in range(len(clusters[1:])):
        for i,col in enumerate(columns):
            #For the first column we want to keep the row index as is, for everything else add one
            if i >= 0:
                #we want to add one to the row index
                r = row+1
                c = col
            else:
                #This will already happen, but just to be more explicit
                r = row
                c = col
            labels.append("wj_row{}_colu{}".format(r,c))
                




            
    if debug:
        print(labels)
    return labels,data















if __name__ == "__main__":
    ################################CHANGE THIS FILE PATH##########################
    baseDir = "/mnt/h/RedCapDataExtractionScripts/NYSPIDataExtraction/test/Woodcock Johnson"
    os.chdir(baseDir)#change the directory
    print(baseDir)
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
 
