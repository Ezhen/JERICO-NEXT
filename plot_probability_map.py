# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import numpy as np
from netCDF4 import Dataset
import datetime 
from mpl_toolkits.basemap import Basemap
import matplotlib as mpl
import calendar
from build_grid import *
import cmocean.cm as cm
from Runge_Kutta import buoy

# Function plots velocity field nicely
cmap = cm.speed

latmin = 70 #100
latmax = 240 #200
lonmin = 250 #75
lonmax = 450 #150

n = Dataset('/home/evgeny/Downloads/sv04-med-ingv-cur-an-fc-h_1531404445014.nc', 'r', format='NETCDF4')
lon = n.variables['lon'][lonmin:lonmax]
lat = n.variables['lat'][latmin:latmax]
u = n.variables['uo'][0,0,latmin:latmax,lonmin:lonmax]
v = n.variables['vo'][0,0,latmin:latmax,lonmin:lonmax]

w=(u**2+v**2)**0.5
#plt.imshow(np.flipud(w))

fig,m1,ax,cax = BUILD_GRID(lon.min(),lon.max(),lat.min(),lat.max(),(lat.max()-lat.min())/2.,2)

lats,lons = np.meshgrid(lat,lon)
x, y = m1(lons, lats)
clevs = np.arange(0,1,0.025)
m1.contourf(x[:],y[:],w.T,clevs,cmap=cmap)
prec = 3
kk = m1.quiver(x[::prec,::prec],y[::prec,::prec],u.T[::prec,::prec],v.T[::prec,::prec],color='black',linewidth=w[::prec,::prec].flatten(),angles='xy',edgecolor='None') 
mpl.colorbar.ColorbarBase(cax, cmap=cmap, boundaries = clevs, orientation='vertical')

dt = 1800 	# s
n_it = 1000 	# number of iterations
lat0,lon0 = 36.7,13.2
#lat0,lon0 = 37.1,15.8
#lat0,lon0 = 38,11
tracer = buoy(lat0,lon0,lat,lon,u,v,dt,n_it)
xfree, yfree = m1(tracer[1], tracer[0])
m1.plot(xfree[0],yfree[0], 'o',c='w',linewidth=50,label='initial position')
m1.plot(xfree,yfree, label='no correction',linewidth=3)
m1.plot(xfree[-1],yfree[-1], 'o',c='r',linewidth=50,label='last position')
#plt.legend(loc=1)
plt.show()
