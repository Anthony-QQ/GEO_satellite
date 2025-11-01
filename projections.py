import numpy as np



'''
START PROJECTION FUNCTIONS
'''


def remove_small_items(array, indicator_array, min_val=-10000000):
    i_r = np.argwhere(indicator_array < min_val)
    print(i_r)
    if len(i_r) > 0:
        array = np.delete(array, i_r, 0)
    return array


def remove_large_items(array, indicator_array, max_val=10000000):
    i_r = np.argwhere(indicator_array > max_val)
    if len(i_r) > 0:
        array = np.delete(array, i_r, 0)
    return array


def remove_equal_items(array, indicator_array, equal_val=10000000):
    i_r = np.argwhere(indicator_array == equal_val)
    if len(i_r) > 0:
        array = np.delete(array, i_r, 0)
    return array


def remove_unequal_items(array, indicator_array, unequal_val=10000000):
    i_r = np.argwhere(indicator_array != unequal_val)
    if len(i_r) > 0:
        array = np.delete(array, i_r, 0)
    return array


def NSP_MaxLat(height=35786000, Earth_R=6371000.):
    h = height / Earth_R
    theta_max = np.degrees(np.arccos(1 / (h + 1)))
    return theta_max


def NS_Projection(r_theta_array=[0, 0], height=35786000, Earth_R=6371000.):
    # Near-sided Projection
    theta = np.array(r_theta_array[1])
    phi = np.array(r_theta_array[0])
    h = height / Earth_R
    l_max = h / (1 + h - 1 / (1 + h)) * np.sqrt(np.square(h + 1) - 1) / (h + 1)
    phi_max = np.degrees(np.arccos(1 / (h + 1)))

    do_removal = False
    if phi.ndim != 0:
        phi = np.array([0 if i >= phi_max else i for i in phi])
        do_removal = True
    elif phi > phi_max:
        phi = np.array(0)

    d = np.sin(np.radians(phi))
    l = d * (h / (1 + h - np.cos(np.radians(phi)))) / l_max
    projected_array = np.stack((np.array(l), theta))
    if do_removal:
        projected_array = projected_array.T
        projected_array = remove_equal_items(projected_array, phi, 0)
        projected_array = np.append(projected_array, np.array([[0, 0]]), axis=0)
        projected_array = projected_array.T
    return projected_array


def xy_to_polar(xy_array=[0, 1]):
    z = np.array(xy_array[1]) + 1j * np.array(xy_array[0])
    # theta = np.degrees(np.arctan2(x, y)) #arctan2 can accept y and x as two arrays
    # r = np.sqrt(np.square(x)+np.square(y))
    # theta goes clockwise from positive y-axis
    return np.stack((np.abs(z), np.degrees(np.angle(z))))


def polar_to_xy(r_theta_array=[1, 0]):
    # theta goes clockwise from positive y-axis
    # r is measured in degrees
    r, theta = np.array(r_theta_array[0]), np.radians(np.array(r_theta_array[1]))
    z = r * np.exp(1j * theta)
    y, x = np.real(z), np.imag(z)
    return np.stack((x, y))


def xy_to_FD(xy_array=[0, 0]):
    FD = np.add(np.multiply(np.array(xy_array), 0.5), 0.5)
    return FD


def latlon_to_polar(latlon_array=[0, 0], lon_0=-75):
    lat, lon = np.array(latlon_array[0]), np.subtract(np.array(latlon_array[1]), lon_0)
    if lat.ndim != 0:
        lat = np.array([i + 0.001 if i == 0 else i for i in lat])
        lon = np.array([i + 0.001 if i == 0 else i for i in lon])
    else:
        if lat == 0:
            lat = lat + 0.001
        if lon == 0:
            lon = lon + 0.001
    cos_phi = np.multiply(np.cos(np.radians(lat)), np.cos(np.radians(lon)))
    phi = np.degrees(np.arccos(cos_phi))

    cos_C = (np.cos(np.radians(lat)) - np.cos(np.radians(lon)) * cos_phi) / (
                np.sin(np.radians(lon)) * np.sin(np.radians(phi)))
    C = np.degrees(np.arcsin(cos_C))

    if C.ndim != 0:
        lat_sign = np.where(lat < 0, -1, 1)
        lat_flip = np.where(lat < 0, 180, 0)
        C = np.add(np.multiply(C, lat_sign), lat_flip)
    else:
        if lat >= 0:
            C = C
        else:
            C = 180 - C

    return np.stack((phi, C))


def latlon_to_FD(latlon_array=[0, 0], lon_0=-75, h=35786000, R=6371000.):
    polar = latlon_to_polar(latlon_array, lon_0)
    proj_polar = NS_Projection(polar, h, R)
    proj_xy = polar_to_xy(proj_polar)
    xy_FD = xy_to_FD(proj_xy)
    return xy_FD


def get_crop_raw(centre_latlon=[0, -75], side_deg=90, lon_sat=-75, h=35786000, R=6371000.):
    centre_FD = latlon_to_FD(centre_latlon, lon_sat, h)
    side_FD = side_deg / 180
    crop_raw = [[centre_FD[0] - side_FD, centre_FD[0] + side_FD], [centre_FD[1] - side_FD, centre_FD[1] + side_FD]]
    return crop_raw


def get_crop(crop_raw=[[0, 1], [0, 1]]):
    crop_new = [[max(0, crop_raw[0][0]), min(1, crop_raw[0][1])], [max(0, crop_raw[1][0]), min(1, crop_raw[1][1])]]
    return crop_new


def FD_to_zoom(colsize, FD_array, crop_array=[[0, 1], [0, 1]]):
    x_min, x_max, y_min, y_max = crop_array[0][0], crop_array[0][1], crop_array[1][0], crop_array[1][1]
    # FD_array is a 2-D array with one element for x and one element for y

    FD_x, FD_y = np.array(FD_array[0]), np.array(FD_array[1])
    FD_x, FD_y = np.divide(np.subtract(FD_x, x_min), (x_max - x_min)), np.divide(np.subtract(FD_y, y_max),
                                                                                 (y_min - y_max))
    x_minus, y_plus = min(0, x_min) / (x_max - x_min), max(0, y_max - 1) / (y_min - y_max)
    FD_x, FD_y = np.add(FD_x, x_minus), np.add(FD_y, y_plus)
    FD_x = np.multiply(np.multiply(np.array(FD_x), colsize), x_max - x_min)
    FD_y = np.multiply(np.multiply(np.array(FD_y), colsize), y_max - y_min)
    return np.stack((FD_x, FD_y))


def latlon_to_zoom(colsize, latlon_array=[0, 0], crop_array=[[0, 1], [0, 1]], lon_0=-75, h=35786000, R=6371000.):
    FD_array = latlon_to_FD(latlon_array, lon_0, h, R)
    zoom_array = FD_to_zoom(colsize, FD_array, crop_array)
    return zoom_array


# In[6]:

