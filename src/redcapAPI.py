#!/usr/bin/env python
import requests
import os
import json


class RedCapAPI:
    def __init__(self,APILink = 'https://rc-1.nyspi.org/api/',):
        #The payload to actually send to RedCap
        self.payload= {
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
        #Set the API link 
        self.APILink = APILink


    def getToken(self):
        '''
            This method will use the json file that holds the encrypted API 
            tokens and a user's inputted password to decrypt the api token
            and add it to the payload.
            Inputs:
                - Location of json file that holds the tokens. (Already taken 
                    care of during initialization)
                - Username and Password: This is to be inputted by the user 
                                            when prompted.
        '''


    def addData(self,data):
        '''
            Method adds the Data to the APIData dictionary that we will send
            to RedCap
            Inputs:
                - Data: Dictionary to be added. The dictionary should link the
                        should link the variable name to the value.
            Output:
                - None
        '''
        #Convert the data to json first
		to_import_json = json.dumps([data], separators=(',',':'))
        #Add the data to the payload
        self.payload['data'] = to_import_json


    def toDict(listA,listB):
        #this function will take the elements in the lists and make them into key value pairs
        #The input for this function must be Labels,Data
        outDict = {}
        for i in range(0,len(listA)):
            outDict[listA[i]] = listB[i]	
    return outDict 
    
    def sendtoRedCap(self,keys,values):
        '''
            Method sends data to Redcap once all the preprocessing is done
            Inputs:
                - keys: Variable names in Redcap 
                - values: the value to be uploaded
                Important Note: The values need to be in the same corresponding
                                position in each of the lists to ensure they
                                are linked correctly
            Ouput:
                - statusCode: The Status that the api sends back. This is to verify
                            that the upload was done successfuly.
        '''
        #Convert the key and values lists into a dictionary 
        self.data = self.toDict(keys,values)
        #Add the dictionary to the payload dictionary
        self.addData(data) #Add our data to the payload
		#now we can attempt to send it to RedCap
		r = requests.post(APILink,data=self.payload)
        #Now we can return the status code
		return str(r.status_code)

        
#TODO: Create a Unit test to test everything!!!


'''
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
'''
