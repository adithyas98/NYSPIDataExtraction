import csv
import requests
#from  dataExtractor import readData
import os
import json
import re


#set path where this .py script and result .txt file are both in
directory = r'/Users/gaoyifan/Desktop/Javittlab/EC/TMT'
filename1 = '809tmt1.txt'
filename2 = '809tmt2.txt'
filename3 = '809tmt3.txt'
filename4 = '809tmt4.txt'
filename5 = '809tmt5.txt'

record_id = '16' #enter redcap ID here
print(record_id)

output = [] #create 'output' to hold what we want to write into csv later
var = ['record_id','trial_1_1','trial_1_2','trial_1_3','trial_1_4','trial_1_5','trial_1_6','trial_1_7','trial_1_8','trial_1_9',
'trial_1_10','trial_1_11','trial_1_12','trial_1_13','trial_1_14','trial_1_15','trial_1_16','trial_1_17','trial_1_18',
'trial_1_19','trial_1_20','trial_1_21','trial_1_22','trial_1_23','trial_1_24','trial_1_25','trial_1_26',
'trial_2_1','trial_2_2','trial_2_3','trial_2_4','trial_2_5','trial_2_6','trial_2_7','trial_2_8','trial_2_9','trial_2_10',
'trial_2_11','trial_2_12','trial_2_13','trial_2_14','trial_2_15','trial_2_16','trial_2_17','trial_2_18','trial_2_19',
'trial_2_20','trial_2_21','trial_2_22','trial_2_23','trial_2_24','trial_2_25','trial_2_26',
'trial_3_1','trial_3_2','trial_3_3','trial_3_4','trial_3_5','trial_3_6','trial_3_7','trial_3_8','trial_3_9','trial_3_10',
'trial_3_11','trial_3_12','trial_3_13','trial_3_14','trial_3_15','trial_3_16','trial_3_17','trial_3_18','trial_3_19',
'trial_3_20','trial_3_21','trial_3_22','trial_3_23','trial_3_24','trial_3_25','trial_3_26',
'trial_4_1','trial_4_2','trial_4_3','trial_4_4','trial_4_5','trial_4_6','trial_4_7','trial_4_8','trial_4_9','trial_4_10',
'trial_4_11','trial_4_12','trial_4_13','trial_4_14','trial_4_15','trial_4_16','trial_4_17','trial_4_18','trial_4_19',
'trial_4_20','trial_4_21','trial_4_22','trial_4_23','trial_4_24','trial_4_25','trial_4_26',
'trial_5_1','trial_5_2','trial_5_3','trial_5_4','trial_5_5','trial_5_6','trial_5_7','trial_5_8','trial_5_9','trial_5_10',
'trial_5_11','trial_5_12','trial_5_13','trial_5_14','trial_5_15','trial_5_16','trial_5_17','trial_5_18','trial_5_19',
'trial_5_20','trial_5_21','trial_5_22','trial_5_23','trial_5_24','trial_5_25','trial_5_26']
output.append(var) #write variables into output

data = [] #create 'data' to hold data
#open track1 .txt file using filename1, and define the name of .csv file
with open(filename1,'r') as infile, open ('tmt809.csv','w') as outfile:
	#create a line iterator object
    line = infile.readline() #read first line
    data.append(record_id) #add the pcode to the output list

    #add the pcode as the first item in data
    #data.append(record_id) #add the pcode to the output list

    #note that data is written into 'data' instead of output because they should stay in one line to be one case in csv
    #loops through the actual data
    for line in infile:
        response = line.split()[4]
        print(response)
        if response == 'Same':
            data.append('1')
        elif response == 'Different':
            data.append('2')
        #jump out of loop when we reach an empty line
        if line == ' ':
            break

#close the track1 txt data file
infile.close()

#open track2 .txt file using filename1, and define the name of .csv file
with open(filename2,'r') as infile, open ('tmt809.csv','w') as outfile:
	#create a line iterator object
    line = infile.readline() #read first line

    #note that data is written into 'data' instead of output because they should stay in one line to be one case in csv
    #loops through the actual data
    for line in infile:
        response = line.split()[4]
        print(response)
        if response == 'Same':
            data.append('1')
        elif response == 'Different':
            data.append('2')
        #jump out of loop when we reach an empty line
        if line == ' ':
            break
#close the track2 txt data file
infile.close()

#open track3 .txt file using filename1, and define the name of .csv file
with open(filename3,'r') as infile, open ('tmt809.csv','w') as outfile:
	#create a line iterator object
    line = infile.readline() #read first line

    #note that data is written into 'data' instead of output because they should stay in one line to be one case in csv
    #loops through the actual data
    for line in infile:
        response = line.split()[4]
        print(response)
        if response == 'Same':
            data.append('1')
        elif response == 'Different':
            data.append('2')
        #jump out of loop when we reach an empty line
        if line == ' ':
            break
#close the track3 txt data file
infile.close()

#open track4 .txt file using filename1, and define the name of .csv file
with open(filename4,'r') as infile, open ('tmt809.csv','w') as outfile:
	#create a line iterator object
    line = infile.readline() #read first line

    #note that data is written into 'data' instead of output because they should stay in one line to be one case in csv
    #loops through the actual data
    for line in infile:
        response = line.split()[4]
        print(response)
        if response == 'Same':
            data.append('1')
        elif response == 'Different':
            data.append('2')
        #jump out of loop when we reach an empty line
        if line == ' ':
            break
#close the track4 txt data file
infile.close()

#open track5 .txt file using filename1, and define the name of .csv file
with open(filename5,'r') as infile, open ('tmt809.csv','w') as outfile:
	#create a line iterator object
    line = infile.readline() #read first line

    #note that data is written into 'data' instead of output because they should stay in one line to be one case in csv
    #loops through the actual data
    for line in infile:
        response = line.split()[4]
        print(response)
        if response == 'Same':
            data.append('1')
        elif response == 'Different':
            data.append('2')
        #jump out of loop when we reach an empty line
        if line == ' ':
            break

    #append data as one case into output
    output.append(data)
    print(output)
    #point to the csv outfile
    writer = csv.writer(outfile)
    #write the output (one line of variable and one line of case) into csv
    writer.writerows(output)
