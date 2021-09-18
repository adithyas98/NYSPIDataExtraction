import csv
import requests
#from  dataExtractor import readData
import os
import json
import re

#set path where this .py script and result .txt file are both in
directory = r'/Users/gaoyifan/Desktop/Javittlab/EC/CTOPP_seg'
output = []

#write the output (one line of variable and one line of case) into csv
#var = ['record_id','ctopp_2_rs_9']
#output.append(var)
#print(output)

#create an index for the number of files we already looped through
idx = 0
#write variables into output
for filename in os.listdir(directory):
    if filename.endswith('.csv'):
        with open(filename,'r') as infile, open ('ctopp_seg.csv','w') as outfile: #open the file
            print(filename)
            idx += 1
            print(idx)
            line = infile.readline() #first line
            #copy the header only one time
            if idx == 1:
                #segment the line into items
                header = line.split(',')
                #paste the header into output
                output.append(header)
                line = infile.readline() #second line
                #segment the line into items
                x = line.split(',')
                #paste it into the output
                output.append(x)
            else:
                line = infile.readline() #second line
                #segment the line into items
                x = line.split(',')
                #paste it into the output
                output.append(x)
                print(output)

            #point to the csv outfile
            writer = csv.writer(outfile)
            #write the output (one line of variable and one line of case) into csv
            writer.writerows(output)
            #writer.writerow('\n')
