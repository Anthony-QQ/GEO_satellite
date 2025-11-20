update_ADT = False  #saves ADT txt files according to TC name
save_image = False  #saves TC images to directories sorted by crop status, TC name, band
save_CDO_image = False  #saves CDO analysis image sorted by TC name, band
make_image = True  #creates the images
show_image = True  #makes the image remain stuck in window

plot_all_TC_images = False  #TAKES TIME


TC_pos = [21.5, -53.8]  #random initial guess of TC position
im_extent = [6]  #Length of image, in degrees
crop_param = TC_pos + im_extent

plot_now = True   #Plot now or not
ask_choices = False   #Ask for TC name/time, otherwise the code needs to be modified
ask_TC = False   #Ask for TC name, otherwise the code needs to be modified
ask_time = False   #Ask for TC time, otherwise the code needs to be modified


draw_full = False   #Draw with or without cropping
draw_clean = False   #Draw with or without elements and gridlines in the plot
overwrite_image = True  #saves new image even when old one exist (DEFAULT)
fix_parallax = False
use_track = True   #Use track file or not
plot_track = True   #Show track or not
show_center = True   #Label fitted center or not
cc_size = 1   #Center marker size
use_CDO_size = True   #
show_gridline = True   #Show lat/lon gridlines or not
show_RMW = True   #Display RMW or not
new_RMW = True   #Use newer (box) method of finding RMW or not
draw_CDO = True   #
analyse_CDO = True   #Analyse CDO traits (max/min temperature, standard deviation aka smoothness)
show_CDO_analysis = False   #Show the plots of CDO traits
find_center = True   #Attempt to locate a center, using an eye fit
quick_center = False   #Default to a simpler center-finding algorithm
do_ADT = True

time_range = True
default_cmap = False   #Use default or user-specified colormaps
use_bw_cmap = False   #Use black-and-white colormaps

#cmap_name_list = ['wv_nrl','wv_ssd','wv_cc_2','ir_ca','ir_cc','ir_cc_2']
cmap_name_list = ['wv_cc_2','ir_cc_2']

full_list = ['00_Keith', '01_Erin', '01_Michelle', '96_Hortense', '98_Georges', '98_Mitch', '99_Bret', '99_Floyd', '99_Lenny',
             '03_Lupit', '03_Maemi', '04_Dianmu', '04_Heta', '97_Linda',
             '02_Elida', '02_Hernan', '02_Kenna', '04_Heta10', '05_Meena', '05_Nancy', '05_Olaf', '05_Percy',
             '07_Flossie', '09_Rick11', '10_Celia',
             '03_Isabel', '04_Catarina', '04_Ivan', '05_Emily', '05_Katrina', '05_Rita', '05_Wilma', '07_Dean',
             '07_Felix', '08_Paloma', '09_Rick',
             '10_Earl', '16_Nicole', '17_Harvey', '17_Irma', '17_Jose', '17_Maria',
             '14_Simon', '15_Hilda', '15_Ignacio', '15_Patricia', '18_Hector', '18_Lane',
             '19_Dorian', '20_Epsilon', '20_Eta', '20_Iota', '20_Laura', '21_Sam', '23_Lee', '24_Milton16',
             '23_Jova', '24_Milton', '25_Erin', '25_Melissa']


#Correlated variables
time_range = time_range and ask_time

if draw_full:
    find_center = False
    analyse_CDO = False
    show_CDO_analysis = False
if update_ADT:
    plot_all_TC_images = True
    show_image = False
    save_image = False
    save_CDO_image = False
    show_CDO_analysis = False
if save_image or save_CDO_image:
    make_image = True
    show_image = False
    show_CDO_analysis = False
    default_cmap = True
    if draw_full:
        plot_track = False
        show_center = False
if not (update_ADT or save_CDO_image or save_image):
    plot_all_TC_images = False

if default_cmap:
    cmap_name_list = ['wv_nrl','wv_ssd','wv_cc_2','wv_bw','ir_bd','ir_ca','ir_cc','ir_cc_2','ir_bw']
elif use_bw_cmap:
    cmap_name_list = ['wv_bw', 'ir_bw']

if draw_clean:
    show_gridline = False
    plot_track = False
    show_center = False