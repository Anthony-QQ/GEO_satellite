import ABI_plotter
import GVAR_plotter
from MODIS_plotter import MODIS_list
from GEO_plotter import plot_GEO
from my_cmap import produce_cmap_list
from my_functions import ABI_list, GVAR_list, browse_folder, save_ADT, get_time
from plot_parameters import (cc_size, cmap_name_list, crop_param,
    ask_TC,ask_time,do_ADT,draw_full,plot_all_TC_images,
                             time_range,update_ADT,use_track)

'''
from ABI_plotter import ABI_list
#timeit.timeit('[i*2 for i in range(1000) if i == 900]', number=10000)
#x = [i for i in range(1000) if i == 30][0]
#print(x)
'''






def plot_files(TC_list, f_num_rel, plot_count):
    f_num_list = [0]
    produce_cmap_list()
    print(ABI_list)

    if ask_TC:
        TC_0 = input('Name of TC? Format: yy_Name')
        TC_list = [TC_0]
    print(TC_list)
    for sat_name in GVAR_list:
        folder_list = browse_folder(sat_name)
        print(sat_name, folder_list)
        for TC in TC_list:
            if TC in folder_list:
                if do_ADT:
                    ADT_list = []
                    
                file_list = browse_folder(sat_name, TC)
                im_count = len(file_list)
                print('There are ' + str(im_count) + ' files for ' + str(TC) + ' in ' + sat_name)
                start = int(im_count*f_num_rel)
                end = int(im_count*f_num_rel)+plot_count
                if ask_time and not time_range:
                    start = max(0,min(int(input('Start #? Max = ' + str(im_count))),im_count))
                    end = max(start,min(int(input('End #? Range = ' + str(start) + ' - ' + str(im_count))),im_count))
                f_num_list = range(start,end)

                if plot_all_TC_images or time_range:
                    f_num_list = range(im_count) #override previous assignment of file list
                if time_range:
                    print('Total number of files: ' + str(im_count))
                    min_time_0 = get_time(0, sat_name, TC)
                    max_time_0 = get_time(im_count-1, sat_name, TC)
                    min_time = max(min_time_0,min(int(input('Min time? Range = ' + str(min_time_0) + ' - ' + str(max_time_0) + '\n')),max_time_0))
                    max_time = max(min_time,min(int(input('Max time? Range = ' + str(min_time) + ' - ' + str(max_time_0) + '\n')),max_time_0))
                else:
                    min_time = max_time = 0
                
                for f_num in f_num_list:
                    ADT_item = plot_GEO(f_num,sat_name,TC,crop_param,
                                         no_crop=draw_full,cmap_name_list=cmap_name_list,im_size=10,dpi=100,
                                        TC_marker_r=cc_size,min_time=min_time,max_time=max_time,
                                         use_track=use_track)
                    
                    if do_ADT and type(ADT_item) is list:
                        ADT_list.append(ADT_item)
                
                save_ADT(ADT_list, TC, do_ADT, update_ADT)
                
                
    for sat_name in ABI_list:
        folder_list = browse_folder(sat_name)
        print(sat_name, folder_list)
        for TC in TC_list:
            if TC in folder_list:
                projection = 0
                if do_ADT:
                    ADT_list = []
                    
                file_list = browse_folder(sat_name, TC)
                im_count = len(file_list)
                print('There are ' + str(im_count) + ' files for ' + str(TC) + ' in ' + sat_name)
                start = int(im_count*f_num_rel)
                end = int(im_count*f_num_rel)+plot_count
                
                if ask_time and not time_range and False:
                    start = max(0,min(int(input('Start #? Max = ' + str(im_count))),im_count))
                    end = max(start,min(int(input('End #? Range = ' + str(start) + ' - ' + str(im_count))),im_count))
                    
                f_num_list = range(start,end)

                if plot_all_TC_images or time_range:
                    f_num_list = range(im_count) #override previous assignment of file list
                if time_range and False:
                    print('Total number of files: ' + str(im_count))
                    min_time_0 = get_time(0, sat_name, TC)
                    max_time_0 = get_time(im_count-1, sat_name, TC)
                    min_time = max(min_time_0,min(int(input('Min time? Range = ' + str(min_time_0) + ' - ' + str(max_time_0) + '\n')),max_time_0))
                    max_time = max(min_time,min(int(input('Max time? Range = ' + str(min_time) + ' - ' + str(max_time_0) + '\n')),max_time_0))
                
                for f_num in f_num_list:
                    ADT_item = plot_GEO(f_num,sat_name,TC,crop_param,
                                                    no_crop=draw_full,cmap_name_list=cmap_name_list,im_size=10,dpi=100,
                                        TC_marker_r=cc_size, time_range=time_range)
                                        
                    if do_ADT and type(ADT_item) is list:
                        ADT_list.append(ADT_item)
                
                save_ADT(ADT_list, TC, do_ADT, update_ADT)
'''
    for sat_name in MODIS_list:
        print(sat_name)
        folder_list = browse_folder(sat_name, type='hdf4')
        print(folder_list)
        for TC in TC_list:
            if TC in folder_list:
                file_list = browse_folder(sat_name, type='hdf4')
                im_count = len(file_list)
                print('There are ' + str(im_count) + ' files for ' + str(TC) + ' in ' + sat_name)
                start = int(im_count * f_num_rel)
                end = int(im_count * f_num_rel) + plot_count
                f_num_list = range(start, end)
                for f_num in f_num_list:
                    plot_GEO(f_num, sat_name, TC, crop_param,
                             no_crop=draw_full, cmap_name_list=cmap_name_list, im_size=10, dpi=100, TC_marker_r=cc_size,
                             time_range=time_range)
'''