import gdspy as gp
import numpy as np

def coupler(origin, width, angle, number, factor, period, gap):
	# bend_radius: radius of the bend connecting coupler and waveguide
	bend_radius = (width+gap)*0.5/(1.0/np.cos(0.5*angle)-1.0)
	# coupler_radius: half of the coupler sharp 
	coupler_radius = number*period
	# path: side gap for cladding
	path = gp.Path(gap, (origin[0]+(gap+width)*0.5,origin[1]))
	path.arc(bend_radius, np.pi, angle*0.5+np.pi).segment(coupler_radius*1.2)
	path.x = origin[0]-(gap+width)*0.5
	path.y = origin[1]
	path.arc(bend_radius, 0, -angle*0.5).segment(coupler_radius*1.2)
	
	for i in range(number):
		path = gp.fast_boolean(
			gp.Round(origin, 
				coupler_radius+i*period+period*factor, 
				coupler_radius+(i+1)*period, 
				-np.pi/2.0+angle*0.5,-np.pi/2.0-angle*0.5), 
			path, 'or' )

	return path
