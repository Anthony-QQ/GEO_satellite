from datetime import datetime
import numpy as np
import sys
import xarray as xr
import rioxarray as rxr

import mjd
from my_functions import (CDO_fit, CDO_stats, dateline_treatment, eye_fit_2, get_CDO_r,
                          get_detailed_track, get_eye_box_r, get_eye_r, get_fn, get_mid_temp,
                          get_region_pixels, get_table, get_TC_loc, get_temp_text, get_track, image_type)
from my_plotting import CDO_cs
from config import (analyse_CDO, do_ADT, find_center,
                    make_image, new_RMW,
                    plot_track, quick_center, save_image, show_center, show_image, show_RMW,
                    use_CDO_size, use_track)

MODIS_list = ['Aqua','Terra']

# plot MODIS full .hdf

def get_MODIS(fn):
    ds = rxr.open_rasterio(fn, masked=True)
    print(ds)
    b_num = np.array(ds['bands'])
    return ds


def process_MODIS(f_num, sat_name, TC, sat_type='ABI'):
    fn = get_fn(f_num, sat_name, TC, sat_type)
    print(fn)
    ds = get_MODIS(fn)
    counts_0 = np.array(ds['data'][0])  # somehow the raw counts were multiplied by 32
    if np.max(counts_0) > 1050:
        counts_0 = np.divide(counts_0, 32)
    lats_0 = np.array(ds['lat'])
    lons_0 = np.array(ds['lon'])
    b_num = np.array(ds['bands'])
    BT_table = get_table(sat_name, b_num)
    BT_0 = np.array([[BT_table[int(i)] - 273.15 for i in j] for j in counts_0])

    return ds, BT_0, lats_0, lons_0, b_num


def get_GVAR_time(ds, TC, sat_name, b_num, max_time, min_time):
    top_text = '_'.join([sat_name, 'Band', str(b_num), TC])
    image_dt_text = '_'.join([str(np.array(ds['imageDate'])), str(np.array(ds['imageTime'])).zfill(6)])
    image_datetime_object = datetime.strptime(image_dt_text, '%Y%j_%H%M%S')
    image_mjd = mjd.datetime_to_mjd(image_datetime_object)
    image_datetime_text = image_datetime_object.strftime('%Y%m%d_%H%M%S')

    if min_time != 0 and max_time != 0:
        image_dt_number = int(image_dt_text.replace('_', ''))
        if image_dt_number < min_time or image_dt_number > max_time:
            sys.exit(1)

    return top_text, image_datetime_object, image_datetime_text, image_mjd
