######## 비율 표시...값은 3,4,5,6,7  ...st_m
####part count 별 index 추출
import pandas as pd

def cal_rate(df):
    rate_df = pd.DataFrame(columns=['rate3', 'rate4', 'rate5', 'rate6', 'rate7'])
    spindle_vc = df['spindle_load'].value_counts()
    spindle_len = len(df)
    if 3 in spindle_vc:
        rate3 = spindle_vc[3] / spindle_len
    else:
        rate3= 0
    if 4 in spindle_vc:
        rate4 = spindle_vc[4] / spindle_len
    else:
        rate4= 0
    if 5 in spindle_vc:
        rate5 = spindle_vc[5] / spindle_len
    else:
        rate5= 0
    if 6 in spindle_vc:
        rate6 = spindle_vc[6] / spindle_len
    else:
        rate6= 0    
    if 7 in spindle_vc:
        rate7 = spindle_vc[7] / spindle_len
    else:
        rate7= 0
    new_data = {'rate3':[rate3],'rate4':[rate4],'rate5':[rate5],
                'rate6':[rate6],'rate7':[rate7]}
    rate_df = pd.concat([rate_df, pd.DataFrame(new_data)])    
    return rate_df