update_ADT = False  #saves ADT txt files according to TC name
save_image = False  #saves TC images to directories sorted by crop status, TC name, band
save_CDO_image = False #saves CDO analysis image sorted by TC name, band
make_image = True  #creates the images
show_image = True  #makes the image remain stuck in window

plot_all_TC_images = False  #TAKES TIME


TC_pos = [21.5, -53.8]
im_size = [6]
crop_param = TC_pos + im_size

plot_now = True
ask_choices = False
ask_TC = False
ask_time = False


draw_full = False
draw_clean = False
use_track = True
plot_track = True
show_center = True
cc_size = 1
use_CDO_size = True
show_RMW = True
new_RMW = True
draw_CDO = True
analyse_CDO = True
show_CDO_analysis = False
find_center = True
quick_center = False
do_ADT = True

time_range = True
default_cmap = False
use_bw_cmap = False

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
             '23_Jova', '24_Milton', '25_Erin']

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
    plot_track = False
    show_center = False