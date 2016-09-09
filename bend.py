import numpy
import gdspy

def s_bend(origin, length, height, width, layer):
	r = (length**2 + height**2)/height/4.0
	theta = numpy.arcsin(length/r/2.0)
	path = gdspy.Path(width, origin )
	path.arc(r, -numpy.pi/2.0, -numpy.pi/2.0+theta, layer=layer).arc(r, numpy.pi/2.0+theta, numpy.pi/2.0, layer=layer)
	return path

def splitter(origin, length, height, width, layer):
	sb_up	= s_bend(origin, length, height/2.0, width, layer)
	sb_down	= s_bend(origin, length, -height/2.0, width, layer)
	return gdspy.fast_boolean(sb_up, sb_down, 'or')

def branch(origin, length, height, width, layer):
	r = height/2.0
	path1 = gdspy.Path(width, origin)
	path1.segment(length-r, '+x', layer=layer).turn(r,numpy.pi/2.0,layer=layer)
	path2 = gdspy.Path(width, origin)
	path2.segment(length-r, '+x', layer=layer).turn(r,-numpy.pi/2.0,layer=layer)
	return gdspy.fast_boolean(path1, path2, 'or', layer=layer)

def taper():
cell = gdspy.Cell('test')

#sb = s_bend((0,0),0.1,4,4,3)
spec = {'width':0.8, 'layer':3}

sp = splitter((0,0),length=10,height=20,**spec)

cell.add(sp)

gdspy.LayoutViewer()