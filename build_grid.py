from mpl_toolkits.basemap import Basemap
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable

def BUILD_GRID(llcrnrlon,urcrnrlon,llcrnrlat,urcrnrlat,lat_ts,discr):
	"""
	This function makes a grid frame with Basemap 
							
	 		Attributes 		
	* llcrnrlon - longitude of the lower left corner
	* urcrnrlon - longitude of the upper right corner
	* llcrnrlat - latitude of the lower left corner
	* urcrnrlat - latitude of the upper right corner
	* lat_ts    - central latitude                 
	* discr     - discretization of the grid       
	"""
	fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(10, 10))
	m1 = Basemap(projection='merc',llcrnrlat=llcrnrlat,urcrnrlat=urcrnrlat,llcrnrlon=llcrnrlon,urcrnrlon=urcrnrlon,lat_ts=lat_ts,resolution='i', ax=ax)
	m1.drawparallels(np.arange(llcrnrlat,urcrnrlat,discr),labels=[1,0,0,1],fontsize=10)
	m1.drawmeridians(np.arange(llcrnrlon,urcrnrlon,discr),labels=[1,1,1,0],fontsize=10)
	m1.drawcoastlines()
	m1.drawmapboundary(fill_color='aqua')
	m1.drawcountries()
	m1.fillcontinents(color='#ddaa66',lake_color='#9999FF')
	cax = make_axes_locatable(ax).append_axes("right", size=0.4, pad=0.15)
	return fig,m1,ax,cax
