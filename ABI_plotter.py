from datetime import datetime
import numpy as np
import numpy.ma as ma
from pyproj import Proj
from scipy.optimize import minimize
import sys
import xarray as xr
from my_functions import ABI_list

import mjd
from my_functions import (CDO_fit, CDO_stats, dateline_treatment, eye_fit_2, get_CDO_r,
                          get_detailed_track, get_eye_box_r, get_eye_r, get_fn, get_mid_temp,
                          get_region_pixels, get_table, get_TC_loc, get_temp_text, get_track, image_type)
from my_plotting import CDO_cs
from config import (analyse_CDO, do_ADT, find_center,
                    make_image, new_RMW, plot_all_TC_images,
                    plot_track, quick_center, save_image, show_center, show_image, show_RMW,
                    use_CDO_size, use_track)


#ABI_list = ['GOES_' + str(i) for i in range(16,21)]
ABI_band_list = [8,9,13]


# plot ABI Full-disk

def get_ABI(fn):
    ds = xr.open_dataset(fn)
    return ds


def get_ABI_max(ds):
    BT = np.subtract(np.array(ds['CMI']), 273.15)
    return np.max(BT)

def process_ABI(f_num, sat_name, TC):
    fn = get_fn(f_num, sat_name, TC)
    ds = get_ABI(fn)

    b_num = np.array(ds['band_id'])[0]
    if b_num not in ABI_band_list:
        print(f'Passed band {b_num} image {f_num}')
        return 0  # only process files of the desired bands
    BT_0 = np.subtract(np.array(ds['CMI']), 273.15)
    # image type (water vapour, long-wave infrared etc.)

    proj_details = ds['goes_imager_projection']
    lon_sat = proj_details.attrs['longitude_of_projection_origin']
    height = proj_details.attrs['perspective_point_height']

    x = np.array(ds['x'])
    y = np.array(ds['y'])
    x = np.multiply(np.tan(x), height)
    y = np.multiply(np.tan(y), height)
    xx, yy = np.meshgrid(x, y)
    projection = Proj(f'+proj=geos +ellps=GRS80 +h={height} +lon_0={lon_sat}')
    lons_0, lats_0 = projection(xx, yy, inverse=True)
    lons_0 = np.nan_to_num(lons_0, posinf=lon_sat)
    lats_0 = np.nan_to_num(lats_0, posinf=-81.3)

    return ds, BT_0, lats_0, lons_0, b_num


def get_ABI_time(ds, TC, sat_name, b_num):
    top_text = '_'.join([sat_name, 'Band', str(b_num), TC])
    time_64 = str(ds['t'].values)[0:19]
    image_datetime_object = datetime.strptime(time_64, '%Y-%m-%dT%H:%M:%S')

    image_mjd = mjd.datetime_to_mjd(image_datetime_object)
    image_datetime_text = image_datetime_object.strftime('%Y%m%d_%H%M%S')
    return top_text, image_datetime_object, image_datetime_text, image_mjd
