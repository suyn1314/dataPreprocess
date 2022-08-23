# -*- coding: utf-8 -*-
"""
Created on Mon Aug 22 18:24:06 2022

@author: Enor
"""
import json
import csv



# JSON file to CSV
# Opening JSON file and loading the data
# into the variable data
line_list = []
with open('0013157800087578_02.json',encoding='utf-8') as f:
    while True:
        
        line = f.readline()
        if not line: # 到 EOF，返回空字符串，则终止循环
            break
        json_array = json.loads(line)

        print("coolwaterin:" + json_array["coolwaterin"])
        print("coolwaterout:" + json_array["coolwaterout"])
        print("icewaterin:" + json_array["icewaterin"])
        print("icewaterout:" + json_array["icewaterout"])
        print("tsctemp_l:" + json_array["tsctemp_l"])
        print("tsetemp_l:" + json_array["tsetemp_l"])
        print("tsctemp_r:" + json_array["tsctemp_r"])
        print("tsetemp_r:" + json_array["tsetemp_r"])
        
        
        
        










        
   
