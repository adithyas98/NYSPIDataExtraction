import csv
import requests
#from  dataExtractor import readData
import os
import json
import re

#set path where this .py script and result .txt file are both in
directory = r'/Users/gaoyifan/Desktop/Javittlab/EC/CTOPP_blend'
output = []

#write the output (one line of variable and one line of case) into csv
var = ['record_id','ctopp_2_rs_8']
output.append(var)
print(output)

#output.append(var) #write variables into output
for filename in os.listdir(directory):
    if filename.endswith('.csv'):
        with open(filename,'r') as infile, open ('ctopp_blend.csv','w') as outfile: #open the file
            print(filename)
            line = infile.readline() #first line
            line = infile.readline() #second line
            x = line.split(',')

            output.append(x)
            print(output)
            #output.append(line)
            #if line == ' ':
                #continue
            #print(output)
            #point to the csv outfile
            writer = csv.writer(outfile)
            #write the output (one line of variable and one line of case) into csv
            writer.writerows(output)
            #writer.writerow('\n')
