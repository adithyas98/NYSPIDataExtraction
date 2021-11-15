#!/usr/bin/env python
import os
import re

#Store the directory we want to run the script on
directory = r"/Users/adish/Documents/NYPSI and NKI Research/TextFileDataExtractionProject"
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
		#Now we want to be able to get the rest of the data points
		#We first need to skip over a certain number of columns
		for i in range(0,9):
			line = f.readline()
		for x in range(0,8):
			line = f.readline()
			#now we want to extract the numbers from the data
			# we will extract this and print it as a proof of concept
			dataEntries = re.findall(r'[><-]*\d+\.?\d*',line)
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
#Create the data labels that we an use

#create the base
base = 'tbac_'
#List of the Columns
cols = ['raw_percent','scaled_percent','threshold_value']

#now create the rows
#make sure that the _ are added at the end
rows = ['freq_','intensity_','duration_','pulse_','embedded_','temporal_','syl_order_','syl_recon_']

# the labels take the form base + row + col
#we are going to iterate and create a pair for each of the 24 measurments that we take
#create a list to hold all the values
dataFields = ['tbac_ra','tbac_date','record_id']
for r in rows:
	for c in cols:
		#we want to collect the data in this manner to stay consistent with how it is extracted
		dataFields.append(base + r + c)#Make sure that this is in fact the correct form of the labels
dataFields.append('tbac_auditory_g')#We just need to include this at the end

def toDict(listA,listB):
	#this function will take the elements in the lists and make them into key value pairs
	#The input for this function must be Labels,Data
	outDict = {}
	for i in range(0,len(listA)):
		outDict[listA[i]] = listB[i]	
	return outDict 

if __name__ == "__main__":
	#Iterate through each file and extract data from the file
	for filename in os.listdir(directory):
		if (filename.endswith(".txt")):
			#we only want to index the text files
			#call our readData subroutine on the file
			data = readData(filename)
			print(data)



