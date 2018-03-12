import sys
sys.path.insert(0,'/Library/Frameworks/GDAL.framework/Versions/2.2/Python/3.6/site-packages')
from osgeo import gdal
import matplotlib.pyplot as plt
import numpy as np
import os
%matplotlib inline
DATA = "/Users/huyu/MIT mac/y1s2/11.s941 Big Data/w5/LC08_L1TP_012031_20160627_20170223_01_T1"

def tif2array(location):
    """
    Should:
    1. Use gdal.open to open a connection to a file.
    2. Get band 1 of the raster
    3. Read the band as a numpy array
    4. Convert the numpy array to type 'float32'
    5. Return the numpy array.
    """
    x_data = gdal.Open(location)
    x_band = x_data.GetRasterBand(1)
    x = x_band.ReadAsArray()
    x = x.astype(np.float32)
    return x


red = tif2array(red_path)
nir = tif2array(nir_path)
# tirs = tif2array(tirs_path)

def ndvi_calc(red, nir):
    """ Calculate NDVI"""
    return (nir - red) / (nir + red)

ndvi = ndvi_calc(red, nir)
# plt.imshow(ndvi, cmap='YlGn')
# plt.colorbar()

def process_string (st):
    return float(st.split(' = ')[1].strip('\n'))

def retrieve_meta(meta_text):
    """
    Retrieve variables from the Landsat metadata *_MTL.txt file
    Should return a list of length 4.
    'meta_text' should be the location of your metadata file
    Use the process_string function we created in the workshop.
    """
    with open(meta_text) as f:
        meta = f.readlines()
    matchers = ['RADIANCE_MULT_BAND_10', 'RADIANCE_ADD_BAND_10', 'K1_CONSTANT_BAND_10', 'K2_CONSTANT_BAND_10']
    matching = [process_string(s) for s in meta if any(xs in s for xs in matchers)]
    return matching

# meta = retrieve_meta('//Users/huyu/MIT mac/y1s2/11.s941 Big Data/w5/LC08_L1TP_012031_20160627_20170223_01_T1/LC08_L1TP_012031_20160627_20170223_01_T1_MTL.txt')
# meta[0]
# meta[1]
# meta[2]
# meta[3]
def rad_calc(tirs, var_list):
    """
    Calculate Top of Atmosphere Spectral Radiance
    Note that you'll have to access the metadata variables by
    their index number in the list, instead of naming them like we did in class.
    """
    rad = var_list[0] * tirs + var_list[1]
    return rad

# plt.imshow(rad_calc(tirs, meta), cmap='RdYlGn')
# plt.colorbar()



def bt_calc(rad, var_list):
    """
    Calculate Brightness Temperature
    Again, you'll have to access appropriate metadata variables
    by their index number.
    """
    bt = var_list[3] / np.log((var_list[2]/rad) + 1) - 273.15
    return bt

# plt.imshow(bt_calc(rad_calc(tirs, meta), meta), cmap='RdYlGn')
# plt.colorbar()

def pv_calc(ndvi, ndvi_s, ndvi_v):
    """
    Calculate Proportional Vegetation
    """
    pv = ((ndvi - ndvi_s) / (ndvi_v - ndvi_s)) ** 2
    return pv

# plt.imshow(pv_calc(ndvi, 0.2, 0.5), cmap='RdYlGn')
# plt.colorbar()

def emissivity_calc (pv, ndvi):
    ndvi_dest = ndvi.copy()
    ndvi_dest[np.where(ndvi < 0)] = 0.991
    ndvi_dest[np.where((0 <= ndvi) & (ndvi < 0.2)) ] = 0.966
    ndvi_dest[np.where((0.2 <= ndvi) & (ndvi < 0.5)) ] = (0.973 * pv[np.where((0.2 <= ndvi) & (ndvi < 0.5)) ]) + (0.966 * (1 - pv[np.where((0.2 <= ndvi) & (ndvi < 0.5)) ]) + 0.005)
    ndvi_dest[np.where(ndvi >= 0.5)] = 0.973
    return ndvi_dest




def lst_calc(location):
    """
    Calculate Estimate of Land Surface Temperature.
    Your output should
    ---
    Note that this should take as its input ONLY the location
    of a directory in your file system. That means it will have
    to call your other functions. It should:
    1. Define necessary constants
    2. Read in appropriate tifs (using tif2array)
    3. Retrieve needed variables from metadata (retrieve_meta)
    4. Calculate ndvi, rad, bt, pv, emis using appropriate functions
    5. Calculate land surface temperature and return it.
    Your LST function may return strips of low-values around the raster...
    This is a processing artifact that you're not expected to account for.
    Nothing to worry about!
    """
    DATA = location
    red_path = os.path.join(DATA, 'LC08_L1TP_012031_20160627_20170223_01_T1_B4.tif')
    nir_path = os.path.join(DATA, 'LC08_L1TP_012031_20160627_20170223_01_T1_B5.tif')
    tirs_path = os.path.join(DATA, 'LC08_L1TP_012031_20160627_20170223_01_T1_B10.tif')

    red = tif2array(red_path)
    nir = tif2array(nir_path)
    tirs = tif2array(tirs_path)

    ndvi = ndvi_calc(red, nir)
    # needs to find a way to substitute the director with location
    meta = retrieve_meta('//Users/huyu/MIT mac/y1s2/11.s941 Big Data/w5/LC08_L1TP_012031_20160627_20170223_01_T1/LC08_L1TP_012031_20160627_20170223_01_T1_MTL.txt')

    rad = rad_calc(tirs, meta)

    bt = bt_calc(rad, meta)

    pv = pv_calc(ndvi, 0.2, 0.5)

    emis = emissivity_calc(pv, ndvi)

    wave = 10.8E-06
    # PLANCK'S CONSTANT
    h = 6.626e-34
    # SPEED OF LIGHT
    c = 2.998e8
    # BOLTZMANN's CONSTANT
    s = 1.38e-23
    p = h * c / s

    lst = bt / (1 + (wave * bt / p) * np.log(emis))

    return lst

loc = "/Users/huyu/MIT mac/y1s2/11.s941 Big Data/w5/LC08_L1TP_012031_20160627_20170223_01_T1"
LST = lst_calc(loc)
plt.imshow(LST, cmap='RdYlGn')
plt.colorbar()



# Remove clouds

BQA= tif2array('/Users/huyu/MIT mac/y1s2/11.s941 Big Data/w5/LC08_L1TP_012031_20160627_20170223_01_T1/LC08_L1TP_012031_20160627_20170223_01_T1_BQA.tif')

def cloud_filter(array, bqa):
    """
    Filters out clouds and cloud shadows using values of BQA.
    """
    array_dest = array.copy()
    array_dest[np.where((bqa != 2720) & (bqa != 2724) & (bqa != 2728) & (bqa != 2732)) ] = 'nan'
    return array_dest

# Write Filtered Arrays as .tifs
def array2tif(raster_file, new_raster_file, array):
    """
    Writes 'array' to a new tif, 'new_raster_file',
    whose properties are given by a reference tif,
    here called 'raster_file.'
    """
    # Invoke the GDAL Geotiff driver
    raster = gdal.Open(raster_file)

    driver = gdal.GetDriverByName('GTiff')
    out_raster = driver.Create(new_raster_file,
                        raster.RasterXSize,
                        raster.RasterYSize,
                        1,
                        gdal.GDT_Float32)
    out_raster.SetProjection(raster.GetProjection())
    # Set transformation - same logic as above.
    out_raster.SetGeoTransform(raster.GetGeoTransform())
    # Set up a new band.
    out_band = out_raster.GetRasterBand(1)
    # Set NoData Value
    out_band.SetNoDataValue(-1)
    # Write our Numpy array to the new band!
    out_band.WriteArray(array)

ndvi_filter = cloud_filter(ndvi, BQA)
lst_filter = cloud_filter(LST, BQA)

tirs_path = os.path.join(DATA, 'LC08_L1TP_012031_20160627_20170223_01_T1_B10.tif')
out_path_ndvi = os.path.join(DATA, 'huyu_ndvi_20160627.tif')
array2tif(tirs_path, out_path_ndvi, ndvi_filter)

out_path_lst = os.path.join(DATA, 'huyu_lst_20160627.tif')
array2tif(tirs_path, out_path_lst, lst_filter)
