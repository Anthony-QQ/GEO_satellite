from config import plot_now
from GEO_satellite_image_plotter import plot_files
import time
import config

start_time = time.time()

TC_list = ['17_Irma']
#TC_list = config.full_list
f_num_rel = 0.49 #where to start plotting, from 0 to 1
plot_count = 1

if __name__ == '__main__' and plot_now:
    plot_files(TC_list, f_num_rel, plot_count)

print(f'{time.time() - start_time} seconds spent.')