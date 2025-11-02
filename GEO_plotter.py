from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
import numpy.ma as ma
from pyproj import Proj
from scipy.interpolate import griddata
from scipy.optimize import minimize
import sys
import xarray as xr

from ABI_plotter import (get_ABI, get_ABI_time, process_ABI,
                         ABI_list, ABI_band_list)
from GVAR_plotter import (get_GVAR, get_GVAR_time, process_GVAR,
                          GVAR_list)
from MODIS_plotter import (process_MODIS,
                           MODIS_list)
import mjd
from my_functions import (slice_FD, CDO_fit, CDO_stats, dateline_treatment, eye_fit_2, eye_fit_3, get_CDO_r,
                          get_detailed_track, get_eye_box_r, get_eye_r, get_eye_r_0, get_fn, get_mid_temp,
                          get_region_pixels, get_table, get_TC_loc, get_temp_text, get_track, image_type)
from my_plotting import CDO_cs, plot_image_tuple, plot_image
from plot_parameters import (update_ADT, draw_CDO, analyse_CDO, do_ADT, find_center,
                             make_image, new_RMW, plot_all_TC_images,
                             plot_track, quick_center, save_image, show_CDO_analysis, save_CDO_image, overwrite_image,
                             show_gridline, show_center, show_image, show_RMW,use_CDO_size, use_track)


def plot_GEO(f_num, sat_name, TC, im_crop=None, im_size=10, no_crop=False, cmap_name_list=None,
             dpi=100, TC_marker_r=1, CDO_r_default=1.5, min_time=0, max_time=0,
             time_range=False, use_track=True):
    '''

    :param f_num: file number in TC folder
    :param sat_name: name of satellite
    :param TC: name of TC
    :param im_crop: a len=3 list of center latitude, longitude, square length in degrees
    :param im_size: size of final plot in default units (inches)
    :param no_crop: True = keep original data extent, False = crop to selected area
    :param cmap_name_list: list of colormaps to use
    :param dpi: dpi of the final plot
    :param TC_marker_r: size of the marker of the TC center location
    :param CDO_r_default: Default radius of CDO, in degrees
    :param min_time: start time of series of plots
    :param max_time: end time of series of plots
    :param time_range: use range of time or not
    :param use_track: use provided track data or not
    :return: 1-D list containing ADT output
    '''

    # Only save ABI images in 30-min intervals, process ADT in 10-min intervals
    ABI_interval = 30
    ABI_ADT_interval = 10

    if im_crop is None:
        im_crop = [15, -105, 15]
    if cmap_name_list is None:
        cmap_name_list = ['wv_nrl']
    if sat_name in GVAR_list:
        sat_type = 'GVAR'
    elif sat_name in ABI_list:
        sat_type = 'ABI'
    elif sat_name in MODIS_list:
        sat_type = 'MODIS'
    else:
        sat_type = 'ABI'

    CDO_deltaT = 10  # in Kelvins
    CDO_fixed_width = 60  # in km
    Cloud_height = 15 / 111.  # in degrees latitude
    dateline_adj = False

    # get data
    if sat_type == 'GVAR':
        ds, BT_0, lats_0, lons_0, b_num = process_GVAR(f_num, sat_name, TC)
    elif sat_type == 'MODIS':
        ds, BT_0, lats_0, lons_0, b_num = process_MODIS(f_num, sat_name, TC, sat_type)
    else:
        ds, BT_0, lats_0, lons_0, b_num = process_ABI(f_num, sat_name, TC)

    # dateline correction
    if (np.min(lons_0) < -178):
        dateline_adj = True
        lons_0 = dateline_treatment(lons_0)

    # image type (water vapour, long-wave infrared etc.)
    im_type = image_type(sat_name, b_num)

    # date and time of image
    if sat_type == 'GVAR':
        top_text, image_datetime_object, image_datetime_text, image_mjd = get_GVAR_time(ds, TC, sat_name, b_num,
                                                                                        max_time, min_time)
    else:
        top_text, image_datetime_object, image_datetime_text, image_mjd = get_ABI_time(ds, TC, sat_name, b_num)


    #flags for skipping: 1. timestamp at an offset time; 2. ABI meso (not full disk or GVAR)
    out_of_ABI_time = (image_datetime_object.minute % ABI_interval != 0)
    out_of_ABI_ADT_time = (image_datetime_object.minute % ABI_ADT_interval != 0)
    is_fd = np.max(lats_0) > 70 or np.min(lats_0) < -70
    is_gvar = sat_type == 'GVAR'
    is_meso = not (is_fd or is_gvar)

    is_saving = save_image or save_CDO_image or update_ADT

    skip_condition = out_of_ABI_time and is_meso and is_saving and plot_all_TC_images
    skip_ADT_condition = out_of_ABI_ADT_time and is_meso and is_saving and plot_all_TC_images

    skip_all = not update_ADT and skip_condition

    if skip_all:
        print('Redundant data skipped')
        return 0

    # location and track of the TC based on Best-track and image time
    lat_TC, lon_TC, i_s = im_crop
    if use_track:
        TC_track = get_track(TC, dateline_adj)
        lat_TC, lon_TC = get_TC_loc(TC_track, image_mjd, dateline_adj)
        xpTrack, ypTrack = get_detailed_track(TC_track, image_mjd, i_s, dateline_adj)

    lat_min, lat_max, lon_min, lon_max = (lat_TC - i_s / 2, lat_TC + i_s / 2,
                                          lon_TC - i_s / 2 / np.cos(np.radians(lat_TC)),
                                          lon_TC + i_s / 2 / np.cos(np.radians(lat_TC)))
    print('TC location:', np.round(lat_TC, 2), np.round(lon_TC, 2))

    # convert counts to brightness temperature

    # slice minimal data (for FD)

    BT_sliced, lats_sliced, lons_sliced = slice_FD(BT_0, lats_0, lons_0, lat_min, lat_max, lon_min, lon_max)

    # crop data
    if no_crop:
        BT_cropped = BT_0
        lats = lats_0
        lons = lons_0
        lat_min, lat_max, lon_min, lon_max = np.min(lats), np.max(lats), np.min(lons), np.max(lons)
        crop_status = 'Not_cropped'
    else:
        BT_0, lats_0, lons_0 = BT_sliced, lats_sliced, lons_sliced

        keep_values = np.multiply(np.multiply((lats_0 > lat_min), (lats_0 < lat_max)),
                                  np.multiply((lons_0 > lon_min), (lons_0 < lon_max)))
        BT_cropped = ma.masked_array(BT_0, mask=np.invert(keep_values))
        lats = np.minimum(np.maximum(lats_0, lat_min), lat_max)
        lons = np.minimum(np.maximum(lons_0, lon_min), lon_max)

        crop_status = 'Cropped'

    # find rough CDO size
    zz = np.cos(lat_TC * np.pi / 180) * np.subtract(lons_0, lon_TC) + 1j * np.subtract(lats_0, lat_TC)
    distances = np.abs(zz)
    angles = np.angle(zz)

    if no_crop:
        zz_sliced = np.cos(lat_TC * np.pi / 180) * np.subtract(lons_sliced, lon_TC) + 1j * np.subtract(lats_sliced,
                                                                                                       lat_TC)
        distances_sliced = np.abs(zz_sliced)
        angles_sliced = np.angle(zz_sliced)
    else:
        zz_sliced = zz
        distances_sliced = distances
        angles_sliced = angles


    edge_crude = CDO_stats(BT_sliced, distances_sliced, angles_sliced, override_T=True)
    R_bounds = [0, min(0.8, max(0.4, edge_crude / 2)), max(edge_crude, CDO_r_default), 10000]
    R_i_list = np.digitize(distances_sliced, R_bounds)
    min_temp = np.min(BT_sliced[R_i_list == 2])
    av_temp = np.mean(BT_sliced[R_i_list == 2])
    max_temp = np.max(BT_sliced[R_i_list == 1])

    mid_temp = get_mid_temp(min_temp, max_temp, im_type, TC)



    Eye_area_r = get_eye_r(BT_sliced, distances_sliced, max(0.4, edge_crude / 3), mid_temp)

    R_edge = CDO_stats(BT_sliced, distances_sliced, angles_sliced, r=Eye_area_r)
    R_bounds = [0, Eye_area_r / 111, max(R_edge , Eye_area_r/111 + 1), 10000]
    R_i_list = np.digitize(distances_sliced, R_bounds)
    CDO_mask = np.invert(distances_sliced < max(R_edge, Eye_area_r/111 + 1))
    Eye_mask = np.invert(np.multiply((BT_sliced > mid_temp), distances_sliced < R_edge))
    BT_CDO = ma.masked_array(BT_sliced, mask=CDO_mask)
    BT_Eye = ma.masked_array(BT_sliced, mask=Eye_mask)



    '''
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
    Eye_area_r = get_eye_r_0(BT_Eye, mid_temp, Eye_r)

    # new iteration of CDO and eye size
    CDO_area_r = Eye_area_r + CDO_fixed_width

    Eye_r = (CDO_area_r / 1.5) / 111
    Eye_keep = get_region_pixels(lats_0, lons_0, lat_TC, lon_TC, Eye_r)
    BT_Eye = ma.masked_array(BT_0, mask=np.invert(Eye_keep))
    max_temp = np.ma.max(BT_Eye)

    mid_temp = get_mid_temp(min_temp, max_temp, im_type)

    # assumes entire eye is within the preliminary square region
    Eye_area_r = get_eye_r_0(BT_Eye, mid_temp, Eye_r)
    print(
        f'Eye pixel count: {np.ma.sum(BT_Eye > mid_temp)}, Eye frame count: {np.ma.count(BT_Eye)}, CDO radius: {CDO_area_r}')
'''


    #ADT part

    lats_Eye = ma.masked_array(lats_sliced, mask=Eye_mask)
    lons_Eye = ma.masked_array(lons_sliced, mask=Eye_mask)

    R_inner = (Eye_area_r * 1.2 + 15) / 111  # in degrees latitude
    R_out = R_inner + CDO_fixed_width / 111  # also in degrees latitude


    if Eye_area_r > -0.1:

        CDO_limit = CDO_stats(BT_sliced, distances_sliced, angles_sliced)
        print(f'CDO edge (deg): {CDO_limit}')

        finder_limit = max(2, min(2 * CDO_limit, i_s * 0.8))

        if find_center:
            lat_rough = np.ma.mean(lats_Eye)
            lon_rough = np.ma.mean(lons_Eye)

            rough_deviation = np.abs(lat_rough - lat_TC + 1j * (lon_rough - lon_TC))

            if not (quick_center or (out_of_ABI_ADT_time and is_meso and update_ADT)):

                x = np.array([lat_TC, lon_TC])
                print(f'Starting array: {x}')

                spiral_fit = True

                if spiral_fit:

                    #Non-nearest interpolation requires massive computing time
                    X = np.linspace(lon_TC - finder_limit, lon_TC + finder_limit, int(finder_limit / 0.01))
                    Y = np.linspace(lat_TC - finder_limit, lat_TC + finder_limit, int(finder_limit / 0.01))
                    xi, yi = np.meshgrid(X, Y)
                    zi = griddata(np.dstack((lons_sliced.ravel(), lats_sliced.ravel()))[0], BT_sliced.ravel(), (xi, yi),
                                  method='nearest')


                    print(f'Interpolation finished.')

                    gradient = np.gradient(zi)
                    gradient = gradient[1] + 1j * gradient[0]


                    c = (xi, yi, gradient, lat_TC, lon_TC)
                    x_new = minimize(eye_fit_3, x*0.975, args=c, method='Nelder-Mead',
                                     options={'maxiter': 100, 'return_all': False})
                else:
                    c = (lats_sliced, lons_sliced, BT_CDO, Eye_area_r, finder_limit, lat_TC, lon_TC)
                    x_new = minimize(eye_fit_2, x*0.975, args=c, method='Nelder-Mead',
                                     options={'maxiter': 100, 'return_all': False})

                lat_TC, lon_TC = x_new['x']
                print('New location (slow):', lat_TC, lon_TC)

            elif CDO_limit > 0.6 and np.ma.count(lats_Eye) >= 1:
                lat_TC = lat_rough
                lon_TC = lon_rough
                print('New location (quick):', lat_TC, lon_TC)
            else:
                print('Old location', lat_TC, lon_TC)
        else:
            print('Old location', lat_TC, lon_TC)
    else:
        CDO_limit = 1
        print('Old location', lat_TC, lon_TC)



    zz = np.cos(lat_TC * np.pi / 180) * np.subtract(lons_0, lon_TC) + 1j * np.subtract(lats_0, lat_TC)
    distances = np.abs(zz)
    #Angles from East going counter-clockwise
    angles = np.angle(zz)

    Eye_mask = np.invert(np.multiply((BT_sliced > mid_temp), distances_sliced < R_edge))
    BT_CDO = ma.masked_array(BT_sliced, mask=CDO_mask)
    BT_Eye = ma.masked_array(BT_sliced, mask=Eye_mask)
    lats_Eye = ma.masked_array(lats_sliced, mask=Eye_mask)
    lons_Eye = ma.masked_array(lons_sliced, mask=Eye_mask)

    if new_RMW and (Eye_area_r > 5):
        Eye_box_r = get_eye_box_r(lats_Eye, lons_Eye, lat_TC)
        print(f'Area r: {Eye_area_r}, Box r: {Eye_box_r}')
        if (Eye_box_r > 0.5 * Eye_area_r) and (Eye_box_r < 1.5 * Eye_area_r):
            Eye_area_r = Eye_box_r

    print(f'Eye radius: {Eye_area_r}')

    R_inner = (Eye_area_r * 1.3 + 10) / 111  # in degrees latitude
    R_out = R_inner + CDO_fixed_width / 111  # also in degrees latitude

    R_edge = CDO_stats(BT_sliced, distances_sliced, angles_sliced, r=Eye_area_r)
    print('CDO/Eye radius:', np.round(R_edge * 111, 1), np.round(Eye_area_r, 1))

    CDO_fixed_keep = np.multiply((distances_sliced > R_inner), (distances_sliced < R_out))
    BT_CDO_fixed = ma.masked_array(BT_sliced, mask=np.invert(CDO_fixed_keep))

    R_bounds_1 = [0, R_inner, R_out, 10000]
    R_i_list_1 = np.digitize(distances_sliced, R_bounds_1)
    CDO_ADT_fixed = BT_sliced[R_i_list_1 == 2]
    CDO_fixed_temp = np.average(CDO_ADT_fixed)

    R_bounds_2 = [0, max(R_edge,0.4), 10000]
    R_i_list_2 = np.digitize(distances_sliced, R_bounds_2)
    max_temp = np.max(BT_sliced[R_i_list_2 == 1])




    #image
    lat_range, lon_range = lat_max - lat_min, lon_max - lon_min
    im_scale = max(i_s, lat_range, lon_range)  # used in size of TC centre marker
    ratio = 1 / np.cos(np.radians(lat_TC))

    if use_CDO_size:
        if do_ADT:
            TC_marker_r = R_out
        else:
            TC_marker_r = CDO_r_default / 111
    cm_size = 11800 * (im_size / im_scale * TC_marker_r) ** 2

    temp_text = get_temp_text(min_temp, max_temp, av_temp, CDO_fixed_temp, do_ADT)
    pos_text = ' '.join(['BST location (N,E):', str(np.round(lat_TC, 2)), ',', str(np.round(lon_TC, 2))])

    if (not skip_condition or not (save_image or save_CDO_image)) and not update_ADT:



        if draw_CDO:
            name_dict = {'top_text': top_text, 'pos_text': pos_text, 'temp_text': temp_text, 'TC': TC,
                         'E_T': max_temp, 'CDO_T': CDO_fixed_temp, 'CDO_lines':(R_inner,R_out,R_edge,Eye_area_r/111),
                         'f_num': f_num, 'b_num': b_num,
                         'image_datetime_text': image_datetime_text, 'sat_name': sat_name}
            boolean_dict = {'show': show_CDO_analysis, 'do': make_image, 'save': save_CDO_image, 'symmetric': True}

            CDO_cs(BT_sliced, distances_sliced, angles_sliced, r=Eye_area_r, b_dict=boolean_dict, n_dict=name_dict)

        if analyse_CDO:
            CH_ring = []
            for order in [0]:
                amplitude = np.ma.sum(BT_CDO_fixed) / np.ma.count(BT_CDO_fixed)
                a_0 = amplitude
                CH_ring.append({'order': order, 'amplitude': np.round(amplitude,3), 'angle': 0})
            for order in range(1, 5):
                filter_1 = np.cos(angles * order)
                filter_2 = np.cos(angles * order - np.pi / 2)
                element = (np.ma.average(np.multiply(filter_1, BT_CDO_fixed - a_0)) + 1j * np.ma.average(
                    np.multiply(filter_2, BT_CDO_fixed - a_0))) / np.pi**0.5
                amplitude = np.abs(element) * 2 * np.pi
                direction = np.angle(element) / order
                CH_ring.append({'order': order, 'amplitude': np.round(amplitude,3), 'angle': np.round(direction * 180 / np.pi,1)})
            print(f'Harmonics analysis: {CH_ring}')

            BT_smoothed = BT_CDO_fixed
            for order in range(0,2):
                BT_smoothed = (BT_smoothed - CH_ring[order]['amplitude'] *
                               np.cos((CH_ring[order]['angle']*np.pi/180-angles)*order) / (1 if order is 0 else np.pi**0.5))
            print(f'Symmetrical CDO-wide stdev: {np.ma.std(BT_smoothed)}')



    # draw image
        if make_image:

            for cmap_name in cmap_name_list:

                if cmap_name[0:2] == im_type:
                    dict_plotting = {'lons': lons, 'lats': lats, 'BT': BT_cropped, 'lon_TC': lon_TC, 'lat_TC': lat_TC,

                                     'cm_size': cm_size, 'im_size': im_size, 'dpi': dpi, 'ratio': ratio,
                                     'Eye_area_r': Eye_area_r,'R_edge': R_edge, 'R_inner': R_inner, 'R_out': R_out,
                                     'xpTrack': xpTrack, 'ypTrack': ypTrack,

                                     'top_text': top_text, 'pos_text': pos_text, 'temp_text': temp_text,'TC': TC,
                                     'cmap_name': cmap_name,'image_datetime_text': image_datetime_text, 'f_num': f_num,
                                     'sat_name': sat_name, 'b_num': b_num,

                                     'analyse_CDO': analyse_CDO, 'do_ADT': do_ADT, 'new_RMW': new_RMW,
                                     'no_crop': no_crop,'crop_status': crop_status, 'plot_track': plot_track,
                                     'save_image': save_image, 'overwrite_image': overwrite_image,
                                     'show_gridline': show_gridline,'show_center': show_center,
                                     'show_image': show_image, 'show_RMW': show_RMW, 'use_track': use_track}


                    plot_image(input=dict_plotting)

    if do_ADT:
        if Eye_area_r < 2:
            max_temp = CDO_fixed_temp
        ADT_data = [image_mjd, np.sum(b_num), CDO_fixed_temp, max_temp, Eye_area_r, R_edge * 111, float(lat_TC), float(lon_TC)]
        print('ADT input:', ADT_data)
        return ADT_data
    else:
        return BT_eye
    return 0
