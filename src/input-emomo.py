#!/usr/bin/env python3

import os
import json
import pandas as pd
import requests
from datetime import datetime
import sys

dir_path = os.path.dirname(os.path.realpath(__file__))
dt_string = datetime.now().strftime("%m_%d_%Y___%H_%M")

output_file = open(r"" + dir_path + "/emomo_logs/emomo_API_log_" + dt_string + ".txt", "w");
sys.stdout = output_file

API_TOKEN = 'E0B6D18D64DD7583754A3D444F8A90D6'
DIRECTORY = '/home/jec2268/NYSPI/EMOMO/test_dir_1'
CUR_DIR_PATH = os.path.dirname(os.path.realpath(__file__))

MAPPING = {24: 'afraid_stat_', 14: 'afraid_dyn_', 23: 'angry_stat_',
           13: 'angry_dyn_', 21: 'happy_stat_', 11: 'happy_dyn_', 
           22: 'sad_stat_', 12: 'sad_dyn_', 25: 'ambig_stat_', 
           15: 'ambig_dyn_'}

def build_dataframe(filename):
    data = pd.read_csv(filename, delimiter='\t')
    data['stim_codes'] = pd.Categorical(data['stim_codes'], [24, 14, 23, 13, 21, 11, 22, 12, 25, 15])
    return data

def extract_info(dataframe):
    result_counts = dataframe.copy().groupby(['stim_codes', 'ACCURACY']).size().unstack() \
                           .reset_index().set_index('stim_codes') \
                           .rename(columns={-1:"no_response", 0:"incorrect", 1:"correct"}) \
                           .rename(index=MAPPING)

    result_counts = result_counts.fillna(0)
    result_counts['total'] = result_counts['no_response'] + result_counts['incorrect'] + result_counts['correct'] 
    result_counts['percent_corr'] = (100*(result_counts['correct']/result_counts['total'])).astype(int)

    return result_counts


def convert_to_json(result_dataframe, record_id):
    
    json_temp = result_dataframe.to_dict()
    json_final = {}
    for i in json_temp:
        for field in json_temp[i]:
            json_final[field + i] = json_temp[i][field]
    json_final['record_id'] = record_id
    json_final['emomo_import_testing_complete'] = 2
    json_fields = json.dumps([json_final])
    return json_fields

def make_api_call(json_object):
    fields = {
        'token': API_TOKEN,
        'content': 'record',
        'format': 'json',
        'type': 'flat',
        'data': json_object,
    }
    r=requests.post('https://rc-1.nyspi.org/api/',data=fields)
    if r.status_code != 200:
        print('ERROR: problem with record import!')
        exit()

def get_id(filename):
    code = filename[:3]
    participant_id = 'ecr_0' + code[0] + '_00'+ code[1:]
    return participant_id

def is_complete(filename):
    part_id = get_id(filename)
    fields = {
        'token': API_TOKEN,
        'content': 'record', 
        'format': 'json',
        'type': 'flat',
        'records': part_id,
        'forms': 'emomo_import_testing'
    }
    r=requests.post('https://rc-1.nyspi.org/api/', data=fields)
    if r.status_code != 200:
        print('ERROR: problem with record export!')
        exit()
    if 'emomo_import_testing_complete' in r.text:
        dict_val = json.loads(r.text)[0]
        if dict_val['emomo_import_testing_complete'] == str(2):
            return True
    return False

def main():
    results_raw=[]
    for entry in os.scandir(DIRECTORY):
        if entry.path.endswith('txt') and entry.is_file() and 'dye' in entry.path:
            results_raw.append(entry.path)
 #   while True:
  #      directory = input('\nenter a FULL PATH to the directory: ')
   #     try: 
    #        for entry in os.scandir(directory):
     #           if entry.path.endswith('.txt') and entry.is_file() and 'dye' in entry.path:
      #              results_raw.append(entry.path)
       #     break
        #except:
         #   print("\nINVALID directory!")
    
    print("\nFOUND " + str(len(results_raw)) + " RESULT FILES IN DIRECTORY: " + DIRECTORY)
    print("-------------------------------------")
    print('\n'.join(map(str, [path.rsplit('/', 1)[-1] for path in results_raw])))
    print("-------------------------------------\n")
   
    count = 0
    for file in results_raw:
        file_name = file.rsplit('/', 1)[-1]
        if not is_complete(file_name):
        #record_id = input("enter RECORD ID for file: (" + file_name + ")\n")
        #if record_id=='i' or record_id == 'I':
         #   print('file ignored')
          #  continue
            initial_table = build_dataframe(file)
            formatted_table = extract_info(initial_table)
            json_formatted = convert_to_json(formatted_table, get_id(file_name))
            make_api_call(json_formatted)
            print('updated participant ID: ' + get_id(file_name))
            count += 1
    if count > 0:
        print('\nSuccessfully updated ' + str(count) + ' records.\n')
    else:
        print('no records updated.\n')
    output_file.close()

if __name__ == "__main__":
    main()
    
