#!/usr/bin/env python
import requests
import os
import json


class RedCapAPI:
    def __init__(self):
        self.APIData = {
            'token': '',
            'content': 'record',
            'format': 'json',
            'type': 'flat',
            'overwriteBehavior': 'normal',
            'forceAutoNumber': 'false',
            'data': '',
            'returnContent': 'count',
            'returnFormat': 'json'
        }

    #TODO: Create a function that can get the API token


    def toDict(listA,listB):
        #this function will take the elements in the lists and make them into key value pairs
        #The input for this function must be Labels,Data
        outDict = {}
        for i in range(0,len(listA)):
            outDict[listA[i]] = listB[i]	
    return outDict 
    
    def sendtoRedCap(self):
        #TODO: Create a method that will actually send data to redcap through the API



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
