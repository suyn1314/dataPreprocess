# -*- coding: utf-8 -*-
"""
Created on Mon Aug 22 18:24:06 2022

@author: Enor
"""
import json
import pandas as pd
import matplotlib.pyplot as plt
from scipy import interpolate
#須安裝: pip install tsmoothie
from tsmoothie.smoother import LowessSmoother

# JSON file to CSV
# Opening JSON file and loading the data
# into the variable data
month = '09'

cop_list = [] 
cop_number = []
cop_date = []
running_time =[]
operation_num =[]
count = -1
datasets = f'datasets/2020/0013157800087578_{month}.json'
        
print(f'{month}月資料執行中....')        
with open(datasets,encoding='utf-8') as f:
    while True:
        
        #print(dataMonth)
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
        coolkw = (( 1300 * (icewaterin - icewaterout) * 60) / 860)
        
        """
        coolkw_list.insert(count, coolkw)
        time_list.insert(count, count)
        """
        
        #如果有電流
        if  kw_right > 0 or kw_left > 0:
            count +=1
            kw = kw_right + kw_left
            cop = coolkw / kw
            if  0 < cop < 4.3 :
                cop_list.insert(count, cop)
                cop_number.insert(count, count)
                cop_date.insert(count, time)
                running_time.insert(count, 3) #每筆資料間格3min
                operation_num.insert(count, 0)
               # print("日期:" + time)
               # print(f'冷凍能力 kw: {coolkw} Kw')
               # print(f'總耗電(KW): {kw} KW')
               # print(f'COP: {cop}')
                
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

        
        #t1 = 開始時間
        #t2 = 結束時間
        
        #h1 = (蒸發器出口溫 ,蒸發器壓力)
        #h2 = (壓縮機出口溫度 ,冷凝器壓力)
        #h3 = (冷凝器出口溫度 ,冷凝器壓力)
        
        #Tc = 低溫端溫度 ， Th  = 高溫端溫度
        

        #COP = 製冷能力(KW) / 消耗電力(KW) = 蒸發器入出口焓差 / 壓縮機出入口焓差
        #COP = ((t2h1 - t1h1) - (t2h3 - t1h3)) / ((t2h2 - t1h2) - (t2h1 - t1h1)) = Tc / (Th - Tc)
        
        
#print(cop_left_date)
#print(time_list)
print('平滑處理中....')
#平滑處理(scipy)
funR = interpolate.interp1d(cop_number,cop_list,kind='cubic')
sR = funR(cop_number)
#平滑處理(Tsmoothie)
tsmoothieR = LowessSmoother(smooth_fraction = 0.02,iterations=1)
tsmoothieR.smooth(cop_list)
tR = tsmoothieR.smooth_data #東西存在.smooth_data 裡面
COP = [float(x) for item in tR for x in item ] #刪除np.ndarray中的括號

print('畫圖中....')
#畫圖

print(cop_number)

fig1 , ax1 = plt.subplots(figsize=(10,5),dpi=200)
plt.ylim([0, 5])
plt.title("COP Data") # title
plt.ylabel("COP") # y label
plt.xlabel("Time 3 min/number") # x label

ax2 = ax1.twinx()
ax1.plot(cop_number, cop_list, color='tab:blue')
ax2.plot(cop_number, COP, color='black')
ax2.set_ylim([0, 5])
plt.savefig(f'img/2020Data{month}.png')

"""
#平滑數據
fig1 = plt.figure(figsize=(10,5),dpi=200)       
plt.title("COP Data") # title
plt.ylabel("COP") # y label
plt.xlabel("Time 3 min/number") # x label
plt.plot(cop_number,COP)#(x,y)
plt.ylim([0, 5])
plt.savefig(f'img/2020Data{month}.png')

#原始數據
fig3 = plt.figure(figsize=(10,5),dpi=200)       
plt.title("Orgin COP Data") # title
plt.ylabel("COP") # y label
plt.xlabel("Time 3 min/number") # x label
plt.plot(cop_number,cop_list)#(x,y)
plt.ylim([0, 5])
plt.savefig(f'img/2020OrginData{month}.png')
"""

print('存檔中....')
#存檔 趨勢數據
copDictionary = {"time" : cop_date ,
                 "Month" : month,
                   "COP" : COP ,
                   "operation_num" : operation_num ,
                   "running_time" : running_time
                   }
copData=pd.DataFrame(data=copDictionary)
copData.to_csv(f'datasets/copData/2020copData{month}.csv',encoding='utf-8')

#存檔 原始數據
copDictionary = {"time" : cop_date ,
                 "Month" : month,
                   "COP" : cop_list ,
                   "operation_num" : operation_num ,
                   "running_time" : running_time
                   }
copData=pd.DataFrame(data=copDictionary)
copData.to_csv(f'datasets/copData/2020copOrginData{month}.csv',encoding='utf-8')








        
   
