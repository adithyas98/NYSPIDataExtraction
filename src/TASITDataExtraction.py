#!/usr/bin/env python
#Author: Adithya Shastry
#Email: ams2590@columbia.edu
'''
This script will extract data from TASIT text files. The function will return 
multiple lists that contain the labels and the data.
'''
import os
import re
from redcapAPI import RedCapAPI
import csv


def extractTASITData(filename,debug=False):
    '''
    This method will extract the data and the labels from the tasit text file
    Inputs:
        - filename: the file filepath to the tasit data file
    Outputs:
        - a list of labels and data points that correspond to those labels
    '''
    base = '' #holds the value of the TASIT experiment type (A or B)
    data = [] #create an array to store the data
    #first we want to open the tsv file
    with open(filename) as f:
        tsv = csv.reader(f,delimiter="\t")
        next(tsv)#skip the header
        #we can extract the data points we want now
        for i,row in enumerate(tsv):
            #Extract the record ID
            if i == 0:
                #We want to extract the record_id from one of the 16 rows
                ID = list(row[0])[0:3]
                #figure out the redcap id : XYY -> ecr_0X_00YY
                data.append("ecr_0{}_00{}{}".format(ID[0],ID[1],ID[2]))

                #Extract the tasit test (A or B)
                if list(row[0])[-1].lower() == 'a'.lower():
                    #Then we have tasit A
                    base = 'tasita'
                elif list(row[0])[-1].lower() == 'b'.lower():
                    #Then we have tasit B
                    base = 'tasitb'


                
            if debug:
                print("Extracting:{}".format(row[5:9]))
            for el in row[5:9]:
                if el.lower() == 'yes':
                    data.append(1)
                elif el.lower() == 'no':
                    data.append(0)
                else:
                    #The answer is don't know
                    data.append(6)

        #Create the labels
        labels = ['record_id']
        for i in range(1,17):
            labels.append("{}_{}_do".format(base,i))
            labels.append("{}_{}_say".format(base,i))
            labels.append("{}_{}_think".format(base,i))
            labels.append("{}_{}_feel".format(base,i))

        if debug:
            print("Number of Data Points: {}".format(len(data)))
            print("Data:{}".format(data))
            print("Labels:{}".format(labels))
            print("Number of labels:{}".format(len(labels)))
            print("Is the number of Labels equal to the number of data points? {}".format(len(labels) == len(data)))
    return labels,data,base
        



if __name__ == '__main__':
    errorFiles = [] #A list to hold the names of error files
    #run extract data
    baseDir = "/Users/adish/Documents/NYPSI and NKI Research/RedCapEncryptionProject/NYSPI-ExpTher-2021/test/TASITdata"
    os.chdir(baseDir)
    dataDictsA = []
    dataDictsB = []
    rc = RedCapAPI()
    for f in os.listdir():
        if f.endswith('.txt'):
            labels,data,base = extractTASITData(f,debug=True)
            if len(labels) != len(data):
                #Then we want to append the error files to a list
                errorFiles.append(f)
            else:
                #We don't have any issues so continue normally
                if base == 'tasita':
                    dataDictsA.append(rc.toDict(labels,data))
                elif base == 'tasitb':
                    dataDictsB.append(rc.toDict(labels,data))

    #Write the Tasit A csv
    #write the header
    header = dataDictsA[0].keys()
    rc.addCSVHeader(header,"TASITA")
    for d in dataDictsA:
        h = d.keys()
        rc.toCSV(d,"TASITA",h)

    #Write the Tasit B csv
    #write the header
    header = dataDictsB[0].keys()
    rc.addCSVHeader(header,"TASITB")
    for d in dataDictsB:
        h = d.keys()
        rc.toCSV(d,"TASITB",h)
 


    print("Files with a mismatch of datapoints and labels")
    for f in errorFiles:
        print('{}\n'.format(f))
               
            


