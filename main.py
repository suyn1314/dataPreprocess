import os
from os import listdir
from os.path import isfile, isdir, join
import json
import csv
import matplotlib.pyplot as plt
import numpy as np
import moment
import argparse
import math

import pandas as pd
import numpy as np

from hotelling import hotellingFilter
from dimensionalityReduction2 import transform_data, reduce_data
"""
JSON2CSV -> hotelling -> dimensionalityReduction2

{
"_id":{"$oid":"5e344f09b8f09cb14ddaa673"}, 0.id
"coolwaterin":"19.9",      1.冷卻水入口溫度
"coolwaterout":"21.5",     2.冷卻水出口溫度
"icewaterin":"16.8",       3.冰水入口溫度
"icewaterout":"16",        4.冰水出口溫度
"pipeouttemp_l":"22.6",    5.左機吐出溫度
"pipeouttemp_r":"22.7",    6.右機吐出溫度
"comphipress_l":"4.34",    7.左機高壓
"complowpress_l":"4.32",   8.左機低壓
"comphipress_r":"4.2",     9.右機高壓
"complowpress_r":"4.22",  10.右機低壓
"voltage":"37",           11.電壓
"circuit_l":"0",          12.左機電流
"circuit_r":"0",          13.右機電流
"lev_l":"0",              14.左機LEV開度
"lev_r":"0",              15.右機LEV開度 
"compfrequency":"0",      16.壓縮機頻率
"tsetemp_l":"17.3",       17.左飽和冷凝溫度(Tsc) 右飽和蒸發溫度(Tse)
"tsctemp_r":"16.6",       18.左飽和蒸發溫度(Tse)
"tsetemp_r":"16.6",       19.右飽和冷凝溫度(Tsc)
"kw_l":"0",               20.左耗電(KW)
"kw_r":"0",               21.右耗電(KW)
"settemperature":"13.5",  22.冰水設定溫度
"leftcompruntime":"10223",23.左機累計運轉時數
"rightcompruntime":"7001",24.右機累計運轉時數
"systemminute":"1",       25.PLC時間
"icewateriotempset":"1",  26.
"errorcode_1_str":"0",    27.
"errorcode_2_str":"0",    28.
"copplcleft":"0",         29.
"copplcright":"0",        30.
"timestamp":"2020-02-01 00:00:09" 31.資料存入資料庫時間
}
0時間
1冰水入口溫度
2冰水出口溫度
3冷卻水入口溫度
4冷卻水出口溫度
5右機LEV開度Step
6右機低壓
7右機吐出溫度
8右機電流
9右機高壓
10右耗電
11右飽和冷凝溫度
12右飽和蒸發溫度
13壓縮機頻率        
14左機LEV開度Step   
15左機低壓 #
16左機吐出溫度  %
17左機電流
18左機高壓 #
19左耗電
20左飽和冷凝溫度（冷凝器出口） %
21左飽和蒸發溫度(蒸發器出口 假設吸入) %
22設溫

{
 "name":"PQ",
 "columns":[
     "time","冰水入口溫度","冰水出口溫度","冷卻水入口溫度","冷卻水出口溫度","右機LEV開度Step","右機低壓","右機吐出溫度","右機電流","右機高壓","右耗電","右飽和冷凝溫度","右飽和蒸發溫度","壓縮機頻率","左機LEV開度Step","左機低壓","左機吐出溫度","左機電流","左機高壓","左耗電","左飽和冷凝溫度","左飽和蒸發溫度","設溫"],
 "values":[[1588263125,15.6,15.2,33.2,33.4,null,4.38,51.7,0,4.42,0,null,null,0,null,4.18,50.7,0,4.27,0,null,null,9]

"""

def main():
    '''
    將資料整理成有用的資料
    '''
    parser = argparse.ArgumentParser()

    # BP parameter
    parser.add_argument('--bp', default=True,
                        help='True : BP AIR CONDITIONER , False: AIR CONDITIONER')

    args = parser.parse_args()


    JSON2CSV("datasets/rawData/")
    
    makeUsefulData(args, "datasets/rawData_csv/")
    hotellingFilter(args,"datasets/usefulData")

    transform_data(args, "datasets/hotelling")
    reduce_data("datasets/copData")


def JSON2CSV(dirName):
    '''
    convert JSON format into CSV format
    '''
    save_dir = "datasets/rawData_csv/"
    # get all folder name in save_dir
    folders = listdir(dirName)

    for folderName in folders:
        # get all file in folder
        files = listdir(join(dirName, folderName))
        # create save dir
        save_dir = join("datasets", "rawData_csv", folderName)

        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        for fileName in files:
            with open(join(dirName, folderName, fileName), 'r', encoding='utf-8') as f:
                jsonData = json.loads(f.read())
                # 開啟輸出的 CSV 檔案
                with open(join(save_dir, fileName.split('.')[0]+'.csv', encoding='utf-8'), 'w', newline='') as csvfile:
                    # 建立 CSV 檔寫入器
                    writer = csv.writer(csvfile)
                    # 寫入資料
                    writer.writerow(jsonData['columns'])
                    for rowData in jsonData['values']:
                            writer.writerow(rowData)


def makeUsefulData(args, dirName):
    folders = listdir(dirName)
    
    for folderName in folders:
        filtedData = []
        files = listdir(join(dirName, folderName))
        files = sorted(files)
        operation_num = 1
        running_time = 0

        save_dir = join("datasets", "usefulData", folderName)
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        for fileName in files:
            df = pd.read_csv(join(dirName, folderName, fileName))
            titles = np.array(df.columns)
            datas = df.iloc[:, :].to_numpy(dtype=float)
            datas, operation_num, running_time = filterData(args, datas, operation_num, running_time)

            # print(join(dirName, folderName, fileName), np.sum(datas[:,:],axis=0)/datas.shape[0])
            # break

            # 開啟輸出的 CSV 檔案
            if datas.shape[0] > 0:
                operation_num += 1
                # if args.bp:
                #     datas[:,14:-1] = meanfilter(datas[:,14:-1])
                print(moment.unix(datas[0,0]))
                with open(join(save_dir, fileName.split('.')[0]+'.csv'), 'w', newline='') as csvfile:
                    # 建立 CSV 檔寫入器
                    writer = csv.writer(csvfile)
                    # 寫入資料
                    titles = (titles).tolist()
                    titles.append('開機次數')
                    titles.append('運轉時間')
                    writer.writerow(titles)

                    for r in range(datas.shape[0]):
                        # if datas[r,3]<24:
                        #     print(datas[r,0], moment.unix(datas[r,0]),"==")
                        writer.writerow(datas[r,:])
                        filtedData.append(datas[r,:])
        
        filtedData = np.array(filtedData)

        if args.bp:
            print(filtedData.shape)
            drawPlot(filtedData, folderName)
            
"""          
        else:
            drawPlot2(filtedData, folderName)
"""

def filterData(args, datas, operation_num, running_time):
    '''
    it only retain working data.

    # 開機次數
    operation_num
    # 運轉時間
    running_time
    '''

    filtedData = []


    idx_list=[]
    if args.bp:
        #15左機低壓  18左機高壓  16左機吐出溫度  21左飽和蒸發溫度(蒸發器出口)  20左飽和冷凝溫度（冷凝器出口）19左耗電
        idx_list = [15, 18, 16, 21, 20, 19]
    else:
        #右機低壓 9右機高壓 7右機吐出溫度 12右飽和蒸發溫度(資料缺) 11右飽和冷凝溫度 10右耗電
        idx_list = [6, 9, 7, 12, 11, 10]
    # idx_list = [16]
    values_mean = np.zeros((len(idx_list)))

    first_data_flag = True
    ignore_data_num = 1
    ignore_data_cnt = 1

    # 先取得第一筆資料時間
    if datas.shape[0] >0:
        # 0時間
        current_unix = datas[0,0]
        # print(current_unix)

    for i in range(datas.shape[0]):
        data = datas[i,:]

        if args.bp:
            # 左機電流
            electric_current = data[17]
            # 左耗電
            power_current = data[19]
            # 壓縮機頻率       
            freq = data[13]
        else:
            # 右機電流
            electric_current = data[8]
            # 右耗電
            power_current = data[10]
            # 壓縮機預設頻率  
            freq = 60


        if (electric_current > 0 and electric_current <500) and (power_current > 0 and power_current <100) and (freq >0):
            if first_data_flag == True:
                if ignore_data_cnt < ignore_data_num:
                    ignore_data_cnt = ignore_data_cnt+1
                    running_time = running_time +2
                    continue
                
                if np.abs(data[0]-current_unix) > 600:
                    print(operation_num)
                    print(data[0])
                    operation_num += 1
                    print(operation_num)
                first_data_flag = False
                running_time = running_time +2
            else:
                error_flag = False
                for x, idx in enumerate(idx_list):
                    if not(data[idx] < 100 and data[idx] > 0):
                        # print(data[0], moment.unix(data[0]),"==")
                        error_flag = True
                        break
                if error_flag == False:
                    # print(data)
                    running_time = running_time +2
                    data = np.concatenate((np.reshape(data,(1,data.shape[0])), np.array([[operation_num,running_time]])), axis=1)
                    filtedData.append(data[0,:])
        else:
            if first_data_flag != True and len(filtedData)>0:
                filtedData.pop()
            first_data_flag = True
            ignore_data_cnt = 0

        # 更改為現在時間
        current_unix = data[0]
    

    filtedData = np.array(filtedData)
    if filtedData.shape[0]>0:
        _, idx = np.unique(filtedData[:,0], return_index=True)
        filtedData = filtedData[np.sort(idx),:]
    return filtedData, operation_num, running_time

def drawPlot(datas, folderName):
    '''
    變頻
    '''
    fig, axs = plt.subplots(7, 1)
    
    axs[0].plot(datas[:,16], label='Compressor discharge', color='#ff3300')
    axs[0].plot(datas[:,20], label='Condenser outlet', color='#ffb969')
    # axs[0].plot(datas[:,21], label='Evaporator outlet', color='#9bbcff')

    axs[1].plot(datas[:,21], label='Evaporator outlet', color='#9bbcff')

    axs[2].plot(datas[:,2], label='Evaporator water outlet', color='b')
    axs[2].plot(datas[:,1], label='Evaporator water inlet', color='orange')

    axs[3].plot(datas[:,4], label='Condenser water outlet', color='b')
    axs[3].plot(datas[:,3], label='Condenser water inlet', color='orange')

    axs[4].plot(datas[:,19], label='Compressor power', color='orange')

    axs[5].plot(datas[:,18], label='Compressor high pressure', color='#ff3300')
    axs[6].plot(datas[:,15], label='Compressor low pressure', color='#9bbcff')
    
    for ax in axs:
        ax.legend()
        ax.grid()
    fig.canvas.set_window_title(folderName+'變頻')
    plt.subplots_adjust(hspace=0.5)
    plt.show()
"""
def drawPlot2(datas, folderName):
    '''
    定頻
    '''
    fig, axs = plt.subplots(5, 1)
    
    axs[0].plot(datas[:,7], label='Compressor discharge', color='#ff3300')
    axs[0].plot(datas[:,11], label='Condenser outlet', color='#ffb969')
    # axs[0].plot(datas[:,21], label='Evaporator outlet', color='#9bbcff')

    axs[1].plot(datas[:,12], label='Evaporator outlet', color='r')

    axs[2].plot(datas[:,2], label='Evaporator water outlet', color='b')
    axs[2].plot(datas[:,1], label='Evaporator water inlet', color='orange')

    axs[3].plot(datas[:,4], label='Condenser water outlet', color='b')
    axs[3].plot(datas[:,3], label='Condenser water inlet', color='orange')

    axs[4].plot(datas[:,10], label='Compressor power', color='orange')
    
    for ax in axs:
        ax.legend()
        ax.grid()
    fig.canvas.set_window_title(folderName+'定頻')
    plt.subplots_adjust(hspace=0.5)
    plt.show()
"""
def Gaussianfilter(y):

    y = y.swapaxes(0,1)

    r=2
    sigma=1
    gaussTemp = np.zeros((r*2-1, 1))
    for i in range(1,r*2):
        gaussTemp[i-1]= math.exp(-(i-r)**2/(2*sigma**2))/(sigma*math.sqrt(2*math.pi))
    
    y_filted = np.copy(y)
    for i in range(r, y.shape[1]-r):
        print(y[:,i-r+1:i+r])
        print(gaussTemp)
        y_filted[:,i-1:i] = np.matmul(y[:,i-r+1:i+r], gaussTemp)
        print(y_filted[:,i-1:i],"==")

    y_filted = y_filted.swapaxes(0,1)
    return y_filted


def meanfilter(y):

    y = y.swapaxes(0,1)

    r=2
    gaussTemp = np.ones((r*2-1, 1))/(r*2-1)

    
    y_filted = np.copy(y)
    for i in range(r-1, y.shape[1]-(r-1)):
        # print(y[:,i-r+1:i+r])
        y_filted[:,i-1:i] = np.matmul(y[:,i-r+1:i+r], gaussTemp)
        # print(y_filted[:,i-1:i],"==")

    y_filted = y_filted.swapaxes(0,1)
    return y_filted
    
if __name__ == "__main__":
    main()
