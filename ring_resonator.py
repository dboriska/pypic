from basic import *
from coupler import *

cell_tot = gdspy.Cell('tot')

ring_r = 40
length = 250
width = 0.5
dx = 0.3
spec={'layer':1}
bend_r = 20

import gdspy
import numpy

#path=gdspy.Path(0.5,(0,0)).segment(20,'+x')
for l in range(3):
	for c in range(2):
		ring_origin = (length/2.0, ring_r+dx+bend_r+width)
		cell = gdspy.Cell('cell %s %s' % (l,c))
		#%s %s' % 'l' 'c')
		ring = gdspy.Round(ring_origin, inner_radius=ring_r-width/2.0, radius=ring_r+width/2.0, **spec)
		cell.add(ring)
		path=gdspy.Path(width,(0,0))
		path.arc(bend_r,numpy.pi,numpy.pi/2.0,**spec).segment(length-2*bend_r,**spec).arc(bend_r,numpy.pi/2.0,0,**spec)
		cell.add(path)

		for i in [0,length]:
			coupler((i,0),width,numpy.pi/4.0,20,0.8+l*0.1, 0.6+c*0.05, cell, **spec)

		cell.add(mark((125,20),330,160,**spec))
		cell.add(gdspy.Text('%s %s' % (l,c), 10, (100, -35), **spec))

		cell_tot.add(gdspy.CellReference(cell, (360*l, 190*c),rotation=0))

gdspy.gds_print('tutorial.gds', unit=1.0e-6, precision=1.0e-9)

#gdspy.LayoutViewer()