import numpy
import gdspy	

from coupler import coupler

length = 200
ring_r = 40
bend_r = 20
width = 0.6
dx = 0.6

ring_origin = (length/2.0, ring_r+dx+width+bend_r)

#for i in range(10):
#	cell = gdspy.Cell('cell_%s' % i)

cell = gdspy.Cell('cellname')

spec={'layer':1}

ring = gdspy.Round(ring_origin, inner_radius=ring_r-width/2.0, radius=ring_r+width/2.0,**spec)
cell.add(ring)

path=gdspy.Path(width,(0,0))
path.arc(bend_r,numpy.pi,numpy.pi/2.0,**spec).segment(length-2*bend_r,**spec).arc(bend_r,numpy.pi/2.0,0,**spec)
cell.add(path)

for i in [0,length]:
	coupler((i,0),0.6,numpy.pi/4.0,20,1.2, 0.8, cell,1)

gdspy.LayoutViewer()	 
	

