import csv
import requests
#from  dataExtractor import readData
import os
import json
import re


#set path where this .py script and result .txt file are both in
directory = r'/Users/gaoyifan/Desktop/Javittlab/EC/quickIQ'
filename = 'qt3006.txt' #define form 3 .txt file name
record_id = '37' #enter redcap ID here

output = [] #create 'output' to hold what we want to write into csv later
var = ['record_id','sheet_easy','exercise_easy','machine_easy','burners_easy',
'audience_easy','dish_easy','drying_easy','food_easy','fork_easy','crowd_easy',
'slice_easy','washing_easy','tears_easy','fighting_easy','kitchen_easy',
'tasty_easy','windy_6','pitiful_6','contest_7','sorrow_8','loser_7',
'heartbreak_8','struggle_9','rotary','opponents_9','grief_10','utensils_11',
'lever_11','portion_12','edible_12','exhibition_13','soothed_13',
'caress_14','conbatant','forlorn_15','nutrient_15','solace_16',
'pacify_16_or_14','contorted_17','jets_17','doleful_18','tines_18',
'disconsolate_18','sustenance_18','maudlin_hard','gustatory_hard',
'poignant_hard','bellicose_hard','comestible_hard','despondency_hard']
output.append(var) #write variables into output

data = [] #create 'data' to hold data
#open form 3 .txt file using filename, and define the name of .csv file
with open(filename,'r') as infile, open ('qt3006.csv','w') as outfile:
	#create a line iterator object
    line = infile.readline() #read first line

    print(record_id)
    #add the pcode as the first item in data
    data.append(record_id) #add the pcode to the output list

    #note that data is written into 'data' instead of output because they should stay in one line to be one case in csv
    #loops through the actual data
    for line in infile:
        #take the [2] (third) item after line split
        response = line.split()[4]
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
