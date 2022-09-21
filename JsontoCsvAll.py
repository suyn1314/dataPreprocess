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
import statistics

#開始月份
beginMonth = 1
#結束月份
endMonth = 12


totalcount = -1
countlist=[]
avg_list=[]
avg_count=[]

for i in range(beginMonth, endMonth+1):

    if i < 10:
        month = f'0{i}'
        cop_list = [] 
        cop_number = []
        cop_date = []
        running_time =[]
        operation_num =[]
        count = -1
        
        
        #Read_json (month,count,totalcount)
        print(f'{month}月資料執行中....')    
        datasets = f'datasets/2020/0013157800087578_{month}.json'
        
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
                
                # 冷凍能力(kw) = (流量 * 進出水溫差(C) * 60(h/m)) / 860
                coolkw = (( 1300 * (icewaterin - icewaterout) * 60) / 860)
                
    
                
                #如果有電流
                if  kw_right > 0 or kw_left > 0:
                    count +=1
                    totalcount +=1
                    kw = kw_right + kw_left
                    cop = coolkw / kw
                    if  0 < cop < 4.3 :
                        cop_list.insert(count, cop)
                        cop_number.insert(count, count)
                        cop_date.insert(count, time)
                        running_time.insert(count, 3) #每筆資料間格3min
                        operation_num.insert(count, 0)
                        countlist.insert(totalcount,totalcount)

        print('平滑處理中....')
        #平滑處理(scipy)
        funR = interpolate.interp1d(cop_number,cop_list,kind='cubic')
        sR = funR(cop_number)
        #平滑處理(Tsmoothie)
        tsmoothieR = LowessSmoother(smooth_fraction = 0.02,iterations=1)
        tsmoothieR.smooth(cop_list)
        tR = tsmoothieR.smooth_data #東西存在.smooth_data 裡面
        COP = [float(x) for item in tR for x in item ] #刪除np.ndarray中的括號
        #當月平均COP
        avg = statistics.mean(cop_list)
        print(f'{month}月COP平均為:{avg}')
        avg_list.insert(i, avg)
        avg_count.insert(i, i)
        
        
        print('畫圖中....')
        #畫圖
        fig1 = plt.figure(figsize=(10,5),dpi=200)       
        plt.title(f'{month} COP Data') # title
        plt.ylabel("COP") # y label
        plt.xlabel("Time 3 min/number") # x label
        plt.plot(cop_number,COP)#(x,y)
        plt.ylim([0, 5])
        plt.savefig(f'img/2020Data{month}.png')
        
        
        #原始數據
        fig3 = plt.figure(figsize=(10,5),dpi=200)       
        plt.title(f'{month} Orgin COP Data') # title
        plt.ylabel("COP") # y label
        plt.xlabel("Time 3 min/number") # x label
        plt.plot(cop_number,cop_list)#(x,y)
        plt.ylim([0, 5])
        plt.savefig(f'img/2020OrginData{month}.png')
        #COP_save_csv (month)
        
        print('存檔中....')
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
    else:
        month = f'{i}'
        cop_list = [] 
        cop_number = []
        cop_date = []
        running_time =[]
        operation_num =[]
        count = -1
        
        #Read_json (month,count,totalcount)
        print(f'{month}月資料執行中....')    
        datasets = f'datasets/2020/0013157800087578_{month}.json'
                
            
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
                
                # 冷凍能力(kw) = (流量 * 進出水溫差(C) * 60(h/m)) / 860
                coolkw = (( 1300 * (icewaterin - icewaterout) * 60) / 860)
                
    
                
                #如果有電流
                if  kw_right > 0 or kw_left > 0:
                    count +=1
                    totalcount +=1
                    kw = kw_right + kw_left
                    cop = coolkw / kw
                    if  0 < cop < 4.3 :
                        cop_list.insert(count, cop)
                        cop_number.insert(count, count)
                        cop_date.insert(count, time)
                        running_time.insert(count, 3) #每筆資料間格3min
                        operation_num.insert(count, 0)
                        countlist.insert(totalcount,totalcount)
        
        
        print('平滑處理中....')
        #平滑處理(scipy)
        funR = interpolate.interp1d(cop_number,cop_list,kind='cubic')
        sR = funR(cop_number)
        #平滑處理(Tsmoothie)
        tsmoothieR = LowessSmoother(smooth_fraction = 0.02,iterations=1)
        tsmoothieR.smooth(cop_list)
        tR = tsmoothieR.smooth_data #東西存在.smooth_data 裡面
        COP = [float(x) for item in tR for x in item ] #刪除np.ndarray中的括號
        #當月平均COP
        avg = statistics.mean(cop_list)
        print(f'{month}月COP平均為:{avg}')
        avg_list.insert(i, avg)
        avg_count.insert(i, i)
        
        
        print('畫圖中....')
        #畫圖
        fig1 = plt.figure(figsize=(10,5),dpi=200)       
        plt.title(f'{month} COP Data') # title
        plt.ylabel("COP") # y label
        plt.xlabel("Time 3 min/number") # x label
        plt.plot(cop_number,COP)#(x,y)
        plt.ylim([0, 5])
        plt.savefig(f'img/2020Data{month}.png')
        
        
        #原始數據
        fig2 = plt.figure(figsize=(10,5),dpi=200)       
        plt.title(f'{month} Orgin COP Data') # title
        plt.ylabel("COP") # y label
        plt.xlabel("Time 3 min/number") # x label
        plt.plot(cop_number,cop_list)#(x,y)
        plt.ylim([0, 5])
        plt.savefig(f'img/2020DataOrgin{month}.png')
        #COP_save_csv (month)
        
        print('存檔中....')
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
    pass


fig3 = plt.figure(figsize=(10,5),dpi=200)       
plt.title("COP 2020 Data Avg") # title
plt.ylabel("COP") # y label
plt.xlabel("month") # x label
plt.plot(avg_count,avg_list)#(x,y)
plt.ylim([0, 5])
plt.savefig(f'img/2020DataAvg.png')
    








        
   
