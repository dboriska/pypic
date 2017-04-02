from basic import *	
from coupler import *

length = 250
width = 1.0
dx = 0.4
spec={'layer':1}
bend_r = 20

cell_tot = gdspy.Cell('Final')
cell_tot.add(bounding_box((600,400),1200,800, **spec))
	
for l in range(2):
	for c in range(2):
		for r in range(2):
			ring_r = 30 + r*10
			ring_origin = (length/2.0, ring_r+dx+bend_r+width)
			ring=gdspy.Round(ring_origin, inner_radius=ring_r-width/2.0, radius=ring_r+width/2.0, **spec)
			path=gdspy.Path(width,(0,0))
			path.arc(bend_r,numpy.pi,numpy.pi/2.0,**spec).segment(length-2*bend_r,**spec).arc(bend_r,numpy.pi/2.0,0,**spec)
			cell = gdspy.Cell('%s%s%s' % (l+1,c+1,r))
			cell.add(ring)
			cell.add(path)
			factor = 0.3+0.05*c
			period = 1.129 + 0.01*l
			for i in [0,length]:
				coupler((i,0),width,numpy.pi/4.0,20,period,factor, cell, **spec)
			cell.add(mark((125,20),330,160,**spec))
			cell.add(gdspy.Text('%s %s %s \n %s' % (period, factor, ring_r, cell.name), 10, (40, -35), **spec))
			cell_tot.add(gdspy.CellReference(cell, (360*(2*l+ r%2), 190*(2*c+ r//2)), rotation=0))

# gdspy.gds_print('ring_resonator_SiN_%s_%s_%s.gds' % (l+1, c+1, r+1), unit=1.0e-6, precision=1.0e-9)
gdspy.LayoutViewer()