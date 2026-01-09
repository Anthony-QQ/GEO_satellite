import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from colorspacious import cspace_converter
from matplotlib.colors import Colormap, ListedColormap, LinearSegmentedColormap

from my_functions import image_type


class my_cmap:
    def __init__(self):
        pass

    def wv_nrl(self):
        cvals = [-70, -56, -42, -35, -28, -14, 0]
        colors = ['#800000', '#ff8000', '#ffff80', '#80ff80', '#80ffff', '#0080ff', '#800080']
        wv_nrl = produce_cmap(cvals, colors, 'wv_nrl')




def produce_cmap(cvals, colors, name):
    vmin, vmax = min(cvals), max(cvals)
    norm = plt.Normalize(vmin, vmax)
    tuples = list(zip(map(norm, cvals), colors))
    cmap = LinearSegmentedColormap.from_list(name, tuples, N=4196, gamma=1.0)
    # mpl.colormaps.register(cmap,name=name,force=false)
    return list((cmap, vmin, vmax))


def cmap_fetch(name, type='ir'):
    cmap_dict = {
        'ir_bd': [
        [-80.5,
         -80.5, -75.5,
         -75.5, -69.5,
         -69.5, -63.5,
         -63.5, -53.5,
         -53.5, -41.5,
         -41.5, -30.5,
         -30.5, 9.5,
         9.5, 28],
        ['#555555',
         '#878787', '#878787',
         'w', 'w',
         'k', 'k',
         '#a0a0a0', '#a0a0a0',
         '#6e6e6e', '#6e6e6e',
         '#3c3c3c', '#3c3c3c',
         '#c9c9c9', '#6c6c6c',
         'w', 'k']
    ],
    'ir_bw': [
        [-80, 30],
        ['w', 'k']
    ],
    'ir_ca': [
        [-95, -85.5, -80.5, -75.5, -69.5, -63.5, -53.5, -41.5, -30.5, 9.5,
         9.5, 25, 50],
        ['#ffffff', '#5038b0', '#a068e0', '#c42010', '#ff3000', '#f0b000', '#80ff00', '#18b080', '#0088b8', '#203040',
         '#707070', '#000000', '#501800']
    ],
    'ir_ca_2': [
        [-95, -85.5, -80.5, -75.5, -69.5, -63.5, -53.5, -41.5, -30.5, 9.5,
         9.5, 25, 50],
        ['#ffffff', '#5038b0', '#a068e0', '#a01010', '#ff3000', '#f0b000', '#80ff00', '#18b080', '#0088b8', '#203040',
         '#707070', '#000000', '#501800']
    ],
    'ir_cb': [
        [-100, -85.5,
         -85.5, -80.5,
         -80.5, -75.5,
         -75.5, -69.5,
         -69.5, -63.5,
         -63.5, -53.5,
         -53.5, -41.5,
         -41.5, -30.5,
         -30.5, 9.5,
         9.5, 28],
        ['#6040a0', '#6040a0',
         '#5060d0', '#5060d0',
         '#70a0c0', '#70a0c0',
         '#9edae5', '#9edae5',
         '#208010', '#208010',
         '#bcbd8d', '#bcbd8d',
         '#ff7f0e', '#ff7f0e',
         '#c03030', '#c03030',
         '#c49c94', '#8c564b',
         'w', 'k']
    ],
    'ir_cc': [
        [-85.5,
         -85.5, -80.5,
         -80.5, -75.5,
         -75.5, -69.5,
         -69.5, -63.5,
         -63.5, -53.5,
         -53.5, -41.5,
         -41.5, -30.5,
         -30.5, 9.5,
         9.5, 28],
        ['w',
         '#000096', '#000096',
         '#4169e1', '#4169e1',
         '#00beff', '#00beff',
         '#a0d2ff', '#a0d2ff',
         '#ffe132', '#ffe132',
         '#ff6e00', '#ff6e00',
         '#a02323', '#a02323',
         '#ffe1e1', '#644646',
         'w', 'k']
    ],
    'ir_cc_2': [
        [-100, -92,
         -92, -85.5,
         -85.5, -80.5,
         -80.5, -75.5,
         -75.5, -69.5,
         -69.5, -63.5,
         -63.5, -53.5,
         -53.5, -41.5,
         -41.5, -30.5,
         -30.5, 9.5,
         9.5, 28],
        ['w', '#fad2fa',
         '#d7d7e1', '#7171e1',
         '#4132a0', '#000087',
         '#231ee1', '#5a50f5',
         '#1478f0', '#28b4f0',
         '#5acdf0', '#afffff',
         '#ffff50', '#ffbe32',
         '#ff8c00', '#dc5a00',
         '#a02300', '#640000',
         '#e1b9b9', '#734b4b',
         'w', 'k']
    ],
    'ir_cc_3': [
        [-100, -92,
         -92, -85.5,
         -85.5, -80.5,
         -80.5, -75.5,
         -75.5, -69.5,
         -69.5, -66.5, -63.5,
         -63.5, -53.5,
         -53.5, -41.5,
         -41.5, -30.5,
         -30.5, 9.5,
         9.5, 28],
        ['w', '#f8ccee',
         '#c0bbee', '#8877dd',
         '#552abb', '#220088',
         '#5533ff', '#6655ff',
         '#4488ff', '#55bbee',
         '#66ccaa', '#a0dfa0', '#bbe866',
         '#fff844', '#ffbb33',
         '#ff8822', '#dd5522',
         '#992211', '#660000',
         '#ddbbbb', '#775555',
         'w', 'k']
    ],
    'ir_cc_4': [
        [-85.5,
         -85.5, -80.5,
         -80.5, -75.5,
         -75.5, -69.5,
         -69.5, -63.5,
         -63.5, -53.5,
         -53.5, -41.5,
         -41.5, -30.5,
         -30.5, 9.5,
         9.5, 28],
        ['w',
         '#000096', '#000096',
         '#4169e1', '#4169e1',
         '#00beff', '#00beff',
         '#88dd99', '#88dd99',
         '#ffe132', '#ffe132',
         '#ff6e00', '#ff6e00',
         '#a02323', '#a02323',
         '#ffe1e1', '#644646',
         'w', 'k']
    ],
    'ir_color': [
        [-100, -90,
         -90, -80,
         -80, -70,
         -70, -60,
         -60, -50,
         -50, -30,
         -30, 28],
        ['#5000a0', 'w',
         'k', '#ffff00',
         '#ff0000', '#640000',
         '#00ff00', '#006400',
         '#0000ff', '#000064',
         '#545454', '#a8ffff',
         'w', 'k']
    ],
    'ir_nrl_h_1': [
        [-173, -123, -93,
         -93, -83, -73, -63, -61,
         -61, -53, -45,
         -45, -43, -33, -23, -20,
         -20, -13, -3, 7, 47],
        ['#00194c', 'w', '#a363e5',
         '#a36319', '#bd4310', '#da290a', '#f40a03', '#fa0504',
         '#f3cc02', '#f2de01', '#f2f301',
         '#8bf201', '#81ed01', '#4ed300', '#21bd01', '#0db402',
         '#05dbff', '#05a6ea', '#0457cf', '#0507b4', '#050700']
    ],
    'ir_pct_1': [
        [-173, -143, -113,
         -113, -81,
         -81, -65,
         -65, -40,
         -40, -13, 27],
        ['#00194b', 'w', '#a05fe6',
         '#a05f19', '#fa0000',
         '#f0c800', '#ffff00',
         '#8cf200', '#0eb400',
         '#05dcff', '#0507b4', '#050700']
    ],
    'ir_pct_2': [
        [-193, -168, -143,
         -143, -113,
         -113, -81,
         -81, -65,
         -65, -40,
         -40, -13,
         -13, 7, 17, 32],
        ['#003333', '#88bba0', '#ddffee',
         '#ffddee', '#aa7788',
         '#a36319', '#f90602',
         '#f8c30d', '#f1e400',
         '#8ef101', '#0bb617',
         '#0ad5c2', '#0000bb',
         '#040483', '#6a5acd', '#a590cc', '#e4e4ee']
    ],
    'ir_test_1': [
        [-95, -90, -85, -81, -76, -70, -64, -54, -42, -31, -12, 7, 11, 30, 45],
        ['#FFFFFF', '#FAEEFA', '#D0DDF5', '#99D0FF', '#77D0DD', '#77C3BB', '#55BB88', '#44B044', '#77AA44', '#90A077', '#8C8877', '#886666', '#772255', '#441155', '#111111']
    ],
    'pct_1': [
        list(np.array([100, 130, 160,
                       160, 192,
                       192, 208,
                       208, 233,
                       233, 265, 280, 300]) - 273.15),
        ['#00194b', 'w', '#a05fe6',
         '#a05f19', '#fa0000',
         '#f0c800', '#ffff00',
         '#8cf200', '#0eb400',
         '#05dcff', '#0000bb', '#6a5acd', '#eeeeee']
    ],
    'wv_bd': [
        [-80,
         -80, -75,
         -75, -69,
         -69, -63,
         -63, -57,
         -57, -51,
         -51, -45,
         -45, -30,
         -30, -16,
         -16, -5],
        ['#555555',
         '#878787', '#878787',
         'w', 'w',
         'k', 'k',
         '#a0a0a0', '#a0a0a0',
         '#6e6e6e', '#6e6e6e',
         '#3c3c3c', '#3c3c3c',
         '#c9c9c9', '#6c6c6c',
         'w', '#808080',
         '#606060', 'k']
    ],
    'wv_bw': [
        [-80, 0],
        ['w', 'k']
    ],
    'wv_cc': [
        [-85,
         -85, -80,
         -80, -75,
         -75, -70,
         -70, -64,
         -64, -57,
         -57, -51,
         -51, -45,
         -45, -30,
         -30, -16,
         -16, -5],
        ['w',
         '#000096', '#000096',
         '#4169e1', '#4169e1',
         '#00beff', '#00beff',
         '#a0d2ff', '#a0d2ff',
         '#ffe132', '#ffe132',
         '#ff6e00', '#ff6e00',
         '#a02323', '#a02323',
         '#ffe1e1', '#644646',
         'w', '#3c3c3c',
         '#5f5ff0', 'k']
    ],
    'wv_cc_2': [
        [-100, -90,
         -90, -85,
         -85, -80,
         -80, -75,
         -75, -70,
         -70, -64,
         -64, -57,
         -57, -51,
         -51, -45,
         -45, -30,
         -30, -25,
         -25, -20,
         -20, -15,
         -15, -5],
        ['w', '#fad2fa',
         '#d7d7e1', '#7171e1',
         '#4132a0', '#00008c',
         '#231ee1', '#5a50f5',
         '#1478f0', '#28b4f0',
         '#5acdf0', '#afffff',
         '#ffff50', '#ffbe32',
         '#ff8c00', '#dc5a00',
         '#a02300', '#640000',
         '#e1b9b9', '#734b4b',
         'w', '#bbffbb',
         '#aad7d7', '#9bb9b9',
         '#7dafe1', '#6482f0',
         '#6e41f0', 'k']
    ],
    'wv_color': [
        [-100, -90,
         -90, -80,
         -80, -70,
         -70, -60,
         -60, -50,
         -50, -40,
         -40, -28, -10],
        ['#5000a0', 'w',
         'k', '#ffff00',
         '#ff0000', '#640000',
         '#00ff00', '#006400',
         '#0000ff', '#000064',
         '#545454', '#a8ffff',
         'w', '#636363', 'k']
    ],
    'wv_nrl': [
        [-70, -56, -42, -35, -28, -14, 0],
        ['#800000', '#ff8000', '#ffff80', '#80ff80', '#80ffff', '#0080ff', '#800080']
    ],
    'wv_nrl_extend': [
        [-84, -77, -70, -56, -42, -35, -28, -14, 0],
        ['#0000a0', '#400080', '#800000', '#ff8000', '#ffff80', '#80ff80', '#80ffff', '#0080ff', '#800080']
    ],
    'wv_nrld': [
        [-90, -85,
         -85, -80,
         -80, -75,
         -75, -70,
         -70, -64,
         -64, -56,
         -56, -42, -35, -28, -21, -14, -7, 0],
        ['w', '#aaaaaa',
         '#73a0ff', '#7373d7',
         '#9b41b4', '#8732aa',
         '#870a83', '#640f50',
         '#500000', '#820000',
         '#8c2800', '#eb6e00',
         '#ff8000', '#ffff80', '#80ff80', '#80ffff', '#40bfff', '#0080ff', '#4040bf', '#800080']
    ],
    'wv_ssd': [
        [-100, -74, -47.5, -30, -14, -2.5],
        ['#00ffff', '#006c00', 'w', '#0000a8', '#ffff00', '#ff0000']
    ],
    'wv_ssdd': [
        [-100, -85,
         -85, -80,
         -80, -75,
         -75, -70,
         -70, -64,
         -64, -56,
         -56, -46, -30,
         -30, -22.5,
         -22.5, -15, -7,
         -7, 0],
        ['#f0ffff', '#c0e0ff',
         '#80d0f0', '#20a0b0',
         '#60a090', '#3080a0',
         '#508060', '#006030',
         '#007000', '#208020',
         '#40a040', '#70c070',
         '#90d090', 'w', '#2000b0',
         '#002090', '#40a890',
         '#609860', '#ffff00', '#ffa000',
         '#ff7000', '#ff0000']
    ],
    'wv_test_1': [
        [-95, -85, -81, -76, -70, -64, -54, -48, -42, -34, -28, -22, -16, -10, -2],
        ['#F5DDEE', '#CCBBEE', '#99AAFF', '#55A0FF', '#3388CC', '#117088', '#005A55', '#114433', '#335522', '#666622', '#AA7733', '#DD8855', '#FF9977', '#FFBBBB', '#F5DDEE']
    ]
    }

    cvals, colors = cmap_dict.get(name, cmap_dict[f'{type}_bw'])
    return produce_cmap(cvals, colors, name)   #returns list of [cmap, vmin, vmax]


def produce_cmap_list():
    #global cmap_names
    #global cmap_list
    cmap_names = []
    cmap_list = []

    cvals = [-70, -56, -42, -35, -28, -14, 0]
    colors = ['#800000', '#ff8000', '#ffff80', '#80ff80', '#80ffff', '#0080ff', '#800080']
    wv_nrl = produce_cmap(cvals, colors, 'wv_nrl')
    cmap_names.append('wv_nrl')
    cmap_list.append(wv_nrl)

    cvals = [-100, -74, -47.5, -30, -14, -2.5]
    colors = ['#00ffff', '#006c00', 'w', '#0000a8', '#ffff00', '#ff0000']
    cmap_list.append(produce_cmap(cvals, colors, 'wv_ssd'))
    cmap_names.append('wv_ssd')

    cvals = [-84, -77, -70, -56, -42, -35, -28, -14, 0]
    colors = ['#0000a0', '#400080', '#800000', '#ff8000', '#ffff80', '#80ff80', '#80ffff', '#0080ff', '#800080']
    cmap_list.append(produce_cmap(cvals, colors, 'wv_nrl_extend'))
    cmap_names.append('wv_nrl_extend')

    cvals = [-100, -90,
             -90, -80,
             -80, -70,
             -70, -60,
             -60, -50,
             -50, -30,
             -30, 28]
    colors = ['#5000a0', 'w',
              'k', '#ffff00',
              '#ff0000', '#640000',
              '#00ff00', '#006400',
              '#0000ff', '#000064',
              '#545454', '#a8ffff',
              'w', 'k']
    cmap_list.append(produce_cmap(cvals, colors, 'ir_color'))
    cmap_names.append('ir_color')

    cvals = [-100, -90,
             -90, -80,
             -80, -70,
             -70, -60,
             -60, -50,
             -50, -40,
             -40, -28, -10]
    colors = ['#5000a0', 'w',
              'k', '#ffff00',
              '#ff0000', '#640000',
              '#00ff00', '#006400',
              '#0000ff', '#000064',
              '#545454', '#a8ffff',
              'w', '#636363', 'k']
    cmap_list.append(produce_cmap(cvals, colors, 'wv_color'))
    cmap_names.append('wv_color')

    cvals = [-80, 0]
    colors = ['w', 'k']
    cmap_list.append(produce_cmap(cvals, colors, 'wv_bw'))
    cmap_names.append('wv_bw')

    cvals = [-80, 30]
    colors = ['w', 'k']
    cmap_list.append(produce_cmap(cvals, colors, 'ir_bw'))
    cmap_names.append('ir_bw')

    cvals = [-80.5,
             -80.5, -75.5,
             -75.5, -69.5,
             -69.5, -63.5,
             -63.5, -53.5,
             -53.5, -41.5,
             -41.5, -30.5,
             -30.5, 9.5,
             9.5, 28]
    colors = ['#555555',
              '#878787', '#878787',
              'w', 'w',
              'k', 'k',
              '#a0a0a0', '#a0a0a0',
              '#6e6e6e', '#6e6e6e',
              '#3c3c3c', '#3c3c3c',
              '#c9c9c9', '#6c6c6c',
              'w', 'k']
    cmap_list.append(produce_cmap(cvals, colors, 'ir_bd'))
    cmap_names.append('ir_bd')

    cvals = [-95, -85.5, -80.5, -75.5, -69.5, -63.5, -53.5, -41.5, -30.5,
             9.5, 9.5,
             25, 50]
    colors = ['#ffffff', '#5038b0', '#a068e0', '#c42010', '#ff3000', '#f0b000', '#80ff00', '#18b080', '#0088b8',
              '#203040', '#707070',
              '#000000', '#501800']
    cmap_list.append(produce_cmap(cvals, colors, 'ir_ca'))
    cmap_names.append('ir_ca')

    cvals = [-95, -85.5, -80.5, -75.5, -69.5, -63.5, -53.5, -41.5, -30.5,
             9.5,
             9.5, 25, 50]
    colors = ['#ffffff', '#5038b0', '#a068e0', '#a01010', '#ff3000', '#f0b000', '#80ff00', '#18b080', '#0088b8',
              '#203040',
              '#707070', '#000000', '#501800']
    cmap_list.append(produce_cmap(cvals, colors, 'ir_ca_2'))
    cmap_names.append('ir_ca_2')

    cvals = [-85.5,
             -85.5, -80.5,
             -80.5, -75.5,
             -75.5, -69.5,
             -69.5, -63.5,
             -63.5, -53.5,
             -53.5, -41.5,
             -41.5, -30.5,
             -30.5, 9.5,
             9.5, 28]
    colors = ['w',
              '#000096', '#000096',
              '#4169e1', '#4169e1',
              '#00beff', '#00beff',
              '#a0d2ff', '#a0d2ff',
              '#ffe132', '#ffe132',
              '#ff6e00', '#ff6e00',
              '#a02323', '#a02323',
              '#ffe1e1', '#644646',
              'w', 'k']
    cmap_list.append(produce_cmap(cvals, colors, 'ir_cc'))
    cmap_names.append('ir_cc')


    cvals = [-100, -92,
             -92, -85.5,
             -85.5, -80.5,
             -80.5, -75.5,
             -75.5, -69.5,
             -69.5, -63.5,
             -63.5, -53.5,
             -53.5, -41.5,
             -41.5, -30.5,
             -30.5, 9.5,
             9.5, 28]
    colors = ['w', '#fad2fa',
              '#d7d7e1','#7171e1',
              '#4132a0', '#000087',
              '#231ee1', '#5a50f5',
              '#1478f0', '#28b4f0',
              '#5acdf0', '#afffff',
              '#ffff50', '#ffbe32',
              '#ff8c00', '#dc5a00',
              '#a02300', '#640000',
              '#e1b9b9', '#734b4b',
              'w', 'k']
    cmap_list.append(produce_cmap(cvals, colors, 'ir_cc_2'))
    cmap_names.append('ir_cc_2')

    cvals = [-80,
             -80, -75,
             -75, -69,
             -69, -63,
             -63, -57,
             -57, -51,
             -51, -45,
             -45, -30,
             -30, -16,
             -16, -5]
    colors = ['#555555',
              '#878787', '#878787',
              'w', 'w',
              'k', 'k',
              '#a0a0a0', '#a0a0a0',
              '#6e6e6e', '#6e6e6e',
              '#3c3c3c', '#3c3c3c',
              '#c9c9c9', '#6c6c6c',
              'w', '#808080',
              '#606060', 'k']
    cmap_list.append(produce_cmap(cvals, colors, 'wv_bd'))
    cmap_names.append('wv_bd')

    cvals = [-85,
             -85, -80,
             -80, -75,
             -75, -70,
             -70, -64,
             -64, -57,
             -57, -51,
             -51, -45,
             -45, -30,
             -30, -16,
             -16, -5]
    colors = ['w',
              '#000096', '#000096',
              '#4169e1', '#4169e1',
              '#00beff', '#00beff',
              '#a0d2ff', '#a0d2ff',
              '#ffe132', '#ffe132',
              '#ff6e00', '#ff6e00',
              '#a02323', '#a02323',
              '#ffe1e1', '#644646',
              'w', '#3c3c3c',
              '#5f5ff0', 'k']
    cmap_list.append(produce_cmap(cvals, colors, 'wv_cc'))
    cmap_names.append('wv_cc')

    cvals = [-100, -90,
             -90, -85,
             -85, -80,
             -80, -75,
             -75, -70,
             -70, -64,
             -64, -57,
             -57, -51,
             -51, -45,
             -45, -30,
             -30, -25,
             -25, -20,
             -20, -15,
             -15, -5]
    colors = ['w', '#fad2fa',
              '#d7d7e1', '#7171e1',
              '#4132a0', '#00008c',
              '#231ee1', '#5a50f5',
              '#1478f0', '#28b4f0',
              '#5acdf0', '#afffff',
              '#ffff50', '#ffbe32',
              '#ff8c00', '#dc5a00',
              '#a02300', '#640000',
              '#e1b9b9', '#734b4b',
              'w', '#bbffbb',
              '#aad7d7', '#9bb9b9',
              '#7dafe1', '#6482f0',
              '#6e41f0', 'k']
    cmap_list.append(produce_cmap(cvals, colors, 'wv_cc_2'))
    cmap_names.append('wv_cc_2')

    cvals = [-90, -85,
             -85, -80,
             -80, -75,
             -75, -70,
             -70, -64,
             -64, -56,
             -56, -42, -35, -28, -21, -14, -7, 0]
    colors = ['w', '#aaaaaa',
              '#73a0ff', '#7373d7',
              '#9b41b4', '#8732aa',
              '#870a83', '#640f50',
              '#500000', '#820000',
              '#8c2800', '#eb6e00',
              '#ff8000', '#ffff80', '#80ff80', '#80ffff', '#40bfff', '#0080ff', '#4040bf', '#800080']
    cmap_list.append(produce_cmap(cvals, colors, 'wv_nrld'))
    cmap_names.append('wv_nrld')

    cvals = [-100, -85,
             -85, -80,
             -80, -75,
             -75, -70,
             -70, -64,
             -64, -56,
             -56, -46, -30,
             -30, -22.5,
             -22.5, -15, -7,
             -7, 0]
    colors = ['#f0ffff', '#c0e0ff',
              '#80d0f0', '#20a0b0',
              '#60a090', '#3080a0',
              '#508060', '#006030',
              '#007000', '#208020',
              '#40a040', '#70c070',
              '#90d090', 'w', '#2000b0',
              '#002090', '#40a890',
              '#609860', '#ffff00', '#ffa000',
              '#ff7000', '#ff0000']
    cmap_list.append(produce_cmap(cvals, colors, 'wv_ssdd'))
    cmap_names.append('wv_ssdd')

    cvals = [-100, -85.5,
             -85.5, -80.5,
             -80.5, -75.5,
             -75.5, -69.5,
             -69.5, -63.5,
             -63.5, -53.5,
             -53.5, -41.5,
             -41.5, -30.5,
             -30.5, 9.5,
             9.5, 28]
    colors = ['#6040a0','#6040a0',
              '#5060d0', '#5060d0',
              '#70a0c0', '#70a0c0',
              '#9edae5', '#9edae5',
              '#208010', '#208010',
              '#bcbd8d', '#bcbd8d',
              '#ff7f0e', '#ff7f0e',
              '#c03030', '#c03030',
              '#c49c94', '#8c564b',
              'w', 'k']
    cmap_list.append(produce_cmap(cvals, colors, 'ir_cb'))
    cmap_names.append('ir_cb')

    cvals = [-95, -85, -81, -76, -70,
             -64, -54, -48, -42, -34,
             -28, -22, -16, -10, -2]
    colors = ['#F5DDEE','#CCBBEE','#99AAFF','#55A0FF','#3388CC',
              '#117088','#005A55','#114433','#335522','#666622',
              '#AA7733','#DD8855','#FF9977','#FFBBBB','#F5DDEE']
    cmap_list.append(produce_cmap(cvals, colors, 'wv_test_1'))
    cmap_names.append('wv_test_1')

    cvals = [-95, -90, -85, -81, -76,
             -70, -64, -54, -42, -31,
             -12, 7, 11, 30, 45]
    colors = ['#FFFFFF','#FAEEFA','#D0DDF5','#99D0FF','#77D0DD',
              '#77C3BB','#55BB88','#44B044','#77AA44','#90A077',
              '#8C8877','#886666','#772255','#441155','#111111']
    cmap_list.append(produce_cmap(cvals, colors, 'ir_test_1'))
    cmap_names.append('ir_test_1')

    cvals = [-173, -123, -93,
             -93, -83, -73, -63, -61,
             -61, -53, -45,
             -45, -43, -33, -23, -20,
             -20, -13, -3, 7, 47]
    colors = ['#00194c', 'w', '#a363e5',
              '#a36319', '#bd4310', '#da290a', '#f40a03', '#fa0504',
              '#f3cc02', '#f2de01', '#f2f301',
              '#8bf201', '#81ed01', '#4ed300', '#21bd01', '#0db402',
              '#05dbff', '#05a6ea', '#0457cf', '#0507b4', '#050700']
    cmap_list.append(produce_cmap(cvals, colors, 'ir_nrl_h_1'))
    cmap_names.append('ir_nrl_h_1')

    cvals = [-173, -143, -113,
             -113, -81,
             -81, -65,
             -65, -40,
             -40, -13, 27]
    colors = ['#00194b', 'w', '#a05fe6',
              '#a05f19', '#fa0000',
              '#f0c800', '#ffff00',
              '#8cf200', '#0eb400',
              '#05dcff', '#0507b4', '#050700']
    cmap_list.append(produce_cmap(cvals, colors, 'ir_pct_1'))
    cmap_names.append('ir_pct_1')


    cvals = [-193, -168, -143,
             -143, -113,
             -113, -81,
             -81, -65,
             -65, -40,
             -40, -13,
             -13, 7, 17, 32]
    colors = ['#003333', '#88bba0', '#ddffee',
              '#ffddee', '#aa7788',
              '#a36319', '#f90602',
              '#f8c30d', '#f1e400',
              '#8ef101', '#0bb617',
              '#0ad5c2', '#0000bb',
              '#040483', '#6a5acd', '#a590cc', '#e4e4ee']
    cmap_list.append(produce_cmap(cvals, colors, 'ir_pct_2'))
    cmap_names.append('ir_pct_2')

    cvals = list(np.array([100, 130, 160,
             160, 192,
             192, 208,
             208, 233,
             233, 265, 280, 300]) - 273.15)
    colors = ['#00194b', 'w', '#a05fe6',
              '#a05f19', '#fa0000',
              '#f0c800', '#ffff00',
              '#8cf200', '#0eb400',
              '#05dcff', '#0000bb', '#6a5acd', '#eeeeee']
    cmap_list.append(produce_cmap(cvals, colors, 'pct_1'))
    cmap_names.append('pct_1')

    return cmap_names, cmap_list



def get_cmap_2(name='wv_nrl', sat_name='GOES_15_GVAR', b_num=3):
    '''
    cmap_names = ['wv_nrl', 'wv_ssd', 'wv_nrl_extend']
    cmap_list = []
    '''

    '''
    cdict_nrl = {'red': [[0.0, 0.5, 0.5],
                      [0.2, 1.0, 1.0],
                      [0.4, 1.0, 1.0],
                      [0.5, 0.5, 0.5],
                      [0.6, 0.5, 0.5],
                      [0.8, 0.0, 0.0],
                      [1.0, 0.5, 0.5]],
                 'green': [[0.0, 0.0, 0.0],
                      [0.4, 1.0, 1.0],
                      [0.6, 1.0, 1.0],
                      [0.8, 0.5, 0.5],
                      [1.0, 0.0, 0.0]],
                 'blue': [[0.0, 0.0, 0.0],
                      [0.2, 0.0, 0.0],
                      [0.4, 0.5, 0.5],
                      [0.5, 0.5, 0.5],
                      [0.6, 1.0, 1.0],
                      [0.8, 1.0, 1.0],
                      [1.0, 0.5, 0.5]]}
    wv_nrl = LinearSegmentedColormap('wv_nrl', segmentdata=cdict_nrl)
    cmap_list.append(list((wv_nrl,-70,0)))


    cdict_ssd = {'red': [[0.0, 0.0, 0.0],
                      [0.27, 0.0, 0.0],
                      [0.54, 1.0, 1.0],
                      [0.72, 0.0, 0.0],
                      [0.88, 1.0, 1.0],
                      [1.0, 1.0, 1.0]],
                 'green': [[0.0, 1.0, 1.0],
                      [0.27, 0.42, 0.42],
                      [0.54, 1.0, 1.0],
                      [0.72, 0.0, 0.0],
                      [0.88, 1.0, 1.0],
                      [1.0, 0.0, 0.0]],
                 'blue': [[0.0, 1.0, 1.0],
                      [0.27, 0.0, 0.0],
                      [0.54, 1.0, 1.0],
                      [0.72, 0.66, 0.66],
                      [0.88, 0.0, 0.0],
                      [1.0, 0.0, 0.0]]}
    wv_ssd = LinearSegmentedColormap('wv_ssd', segmentdata=cdict_ssd)
    cmap_list.append(list((wv_ssd,-100,-2)))
    '''

    im_type = image_type(sat_name, b_num)

    if (cmap_names.count(name) == 0 or name[0:2] != im_type):
        if im_type == 'wv':
            return cmap_list[0]
        elif im_type == 'ir':
            return cmap_list[3]
        else:
            return cmap_list[3]
    else:
        i = cmap_names.index(name)
        return cmap_list[i]

def get_cmap(name='ir_bw', sat_name='GOES_15_GVAR', b_num=3):
    im_type = image_type(sat_name, b_num)
    return cmap_fetch(name, im_type)



# Indices to step through colormap

def display_my_cmaps(inputs=None):
    cmap_names, cmap_list = produce_cmap_list()
    cmaps = {}
    gradient = np.linspace(-100, 50, 500)

    if inputs == None:
        cmap_list_display = cmap_list
    else:
        cmap_list_display = [i for i in cmap_list if i[0].name in inputs]

    # Create figure and adjust figure height to number of colormaps
    nrows = len(cmap_list_display)
    figh = 0.35 + 0.15 + (nrows + (nrows - 1) * 0.1) * 0.22
    fig, axs = plt.subplots(nrows=nrows, figsize=(14, figh))
    fig.subplots_adjust(top=1 - 0.35 / figh, bottom=0.25 / figh,
                        left=0.1, right=0.97)
    axs[0].set_title(f'My colormaps', fontsize=14)


    for ax, cmap in zip(axs, cmap_list_display):
        ax.pcolormesh(list(gradient), [0,1], [list(gradient),list(gradient)], cmap=cmap[0], vmin=cmap[1], vmax=cmap[2])
        ax.text(-0.01, 0.5, cmap[0].name, va='center', ha='right', fontsize=10,
                transform=ax.transAxes)
        ax.axis('off')
        ax.xaxis.set_visible(False)  # Hide X-axis
        ax.yaxis.set_visible(False)  # Hide Y-axis


    axs[nrows - 1].axis('on')
    axs[nrows - 1].xaxis.set_visible(True)
    for direction in ['left','right','bottom','top']:
        axs[nrows-1].spines[direction].set_color('none')


    plt.show()

    return 0

if False:
    display_my_cmaps(['wv_nrl','wv_ssd','wv_nrl_extend','ir_color','wv_color','ir_bd','ir_ca_2','ir_cc','ir_cc_2',
                  'wv_bd','wv_cc','wv_cc_2','wv_nrld','wv_ssdd','ir_cb','wv_test_1','ir_test_1'])