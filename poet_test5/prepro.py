###pyenv 사용하여 python 버전 설정
###poetry env use 3.8.5
###poetry install  실행 필요

import pandas as pd
import tensorflow as tf
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import dtw
from pickle import load
import __concat__ as r
import cal_rate as cr

def modi37(x):
    if x < 3.0:
        return 3.0
    elif x > 7.0:
        return 7.0
    return x    



##### 공백값 제거
r.concat('../data')

### 공백 제거한 데이터 읽고 병합
cycle_data1 = pd.read_csv('../data/rev_prg1.csv')
cycle_data2 = pd.read_csv('../data/rev_prg2.csv')
cycle_data3 = pd.read_csv('../data/rev_prg3.csv')
cycle_data = pd.concat([cycle_data1,cycle_data2,cycle_data3]).sort_values(['time']).reset_index(drop=True)

### 스케일러 로드
load_minmax_scaler = load(open('../ref/minmax_scaler.pkl', 'rb'))

#### dtw 기준값 읽기
dtw_base = pd.read_csv('../ref/dtw_interpol_df.csv')
#dtw_base_data = pd.read_csv('')


#### 불필요한 데이터 제거 및 컬럼 추출   --> 나중에 spindle_speed 추가
condition1 = (cycle_data.modal_T != 0) &(cycle_data.connected==True) &(cycle_data.status == 3) &(cycle_data.main_program_number == 6502.0)
columns = ['time','modal_T','spindle_load','axis_1_load','axis_2_load','axis_3_load','axis_1_pos_abs','axis_2_pos_abs','axis_3_pos_abs','part_count']
data_ = cycle_data[columns][condition1].reset_index(drop = True)
data_.time = pd.to_datetime(data_.time)

##### 다른 작업을 위한 값 추출 및 변환
data_['tool_num'] = data_['modal_T']//100
data_['time_d'] = data_['time'].dt.day
data_['time_h'] = data_['time'].dt.hour
data_['time_m'] = data_['time'].dt.minute 
data_['time_s'] = data_['time'].dt.second
data_['time_ms'] = data_['time'].dt.microsecond//100000 

##### 중복 제거
data_1 = data_.drop_duplicates(['time_d','time_h','time_s','time_m','spindle_load', 'axis_1_load', 'axis_2_load','axis_1_pos_abs','axis_2_pos_abs','axis_3_pos_abs','part_count']).reset_index(drop=True)

##### 해당 툴에 대한 데이터 분리
data_42 = data_1[(data_1.tool_num==42)].reset_index(drop=True)


#####  auto-encoder 용 변환
au_data_42 = data_42.copy()
####
condition_4th = (au_data_42.spindle_load>4)
au_data_42 = au_data_42[condition_4th].drop_duplicates().reset_index().drop('index',axis=1)
columns = ['time','modal_T','part_count','spindle_load']
au_data_42 = au_data_42[columns]

######## scaler 적용
au_data_42['spd_scaler'] = load_minmax_scaler.fit_transform(au_data_42.spindle_load.values.reshape(-1,1))


######## DTW 돌리기 위한 전처리
aa = []
for i,ii in zip(au_data_42.spindle_load.index,au_data_42.spindle_load) :
    if ii <= 10 :
        aa.append(1)
    elif 10 < ii <= 20:
        aa.append(2)
    elif 20 < ii <= 30:
        aa.append(3)
    elif 30 < ii <= 40:
        aa.append(4)
    elif 40 < ii <= 50:
        aa.append(5)
    else :
        aa.append(6)

au_data_42['spd'] = aa
######## DTW 수행 및 범주 분류

a = dtw_base.spd.values
b = au_data_42.spd.values
query = np.sin(a) 
query2 = np.sin(b)
dis = dtw.dtw(query, query2, keep_internals=True).distance

if dis < 5 :
    dtw_dis = 1
    
elif 5<= dis < 10:
    dtw_dis=2
    
elif 10 <= dis  :
    dtw_dis=3

######## DTW 기준 크기에 맞추어 보간
######## 보간 결과 저장 형태를 어떻게 해야 할 것인가....
a = dtw_base.spd_scaler.values
b = au_data_42.spd_scaler.values
interp_au_data_42 = np.interp(np.arange(0,a.shape[0]),np.linspace(0,a.shape[0],num=b.shape[0]),b)
pd.DataFrame(interp_au_data_42).to_csv('../pre_res/ae_pre.csv', index=False)

### 범주 저장은 사용하지 않음
### pd.DataFrame([dtw_dis], index=['dtw_dis']).to_csv('../pre_res/dtw_dis.csv')



##### classification 용 변환
######## 상한 하한 변경
cla_data_42 = data_42.copy()
cla_data_42['spindle_load'] = cla_data_42['spindle_load'].apply(modi37)

######## 비율로 데이터 표시
data_42_rate = cr.cal_rate(cla_data_42)

######## 비율 데이터프레임 저장
data_42_rate.to_csv('../pre_res/rate_df.csv', index=False)
