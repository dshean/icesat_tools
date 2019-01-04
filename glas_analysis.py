#! /usr/bin/env python

#Sample analysis workflow
#Clustering, gridding

import numpy as np
from pygeotools.lib import timelib, geolib, iolib
from osgeo import osr

glas_csv_fn='GLAH14_chad_refdemfilt.csv'
srtm_fn='chad_nasadem_hgt_merge_hgt_adj_proj_hs_az315.tif'
srtm_ds=iolib.fn_getds(srtm_fn)

# dt_ordinal, dt_YYYYMMDD, lat, lon, z_WGS84, z_refdem_med_WGS84, z_refdem_nmad
glas_pts = np.loadtxt(glas_csv_fn, delimiter=',', skiprows=1, dtype=None)

srs=osr.SpatialReference()
srs.ImportFromEPSG(32633)
x, y, z = geolib.cT_helper(glas_pts[:,3], glas_pts[:,2], glas_pts[:,4], geolib.wgs_srs, srs)

#pt_array = glas_pts[:,[3,2,4,0]]
pt_array = np.array([x, y, z, glas_pts[:,0]]).T

#Cluster
dt_thresh=16.0
d = np.diff(pt_array[:,3])
b = np.nonzero(d > dt_thresh)[0] + 1
b = np.hstack((0, b, d.shape[0]))
f_list = []
dt_list = []
for i in range(len(b)-1):
    f = pt_array[b[i]:b[i+1]]
    min_dt = timelib.o2dt(f[:,3].min())
    max_dt = timelib.o2dt(f[:,3].max())
    mid_dt = f[:,3].min() + (f[:,3].max() - f[:,3].min())/2.0
    mean_dt = timelib.o2dt(f[:,3].mean())
    med_dt = timelib.o2dt(np.median(f[:,3]))
    f_list.append(f)
    dt_list.append([min_dt, max_dt, mid_dt, mean_dt, med_dt])

statlist=('median', 'mean', 'count', 'std')
res=300
for n,f in enumerate(f_list):
    mean_dt = dt_list[n][3]
    for stat in statlist:
        g_count, ds = geolib.block_stats_grid_gen(f[:,0], f[:,1], f[:,2], res=res, srs=srs, stat=stat)
        out_fn = mean_dt.strftime('%Y%m%d_%H%M_')+stat+'_'+str(res)+'m.tif'
        iolib.writeGTiff(g_count, out_fn, ds)

#Make stacks
#Create function to wrap ASP point2dem for interpolation
