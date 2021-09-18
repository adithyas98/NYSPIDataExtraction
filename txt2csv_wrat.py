import csv
import requests
#from  dataExtractor import readData
import os
import json
import re


#set path where this .py script and result .txt file are both in
directory = r'/Users/gaoyifan/Desktop/Javittlab/EC/WRAT'
filename = 'wrat809.txt' #define .txt file name
record_id = '16' #enter redcap ID here

output = [] #create 'output' to hold what we want to write into csv later
var = ['record_id','wrat_1_raw']
output.append(var) #write variables into output

data = []
with open(filename,'r') as infile, open ('wrat809.csv','w') as outfile: #open the file
	#create a line iterator object
    line = infile.readline() #first line
    print(record_id)
    #add the pcode as the first item in data
    data.append(record_id) #add the pcode to the output list

    score = 0 #create the score that starts at 0 and we will add the scores up using loop
    #read through all lines
    for line in infile:
        #take the response (fourth item in the line)
        #add 1 to score if the response is correct (yes)
        if line.split()[3] == 'yes':
            #print(line.split()[3])
            score = score + 1
        #do nothing to the score if the response is incorrect (no)
        elif line.split()[3] == 'no':
            #print(line.split()[3])
            score = score
        #jump out of loop when we reach an empty line
        if line == ' ':
            break
    data.append(score)
    #append data as one case into output
    output.append(data)
    print(output)
    #point to the csv outfile
    writer = csv.writer(outfile)
    #write the output (one line of variable and one line of case) into csv
    writer.writerows(output)



    #append data as one case into output
    # output.append(data)
    # print(output)
    # #point to the csv outfile
    # writer = csv.writer(outfile)
    # #write the output (one line of variable and one line of case) into csv
    # writer.writerows(output)
    #
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
