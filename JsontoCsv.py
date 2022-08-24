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
with open('datasets/7578_2021/0013157800087578_02.json',encoding='utf-8') as f:
    while True:
        
        line = f.readline()
        if not line: # 到 EOF，返回空字符串，则终止循环
            break
        json_array = json.loads(line)
        
        #t1 = 開始時間
        #t2 = 結束時間
        
        #h1 = (蒸發器出口溫 ,蒸發器壓力)
        #h2 = (壓縮機出口溫度 ,冷凝器壓力)
        #h3 = (冷凝器出口溫度 ,冷凝器壓力)
        
        #Tc = 低溫端溫度 ， Th  = 高溫端溫度
        

        #COP = 製冷能力(KW) / 消耗電力(KW) = 蒸發器入出口焓差 / 壓縮機出入口焓差
        #COP = ((t2h1 - t1h1) - (t2h3 - t1h3)) / ((t2h2 - t1h2) - (t2h1 - t1h1)) = Tc / (Th - Tc)
        
        print("日期:" + json_array["timestamp"])
        print("冷卻水入口溫度:" + json_array["coolwaterin"] + "℃")
        print("冷卻水出口溫度:" + json_array["coolwaterout"] + "℃")
        print("冰水入口溫度:" + json_array["icewaterin"] + "℃")
        print("冰水出口溫度:" + json_array["icewaterout"] + "℃")
        print("左飽和蒸發溫度(Tse):" + json_array["tsetemp_l"] + "℃")
        print("左飽和蒸發溫度(Tse):" + json_array["tsctemp_r"] + "℃")
        print("右飽和冷凝溫度(Tsc):" + json_array["tsetemp_r"] + "℃")
        print("右飽和蒸發溫度(Tse):" + json_array["tsctemp_l"] + "℃")
        print("左耗電(KW):" + json_array["kw_l"] + "KW")
        print("右耗電(KW): " + json_array["kw_r"] + "KW")
        
        
        
        
        










        
   
