import csv
import requests
#from  dataExtractor import readData
import os
import json
import re


#set path where this .py script and result .txt file are both in
directory = r'/Users/gaoyifan/Desktop/Javittlab/EC/swedish'
filename = 'swed412.txt' #define .txt file name
record_id = '38' #enter redcap ID here

output = [] #create 'output' to hold what we want to write into csv later
var = ['record_id','abbrev_swed_emo_1','abbrev_swed_intensity_1',
'abbrev_swed_emo_2','abbrev_swed_intensity_2',
'abbrev_swed_emo_3','abbrev_swed_intensity_3',
'abbrev_swed_emo_4','abbrev_swed_intensity_4',
'abbrev_swed_emo_5','abbrev_swed_intensity_5',
'abbrev_swed_emo_6','abbrev_swed_intensity_6',
'abbrev_swed_emo_7','abbrev_swed_intensity_7',
'abbrev_swed_emo_8','abbrev_swed_intensity_8',
'abbrev_swed_emo_9','abbrev_swed_intensity_9',
'abbrev_swed_emo_10','abbrev_swed_intensity_10',
'abbrev_swed_emo_11','abbrev_swed_intensity_11',
'abbrev_swed_emo_12','abbrev_swed_intensity_12',
'abbrev_swed_emo_13','abbrev_swed_intensity_13',
'abbrev_swed_emo_14','abbrev_swed_intensity_14',
'abbrev_swed_emo_15','abbrev_swed_intensity_15',
'abbrev_swed_emo_16','abbrev_swed_intensity_16',
'abbrev_swed_emo_17','abbrev_swed_intensity_17',
'abbrev_swed_emo_18','abbrev_swed_intensity_18',
'abbrev_swed_emo_19','abbrev_swed_intensity_19',
'abbrev_swed_emo_20','abbrev_swed_intensity_20',
'abbrev_swed_emo_21','abbrev_swed_intensity_21',
'abbrev_swed_emo_22','abbrev_swed_intensity_22',
'abbrev_swed_emo_23','abbrev_swed_intensity_23',
'abbrev_swed_emo_24','abbrev_swed_intensity_24',
'abbrev_swed_emo_25','abbrev_swed_intensity_25',
'abbrev_swed_emo_26','abbrev_swed_intensity_26',
'abbrev_swed_emo_27','abbrev_swed_intensity_27',
'abbrev_swed_emo_28','abbrev_swed_intensity_28',
'abbrev_swed_emo_29','abbrev_swed_intensity_29',
'abbrev_swed_emo_30','abbrev_swed_intensity_30',
'abbrev_swed_emo_31','abbrev_swed_intensity_31',
'abbrev_swed_emo_32','abbrev_swed_intensity_32',
'abbrev_swed_emo_33','abbrev_swed_intensity_33']
output.append(var) #write variables into output

data = [] #create 'data' to hold data
with open(filename,'r') as infile, open ('swed412.csv','w') as outfile: #open the file
	#create a line iterator object
    line = infile.readline() #first line
    print(record_id)
    #add the pcode as the first item in data
    data.append(record_id) #add the pcode to the output list

    #note that data is written into 'data' instead of output because they should stay in one line to be one case in csv
    #loops through the data
    #extract emotion rating
    for line in infile:
        if line.split()[4] == 'Intensity"': #for no intensity trials, we have to skip one more item
            response1 = line.split()[5]
            #print(response1)
            if response1 == 'Happy':
                data.append('1')
            elif response1 == 'Sad':
                data.append('2')
            elif response1 == 'Angry':
                data.append('3')
            elif response1 == 'Fearful':
                data.append('4')
            elif response1 == 'No_Emotion':
                data.append('5')
        else:
            response1 = line.split()[4]
            #print(response1)
            if response1 == 'Happy':
                data.append('1')
            elif response1 == 'Sad':
                data.append('2')
            elif response1 == 'Angry':
                data.append('3')
            elif response1 == 'Fearful':
                data.append('4')
            elif response1 == 'No_Emotion':
                data.append('5')

        #extract intensity rating
        if line.split()[4] == 'Intensity"':
            response2 = line.split()[7]
            #print(response2)
            data.append(response2)
        else:
            response2 = line.split()[6]
            #print(response2)
            data.append(response2)
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
