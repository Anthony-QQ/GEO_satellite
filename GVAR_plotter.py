from datetime import datetime
import numpy as np
import numpy.ma as ma
from scipy.optimize import minimize
import sys
import xarray as xr

import mjd
from my_functions import (CDO_fit, CDO_stats, dateline_treatment, eye_fit_2, get_CDO_r,
                          get_detailed_track, get_eye_box_r, get_eye_r, get_fn, get_mid_temp,
                          get_region_pixels, get_table, get_TC_loc, get_temp_text, get_track, image_type)
from my_plotting import CDO_cs
from config import (analyse_CDO, do_ADT, find_center,
                    make_image, new_RMW,
                    plot_track, quick_center, save_image, show_center, show_image, show_RMW,
                    use_CDO_size, use_track)

GVAR_list = ['GOES_'+str(i)+'_GVAR' for i in range(8,16)]

# plot GVAR .nc

def get_GVAR(fn):
    ds = xr.open_dataset(fn)
    b_num = np.array(ds['bands'])
    return ds


def process_GVAR(f_num, sat_name, TC):
    fn = get_fn(f_num, sat_name, TC)
    print(fn)
    ds = get_GVAR(fn)
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

'''
def plot_GVAR(f_num, sat_name, TC, im_crop=[15, -105, 15], im_size=10, no_crop=False, cmap_name_list=['wv_nrl'],
              dpi=100, TC_marker_r=1, CDO_r=2.5, min_time=0, max_time=0,
              use_track=True):


    CDO_deltaT = 10  # in Kelvins
    CDO_fixed_width = 60  # in km
    Cloud_height = 15 / 111.  # in degrees latitude
    dateline_adj = False

    # get data
    fn = get_fn(f_num, sat_name, TC)
    ds = get_GVAR(fn)
    counts_0 = np.array(ds['data'][0])  # somehow the raw counts were multiplied by 32
    if np.max(counts_0) > 1050:
        counts_0 = np.divide(counts_0, 32)
    lats_0 = np.array(ds['lat'])
    lons_0 = np.array(ds['lon'])
    b_num = np.array(ds['bands'])

    # dateline correction
    if (np.min(lons_0) < -178):
        dateline_adj = True
        lons_0 = dateline_treatment(lons_0)

    # image type (water vapour, long-wave infrared etc.)
    im_type = image_type(sat_name, b_num)

    # date and time of image
    top_text = '_'.join([sat_name, 'Band', str(b_num), TC])
    image_dt_text = '_'.join([str(np.array(ds['imageDate'])), str(np.array(ds['imageTime'])).zfill(6)])
    image_datetime_object = datetime.strptime(image_dt_text, '%Y%j_%H%M%S')
    image_mjd = mjd.datetime_to_mjd(image_datetime_object)
    image_datetime_text = image_datetime_object.strftime('%Y%m%d_%H%M%S')

    if min_time != 0 and max_time != 0:
        image_dt_number = int(image_dt_text.replace('_', ''))
        if image_dt_number < min_time or image_dt_number > max_time:
            sys.exit(1)

    # location and track of the TC based on Best-track and image time

    lat_TC, lon_TC, i_s = im_crop
    if use_track:
        TC_track = get_track(TC, dateline_adj)
        lat_TC, lon_TC = get_TC_loc(TC_track, image_mjd, dateline_adj)
        if plot_track:
            xpTrack, ypTrack = get_detailed_track(TC_track, image_mjd, i_s, dateline_adj)

    lat_min, lat_max, lon_min, lon_max = lat_TC - i_s / 2, lat_TC + i_s / 2, lon_TC - i_s / 2, lon_TC + i_s / 2
    print('TC location:', np.round(lat_TC, 2), np.round(lon_TC, 2))

    # convert counts to brightness temperature
    BT_table = get_table(sat_name, b_num)
    BT_0 = np.array([[BT_table[int(i)] - 273.15 for i in j] for j in counts_0])

    # crop data
    if no_crop:
        BT = BT_0
        lats = lats_0
        lons = lons_0
        lat_min, lat_max, lon_min, lon_max = np.min(lats), np.max(lats), np.min(lons), np.max(lons)
        crop_status = 'Not_cropped'
    else:
        keep_values = np.multiply(np.multiply((lats_0 > lat_min), (lats_0 < lat_max)),
                                  np.multiply((lons_0 > lon_min), (lons_0 < lon_max)))
        BT = ma.masked_array(BT_0, mask=np.invert(keep_values))
        lats = np.minimum(np.maximum(lats_0, lat_min), lat_max)
        lons = np.minimum(np.maximum(lons_0, lon_min), lon_max)
        crop_status = 'Cropped'

    # find rough CDO size

    CDO_keep = get_region_pixels(lats_0, lons_0, lat_TC, lon_TC, CDO_r)
    BT_CDO = ma.masked_array(BT_0, mask=np.invert(CDO_keep))
    min_temp, av_temp = np.ma.min(BT_CDO), np.ma.average(BT_CDO)
    CDO_area_r = np.sqrt(np.ma.sum(BT_CDO < min_temp + CDO_deltaT) / np.ma.count(BT_CDO) / np.pi) * 111 * CDO_r * 2
    CDO_limit = CDO_area_r

    Eye_r = (CDO_area_r / 2 - 0) / 111  # Preliminary region of the eye, slightly less than half of that of the CDO
    Eye_keep = get_region_pixels(lats_0, lons_0, lat_TC, lon_TC, Eye_r)
    BT_Eye = ma.masked_array(BT_0, mask=np.invert(Eye_keep))
    max_temp = np.ma.max(BT_Eye)

    mid_temp = get_mid_temp(min_temp, max_temp, im_type)

    # assumes entire eye is within the preliminary square region
    Eye_area_r = get_eye_r(BT_Eye, mid_temp, Eye_r)

    # new iteration of CDO and eye size
    CDO_area_r = Eye_area_r + CDO_fixed_width

    Eye_r = (CDO_area_r / 1.5) / 111
    Eye_keep = get_region_pixels(lats_0, lons_0, lat_TC, lon_TC, Eye_r)
    BT_Eye = ma.masked_array(BT_0, mask=np.invert(Eye_keep))
    max_temp = np.ma.max(BT_Eye)

    mid_temp = get_mid_temp(min_temp, max_temp, im_type)

    # assumes entire eye is within the preliminary square region
    Eye_area_r = get_eye_r(BT_Eye, mid_temp, Eye_r)
    print(
        f'Eye pixel count: {np.ma.sum(BT_Eye > mid_temp)}, Eye frame count: {np.ma.count(BT_Eye)}, CDO radius: {CDO_area_r}')

    if do_ADT:
        Eye_mask = np.invert(np.multiply((BT_Eye > mid_temp), Eye_keep))
        lats_Eye = ma.masked_array(lats_0, mask=Eye_mask)
        lons_Eye = ma.masked_array(lons_0, mask=Eye_mask)

        R_inner = (Eye_area_r * 1.2 + 15) / 111  # in degrees latitude
        R_out = R_inner + CDO_fixed_width / 111  # also in degrees latitude

        zz = np.subtract(lats_0, lat_TC) - 1j * np.cos(lat_TC * np.pi / 180) * np.subtract(lons_0, lon_TC)
        distances = np.abs(zz)
        angles = np.angle(zz)

        if Eye_area_r > 0:

            R_bounds = [0, R_inner, R_out, 10000]
            R_i_list = np.digitize(distances, R_bounds)
            CDO_fixed_temp = np.average(BT_0[R_i_list == 2])

            CDO_limit = CDO_stats(BT_0, distances, angles)
            print(CDO_limit)

            if find_center:
                if CDO_limit > 0.8:

                    lat_TC = np.ma.mean(lats_Eye)
                    lon_TC = np.ma.mean(lons_Eye)
                    print('New location (quick):', lat_TC, lon_TC)
                else:
                    c = (lats_0, lons_0, BT_CDO, Eye_area_r, lat_TC, lon_TC)
                    x = np.array([lat_TC, lon_TC])
                    print(x)
                    x_new = minimize(eye_fit, x, args=c, method='Nelder-Mead',
                                     options={'maxiter': 100, 'return_all': False})
                    lat_TC, lon_TC = x_new['x']
                    print('New location (slow):', lat_TC, lon_TC)
        else:
            print('Old location', lat_TC, lon_TC)

        if new_RMW and (Eye_area_r > 5):
            Eye_box_r = get_eye_box_r(lats_Eye, lons_Eye, lat_TC)
            print(Eye_area_r, Eye_box_r)
            if (Eye_box_r > 0.5 * Eye_area_r) and (Eye_box_r < 1.5 * Eye_area_r):
                Eye_area_r = Eye_box_r

        zz = np.subtract(lats_0, lat_TC) - 1j * np.cos(lat_TC * np.pi / 180) * np.subtract(lons_0, lon_TC)
        distances = np.abs(zz)
        angles = np.angle(zz)

        R_edge = CDO_stats(BT_0, distances, angles, r=Eye_area_r)
        print('CDO/Eye radius:', np.round(R_edge * 111, 1), np.round(Eye_area_r, 1))

        CDO_fixed_keep = np.multiply((distances > R_inner), (distances < R_out))
        BT_CDO_fixed = ma.masked_array(BT_0, mask=np.invert(CDO_fixed_keep))

        R_bounds = [0, R_inner, R_out, 10000]
        R_i_list = np.digitize(distances, R_bounds)
        CDO_fixed_temp = np.average(BT_0[R_i_list == 2])

        R_bounds = [0, R_edge, 10000]
        R_i_list = np.digitize(distances, R_bounds)
        try:
            BT_Eye = np.max(BT_0[R_i_list == 1])
        except:
            BT_Eye += 0

        if analyse_CDO:
            CDO_cs(BT_0, distances, angles, show=show_image, do=make_image)

            CH_ring = []
            for order in range(1, 5):
                filter_1 = np.cos(angles * order)
                filter_2 = np.cos(angles * order - np.pi / 2)
                element = -(np.ma.sum(np.multiply(filter_1, BT_CDO_fixed)) - 1j * np.ma.sum(
                    np.multiply(filter_2, BT_CDO_fixed))) / np.ma.count(BT_CDO_fixed)
                amplitude = np.abs(element)
                direction = np.angle(element) / order
                CH_ring.append(f'{order=},{amplitude:.2f},{direction * 180 / np.pi:.0f}')
            print(CH_ring)


    # image
    lat_range, lon_range = lat_max - lat_min, lon_max - lon_min
    im_scale = max(i_s, lat_range, lon_range)  # used in size of TC centre marker
    ratio = 1 / np.cos(np.radians(lat_TC))

    if use_CDO_size:
        if do_ADT:
            TC_marker_r = R_out
        else:
            TC_marker_r = CDO_area_r / 111
    cm_size = 11800 * (im_size / im_scale * TC_marker_r) ** 2

    temp_text = get_temp_text(min_temp, max_temp, av_temp, CDO_fixed_temp, do_ADT)
    pos_text = ' '.join(['BST location (N,E):', str(np.round(lat_TC, 2)), ',', str(np.round(lon_TC, 2))])

    # draw image
    if make_image:
        for cmap_name in cmap_name_list:

            if cmap_name[0:2] == im_type:
                bundle_1 = (lons, lats, BT, lon_TC, lat_TC)
                bundle_2 = (cm_size, im_size, dpi, ratio, Eye_area_r, R_edge, R_inner, R_out, crop_status, xpTrack, ypTrack)
                bundle_3 = (
                top_text, pos_text, temp_text, image_datetime_text, TC, cmap_name, f_num, sat_name, b_num)
                bundle_4 = (analyse_CDO, do_ADT, new_RMW, no_crop, plot_track, save_image, show_center, show_image, show_RMW, use_track)
                bundle = (bundle_1, bundle_2, bundle_3, bundle_4)

                plot_image(bundle)

    if do_ADT:
        if Eye_area_r < 2:
            max_temp = CDO_fixed_temp
        ADT_data = [image_mjd, np.sum(b_num), CDO_fixed_temp, max_temp, Eye_area_r, R_edge * 111]
        print('ADT input:', ADT_data)
        return ADT_data
    else:
        return BT_eye
    return 0
'''
