import numpy
import gdspy

def mix(list_com,layer):
	tot = gdspy.Path(1,(0,0))
	for i in list_com:
		tot = gdspy.fast_boolean(i, tot, 'or', layer=layer)
	return tot

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

def taper(origin, length, width1, width2, layer):
	#a = 2*(width1-width2), b = -3.0*a/2.0, c = width1
	path = gdspy.Path(width1,origin)
	path.parametric(lambda t: (t,0), final_width = lambda t: 2*(width1-width2)*t**3-3*(width1-width2)*t**2+width1, 
		layer=layer)
	return path

def mzi(origin, length, height, width, layer):
	spec={'width': width, 'layer': layer}
	origin1=(origin[0]+height/2.0,origin[1])
	origin2=(origin[0]+length,origin[1])
	sp1 = splitter(origin, height/2.0, height, **spec)
	sp2 = splitter(origin2, height/2.0, height, **spec).rotate(numpy.pi,center=origin2)
	path=gdspy.Path(width,origin1,number_of_paths=2,distance=height)
	path.segment(length-height,'+x')
	return mix([sp1,sp2,path],layer)#gdspy.fast_boolean(sp1, sp2, 'or', layer=layer)


cell = gdspy.Cell('test')

#sb = s_bend((0,0),0.1,4,4,3)
spec = {'width':0.8, 'layer':3}

#sp = splitter((0,0),length=10,height=20,**spec)
cell.add(mzi((0,0),10,4,0.1,3))

gdspy.LayoutViewer()