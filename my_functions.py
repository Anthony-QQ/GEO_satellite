import os
import numpy as np
import numpy.ma as ma
from datetime import datetime
from scipy.interpolate import interp1d, griddata, NearestNDInterpolator
import xarray as xr

import mjd

'''
import sys
import variables
import mjd
import projections
import os
import timeit
from datetime import datetime, date, time
#from siphon.catalog import TDSCatalog
import matplotlib.pyplot as plt
#import metpy
#import metpy.calc as mpcalc
import numpy as np
import numpy.ma as ma
import math
import cmath
import netCDF4 as nc #stuck
from netCDF4 import Dataset as NetCDFFile
from pyproj import Proj
import xarray as xr
from scipy import interpolate
from scipy.interpolate import interp1d, griddata
from scipy.optimize import minimize

#from satpy import Scene
from pathlib import Path
from shutil import make_archive
#get_ipython().run_line_magic('matplotlib', 'inline')



#timeit.timeit('[i*2 for i in range(1000) if i == 900]', number=10000)
#x = [i for i in range(1000) if i == 30][0]
#print(x)

'''

GVAR_list = ['GOES_' + str(i) + '_GVAR' for i in range(8, 16)]
ABI_list = ['GOES_' + str(i) for i in range(16, 21)]

def get_sat_file_type(file_type='sat', type='ABI'):
    if type in ['MODIS']:
        return 'hdf4'
    else:
        return 'nc'

def get_folder(type='ABI'):
    if type in ['ABI','AHI','GVAR','MODIS','VIIRS','NOAA']:
        type = get_sat_file_type(type=type)
    path = os.getcwd()
    for i in range(2):  # cwd is 2 layers below the last common directory
        path = os.path.dirname(path)
    if type == 'output_image':
        f = ''
    elif type == 'hdf4':
        f = 'HDF4_Files'
    else:
        f = 'nc_Files'
    folder = os.path.join(path, f)
    return folder

def browse_folder(sat_name, TC_name='', type='ABI'):
    if TC_name != '':
        folder_name = os.path.join(get_folder(type=type), sat_name, TC_name)
    else:
        folder_name = os.path.join(get_folder(type=type), sat_name)
    return os.listdir(folder_name)

def get_fn(f_num, sat_name, TC_name='', type='ABI'):
    if TC_name != '':
        folder_name = os.path.join(get_folder(type=type), sat_name, TC_name, '')
    else:
        folder_name = os.path.join(get_folder(type=type), sat_name, '')
    fn = os.path.join(folder_name, os.listdir(folder_name)[f_num])
    return fn

def get_GVAR(fn):
    ds = xr.open_dataset(fn)
    # print(ds)
    # print(ds.attrs)
    # print(ds['data'])
    b_num = np.array(ds['bands'])
    # print(b_num)
    # print(b_num)
    return ds

def get_time(f_num, sat_name, TC):
    fn = get_fn(f_num, sat_name, TC)
    ds = get_GVAR(fn)
    dt_text = ''.join([str(np.array(ds['imageDate'])), str(np.array(ds['imageTime'])).zfill(6)])
    dt_number = int(dt_text)

    return dt_number

def get_table(sat_name, b_number=3):
    fn = 'D:/Documents/TC and Weather/Program/PyCharm/nc_Files/' + sat_name + '/B_' + str(b_number) + '_table.txt'

    table_file = open(str(fn), "r")
    table = table_file.read()
    table_list = table.split('\n')
    table_list = np.array([float(i) for i in table_list])
    table_file.close()

    # data_folder = Path('nc_Files/')
    # file_to_open = data_folder / 'sat_name' / ('B_'+str(b_number)+'_table.txt')
    # table_list_2 = file_to_open.read_text()

    # not usable, as file path uses double slashes instead of single
    return table_list




def save_ADT(ADT_list, TC, do_ADT, update_ADT):
    if do_ADT:
        print(ADT_list)
        if update_ADT:
            ADT_fname = 'D:/Documents/TC and Weather/Program/PyCharm/ADT/' + TC + '.txt'
            ADT_list = np.array(ADT_list)
            np.savetxt(ADT_fname, ADT_list)
    return 0


def image_type(sat_name='GOES_15_GVAR', b_num=3):
    satellite_list = []
    satellite_list.append(['GOES_16', 8, 'WV'])


    tp = 'wv'
    if sat_name in GVAR_list:
        if b_num == 3:
            tp = 'wv'
        elif b_num in range(4, 7):
            tp = 'ir'
    elif sat_name in ABI_list:
        if b_num in range(8, 11):
            tp = 'wv'
        elif b_num in range(7, 17):
            tp = 'ir'
    return tp


def get_sat_longitude(sat_name, year, lon_TC):
    if sat_name in ['GOES_8_GVAR','GOES_12_GVAR','GOES_13_GVAR','GOES_16','GOES_19']:
        return -75
    elif sat_name in ['GOES_10_GVAR','GOES_11_GVAR']:
        return -135
    elif sat_name in ['GOES_15_GVAR','GOES_17','GOES_18']:
        return -137
    elif sat_name in ['GOES_14_GVAR']:
        return -105
    elif sat_name in ['H9_FD']:
        return 140
    elif sat_name == 'GOES_9_GVAR':
        if year < 2001:
            return -135
        else:
            return 155
    else:
        return lon_TC




def ll_to_float(string):
    sfx = string[-1]
    val = float(string[0:-1])
    if sfx == 'S' or sfx == 'W':
        val *= -1
    return val


def dateline_treatment(longitudes):
    return np.mod(longitudes, 360)


def get_track(TC, dateline_adj):
    fn = 'D:/Documents/TC and Weather/Program/PyCharm/tracks/' + TC + '_track.txt'
    table_file = open(str(fn), "r")
    table = table_file.read()
    table = table.replace(' ', '')
    table_1 = table.split('\n')
    table_list = [i.split(',') for i in table_1]

    # NHC_type track file
    if len(table_list[0][0]) == 8:
        if dateline_adj:
            track_list = [[mjd.datetime_to_mjd(datetime.strptime(i[0] + i[1], '%Y%m%d%H%M')), ll_to_float(i[4]),
                           dateline_treatment(ll_to_float(i[5]))] for i in table_list if len(i) > 2]
        else:
            track_list = [[mjd.datetime_to_mjd(datetime.strptime(i[0] + i[1], '%Y%m%d%H%M')), ll_to_float(i[4]),
                           ll_to_float(i[5])] for i in table_list if len(i) > 2]
    # JTWC_type track file
    elif dateline_adj:
        track_list = [[mjd.datetime_to_mjd(datetime.strptime(i[2], '%Y%m%d%H')), ll_to_float(i[6]) / 10,
                       dateline_treatment(ll_to_float(i[7]) / 10)] for i in table_list if len(i) > 2]
    else:
        track_list = [
            [mjd.datetime_to_mjd(datetime.strptime(i[2], '%Y%m%d%H')), ll_to_float(i[6]) / 10, ll_to_float(i[7]) / 10]
            for i in table_list if len(i) > 2]

    table_file.close()
    return np.array(track_list)


def get_TC_loc(track_list, mjd, dateline_adj):
    mjd_track, lat_track, lon_track = track_list.T

    if dateline_adj:
        lon_track = dateline_treatment(lon_track)
    f_lat = interp1d(mjd_track, lat_track, kind='slinear', fill_value='extrapolate')
    f_lon = interp1d(mjd_track, lon_track, kind='slinear', fill_value='extrapolate')
    mjd_list = np.arange(mjd - 0.5, mjd + 0.5, 1 / 72)

    return [f_lat(mjd), f_lon(mjd)]


def get_detailed_track(track_list, mjd, i_s, dateline_adj):
    mjd_track, lat_track, lon_track = track_list.T
    if dateline_adj:
        lon_track = dateline_treatment(lon_track)

    f_lat = interp1d(mjd_track, lat_track, kind='slinear', fill_value='extrapolate')
    f_lon = interp1d(mjd_track, lon_track, kind='slinear', fill_value='extrapolate')
    mjd_list = np.arange(mjd - 2, mjd + 2, 1 / 72)
    xy_0 = [[f_lon(t), f_lat(t)] for t in mjd_list]
    x_c, y_c = f_lon(mjd), f_lat(mjd)
    x_min, x_max, y_min, y_max = x_c - i_s / 2, x_c + i_s / 2, y_c - i_s / 2, y_c + i_s / 2
    xy_1 = [i for i in xy_0 if (i[0] > x_min and i[0] < x_max and i[1] > y_min and i[1] < y_max)]
    return [i[0] for i in xy_1], [i[1] for i in xy_1]


def r_to_RMW(r=16, new_RMW=True):
    # the input is the radius of -45 degrees (IR), in km
    # old formula is the one used in ADT
    # ADT formula is 2.8068+0.8361*r
    # advanced formula is 3.01+0.60*r
    if new_RMW:
        return 3 + 0.65 * r
    else:
        return 2.8 + 0.8 * r


def slice_FD(BT_0, lats_0, lons_0, lat_min, lat_max, lon_min, lon_max):
    # Find all indices inside the lat/lon bounding box
    inside = (
            (lats_0 >= lat_min) & (lats_0 <= lat_max) &
            (lons_0 >= lon_min) & (lons_0 <= lon_max)
    )

    i_idx, j_idx = np.where(inside)

    if i_idx.size == 0 or j_idx.size == 0:
        raise ValueError("No grid points found inside bounding box.")

    # Find index boundaries and expand by 1 cell in each direction, clipped to array bounds
    i_min = max(i_idx.min() - 1, 0)
    j_min = max(j_idx.min() - 1, 0)
    i_max = min(i_idx.max() + 1, BT_0.shape[0] - 1)
    j_max = min(j_idx.max() + 1, BT_0.shape[1] - 1)

    # Crop arrays
    BT_cropped = BT_0[i_min:i_max + 1, j_min:j_max + 1]
    lats_cropped = lats_0[i_min:i_max + 1, j_min:j_max + 1]
    lons_cropped = lons_0[i_min:i_max + 1, j_min:j_max + 1]

    return BT_cropped, lats_cropped, lons_cropped

def slice_FD_zz(BT_0, lats_0, lons_0, lat_min, lat_max, lon_min, lon_max, lat_TC, lon_TC, no_crop):

    BT_sliced, lats_sliced, lons_sliced = slice_FD(BT_0, lats_0, lons_0, lat_min, lat_max, lon_min, lon_max)
    zz = np.cos(lat_TC * np.pi / 180) * np.subtract(lons_0, lon_TC) + 1j * np.subtract(lats_0, lat_TC)
    distances = np.abs(zz)
    angles = np.angle(zz)

    if no_crop:
        BT_cropped = BT_0
        lats = lats_0
        lons = lons_0
        lat_min, lat_max, lon_min, lon_max = np.min(lats), np.max(lats), np.min(lons), np.max(lons)
        zz_sliced = np.cos(lat_TC * np.pi / 180) * np.subtract(lons_sliced, lon_TC) + 1j * np.subtract(lats_sliced,
                                                                                                       lat_TC)
        distances_sliced = np.abs(zz_sliced)
        angles_sliced = np.angle(zz_sliced)
        crop_status = 'Not_cropped'
    else:
        BT_0, lats_0, lons_0 = BT_sliced, lats_sliced, lons_sliced

        keep_values = np.multiply(np.multiply((lats_0 > lat_min), (lats_0 < lat_max)),
                                  np.multiply((lons_0 > lon_min), (lons_0 < lon_max)))
        BT_cropped = ma.masked_array(BT_0, mask=np.invert(keep_values))
        lats = np.minimum(np.maximum(lats_0, lat_min), lat_max)
        lons = np.minimum(np.maximum(lons_0, lon_min), lon_max)
        zz_sliced = zz
        distances_sliced = distances
        angles_sliced = angles

        crop_status = 'Cropped'


def tropical_height(BT_0):
    '''

    :param BT_0: brightness temperture (in K or C)
    :return: h: height (in km)
    '''
    if np.min(BT_0) > 0:
        BT_0 -= 273.15

    h = (305-BT_0) * (305-201)/(15-0)

    return h


def eye_fit_1(x, *c):
    lat_TC, lon_TC = x
    lats, lons, BT, r, lat_bst, lon_bst = c
    lat_dif, lon_dif = lats - lat_TC, lons - lon_TC
    BT = BT - np.amin(BT)
    BT = np.nan_to_num(BT, nan=0.01)
    d2 = np.add(np.square(lat_dif), np.square(lon_dif)) / (r / 111) ** 2
    # d2[d2 > (1+30/111)] = 0
    weight = np.exp(-1 * d2 / 2)
    product = np.multiply(weight, BT)
    value = np.mean(product)

    d2_bst = ((lat_TC - lat_bst) ** 2 + (lon_TC - lon_bst) ** 2)
    value /= 2 ** (d2_bst / 0.3)

    return -value

def eye_fit_2(x, *c):
    lat_TC, lon_TC = x
    lats, lons, BT, r, finder_limit, lat_bst, lon_bst = c

    '''
    X = np.linspace(lon_TC - finder_limit, lon_TC + finder_limit, 0.02)
    Y = np.linspace(lat_TC - finder_limit, lat_TC + finder_limit, 0.02)
    xi, yi = np.meshgrid(X, Y)
    zi = griddata(np.dstack((lons.ravel(), lats.ravel()))[0], BT.ravel(), (xi, yi),
                  method="linear")

    gradient = np.gradient(zi)
    gradient = gradient[1] + 1j * gradient[0]
    ci = (xi - lon_TC) + 1j * (yi - lat_TC)
    benchmark = np.abs(gradient) / np.maximum(np.abs(ci), 0.05) * np.cos(2 * (np.angle(gradient) - np.angle(ci))) ** 2
    '''

    zz = np.subtract(lats, lat_TC) - 1j * np.cos(lat_TC * np.pi / 180) * np.subtract(lons, lon_TC)
    distances = np.abs(zz)

    r_list = [0, 0.2 * r / 111, 0.7 * r / 111, r / 111 + 0.2, 1.5 * r / 111 + 0.2, 10000]
    r_indices = np.digitize(distances, r_list)

    high_T = np.mean(BT[r_indices == 1])
    mid_T = np.mean(BT[r_indices == 2])
    low_T = np.mean(BT[r_indices == 4])

    d = np.abs(lat_TC - lat_bst + 1j * (lon_TC - lon_bst))
    delta = low_T - 0.7 * high_T - 0.3 * mid_T
    if delta < 100:
        delta += 0
    else:
        delta = 0

    value = delta + d * 20

    return value

def eye_fit_3(x, *c):
    lat_TC, lon_TC = x
    xi, yi, gradient, lat_bst, lon_bst = c

    #Native parameters
    d_index = 0.5
    r_boundary = 1
    bst_offset_index = 2
    spiral_offset = 10

    ci = (xi - lon_TC) + 1j * (yi - lat_TC)
    benchmark = (np.abs(gradient) / np.maximum(np.abs(ci), 0.05) ** d_index
                 * np.cos(2 * (np.angle(gradient) - np.angle(ci) - np.radians(spiral_offset))) ** 2)

    return -np.sum(benchmark) / (r_boundary ** bst_offset_index + np.abs(lat_TC - lat_bst + 1j * (lon_TC - lon_bst)) ** bst_offset_index)


def CDO_fit(x, *c):
    lat_TC, lon_TC = x
    lats, lons, BT, r, lat_bst, lon_bst = c
    lat_dif, lon_dif = lats - lat_TC, lons - lon_TC
    BT = np.nan_to_num(BT, nan=0.)
    d2 = np.add(np.square(lat_dif), np.square(lon_dif)) / (1.5) ** 2  # CDO about 1.5 degree wide
    # d2[d2 > 1.5] = 0
    weight = np.exp(-1 * d2 / 2)
    product = np.multiply(weight, BT)
    value = np.sum(product)

    d2_bst = ((lat_TC - lat_bst) ** 2 + (lon_TC - lon_bst) ** 2)
    value /= 2 ** (d2_bst)

    return value


def get_eye_r_0(BT_Eye, mid_temp, Eye_r):
    r = np.sqrt(np.ma.sum(BT_Eye > mid_temp) / np.ma.count(BT_Eye) / np.pi) * (Eye_r * 222)
    return r

def get_eye_r(BT_0, distances, r_in, mid_temp):
    #takes inputs in degrees, returns radius in km
    r_mask = (distances < r_in)
    Eye_mask = np.multiply((BT_0 > mid_temp), (distances < r_in))
    r = np.sqrt(np.sum(Eye_mask) / np.sum(r_mask)) * r_in * 111
    return r

def get_CDO_r(BT_Eye, mid_temp, Eye_r):
    r = np.sqrt(np.ma.sum(BT_Eye < mid_temp) / np.ma.count(BT_Eye) / np.pi) * (Eye_r * 222)
    return r
def get_eye_box_r(lats_Eye, lons_Eye, lat_TC):
    print(np.ma.max(lats_Eye), np.ma.min(lats_Eye), np.ma.max(lons_Eye), np.ma.min(lons_Eye))
    r = np.mean([np.ma.max(lats_Eye) - np.ma.min(lats_Eye),
                 (np.ma.max(lons_Eye) - np.ma.min(lons_Eye)) * np.cos(lat_TC * np.pi / 180)]) / 2 * 111 + 2
    return r


def get_region_pixels(lats_0, lons_0, lat_TC, lon_TC, r):
    return np.multiply(np.multiply((lats_0 > lat_TC - r), (lats_0 < lat_TC + r)),
                       np.multiply((lons_0 > lon_TC - r), (lons_0 < lon_TC + r)))


def get_mid_temp(min_temp, max_temp, im_type, TC=None):

    cold_list = '04_Heta', '04_Heta10', '05_Olaf'

    T = (min_temp + max_temp) / 2

    if min_temp < -65:
        #convection is strong
        if TC in cold_list and max_temp < -40:
            #eye is cold
            T = max(min_temp + 10, max_temp - 5)

        elif im_type == 'wv':
            T = -49
        elif im_type == 'ir':
            T = -45
    else:
        #convection is weak
        T = min_temp + 20

    print(min_temp, T, max_temp)

    return T


def get_temp_text(min_temp, max_temp, av_temp, CDO_fixed_temp, do_ADT):
    min_temp_text = str(np.around(min_temp, 2))
    max_temp_text = str(np.around(max_temp, 2))
    av_temp_text = str(np.around(av_temp, 2))
    temp_text_1 = 'Average \u2103: ' + av_temp_text
    if do_ADT:
        min_temp_text = str(np.around(CDO_fixed_temp, 2))
        temp_text_2 = ' '.join(['CDO/Eye \u2103:', min_temp_text, ',', max_temp_text])
    else:
        temp_text_2 = ' '.join(['Min/Max \u2103:', min_temp_text, ',', max_temp_text])
    temp_text = temp_text_1 + '\n' + temp_text_2
    temp_text = temp_text_2

    return temp_text


def latlon_points_in_pairs(sp=5, cntr=None, s=90):
    if cntr is None:
        cntr = [0, 0]
    sp_0 = int(sp + 0.9)
    xc, yc = cntr[0], cntr[1]
    if s == 90:
        lat_range = np.arange(-int(89.99 / sp_0) * sp_0, int(89.99 / sp_0) * sp_0, sp_0)
        lon_range = np.arange(0, 360, sp_0)
    else:
        lat_range = np.arange(int((xc-s+0.001) / sp_0) * sp_0, int((xc + s - 0.001) / sp_0) * sp_0, sp_0)
        lon_range = np.arange(int((yc-s+0.001) / sp_0) * sp_0, int((yc + s - 0.001) / sp_0) * sp_0, sp_0)
    list_2d = [[i,j] for i in lat_range for j in lon_range]
    return np.array(list_2d)

def CDO_stats(BT_0, distances, angles, r=20, R_find=3, R_step=0.05, CDO_tolerance=1.5, T_tolerance=4,
              override_T=False):
    try:
        try:
            R_start = np.round(r/111-R_step/2,1) + R_step/2
        except:
            R_start = 0.225

        #binning range
        R_list = np.arange(R_start, R_start + R_find, R_step)

        #binning
        r_indices = np.digitize(distances, R_list)
        T_list = [np.mean(BT_0[r_indices == i]) for i in range(1, len(R_list))]
        std_list = [np.std(BT_0[r_indices == i]) for i in range(1, len(R_list))]

        #trimming
        R_list += R_step / 2
        R_list = R_list[:-1]


        T_min = np.min(T_list)
        T_min_i = np.argmin(T_list)
        R_min = R_list[T_min_i]

        # from half of coldest ring to coldest ring + 2 deg
        std_i_start = int(T_min_i / 2) + 1
        std_i_end = T_min_i + int(2 / R_step)

        # Global smoothest ring
        std_min = np.min(std_list[std_i_start:std_i_end])
        std_min_i = np.argmin(std_list[std_i_start:std_i_end]) + std_i_start
        # Radius of smoothest ring
        R_smooth = R_list[std_min_i]

        #starting from coldest ring outwards
        R_list_truncate = R_list[T_min_i:]
        std_list_truncate = std_list[T_min_i:]
        T_list_truncate = T_list[T_min_i:]

        #First ring that is too rough
        std_edge_i = [n for n, i in enumerate(std_list_truncate) if i > (std_min + CDO_tolerance)][0]
        R_1 = R_list_truncate[std_edge_i]

        #First ring that is too warm
        T_edge_i = [n for n,i in enumerate(T_list_truncate) if i > (T_min + T_tolerance)][0]
        R_2 = R_list_truncate[T_edge_i]

        R_edge = min(R_1,R_2)

        if override_T:
            if max(T_list_truncate) < -50:
                return max(R_list_truncate)
            else:
                T_edge_i = [n for n, i in enumerate(T_list_truncate) if i > -50][0]
                R_edge = R_list_truncate[T_edge_i]

        return R_edge
    except Exception as e:
        print(f'Error occurred: {e}')
        return 0

