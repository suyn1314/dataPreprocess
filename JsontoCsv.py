# -*- coding: utf-8 -*-
"""
Created on Mon Aug 22 18:24:06 2022

@author: Enor
"""
import json
import csv
import numpy as np
import matplotlib.pyplot as plt

# JSON file to CSV
# Opening JSON file and loading the data
# into the variable data


cop_right_list = []
cop_left_list = []
cop_right_time = []
cop_left_time = []
countR = -1
countL = -1
with open('datasets/2020/0013157800087578_09.json',encoding='utf-8') as f:
    while True:
        
        line = f.readline()
        if not line: # 到 EOF，返回空字符串，则终止循环
            break
        
        json_array = json.loads(line)
        icewaterin  = float(json_array["icewaterin"])
        icewaterout = float(json_array["icewaterout"])
        kw_right = float(json_array["kw_r"])
        kw_left = float(json_array["kw_l"])
        time = json_array["timestamp"]
        
        """
        預設冷凍能力 : 877Kw
        出廠cop : 4.3
        """
        
        """
         冰水機流量
         左機 1300L/min
         右機 1200L/min
        """
        # 冷凍能力(kw) = (流量 * 進出水溫差(C) * 60(h/m)) / 860
        coolkw = round((( 1300 * (icewaterin - icewaterout) * 60) / 860),2)
        
        """
        coolkw_list.insert(count, coolkw)
        time_list.insert(count, count)
        """
        
        if  kw_right > 0:
            countR +=1
            cop_right = coolkw / kw_right
            if 0 < cop_right < 4.3 :
                cop_right_list.insert(countR, cop_right)
                cop_right_time.insert(countR, countR)
                print("日期:" + json_array["timestamp"])
                print(f'冷凍能力 kw: {coolkw} Kw')
                print("右耗電(KW): " + json_array["kw_r"] + "KW")
                print(f'右機COP: {cop_right}')
        if  kw_left > 0:
            countL +=1
            cop_left = coolkw / kw_left
            if 0 < cop_left < 4.3:
                cop_left_list.insert(countL, cop_left)
                cop_left_time.insert(countL, countL)
                print("日期:" + json_array["timestamp"])
                print(f'冷凍能力 kw: {coolkw} Kw')
                print("左耗電(KW):" + json_array["kw_l"] + "KW")
                print(f'左機COP: {cop_left}')
        
        
        
        #t1 = 開始時間
        #t2 = 結束時間
        
        #h1 = (蒸發器出口溫 ,蒸發器壓力)
        #h2 = (壓縮機出口溫度 ,冷凝器壓力)
        #h3 = (冷凝器出口溫度 ,冷凝器壓力)
        
        #Tc = 低溫端溫度 ， Th  = 高溫端溫度
        

        #COP = 製冷能力(KW) / 消耗電力(KW) = 蒸發器入出口焓差 / 壓縮機出入口焓差
        #COP = ((t2h1 - t1h1) - (t2h3 - t1h3)) / ((t2h2 - t1h2) - (t2h1 - t1h1)) = Tc / (Th - Tc)
        
        
        """
        print("日期:" + json_array["timestamp"])
        print(f'冷凍能力 kw: {coolkw} Kw')
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
        """
        
        
        
#print(coolkw_list)
#print(time_list)

fig1 = plt.figure(figsize=(40,10),dpi=500)       
plt.title("Right COP") # title
plt.ylabel("COP") # y label
plt.xlabel("Time/number") # x label
plt.plot(cop_right_time,cop_right_list)
plt.savefig("2020DataRight9.png")
plt.show(fig1)

fig2 = plt.figure(figsize=(40,10),dpi=500)       
plt.title("Left COP") # title
plt.ylabel("COP") # y label
plt.xlabel("Time/number") # x label
plt.plot(cop_left_time,cop_left_list)
plt.savefig("2020DataLeft9.png")
plt.show(fig2)








        
   
