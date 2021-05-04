#!/usr/bin/env python

#By Adithya Shastry
import requests
import os
import json

class RedCapAPI:

	def __init__(self,APIKEY,URL='https://rc-1.nyspi.org/api/'):
		self.APIData = {
		    'token': APIKEY,
		    'content': 'record',
		    'format': 'json',
		    'type': 'flat',
		    'overwriteBehavior': 'normal',
		    'forceAutoNumber': 'false',
		    'data': '',
		    'returnContent': 'count',
		    'returnFormat': 'json'
		}
		self.URL = URL
	
	#TODO: Create a method to securly retrieve an API token using RSA, specifically the Cryptography library

	def toDict(listA,listB):
		#this function will take the elements in the lists and make them into key value pairs
		#The input for this function must be Labels,Data
		outDict = {}
		for i in range(0,len(listA)):
			outDict[listA[i]] = listB[i]	
		return outDict 
	def sendData(self,labels,data):
		#first we want to create a dictionary out of the two lists we have
		dataDict = self.toDict(labels,data)
		
		#Add our data to the payload
		to_import_json = json.dumps([dataDict], separators=(',',':'))
		APIData['data'] = to_import_json

		#now we want to send out data over to Redcap
		r = requests.post('https://rc-1.nyspi.org/api/',data=APIData)
		print('HTTP Status: ' + str(r.status_code))
		print(r.json())


