def concat(foldername):
    import pandas as pd
    import os

    filelist = os.listdir(foldername)
    file_name = []

##### 파일명에 rev 들어가면 예외처리
    for file in filelist:
        if 'rev' in file:
            continue
        if file.count(".") == 1:
            if file.split('.')[1] == 'pkl':
                continue
            name = file.split('.')[0]
            if len(name) == 0:
                continue
            file_name.append(name)
        else:
            continue
            
    for filename in file_name:
#        print(filename + '.csv processing')
        data = pd.read_csv(foldername+'/'+filename+'.csv', encoding = 'ISO-8859-1', 
            dtype={'name':str, 'time':str,'nc_id':str,'axis_1_load':float,'axis_1_pos_abs ':float,'axis_2_load':float,
            'axis_2_pos_abs ':float,'axis_3_load':float,'axis_3_pos_abs ':float,'axis_4_pos_abs ':float,'axis_5_pos_abs ':float,
            'axis_6_pos_abs ':float,'spindle_load':float,'part_count':float,'total_part_count':float,'main_program_comment':str, 
            'main_program_number':float,'modal_T':float,'modal_R':float,'modal_H':float, 'spindle_override':float, 'status':float, 'connected':str})

        ####column break
        d_axis_1_load = data['axis_1_load']
        d_axis_2_load = data['axis_2_load']
        d_axis_3_load = data['axis_3_load']
        d_axis_1_pos_abs = data['axis_1_pos_abs']
        d_axis_2_pos_abs = data['axis_2_pos_abs']
        d_axis_3_pos_abs = data['axis_3_pos_abs']
        d_axis_4_pos_abs = data['axis_4_pos_abs']
        d_axis_5_pos_abs = data['axis_5_pos_abs']
        d_axis_6_pos_abs = data['axis_6_pos_abs']
        d_time_sl = data.loc[:, ['time','nc_id', 'spindle_load']]
        d_pc = data['part_count']
        d_tpc = data['total_part_count']
        d_mpc = data['main_program_comment']
        d_mpn = data['main_program_number']
        d_modal_T = data['modal_T']
        d_modal_R = data['modal_R']
        d_modal_H = data['modal_H']
        d_spd_override = data['spindle_override']
        d_status = data['status']
        d_connected = data['connected']

        d_list = [d_time_sl, d_axis_1_load, d_axis_2_load,  d_axis_3_load, d_pc, d_tpc, d_mpc, d_mpn, d_axis_1_pos_abs, d_axis_2_pos_abs, d_axis_3_pos_abs, 
        d_axis_4_pos_abs, d_axis_5_pos_abs, d_axis_6_pos_abs, d_modal_T, d_modal_R, d_modal_H, d_spd_override, d_status, d_connected]
        d_name_list = ['d_time_sl', 'd_axis_1_load', 'd_axis_2_load',  'd_axis_3_load', 'd_pc', 'd_tpc' 'd_mpc', 'd_mpn', 'd_axis_1_pos_abs, ', 'd_axis_2_pos_abs, ', 'd_axis_3_pos_abs, ',
        'd_axis_4_pos_abs, ', 'd_axis_5_pos_abs, ', 'd_axis_6_pos_abs, ', 'd_modal_T', 'd_modal_R', 'd_modal_H', 'd_spd_override', 'd_status', 'd_connected']

        #### null dup
        for d_l in d_list:
            d_l.dropna(inplace = True)
            d_l.reset_index(drop = True, inplace = True)

        #### gen dataframe
        data_tmp = pd.concat(d_list, axis=1)
        data_tmp.dropna(inplace= True)

        data_tmp.to_csv(foldername+'/'+'rev_'+filename+'.csv', index = False)
