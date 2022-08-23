# -*- coding: utf-8 -*-
"""
Created on Tue Aug 23 13:21:17 2022

@author: Enor
"""


import json
import csv

root = '0013157800087578_02.json'


with open(root, encoding='utf-8') as f:
    while True:
        
        line = f.readline()
        if not line: # 到 EOF，返回空字符串，则终止循环
            break
        js = json.loads(line)
        
        print(line)

"""
#剖析json array
input_file = open ('0013157800087578_02.json')
json_array = json.load(input_file)


for item in json_array:
    print("id:" + item['id'])
    print("coolwaterin:" + item['coolwaterin'])
"""