# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import numpy as np
from netCDF4 import Dataset
import datetime,calendar
from mpl_toolkits.basemap import Basemap
import matplotlib as mpl
from build_grid import *
import cmocean.cm as cm
from Runge_Kutta import buoy


timeN = lambda x: datetime.datetime(1970,1,1,0,0,0) + datetime.timedelta(seconds=x)

# Function plots velocity field nicely
cmap = cm.speed

latmin = 70 #100
latmax = 240 #200
lonmin = 250 #75
lonmax = 450 #150
dt = 1800 	# s
n_it = 1000 	# number of iterations
prec = 3

lat0,lon0 = 36.7,13.2
#lat0,lon0 = 37.1,15.8
#lat0,lon0 = 38,11

tracer = np.zeros((2,n_it))
tracer[:,0] = [lat0,lon0]
xfree,yfree = np.zeros((n_it)),np.zeros((n_it))

n = Dataset('/home/evgeny/Downloads/sv04-med-ingv-cur-an-fc-h_1531404445014.nc', 'r', format='NETCDF4')
lon = n.variables['lon'][lonmin:lonmax]
lat = n.variables['lat'][latmin:latmax]
t = n.variables['time'][0]

fig,m1,ax,cax = BUILD_GRID(lon.min(),lon.max(),lat.min(),lat.max(),(lat.max()-lat.min())/2.,2)

lats,lons = np.meshgrid(lat,lon)
x, y = m1(lons, lats)
clevs = np.arange(0,1,0.025)
cb = mpl.colorbar.ColorbarBase(cax, cmap=cmap, boundaries = clevs, orientation='vertical')
cb.ax.set_title('ms-1',fontsize=10)


plt.ion()
u = n.variables['uo'][0,0,latmin:latmax,lonmin:lonmax]
v = n.variables['vo'][0,0,latmin:latmax,lonmin:lonmax]
w=(u**2+v**2)**0.5

C = ax.contourf(x[:],y[:],w.T,clevs,cmap=cmap,alpha=0.9)
q = ax.quiver(x[::prec,::prec],y[::prec,::prec],u.T[::prec,::prec],v.T[::prec,::prec],color='black',linewidth=w[::prec,::prec].flatten(),angles='xy',edgecolor='None',zorder=1)

xfree[0], yfree[0] = m1(tracer[1,0], tracer[0,0])
line, = ax.plot(xfree[0], yfree[0], 'o',c='b',linewidth=50) 
ax.plot(xfree[0], yfree[0], 'o',c='w',linewidth=50,label='initial position') 

ann = ax.annotate('%s' %(timeN(float(n.variables['time'][0])).strftime("%d. %B %Y %H:00")), xy=(0,0), xycoords='axes points',xytext=(210,20), textcoords='axes points',fontsize=12, bbox=dict(facecolor='white', edgecolor='black', pad=5.0))
fig.canvas.draw()
input("Press Enter to continue...")


for i in range(1,n_it):
	ann.remove(); q.remove()
	for coll in C.collections: 
		coll.remove()
	u = n.variables['uo'][int(i/2),0,latmin:latmax,lonmin:lonmax]
	v = n.variables['vo'][int(i/2),0,latmin:latmax,lonmin:lonmax]
	w=(u**2+v**2)**0.5
	C = ax.contourf(x[:],y[:],w.T,clevs,cmap=cmap,alpha=0.9)
	#q.set_UVC(u.T[::prec,::prec],v.T[::prec,::prec])
	q = ax.quiver(x[::prec,::prec],y[::prec,::prec],u.T[::prec,::prec],v.T[::prec,::prec],color='black',linewidth=w[::prec,::prec].flatten(),angles='xy',edgecolor='None',zorder=1)
	tracer[:,i] = buoy(tracer[0,i-1],tracer[1,i-1],lat,lon,u,v,dt)
	xfree[i], yfree[i] = m1(tracer[1,i], tracer[0,i])
	line.set_xdata(xfree[0:i])
	line.set_ydata(yfree[0:i])
	ann = ax.annotate('%s' %(timeN(float(n.variables['time'][int(i/2)])).strftime("%d. %B %Y %H:00")), xy=(0,0), xycoords='axes points',xytext=(210,20), textcoords='axes points',fontsize=12, bbox=dict(facecolor='white', edgecolor='black', pad=5.0))
	fig.canvas.draw()
	input("Press Enter to continue...")
plt.show()
