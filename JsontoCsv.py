# -*- coding: utf-8 -*-
"""
Created on Mon Aug 22 18:24:06 2022

@author: Enor
"""
import json
import csv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import interpolate
#須安裝: pip install tsmoothie
from tsmoothie.utils_func import sim_randomwalk
from tsmoothie.smoother import LowessSmoother

# JSON file to CSV
# Opening JSON file and loading the data
# into the variable data


cop_right_list = [] 
cop_left_list = []
cop_right_number = []
cop_left_number = []
cop_right_date = []
cop_left_date = []
running_time_r =[]
running_time_l = []
operation_num_r =[]
operation_num_l =[]
countR = -1
countL = -1
with open('datasets/2020/0013157800087578_09.json',encoding='utf-8') as f:
    while True:
        
        line = f.readline()
        if not line: # 到 EOF，返回空字符串，则终止循环
            break
        operation_num = []
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
        coolkw = (( 1300 * (icewaterin - icewaterout) * 60) / 860)
        
        """
        coolkw_list.insert(count, coolkw)
        time_list.insert(count, count)
        """
        #如果右機有電流
        if  kw_right > 0:
            countR +=1
            cop_right = coolkw / kw_right
            if 0 < cop_right < 4.3 :
                cop_right_list.insert(countR, cop_right)
                cop_right_number.insert(countR, countR)
                cop_right_date.insert(countR, time)
                running_time_r.insert(countR, 3) #每筆資料間格3min
                operation_num_r.insert(countR, 0)
                print("日期:" + time)
                print(f'冷凍能力 kw: {coolkw} Kw')
                print(f'右耗電(KW): {kw_right} KW')
                print(f'右機COP: {cop_right}')
        
        #如果左機有電流        
        if  kw_left > 0:
            countL +=1
            cop_left = coolkw / kw_left
            if 0 < cop_left < 4.3:
                cop_left_list.insert(countL, cop_left)
                cop_left_number.insert(countL, countL)
                cop_left_date.insert(countL, time)
                running_time_l.insert(countL, 3) #每筆資料間格3min
                operation_num_l.insert(countL, 0)
                print("日期:" + time)
                print(f'冷凍能力 kw: {coolkw} Kw')
                print(f'左耗電(KW): {kw_left} KW')
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
        
#print(cop_left_date)
#print(time_list)
#平滑處理(scipy)
funR = interpolate.interp1d(cop_right_number,cop_right_list,kind='cubic')
sR = funR(cop_right_number)
#平滑處理(Tsmoothie)
tsmoothieR = LowessSmoother(smooth_fraction = 0.02,iterations=1)
tsmoothieR.smooth(cop_right_list)
tR = tsmoothieR.smooth_data #東西存在.smooth_data 裡面
COPr = [float(x) for item in tR for x in item ] #刪除np.ndarray中的括號

tsmoothieL = LowessSmoother(smooth_fraction = 0.02,iterations=1)
tsmoothieL.smooth(cop_left_list)
tL = tsmoothieL.smooth_data #東西存在.smooth_data 裡面
COPl = [float(x) for item in tL for x in item ] #刪除np.ndarray中的括號
#print(np.ndarray.tolist(tR))
#print(COPr)

#右機畫圖
fig1 = plt.figure(figsize=(10,5),dpi=200)       
plt.title("Right COP") # title
plt.ylabel("COP") # y label
plt.xlabel("Time/number") # x label
plt.plot(cop_right_number,COPr)#(x,y)
plt.ylim([0, 5])
plt.savefig("img/2020DataRight9.png")


#左機畫圖
fig2 = plt.figure(figsize=(10,5),dpi=200)       
plt.title("Left COP") # title
plt.ylabel("COP") # y label
plt.xlabel("Time/number") # x label
plt.plot(cop_left_number,COPl)
plt.ylim([0, 5])
plt.savefig("img/2020DataLeft9.png")


#原始數據(右)
fig3 = plt.figure(figsize=(10,5),dpi=200)       
plt.title("Orgin Right COP") # title
plt.ylabel("COP") # y label
plt.xlabel("Time/number") # x label
plt.plot(cop_right_number,cop_right_list)#(x,y)
plt.ylim([0, 5])
plt.savefig("img/2020DataOrginRight9.png")

#原始數據(左)
fig4 = plt.figure(figsize=(10,5),dpi=200)       
plt.title("Orgin Left COP") # title
plt.ylabel("COP") # y label
plt.xlabel("Time/number") # x label
plt.plot(cop_left_number,cop_left_list)
plt.ylim([0, 5])
plt.savefig("img/2020DataOrginLeft9.png")


#右機存檔
rightDictionary = {"time" : cop_right_date ,
                   "C.O.P" : COPr ,
                   "operation_num" : operation_num_r ,
                   "running_time" : running_time_r
                   }
rightCOP=pd.DataFrame(data=rightDictionary)
rightCOP.to_csv('datasets/copData/2020copR9.csv',encoding='utf-8')

#左機存檔
leftDictionary = {"time" : cop_left_date ,
                  "C.O.P" : COPl ,
                  "operation_num" : operation_num_l ,
                  "running_time" : running_time_l
                  }
leftCOP=pd.DataFrame(data=leftDictionary)
leftCOP.to_csv('datasets/copData/2020copL9.csv',encoding='utf-8')






        
   
