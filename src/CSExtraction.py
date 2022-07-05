#!/usr/bin/env python
import os
import re
from redcapAPI import RedCapAPI
import csv
debug = False #Set to false when not debugging















if __name__ == "__main__":
    baseDir = "/Users/adish/Documents/NYPSI and NKI Research/RedCapEncryptionProject/NYSPI-ExpTher-2021/test/DynEmoData"
    os.chdir(baseDir)#change the directory
    errorFiles = []
    rc = RedCapAPI()
    dataDicts = []
    for f in os.listdir():
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
    rc.addCSVHeader(header,"DynEmoCombinedData")
    for d in dataDicts:
        h = d.keys()
        rc.toCSV(d,"DynEmoCombinedData",h)
    print("Problem Files:\n")
    print(errorFiles)
    
