# -*- coding: utf-8 -*-
"""
Created on Tue Aug 23 13:17:05 2022

@author: Enor
"""
import json
import csv


readRoot = '0013157800087578_02.json'
saveRoot = '0013157800087578_02.csv'

with open(readRoot ,encoding='utf-8') as json_file:
    jsondata = json.load(json_file)
data_file = open(saveRoot ,'w' ,newline='',encoding='utf-8')
csv_writer = csv.writer(data_file)
count = 0
for data in jsondata:
    if count == 0:
        header = data.keys()
        csv_writer.writerow(header)
        count += 1
    csv_writer.writerow(data.values())
data_file.close()