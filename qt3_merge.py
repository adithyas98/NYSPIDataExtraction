import csv
import requests
#from  dataExtractor import readData
import os
import json
import re

#set path where this .py script and result .txt file are both in
directory = r'/Users/gaoyifan/Desktop/Javittlab/EC/quickIQ/qt3'
headerf = 'qt3006.csv' #define the csv file to extract header
output = []

#write the output (one line of variable and one line of case) into csv
with open(headerf,'r') as infile: #open the file
    line = infile.readline() #first line
    header = line.split(',')
    output.append(header)
    print(output)

#close the csv data file
infile.close()


#output.append(var) #write variables into output
for filename in os.listdir(directory):
    if filename.endswith('.csv'):
        with open(filename,'r') as infile, open ('qt3_merge.csv','w') as outfile: #open the file
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
