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
    #Create the labels
    labels = ['record_id']
    base = 'tasita'
    for i in range(1,17):
        labels.append("{}_{}_do".format(base,i))
        labels.append("{}_{}_say".format(base,i))
        labels.append("{}_{}_think".format(base,i))
        labels.append("{}_{}_feel".format(base,i))
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
        if debug:
            print("Number of Data Points: {}".format(len(data)))
            print("Data:{}".format(data))
            print("Labels:{}".format(labels))
            print("Number of labels:{}".format(len(labels)))
    return labels,data
        



if __name__ == '__main__':
    #run extract data
    baseDir = "/Users/adish/Documents/NYPSI and NKI Research/RedCapEncryptionProject/NYSPI-ExpTher-2021/test/TASITdata"
    os.chdir(baseDir)
    dataDicts = []
    rc = RedCapAPI()
    for f in os.listdir():
        if f.endswith('.txt'):
            labels,data = extractTASITData(f,debug=True)
            dataDicts.append(rc.toDict(labels,data))

    #Write the CSV
    #write the header
    header = dataDicts[0].keys()
    rc.addCSVHeader(header,"TASITA")
    for d in dataDicts:
        h = d.keys()
        rc.toCSV(d,"TASITA",h)

            
            


