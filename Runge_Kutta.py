from numpy.linalg import inv
import numpy as np

def crd(lat_t,lon_t,lat,lon):
	# calculation of coordinates in terms of a regular grid of a Copernicus product 
	fract_j = (lon_t-lon[0])/(lon[1]-lon[0])
	fract_i = (lat_t-lat[0])/(lat[1]-lat[0])
	i,j = np.floor(fract_i),np.floor(fract_j)
	di,dj = fract_i-i,fract_j-j
	#print(i,j,di,dj,fract_i,fract_j)
	return i,j,di,dj

def vel(x, lat,lon,u,v):
	# check if a tracer still inside the domain
	if x[1]>lon.max() or x[0]>lat.max() or x[1]<lon.min() or x[0]<lat.min():
		return array([0,0])
	i,j,di,dj = crd(x[0],x[1],lat,lon)
	j,i,dj,di = int(j),int(i),int(dj),int(di)
	u00,u10,u01,u11 = tuple((np.array([u[i,j],u[i+1,j],u[i,j+1],u[i+1,j+1]])+np.array([u[i-1,j],u[i,j],u[i-1,j+1],u[i,j+1]])+np.array([u[i,j-1],u[i+1,j-1],u[i,j],u[i+1,j]])+np.array([u[i-1,j-1],u[i,j-1],u[i-1,j],u[i,j]]))/4)
	ub = u00 + di * (u10-u00) 
	ut = u10 + di * (u11-u01) 
	ui = ub + dj * (ut - ub)
	v00,v10,v01,v11 = tuple((np.array([v[i,j],v[i+1,j],v[i,j+1],v[i+1,j+1]])+np.array([v[i-1,j],v[i,j],v[i-1,j+1],v[i,j+1]])+np.array([v[i,j-1],v[i+1,j-1],v[i,j],v[i+1,j]])+np.array([v[i-1,j-1],v[i,j-1],v[i-1,j],v[i,j]]))/4)
	vb = v00 + di * (v10-v00) 
	vt = v10 + di * (v11-v01) 
	vi = vb + dj * (vt - vb)
	ui = ui / np.cos(np.deg2rad(x[0])) / 1.11e5
	vi = vi / 1.11e5
	return np.array([vi,ui])
	
# define runge-kutta function	
def rgk(x, dt, lat,lon,u,v):
	# Runge-Kutta discretization scheme
	xp = x + dt * vel(x,lat,lon,u,v) / 2. 
	x = x + dt * vel(xp,lat,lon,u,v)
	print(x)
	return x

def buoy(lat0,lon0,lat,lon,u,v,dt):
	# declaration of array for a priori quantities
	x_free0 = [lat0,lon0]
	return rgk(x_free0, dt,lat,lon,u,v)


	
	


