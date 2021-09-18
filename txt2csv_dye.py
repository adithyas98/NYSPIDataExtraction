import csv
import requests
#from  dataExtractor import readData
import os
import json
import re


#set path where this .py script and result .txt file are both in
directory = r'/Users/gaoyifan/Desktop/Javittlab/EC/DyeEmo'
filename = '845dye.txt' #define .txt file name
record_id = '5' #enter redcap ID here

output = [] #create 'output' to hold what we want to write into csv later
var = ['record_id','afraidstat_total','afraidstat_correct']
output.append(var) #write variables into output

data = []
with open(filename,'r') as infile, open ('dye801.csv','w') as outfile: #open the file
	#create a line iterator object
    line = infile.readline() #first line
    #print(record_id)
    #add the pcode as the first item in data
    data.append(record_id) #add the pcode to the output list

    score_total = 0 #create the total score that starts at 0 and we will add the scores up using loop
    score_corr = 0 #create the score of correct items that starts at 0 and we will add the scores up using loop
    #read through all lines
    for line in infile:
        #take the response (fourth item in the line)
        #add 1 to score if the response isn't empty
        if line.split()[3] == '1':
            #print(line.split()[3])
            score_total = score_total + 1
            score_corr = score_corr + 1
        elif line.split()[3] == '0':
            #print(line.split()[3])
            score_total = score_total + 1
            score_corr = score_corr
        #don't do anything to the score if the response is empty
        elif line.split()[3] == '-1':
            #print(line.split()[3])
            score_total = score_total
            score_corr = score_corr
        #jump out of loop when we reach an empty line
        if line == ' ':
            break

    data.append(score_total)
    print(score_total)
    data.append(score_corr)
    print(score_corr)
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
