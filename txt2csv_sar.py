import csv
import requests
#from  dataExtractor import readData
import os
import json
import re


#set path where this .py script and result .txt file are both in
directory = r'/Users/gaoyifan/Desktop/Javittlab/EC/sarcasm'
filename = 'sar412.txt' #define .txt file name
record_id = '38' #enter redcap ID here

output = [] #create 'output' to hold what we want to write into csv later
var = ['record_id','test_tape_1','test_tape_2','test_tape_3','practice_tape_4',
'tape_1','tape_2','tape_3','tape_4','tape_5',
'tape_6','tape_7','tape_8','tape_9','tape_10',
'tape_11','tape_12','tape_13','tape_14','tape_15',
'tape_16','tape_17','tape_18','tape_19','tape_20',
'tape_21','tape_22','tape_23','tape_24','tape_25',
'tape_26','tape_27','tape_28','tape_29','tape_30',
'tape_31','tape_32','tape_33','tape_34','tape_35',
'tape_36','tape_37','tape_38','tape_39','tape_40']
output.append(var) #write variables into output

data = [] #create 'data' to hold data
with open(filename,'r') as infile, open ('sar412.csv','w') as outfile: #open the file
	#create a line iterator object
    line = infile.readline() #first line

    print(record_id)
    #add the pcode as the first item in data
    data.append(record_id) #add the pcode to the output list

    #note that data is written into 'data' instead of output because they should stay in one line to be one case in csv
    #loops through the data
    for line in infile:
        response = line.split()[4]
        #print(response)
        if response == 'Sincere':
            data.append('1')
        elif response == 'Sarcastic':
            data.append('0')
        #jump out of loop when we reach an empty line
        if line == ' ':
            break

    #append data as one case into output
    output.append(data)
    #print(output)
    #point to the csv outfile
    writer = csv.writer(outfile)
    #write the output (one line of variable and one line of case) into csv
    writer.writerows(output)


    # taskID = line.split()[0] #take the ID for the task, e.g., qt909
    # #print(taskID)
    # taskIDx = re.split('\D+',taskID)[1] #take the numbers in the taskID
    # #print(taskIDx)
    # root = 'ecr_0' #start of the pcode
    # cohort = str(list(taskIDx)[0]) #cohort type
    # #print(group)
    # bridge = '_00' #add the two zeros before the last two digits of pcode
    # #last two digits of pcode - this may be simplified
    # subject1 = str(list(taskIDx)[1])
    # subject2 = str(list(taskIDx)[2])
    # #print(subject1)
    # #print(subject2)
    # #put them all together
    # pcode = root + cohort + bridge + subject1 + subject2
    # print(pcode)
    # #add the pcode as the first item in data
    # data.append(pcode) #add the pcode to the output list
