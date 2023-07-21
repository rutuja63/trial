import numpy as np
import pandas as pd
import h5py
import os
import argparse
import phoreal as pr
from phoreal.reader import get_atl03_struct
from phoreal.reader import get_atl_coords
from phoreal.reader import get_atl08_struct
from phoreal.reader import get_atl_alongtrack
from phoreal.binner import rebin_atl08
from phoreal.binner import rebin_truth
from phoreal.binner import match_truth_fields
from phoreal.reader import write_pickle, read_pickle
import matplotlib.pyplot as plt
import math
from pyproj import Proj, Transformer



def reproject(inEPSG, outEPSG, a):
    
    lon = np.array(a.lon_ph)
    lat = np.array(a.lat_ph)
    transformer = Transformer.from_crs("EPSG:" + str(inEPSG), "EPSG:"+str(outEPSG))
    x,y = transformer.transform(lat,lon)
    a = a.drop(columns=['easting'])
    a = a.drop(columns=['northing'])

    a = pd.concat([a, pd.DataFrame(x,columns=['easting'])], axis=1)
    a = pd.concat([a, pd.DataFrame(y,columns=['northing'])], axis=1)
    return a
    


if __name__ == '__main__':

#files steve tried his code
    # file_03 = "/exports/csce/datastore/geos/groups/MSCGIS/s2318635/Practise_data/ICESat-2/05052023/ATL03/ATL03_20181227220646_13790103_005_01.h5"
    # file_08 = "/exports/csce/datastore/geos/groups/MSCGIS/s2318635/Practise_data/ICESat-2/05052023/ATL08/ATL08_20181227220646_13790103_005_01.h5"
    
    file_03 = "/home/s2318635/Dissertation_Mdrive/Practise_data/ICESat-2/bulk_data_files/ATL03/ATL03_20190912213302_11730405_006_02.h5"
    file_08 = "/home/s2318635/Dissertation_Mdrive/Practise_data/ICESat-2/bulk_data_files/ATL08/ATL08_20190912213302_11730405_006_02.h5"
    gt = 'gt1l'
    epsg_code  = '32605'
    atl03 = get_atl03_struct(file_03, gt, file_08, epsg_code)
    atl03.df = atl03.df[(atl03.df.lat_ph<=65)& (atl03.df.lat_ph>=62)& (atl03.df.classification > 0)]
    # print("atl03", atl03.df.head(10))
    # print(atl03.df.columns)
    #bounds for steve tried files
    # atl03.df = atl03.df[atl03.df.lon_ph < -154.5]
    # atl03.df = atl03.df[atl03.df.lon_ph > -155.5]
    # bounds tried fro new msw checked file
    # miny = atl03.df.lat_ph.iloc[0]                                                       
    # maxy = atl03.df.lat_ph.iloc[-1]
    # print("bounds", miny, maxy)
    # minx = atl03.df.lon_ph.iloc[0]
    # maxx = atl03.df.lon_ph.iloc[-1]
    # print("bounds", minx, maxx)

    atl03.df = atl03.df.reset_index()
 
    atl03.df = reproject(4326, 32605, atl03.df)
    print(atl03.df.head(10))

   
   
    atl03.df, atl03.rotationData = get_atl_alongtrack(atl03.df)
    print(atl03.df.head(10))

    # atl03.df.to_csv("/exports/csce/datastore/geos/groups/MSCGIS/s2318635/bulkdata/21062023/check_alongtrack.csv")
    # atl08 = pr.reader.get_atl08_struct(file_08, gt, atl03)
    # print(type(atl08))
    # # print(len(atl08))
    # print("atl08", atl08.df.head(10))
    # print(atl08.df.columns)
    # atl08.df.to_csv("/exports/csce/datastore/geos/groups/MSCGIS/s2318635/bulkdata/21062023/atl08.csv")


    # print(atl03.df.head(10))
    # atl03.df.to_csv("/exports/csce/datastore/geos/groups/MSCGIS/s2318635/bulkdata/21062023/atl03struct_62_64.csv")
    # write_pickle(atl03.df, "atl03trim1")
    # atl03 = read_pickle("atl03trim1")
    # atl03.df = atl03
    # print(atl03.df.head(10))
    # print(atl03.df.columns)
    # print(len(atl03.df))
    # atl03.df.to_csv("/exports/csce/datastore/geos/groups/MSCGIS/s2318635/bulkdata/21062023/atl03struct_trimonlat.csv")
    # print(atl03.df.shape[0])
    #get atlcoord functions in phoreal has been modified in readers.py and utils.py
    # df,epsg = get_atl_coords(atl03.df, 32606)
    # print(df.columns)
    # print(df.head(10))



