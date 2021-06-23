#!/usr/bin/env python
import requests
from  dataExtractor import readData
import os
import json



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
#TODO: Create a method that will iterate through the files,extract, and upload the data
#Now with that out of the way, we can extract the data using a subroutine imported from the dataExtractor.py file


directory = r"/Users/adish/Documents/NYPSI and NKI Research/TextFileDataExtractionProject"
APIData = {
    'token': '3FB92F6588C734E6D7FEFC88EFFDC763',
    'content': 'record',
    'format': 'json',
    'type': 'flat',
    'overwriteBehavior': 'normal',
    'forceAutoNumber': 'false',
    'data': '',
    'returnContent': 'count',
    'returnFormat': 'json'
}
#Iterate through each file and extract data from the file
for filename in os.listdir(directory):
	if (filename.endswith(".txt")):
		#we only want to index the text files
		#call our readData subroutine on the file
		extractedData  = readData(filename)
		#now we can create our dictionary
		data = toDict(dataFields,extractedData)
		#Set the Assign the the dictionary to the APIData 'data' field
		#APIData['data'] = [json.dumps(data)]
		to_import_json = json.dumps([data], separators=(',',':'))
		APIData['data'] = to_import_json
		#now we can attempt to RedCap
		r = requests.post('https://rc-1.nyspi.org/api/',data=APIData)
		print('HTTP Status: ' + str(r.status_code))
		print(r.json())
		#TODO figure out how RedCap wants the data once you have a dictionary
