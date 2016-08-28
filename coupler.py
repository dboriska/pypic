import numpy
import gdspy

# coupler() needs call 'cell' 

def coupler(origin, width, angle, number, period, factor, cell, layer):
	lay = layer
	theta = angle*0.5
	radius_tp = width*0.5/(1.0/numpy.cos(theta)-1.0)
	radius = number*period

	origin_left = (origin[0] - radius_tp/numpy.cos(theta), origin[1])
	left = gdspy.Round(origin_left, radius_tp, initial_angle=0, final_angle= -theta, layer=lay)
	origin_right = (origin[0] + radius_tp/numpy.cos(theta), origin[1])
	right =gdspy.Round(origin_right, radius_tp, initial_angle=numpy.pi, final_angle= numpy.pi+theta, layer=lay)
	pie_1 = gdspy.Round(origin, radius_tp*numpy.tan(theta), initial_angle= -numpy.pi, final_angle=0, layer=lay)	
	comp_1 = gdspy.fast_boolean(pie_1, gdspy.fast_boolean(left, right, 'or',layer =lay), 'not',layer =lay)
	
	pie_2 = gdspy.Round(origin, radius, initial_angle= -numpy.pi/2.0+theta, final_angle=-numpy.pi/2.0-theta, layer=lay)		
	comp_2 = gdspy.fast_boolean(pie_2, comp_1, 'or',layer=lay)
	cell.add(comp_2)
	for i in range(number):
		part = gdspy.Round(origin, inner_radius=radius+i*period+period*(1-factor), radius=radius+(i+1)*period, initial_angle= -numpy.pi/2.0+theta, final_angle=-numpy.pi/2.0-theta, layer=lay)
		cell.add(part)
