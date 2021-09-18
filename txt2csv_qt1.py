import csv
import requests
#from  dataExtractor import readData
import os
import json
import re


#set path where this .py script and result .txt file are both in
directory = r'/Users/gaoyifan/Desktop/Javittlab/EC/quickIQ'
filename = 'qt1411.txt' #define form 1 .txt file name
record_id = '35' #enter redcap ID here

output = [] #create 'output' to hold what we want to write into csv later
var = ['record_id','belt','dancing_easy','traffic_easy','whistle_easy',
'fence_easy','drink_easy','wreck_easy','music_easy','medicine_easy',
'gun_easy','pepper_easy','racing_easy','salt_easy','woman_easy','sugar_easy',
'track_easy','school_6','partner_6','couples_7','rails_7','respectful_8',
'betting_8','daring_9','stadium','pedestrian_10','graceful_10','fluid_11',
'solution_11','discipline_12','bleachers_12','crystallized_13','turntable_13',
'saccharin_14','immature_14','cordiality_15','velocity_15','decisive_16',
'laceration','foliage_17','imperative','intimacy_18','concoction_18',
'conviviality_18','chevrons_18','condiment_hard','cacophony_hard',
'miscible_hard','inbibe_hard','amicable_hard','pungent_hard']
output.append(var) #write variables into output

data = [] #create 'data' to hold data
#open form1 .txt file using filename, and define the name of .csv file
with open(filename,'r') as infile, open ('qt1411.csv','w') as outfile:
	#create a line iterator object
    line = infile.readline() #read first line

    print(record_id)
    #add the pcode as the first item in data
    data.append(record_id) #add the pcode to the output list

    #note that data is written into 'data' instead of output because they should stay in one line to be one case in csv
    #loops through the actual data
    for line in infile:
        #take the [2] (third) item after line split
        response = line.split()[2]
        print(response)
        if response == 'Pic1':
            data.append('0')
        elif response == 'Pic2':
            data.append('1')
        elif response == 'Pic3':
            data.append('2')
        elif response == 'Pic4':
            data.append('3')
        elif response == 'IDK':
            data.append('4')
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
