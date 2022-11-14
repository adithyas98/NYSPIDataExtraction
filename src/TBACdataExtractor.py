#!/usr/bin/env python3
import os
import re
from redcapAPI import RedCapAPI

#Store the directory we want to run the script on
def readData(filename):
    #now we can read the file
    #We want to create a list that we can store our data in and return in the end
    output = []
    with open(filename,'r') as f:
        #we want to be able to read each line of the file
        #however, we want to extract data from specific lines
        #create a line iterator object
        line = f.readline()
        #iterate through 6 lines and store the subject id
        for i in range(0,4):
            line=f.readline()
        #Extract the RA name
        output.append(re.findall(r'[A-z]+',line)[3])	
        #Extract the Date
        output.append(re.findall(r'\d{1,2}/\d{1,2}/\d{2,4}',line)[0])
        line = f.readline()#we want to move to the next line
        line = f.readline() #The line should now read the subject ID		

        subjectID =line.split(" ")[1]#This will get the subject's ID number
        output.append(subjectID)#add the subject ID to the output list

        #We need to reorder such that recordid is first
        output[0],output[1],output[2] = output[2],output[0],output[1]

        #Now we want to be able to get the rest of the data points
        #We first need to skip over a certain number of columns
        for i in range(0,9):
            line = f.readline()
        for x in range(0,8):
            line = f.readline()
            #now we want to extract the numbers from the data
            #dataEntries = re.findall(r'[><-]*[A-Za-z0-9]+\.?[A-Za-z0-9]*',line)
            #dataEntries = re.findall(r'[><-]*]\d+\.?\d*',line)#only captures numbers
            dataEntries = re.findall(r'[><-]*(\d+\.?\d*|X+)',line)#Captures numbers and the letter X
            print(dataEntries)
            # We want to add each individual data point in this array to the final output array
            for entry in dataEntries[1:None]:
                output.append(entry)

            #we want to iterate over the dotted lines
            line = f.readline()
        #Skip 10 lines to get to the auditory data
        for i in range(0,10):
            line = f.readline()
        #we want to extract the auditory level data
        output.append(re.findall(r'\d+.?\d*',line)[0]) 
    #we want to return a list that can be processed in the other file
    return output








if __name__ == "__main__":
    #Create the data labels that we an use
    base = 'tbac_'
    #List of the Columns
    cols = ['raw_percent','scaled_percent','threshold_value']
    #make sure that the _ are added at the end
    rows = ['freq_','intensity_','duration_','pulse_','embedded_','temporal_','syl_order_','syl_recon_']
    #we are going to iterate and create a pair for each of the 24 measurments that we take
    #create a list to hold all the values
    dataFields = ['record_id','tbac_ra','tbac_date']
    for r in rows:
        for c in cols:
            #we want to collect the data in this manner to stay consistent with how it is extracted
            dataFields.append(base + r + c)#Make sure that this is in fact the correct form of the labels
    dataFields.append('tbac_auditory_g')#We just need to include this at the end

    ### FILL THIS OUT ###
    #directory = r"/Users/adish/Documents/NYPSI and NKI Research/RedCapEncryptionProject/NYSPI-ExpTher-2021/test/TempTBACData"
    directory = "/mnt/h/RedCapDataExtractionScripts/NYSPIDataExtraction/test/TempTBACData"
    os.chdir(directory)
    allData = dict()
    debug = True
    problemFiles = []
    redcapAPI = RedCapAPI()
    #First add the header
    redcapAPI.addCSVHeader(dataFields,"CombinedData")
    for filename in os.listdir(directory):
        if (filename.endswith(".txt")):
            fullpath = directory + '/' + filename
            if debug:
                print("Currently Reading:{}".format(filename))

            data = readData(fullpath)


            #convert the data into a dictionary
            try:
                fullData = redcapAPI.toDict(dataFields,data)
            except IndexError:
                #For some reason there was an error so we want to log it
                problemFiles.append(filename)
                #we want to then continue to the next iteration
                continue
            #Now we want to save it to a csv
            #Now we can add the data points
            redcapAPI.toCSV(fullData,"TBACCombinedData",dataFields)
            #status = redcapAPI.sendtoRedCap(dataFields, data)

            #print(status)
    print("These were the files we had problems with")
    for name in problemFiles:
        print(name)
        print('\n')


