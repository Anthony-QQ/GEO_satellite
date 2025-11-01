from plot_parameters import plot_now
from GEO_satellite_image_plotter import plot_files


TC_list = ['25_Melissa']
f_num_rel = 0.4 #where to start plotting, from 0 to 1
plot_count = 1

if __name__ == '__main__' and plot_now:
    plot_files(TC_list, f_num_rel, plot_count)