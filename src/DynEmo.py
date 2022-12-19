#!/usr/bin/env python3
import os
import re
from redcapAPI import RedCapAPI
import csv
debug = False #Set to false when not debugging
folder = True #True when we have a folder file structure
def readData(filename):
    #first we want to create a variable to hold the data
    data = []
    header = None#will hold the header of the file
    trials = []#will hold the trial information
    accuracies = []#we want to calculate an avg
    responseTimes = []#we want to calculate an avg
    with open(filename) as f:
        tsv = csv.reader(f,delimiter="\t")
        for i,row in enumerate(tsv):
            if i == 0:
                #now get the parts of the header we want
                header = row[3:4] + row[5:7]
                if debug:
                    #print the header
                    print(header)
                continue
            elif i == 1:
                #we want to extract and get the record ID
                ID = list(re.findall(r'\d+',row[0])[0])
                try:
                    data.append("ecr_0{}_00{}{}".format(ID[0],ID[1],ID[2]))
                except IndexError:
                    #some are formatted weird so we can try one more thing
                    ID = row[0]
                    data.append('ecr_{}'.format(ID))
                if debug:
                    print("ID",ID)
                    print("Data:",data)
            #we want to extract the data normally now
            data.extend(row[3:4] + row[5:7])
            accuracies.append(float(row[3]))
            responseTimes.append(float(row[5]))


            #we also want to extract the trial
            trials.append(row[1])
            
            
                
        data.append(sum(accuracies)/len(accuracies))
        data.append(sum(responseTimes)/len(responseTimes))
        #we basically need to order the labels in the exact same way
        #   we extracted the data
        base = 'dynemo'#redcap needs to to put the data in the right place
        labels = ['record_id']#start off the labels list
        for t in trials:
            #iterate through the trials
            for h in header:
                #we want to iterate through the header to make our labels
                labels.append('{}_{}_{}'.format(base,t,h.lower()))
        labels.append('{}_avg_accuracy'.format(base))
        labels.append('{}_avg_response_time'.format(base))
        #Run some checks to see if everything is working correctly
        if debug:
            print("Number of Data Points: {}".format(len(data)))
            print("Data:{}".format(data))
            print("Labels:{}".format(labels))
            print("Number of labels:{}".format(len(labels)))
            print("Is the number of Labels equal to the number of data points? {}".format(len(labels) == len(data)))
 
        return labels,data



if __name__ == "__main__":
    #baseDir = "/Users/adish/Documents/NYPSI Research/RedCapEncryptionProject/NYSPI-ExpTher-2021/test/DynEmoData/DynEmo/"
    #baseDir = "/mnt/h/RedCapDataExtractionScripts/NYSPIDataExtraction/test/DynEmoData"
    baseDir = "/Users/adish/Documents/NYPSI Research/RedCapEncryptionProject/NYSPI-ExpTher-2021/test/DynEmoData/"

    os.chdir(baseDir)#change the directory
    errorFiles = []
    rc = RedCapAPI()
    dataDicts = []
    baseDirFiles = os.listdir()#list of folders and files in baseDir
    for f in baseDirFiles:
        if folder:
            #If we have a folder file structure, then we want to go into those
            #   folders and extract the txt
            if not os.path.isdir(os.path.join(baseDir,f)):
                #This isn't a folder so we aren't interested
                print(f)
                continue#just want to continue to the next file/folder
            os.chdir(os.path.join(baseDir,f))
            print(os.getcwd())
            for g in os.listdir():
                if g.startswith('RESULTS') and g.endswith('.txt'):
                    #We are looking for RESULTS to be at the begining of the 
                    #   file name
                    print(f)
                    labels,data = readData(g)
                    if len(labels) != len(data):
                        #Then we want to append the error files to a list
                        errorFiles.append(f)
                    else:
                        #if there aren't any issues continue normally
                        #we want to make them into dictionaries
                        dataDicts.append(rc.toDict(labels,data))
        else:
            #We want to run like normal
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
    os.chdir(baseDir)
    header = dataDicts[0].keys()
    rc.addCSVHeader(header,"DynEmoCombinedData")
    for d in dataDicts:
        h = d.keys()
        rc.toCSV(d,"DynEmoCombinedData",h)
    print("Problem Files:\n")
    print(errorFiles)
    
 

                
