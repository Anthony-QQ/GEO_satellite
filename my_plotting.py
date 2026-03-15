import os
import numpy as np
import numpy.ma as ma
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER

import my_cmap
from my_functions import get_folder, r_to_RMW
import config as pm

if pm.plot_all_TC_images and (pm.save_image or pm.save_CDO_image) and False:
    import matplotlib as mpl
    mpl.use('Agg')


def remove_1st_harmonic(BT_no_mean, angles, r_indices, i):
    BT = ma.masked_where(r_indices != i,BT_no_mean)
    angles = ma.masked_where(r_indices != i, angles)

    for order in [1]:
        filter_1 = np.cos(angles * order)
        filter_2 = np.cos(angles * order - np.pi / 2)
        element = (np.ma.sum(np.multiply(filter_1, BT)) + 1j * np.ma.sum(
            np.multiply(filter_2, BT))) / np.ma.count(BT)
        amplitude = np.abs(element) * 2
        direction = np.angle(element) / order
        CH_ring = {'order': order, 'amplitude': np.round(amplitude, 3), 'angle': np.round(direction * 180 / np.pi, 1)}
    BT_smoothed = BT

    for order in [1]:
        BT_smoothed = (BT_smoothed - CH_ring['amplitude'] *
                       np.cos((CH_ring['angle'] * np.pi / 180 - angles) * order))
    ring_average = np.ma.average(BT_smoothed)
    return np.ma.std(BT_smoothed)


def CDO_cs(BT_0, distances, angles, b_dict=None, n_dict=None, r=10, R_find=3, R_step=0.05):

    if b_dict is None:
        show, do, save = False, False, False
    else:
        show = b_dict['show']
        do = b_dict['do']
        save = b_dict['save']


    if n_dict is None:
        R_inner = R_out = R_edge = R_eye = None

    else:
        R_inner, R_out, R_edge, R_eye = n_dict['CDO_lines']


    # distances are in degrees
    try:
        #minimum radius to start analysis
        R_start = np.round(R_eye-R_step/2,1) + R_step/2
    except:
        R_start = 0.25-R_step/2

    if do:
        #binning range
        R_list = np.arange(R_start, R_start + R_find, R_step)

        #binning
        r_indices = np.digitize(distances, R_list)
        T_list = [np.mean(BT_0[r_indices == i]) for i in range(1, len(R_list))]
        std_list = [np.std(BT_0[r_indices == i]) for i in range(1, len(R_list))]


        #trimming
        R_list += R_step / 2
        R_list = R_list[:-1]

        #Global coldest ring
        T_min = np.min(T_list)
        T_min_i = np.argmin(T_list)

        #Radius of coldest ring
        R_min = R_list[T_min_i]

        #from half of coldest ring to coldest ring + 2 deg
        std_i_start = int(T_min_i / 2) + 1
        std_i_end = T_min_i + int(2/R_step)


        #Global smoothest ring
        std_min = np.min(std_list[std_i_start:std_i_end])
        std_min_i = np.argmin(std_list[std_i_start:std_i_end]) + std_i_start
        #Radius of smoothest ring
        R_smooth = R_list[std_min_i]


        if do:


            fig, ax1 = plt.subplots(figsize=(8,6))

            color = 'b'
            ax1.set_xlabel('r (degrees)')
            ax1.set_ylabel('Temperature', color=color)

            y_min = int(T_min/2)*2-2
            y_max = int(T_min/2)*2+30
            ax1.set_ylim(y_min, y_max)

            #plotting main graph
            ax1.plot(R_list, T_list, '.-', color=color)
            ax1.tick_params(axis='y', labelcolor=color)

            #plotting CDO boundaries
            if n_dict is not None:

                ax1.plot([R_inner, R_inner], [T_min - 2, T_min + 10], 'm:')
                ax1.plot([R_out, R_out], [T_min - 2, T_min + 10], 'm:')
                ax1.plot([R_edge, R_edge], [T_min - 2, T_min + 10], 'g:')


            ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
            ax2.set_ylim(0, 14)


            color = 'r'
            ax2.set_ylabel('standard deviation', color=color)  # we already handled the x-label with ax1
            ax2.plot(R_list, std_list, '.-', color=color)
            ax2.tick_params(axis='y', labelcolor=color)

            ax1.scatter(R_min, T_min, c='b', label=f'Min_T {np.round(T_min ,1)}')
            ax2.scatter(R_smooth, std_min, c='r', label=f'Min_stdev {std_min:.2f}')

            if b_dict['symmetric']:
                symm_std_list = [remove_1st_harmonic(BT_0 - T_list[i - 1], angles, r_indices, i) for i in
                                 range(1, len(R_list)+1)]
                symm_std_min = np.min(symm_std_list[std_i_start:std_i_end])
                R_symm_smooth = R_list[np.argmin(symm_std_list[std_i_start:std_i_end]) + std_i_start]
                color = 'm'
                ax2.plot(R_list, symm_std_list, '.-', color=color)
                ax2.scatter(R_symm_smooth, symm_std_min, c=color, label=f'Min_symm_stdev {symm_std_min:.2f}')


            ax1.grid(axis='x')
            ax2.grid(axis='y')

            # fig.tight_layout()  # use this if the right y-label is slightly clipped
            fig.legend(loc='upper left')

            if n_dict is not None:
                # naming title and putting eye temp to upper right
                title_text = f'{n_dict['top_text']}\nCDO Analysis\nTime valid:{n_dict['image_datetime_text']}'
                ax1.set_title(title_text, fontsize=12)
                plt.title(f'Eye temp: {n_dict['E_T']:.2f}', loc='right', fontsize=10)

                # saving image to file
                if save:

                    image_name = f'{n_dict['top_text']}_CDO_analysis_{n_dict['image_datetime_text']}'
                    target_dir = os.path.join(get_folder(type='output_image'),
                                              'CDO_analysis',
                                              n_dict['TC'],
                                              f'Band_{n_dict['b_num']}')
                    print(target_dir)
                    os.makedirs(target_dir, exist_ok=True)

                    target_name = os.path.join(target_dir, image_name)
                    plt.savefig(target_name)  # saves to png file by default
                    print(f'Final path is {target_name}')

                    show = False

            if show and not save:
                plt.show()
            plt.close()

        print(f'Coldest ring has T={T_min:.1f} at r={R_min:.2f} deg,'
             f'smoothest ring has stdev of {std_min:.2f} at r={R_smooth:.2f} deg.')

    return 0



def plot_image(**kwargs):
    #(bundle_1, bundle_2, bundle_3, bundle_4) = bundle
    #(lons, lats, BT, lon_TC, lat_TC) = bundle_1
    #(cm_size, im_size, dpi, ratio, Eye_area_r, R_edge, R_inner, R_out, crop_status, xpTrack, ypTrack) = bundle_2
    #(top_text, pos_text, temp_text, image_datetime_text, TC, cmap_name, f_num, sat_name, b_num) = bundle_3
    #(analyse_CDO, do_ADT, new_RMW, no_crop, plot_track, save_image, show_center, show_image, show_RMW, use_track) = bundle_4

    my_input = kwargs['input']

    fig = plt.figure(num=np.mod(my_input['f_num'] + 1, 20), dpi=my_input['dpi'], facecolor='w',
                     figsize=(my_input['im_size'], my_input['im_size']), clear=True)

    ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree(
        central_longitude=180 if my_input['dateline_adj'] else 0) if pm.use_cartopy else 'rectilinear')

    default_proj = ccrs.PlateCarree() if pm.use_cartopy else ax.transData

    # Figure size
    ax.set_aspect(my_input['ratio'])
    ax.set_box_aspect(my_input['ratio'] ** 0)

    # colourmap limits
    cmap, vmin, vmax = my_cmap.get_cmap(my_input['cmap_name'], my_input['sat_name'], my_input['b_num'])

    # Actual image
    im = ax.pcolormesh(my_input['lons'], my_input['lats'], my_input['BT'],
                       cmap=cmap, vmin=vmin, vmax=vmax, shading='nearest', transform=default_proj)

    if pm.use_cartopy:
        ax.set_extent(my_input['extent'], crs=ccrs.PlateCarree())
        if pm.show_coastline:
            ax.add_feature(pm.coast)

    if pm.show_center and (not pm.draw_full or pm.use_track):
        theta = np.linspace(0, 2 * np.pi, 150)

        # Mark centre of eye using small circle
        if my_input['Eye_area_r'] > 10:
            plt.scatter(my_input['lon_TC'], my_input['lat_TC'], s=my_input['cm_size'] / 2500,
                        facecolors=(1, 0, 0, 0.5), edgecolors='none', transform=default_proj)

        # Mark CDO sizes using parametric circles
        lon_inner = my_input['R_inner'] * np.cos(theta) * my_input['ratio'] + my_input['lon_TC']
        lat_inner = my_input['R_inner'] * np.sin(theta) + my_input['lat_TC']
        lon_outer = my_input['R_out'] * np.cos(theta) * my_input['ratio'] + my_input['lon_TC']
        lat_outer = my_input['R_out'] * np.sin(theta) + my_input['lat_TC']
        plt.plot(lon_inner, lat_inner, '-.', color=(1, 0, 1, 0.5), transform=default_proj)
        plt.plot(lon_outer, lat_outer, '-.', color=(1, 0, 1, 0.5), transform=default_proj)

        # Mark CDO edge
        lon_edge = my_input['R_edge'] * np.cos(theta) * my_input['ratio'] + my_input['lon_TC']
        lat_edge = my_input['R_edge'] * np.sin(theta) + my_input['lat_TC']
        plt.plot(lon_edge, lat_edge, '-.', color=(0, 0.9, 0, 0.5), transform=default_proj)

    # Draw gridlines
    if pm.show_gridline:
        if pm.use_cartopy:
            grid_interval = 2 ** (round(np.log2(pm.im_extent[0]), 0) - 3)
            gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True, linewidth=0.5, color='black', alpha=0.5, linestyle='--')
            gl.top_labels = False  # suppress top labels
            gl.right_labels = False  # suppress right labels
            gl.xlocator = mticker.FixedLocator(np.arange(-180, 180, grid_interval))  # Control gridline spacing
            gl.ylocator = mticker.FixedLocator(np.arange(-90, 90, grid_interval))
            gl.xformatter = LONGITUDE_FORMATTER
            gl.yformatter = LATITUDE_FORMATTER
            gl.xlabel_style = {'size': 8, 'color': 'k'}  # Customize label style
            gl.ylabel_style = {'size': 8, 'color': 'k'}
        else:
            ax.grid(linewidth=0.5, color='black', alpha=0.5, linestyle='--')
            ax.set_xlabel('Longitude', color='k')
            ax.set_ylabel('Latitude', color='k')


    # Draw BST track
    if pm.use_track and pm.plot_track:
        ax.plot(my_input['xpTrack'], my_input['ypTrack'], '-.', color=(0, 0, 0, 0.5), transform=default_proj)

    # Add title of chart
    image_type_text = f'{my_input['crop_status']}_{my_input['cmap_name']}'
    title_text = f'{my_input['top_text']} \n {image_type_text} \nTime valid:{my_input['image_datetime_text']}'
    ax.set_title(title_text, fontsize=16)

    # Place colormap bar
    cax = fig.add_axes([ax.get_position().x1 + 0.01, ax.get_position().y0, 0.02, ax.get_position().height])
    plt.colorbar(im, cax=cax)

    # temperatures and position information
    if pm.show_RMW:
        if my_input['Eye_area_r'] > 10:
            acc = 1
        else:
            acc = 1
        # uses the RMW formula also found in ADT document
        RMW_text = (f'R: {np.round(my_input['Eye_area_r'], acc)} km, '
                    f'RMW: {np.round(r_to_RMW(my_input['Eye_area_r'], my_input['new_RMW']), acc)} km')
        CDO_text = f'CDO R: {np.round(my_input['R_edge'] * 111, 0)} km'

        plt.title(f'{RMW_text}\n{CDO_text}\n{my_input['pos_text']}\n{my_input['temp_text']}',
                  loc='right', fontsize=10)
    else:
        plt.title(f'{my_input['pos_text']}\n{my_input['temp_text']}', loc='right', fontsize=10)

    # Saving to image
    if pm.save_image:
        image_name = f'{my_input['top_text']}_{image_type_text}_{my_input['image_datetime_text']}'

        # The folder for output_images is on the same level as the folder with .nc files
        target_dir = os.path.join(get_folder(type='output_image'),
                                  my_input['crop_status'],
                                  my_input['TC'],
                                  f'Band_{my_input['b_num']}')
        print(target_dir)
        os.makedirs(target_dir, exist_ok=True)

        # Joins paths to get destination path
        target_name = os.path.join(target_dir, image_name)

        plt.savefig(target_name)  # saves to png file by desirable default behaviour
        print(f'Saved to {target_name}')

    if pm.show_image:
        plt.show()

    #fig.clear()
    plt.clf()
    plt.close()


    '''
    BT_grad = np.gradient(BT)

    for i in range(-5,5):
        for j in range(-5,5):
            polar = (lats-lat_TC+i/10) - 1j*(lons-lon_TC+j/10)
            polar = np.multiply(polar,np.exp(-np.abs(polar)))
            dot_z = BT_grad[0]*np.real(polar) + BT_grad[1]*np.imag(polar)

            print(i/10, j/10, np.sum(dot_z))
    '''


    return 0

def plot_ABI_hist(ds, im_size=8):
    plt.figure(2, figsize=(im_size, im_size))
    plt.hist(ds['Sectorized_CMI'].to_masked_array().compressed(), bins=255)
    plt.show()
    plt.close()
    return 0
